class Helper:
    
    def formatProperties(self, properties):
        
        query = "{"
        
        for key,val in properties.items():      
            query += key
            if type(val) == str:
                query += ":'"
                query += val + "',"
            else:
                query += ":"
                query += str(val) + ","
                
        query = query[:-1] + "}"
        
        return query
    
    
def formatEntities(NER):
        entities = []
        element = len(entities)
        #print(NER)
                
        for i in range(0, len(NER)):
            
            try:

                if NER[i]['entity'][0] == 'B' and NER[i]['word'][0] != '#':
                    entities.append({'entity':NER[i]['entity'][2:], 'word':NER[i]['word'], 'start':NER[i]['start'], 'end':NER[i]['end']})
                    element = len(entities) - 1

                else:



                    if NER[i]['word'][0] == '#':

                        entities[-1]['word'] += NER[i]['word'].replace('#','')

                    else:
                        entities[-1]['word'] += ' ' +  NER[i]['word'].replace('#','')
                    entities[-1]['end'] = NER[i]['end']
            except Exception as e:
                print(e, NER[i])
                
        return entities