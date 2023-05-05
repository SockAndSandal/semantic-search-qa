from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# given a graphdatabase driver, return a list of all the filenamnes in the database
def get_filenames(driver):
    session = driver.session()
    result = session.run("MATCH (n:File) RETURN n.name AS name")
    filenames = []
    for record in result:
        filenames.append(record["name"])
    session.close()
    return filenames

class rasa_test_work(Action): 
    def name(self): 
        return "action_rasa_test_work"

    def run(self, dispatcher, tracker, domain):
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234"))
        filenames = get_filenames(driver)
        dispatcher.utter_message(text="The filenames are: " + str(filenames))
        return []
    
