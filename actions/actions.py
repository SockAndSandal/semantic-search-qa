from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from neo4j import GraphDatabase

class FindFileAction(Action):
    def name(self) -> Text:
        return "action_find_file"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        # Get the file name and folder name from the slots
        file_name = tracker.get_slot("file_name")
        folder_name = tracker.get_slot("folder_name")

        # Connect to the Neo4j database
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            # Find the folder node with the given name
            result = session.run("MATCH (folder:Folder {name: $name}) RETURN folder", name=folder_name)
            folder_node = result.single().get("folder")

            # Find the file node with the given name inside the folder node
            result = session.run("MATCH (folder)-[:CONTAINS]->(file:File {name: $name}) RETURN file", name=file_name, folder=folder_node)
            file_node = result.single().get("file")

            if file_node:
                # If the file node is found, extract the file path and send it as a message
                file_path = file_node.get("path")
                dispatcher.utter_message(f"The file {file_name} is located at {file_path}")
            else:
                # If the file node is not found, send a message indicating that the file was not found
                dispatcher.utter_message(f"Sorry, I couldn't find the file {file_name} in the folder {folder_name}")

        return []
