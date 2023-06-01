from py2neo import Graph
from Helper import Helper
import subprocess


class Neo4jConnection:
    
    '''
    Get BOLT URL, username, pwd
    Create Session.
    Run queries through session.
    '''
    
    def __init__(self, uri=None, user=None, password=None):
        self.uri = uri if uri else "bolt://localhost:7687"
        self.user = user if user else "neo4j"
        self.password = password if password else "neo4jneo4j"
        self.graph = None
        self.queryGenerator = QueryGenerator()
        
    def connect(self):
        
        try:
            self.graph = Graph(self.uri, auth=(self.user, self.password))
            return "OK"
        except Exception as e:
            return e
    
    def run(self, node1=None, func=None, node2=None, relationship=None, prop=None, val=None):
        
        
        query = ""
        
        if func == "CREATE":
            
            if self.exists(node1):
                print("Node Exists. Cannot create nodes with redundant names.")
                return -1
            
            query = self.queryGenerator.create(node1.type, node1.getProperties())
            
        elif func == "IF_PATH_EXISTS":
            
            query = self.queryGenerator.check_file(node1, 'name')
            
        elif func=="MODIFIED_TIME":
            
            query = self.queryGenerator.check(name=node1, Type='Files', Property='mtime')

        elif func=="ACCESS_TIME":
            
            query = self.queryGenerator.check(name=node1, Type='Files', Property='atime')
            
            
      
        elif func == "DELETE":
            
            if self.exists(node1) == False:
                print("Node doesn't exist")
                return -1
            
            query = self.queryGenerator.delete(node1.type, node1.getProperties())

        elif func == "DELETE_NAME":
            
            query = self.queryGenerator.delete('Files', "{name:'" + str(node1) +"'}")
            
        elif func == "UPDATE":
            pass
            
        elif func == "LINK":
            
            if node2 == None:
                print("Node2 Argument Missing")
                return -1
            if self.exists(node1) == False:
                print(self.exists(node1))
                print("Create Node 1")
                return -1
            if self.exists(node2) == False:
                print("Create Node 2")
                return -1
            if relationship == None:
                print("Add relationship")
                return -1
             
            if self.graph.run(self.queryGenerator.relationship_exists(node1, node2, relationship)).evaluate():
                print("Relationship exists")
                return -1
                
            query = self.queryGenerator.connect_nodes(node1, node2, relationship)

        elif func == "KEYWORDS_REFRESH":
            query = self.queryGenerator.deleteKeywords()

        elif func == "UPDATE_PROP":
            query = self.queryGenerator.updateProp(name=node1, prop=prop, val=val)
            
        else:
            
            print("Unknown Function. Choose one of the following: [CREATE, DELETE, UPDATE, LINK]")
            return -1
            
        
        try:
            return self.graph.run(query)
        except:
            print("Query ERROR!")
            print(query)
            return -1
    
    def exists(self, node):
        
        prop = 'name'
        
        count = self.graph.nodes.match(node.type, name=node.properties[prop]).first()
        print(count)
        
        return False if count == None else True
        
    def startServer(self):

        neo4j_home = "/Users/ram/Desktop/Final-Project/NEO4J-HOME"
        server_config = "/path/to/n,eo4j/conf/neo4j.conf"

        # Check if the Neo4j server is already running
        status_output = subprocess.check_output([f"{neo4j_home}/bin/neo4j", "status"], stderr=subprocess.STDOUT)

        if b"Neo4j is running" in status_output:
            print("Neo4j server is already running.")
        else:
            print("Starting Neo4j server...")
            subprocess.run([f"{neo4j_home}/bin/neo4j", "start", "-c", server_config])

        

class File:
    
    def __init__(self, properties: dict , type="Files"):
        
        self.properties = {}
        
        for key, val in properties.items():
            self.properties[key] = val
#             self.properties['date_created'] = date_created
#             self.properties['date_modified'] = date_modified
#             self.properties['file_format'] = file_format
        self.type = type
        self.Help = Helper()
        
    def getProperties(self):
        
        return self.Help.formatProperties(self.properties)
        
        
class Keyword:
    
    def __init__(self, name, relationship, type="Keywords"):
        
        self.properties = {}
        self.properties['name'] = name
        self.relationship = relationship
        self.type = type
        self.Help = Helper()
        
    def getProperties(self):
        return self.Help.formatProperties(self.properties)
    
    def getRelationship(self):
        return self.relationship
    
        

class QueryGenerator:
    
    def __init__(self, conn=None):
        self.conn = conn

    def delete(self, node: str, properties: str):
        
        query = "MATCH (m:" + node + " " + properties + ") DETACH DELETE m"
        return query

    def create(self, node: str, properties: str):
        
        query = "CREATE (n:" + node + " " + properties + ")"
        return query
    
    def update(self, node: str, properties: str):
        
        return self.delete(node, properties) + " " + self.create(node, properties)

    def check(self, name: str, Type: str, Property: str):
        query = "MATCH (n1:" + Type + "{name:'" + name + "'})" + "RETURN n1." + Property
        return query 
    
    def check_file(self, name: str, Property: str):
        query = "MATCH (n1) WHERE n1." + Property + "= '" + name + "' RETURN n1"
        return query 
    
    def connect_nodes(self, node1, node2, relationship):
        
        query = "MATCH (n1:" + node1.type + node1.getProperties() + "),"
        query += "(n2:" + node2.type + node2.getProperties() + ") "
        query += "CREATE (n1) - [:" + relationship + "] -> (n2)"
    
        return query
    
    def relationship_exists(self, node1, node2, relationship):
        
        query = "RETURN EXISTS( (:"+ node1.type + "{ name: '"+ node1.properties['name'] + "'})-[:"+ relationship + "]-"
        query += "(:" + node2.type + "{name: '" + node2.properties['name'] +"'}) )"
        
        
        query = "MATCH (a:" + node1.type + "{name: '"+ node1.properties['name'] +  "'}), (b:" + node2.type + "{name: '" + node2.properties['name'] + "'}) "
        query += " RETURN EXISTS ((a)-[:" + relationship + "]-(b))"
        
        return query
    
    def deleteKeywords(self):

        query = "MATCH (n:Keywords) WHERE NOT (n)-[]-() DELETE n"
        return query
    
    def updateProp(self, name, prop, val, type='Files'):

        query = "MATCH (n:"+ type + "{name: '" + name +"'}) SET n." +prop+" = '"+ val + "' RETURN n"
        return query
        
if __name__ == "__main__":
    DB = Neo4jConnection()
    print(DB.connect())
  
