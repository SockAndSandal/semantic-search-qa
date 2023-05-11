from datetime import datetime
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

class ActionFindRecentlyOpenedFiles(Action):
    
    def name(self) -> Text:
        return "action_find_recently_opened_files"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:

        current_date = datetime.datetime.now()

        # Connect to the Neo4j database
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            
            # Find the folder node with the given name
            result = session.run("MATCH (f:Files) WHERE f.atime <= {date} RETURN file ORDER BY f.atime DESC LIMIT 1", date=current_date)
            file_node = result.single().get("file")

            if file_node:
                # If the file node is found, extract the file path and send it as a message
                file_path = file_node.get("name")
                dispatcher.utter_message(f"The recently accessed file is at the path: {file_path}")
            else:
                # If the file node is not found, send a message indicating that the file was not found
                dispatcher.utter_message(f"Sorry, I couldn't find any recently accessed files")

class ActionFindRecentlyCreatedFiles(Action):
    
    def name(self) -> Text:
        return "action_find_recently_created_files"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:

        current_date = datetime.datetime.now()

        # Connect to the Neo4j database
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            
            # Find the folder node with the given name
            result = session.run("MATCH (f:Files) WHERE f.ctime <= {date} RETURN file ORDER BY f.ctime DESC LIMIT 1", date=current_date)
            file_node = result.single().get("file")

            if file_node:
                # If the file node is found, extract the file path and send it as a message
                file_path = file_node.get("name")
                dispatcher.utter_message(f"The recently created file is at the path: {file_path}")
            else:
                # If the file node is not found, send a message indicating that the file was not found
                dispatcher.utter_message(f"Sorry, I couldn't find any recently created files")

class ActionFindRecentlyModifiedFiles(Action):
    
    def name(self) -> Text:
        return "action_find_recently_modified_files"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:

        current_date = datetime.datetime.now()

        # Connect to the Neo4j database
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            
            # Find the folder node with the given name
            result = session.run("MATCH (f:Files) WHERE f.mtime <= {date} RETURN file ORDER BY f.mtime DESC LIMIT 1", date=current_date)
            file_node = result.single().get("file")

            if file_node:
                # If the file node is found, extract the file path and send it as a message
                file_path = file_node.get("name")
                dispatcher.utter_message(f"The recently modified file is at the path: {file_path}")
            else:
                # If the file node is not found, send a message indicating that the files were not found
                dispatcher.utter_message(f"Sorry, I couldn't find any recently modified files")


class ActionFindRecentlyOpenedForms(Action):
    def name(self) -> str:
        return "action_find_recently_opened_forms"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        forms = get_recently_opened_forms()

        if forms:
            response = "Here are the recently opened forms:\n"
            for form in forms:
                response += f"- {form}\n"
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("No recently opened forms were found.")

        return []

class ActionFindRecentlyOpenedPublications(Action):
    def name(self) -> str:
        return "action_find_recently_opened_scientific_publications"

    async def run(self, dispatcher: CollectingDispatcher, 
                  tracker: Tracker, 
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #type wise classification

        if publications:
            response = "Here are the recently opened scientific publications:\n"
            for publication in publications:
                response += f"- {publication}\n"
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("No recently opened scientific publications were found.")

        return []


class ActionFindFormsByTimePeriod(Action):
    def name(self) -> str:
        return "action_find_forms_by_time_period"

    async def run(self, dispatcher: CollectingDispatcher, 
                  tracker: Tracker, 
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the extracted entities
        form_action = tracker.get_slot("form_action")
        time_period = tracker.get_slot("time_period")

        # Retrieve the requested forms based on the extracted entities
        # If forms are found, display them in a formatted response
        if forms:
            response = f"Here are the forms you {form_action} {time_period}:\n"
            for form in forms:
                response += f"- {form}\n"
            dispatcher.utter_message(response)

        # If no forms are found, inform the user
        else:
            dispatcher.utter_message(f"No forms were found that you {form_action} {time_period}.")

        return []

def find_number_of_files_by_format(file_format):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        # Find the number of files in the given format
        result = session.run("MATCH (file:File) WHERE file.format = $format RETURN count(file)", format=file_format)
        number = result.single().get("count(file)")

    return number

class ActionFindNumberofFilesbyFormat(Action):
    def name(self) -> str:
        return "action_find_number_of_files_by_format"

    async def run(self, dispatcher: CollectingDispatcher, 
                  tracker: Tracker, 
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the extracted entities
        file_format = tracker.get_slot("file_format")
        number = find_number_of_files_by_format(file_format)
        if number == 0:
            dispatcher.utter_message(f"No files were found in {file_format} format.")
        else:
            response = f"The number of files in {file_format} format are {number}:\n"
            dispatcher.utter_message(response)
        return []