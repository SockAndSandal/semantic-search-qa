from ProcessingFiles import PreprocessFiles
from GraphDB import File, Keyword, QueryGenerator, Neo4jConnection
import os
from Helper import formatEntities


"""

While True:
    Read Files properties
    if file not in Graph,
        add it to graph
    if files in graph not found in path, 
        delete file in graph
    
"""

class Main():

    def __init__ (self, folder_path):

        self.path = folder_path
        self.DB = Neo4jConnection()
        self.DB.connect()
        self.Query = QueryGenerator()
        self.preProcess = PreprocessFiles()

    

  


    
    def read(self):

        # Get a list of all files in the directory
        file_list = os.listdir(self.path)

        # Filter the list to include only PDF files
        #pdf_list = [self.path+"/"+ f for f in file_list if f.endswith(".pdf")]
        all_list = [self.path+"/"+f for f in file_list]

        #check if pdf in graph
        for f in all_list:
    
            print(f)
            l = self.preProcess.getMetaData(f)

            func = None
            
            cursor1 = self.DB.run(node1=f, func='IF_PATH_EXISTS')
            print("HERE###################")
            val = len(list(cursor1))
            print(val)
            if val == int(1):
                cursor2 = self.DB.run(node1=f, func='MODIFIED_TIME')
                time = [record for record in cursor2][0]
                print("TIME ########################")
                print(time)
                print(str(time).replace("'",""),str(l['mtime']) )
                if str(time).replace("'","") != str(l['mtime']):
                    func = 'UPDATE'
                    
            else:
                func = 'CREATE'
                
            print(func)
                
            if func:
                l = self.preProcess.getMetaData(f)
                print(l)
                text = self.preProcess.convertPDF(f)
                try:
                    if isinstance(text, bytes):
                        text = text.decode('utf-8')
                        l['numPages'] = text.count('\x0c') + 1
                    else:
                        l['numPages'] = len(text.split('\f'))
                except:
                    print(f)
                    
                #print(text)

                NER = self.preProcess.getEntities(text)
                entities = formatEntities(NER)

                print(len(entities))
                
                node = File(l)
                cursor = self.DB.run(node1=node, func=func)
                print("Creating...")
                print(cursor)
                
                for ent in entities:
                    entity = Keyword(name=ent['word'], relationship=ent['entity'])
                    print(entity.getProperties(), entity.getRelationship())
                    cursor = self.DB.run(node1=entity, func='CREATE')
                    #cursor = DB.run(node1=File(l), func='CREATE')
                    cursor = self.DB.run(node1=node, node2=entity, func='LINK', relationship=entity.getRelationship())
                
                docType = self.preProcess.getType(f,False)
                if docType:
                    entity = Keyword(name=docType, relationship='TYPE')
                    cursor = self.DB.run(node1=entity, func='CREATE')
                    cursor = self.DB.run(node1=node, node2=entity, func='LINK', relationship=entity.getRelationship())


    def delete(self, path):
        self.DB.run(node1=path, func="DELETE_NAME")
        self.DB.run(func='KEYWORDS_REFRESH')
        pass

    def getATIME(self, file, prop):
        cursor = self.DB.run(node1=file, func='ACCESS_TIME')
        prop = [record for record in cursor][0]
        return prop
    
    def updateATIME(self, file, prop, val):
        self.DB.run(node1=file, func='UPDATE_PROP', prop=prop, val=val)



    def create(self, path):
        l = self.preProcess.getMetaData(path)
        text = self.preProcess.convertPDF(path)

        if isinstance(text, bytes):
            text = text.decode('utf-8')
            l['numPages'] = text.count('\x0c') + 1
        else:
            l['numPages'] = len(text.split('\f'))
                #print(text)

        NER = self.preProcess.getEntities(text)
        entities = formatEntities(NER)

        print(len(entities))
                
        node = File(l)
        cursor = self.DB.run(node1=node, func='CREATE')
        print("Creating...")
        print(cursor)
                
        for ent in entities:
            entity = Keyword(name=ent['word'], relationship=ent['entity'])
            print(entity.getProperties(), entity.getRelationship())
            cursor = self.DB.run(node1=entity, func='CREATE')
                    #cursor = DB.run(node1=File(l), func='CREATE')
            cursor = self.DB.run(node1=node, node2=entity, func='LINK', relationship=entity.getRelationship())
                
        docType = self.preProcess.getType(path,False)
        if docType:
            entity = Keyword(name=docType, relationship='TYPE')
            cursor = self.DB.run(node1=entity, func='CREATE')
            cursor = self.DB.run(node1=node, node2=entity, func='LINK', relationship=entity.getRelationship())

        
                                




