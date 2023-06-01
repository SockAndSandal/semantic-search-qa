from datetime import datetime
import getpass
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from neo4j import GraphDatabase
from rasa_sdk.events import FollowupAction

class ActionGetUserName(Action):
    def name(self) -> Text:
        return "action_get_user_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = getpass.getuser()
        dispatcher.utter_message(f"Thank you, {user_name}! How can I assist you today?")
        return []

class ActionAcknowledgeName(Action):
    def name(self) -> Text:
        return "action_acknowledge_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Great! How can I assist you today?")
        return []

# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         return "action_default_fallback"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message("I'm sorry, but I didn't understand that. Can you please rephrase your request?")
#         return []

class UtterGreet(Action):
    def name(self) -> Text:
        return "utter_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Hello! How can I assist you today?")
        return []

class UtterYouAreWelcome(Action):
    def name(self) -> Text:
        return "utter_you_are_welcome"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("You're welcome!")
        return []

class UtterGoodbye(Action):
    def name(self) -> Text:
        return "utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Goodbye! Have a great day!")
        return []

class FindFileAction(Action):
    def name(self) -> Text:
        return "action_find_file"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        # Get the file name and folder name from the slots
        file_name = tracker.get_slot("file_name")
        folder_name = tracker.get_slot("folder_name")
        try:
            if file_name != None:
                driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))
                with driver.session() as session:
                
                    print(file_name)
                    # Find the file node with the given name inside the folder node
                    result = session.run("MATCH (file:Files) WHERE file.name CONTAINS $name RETURN file", name=file_name)
                    file_record = result.single()
                    if file_record is not None:
                        file_node = file_record.get("file")
                        # If the file node is found, extract the file path and send it as a message
                        file_path = file_node.get("name")
                        dispatcher.utter_message(f"Is this the file:'{file_path}'")
                        SlotSet("file_name", file_path)
                        return [SlotSet("file_name", file_path)]
                    else:
                        # If the file node is not found, send a message indicating that the file was not found
                        dispatcher.utter_message(f"Sorry, I couldn't find the file {file_name}")
            else:
    
                dispatcher.utter_message(text="I'm sorry, I didn't catch the file name. Could you please provide it?")
                print("Nothing in find_file")
                return [SlotSet("file_name", None)]

        except:
            return [FollowupAction("action_fallback")]
            


        return []

class ActionFindRecentlyOpenedFiles(Action):
    
    def name(self) -> Text:
        return "action_find_recently_opened_files"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:

        current_date = datetime.now().isoformat()

        # Connect to the Neo4j database
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))
        with driver.session() as session:
            
            # Find the folder node with the given name
            result = session.run("MATCH (f:Files) RETURN f ORDER BY datetime(f.atime) DESC LIMIT 1")
            file_node = result.single().get("f")

            if file_node:
                # If the file node is found, extract the file path and send it as a message
                file_path = file_node.get("name")
                dispatcher.utter_message(f"Here's the recently accesed file: '{file_path}'")
            else:
                # If the file node is not found, send a message indicating that the file was not found
                dispatcher.utter_message(f"Sorry, I couldn't find any recently accessed files")

class ActionFindRecentlyCreatedFiles(Action):
    
    def name(self) -> Text:
        return "action_find_recently_created_files"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:

        current_date = datetime.now().isoformat()

        # Connect to the Neo4j database
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))
        with driver.session() as session:
            
            # Find the folder node with the given name
            result = session.run("MATCH (f:Files) RETURN f ORDER BY datetime(f.ctime) DESC LIMIT 1")
            file_node = result.single().get("f")

            if file_node:
                # If the file node is found, extract the file path and send it as a message
                file_path = file_node.get("name")
                dispatcher.utter_message(f"Here's the recently created file: '{file_path}'")
                SlotSet("file_name", file_path)
                return [SlotSet("file_name", file_path)]
            else:
                # If the file node is not found, send a message indicating that the file was not found
                dispatcher.utter_message(f"Sorry, I couldn't find any recently created files")

class ActionFindRecentlyModifiedFiles(Action):
    
    def name(self) -> Text:
        return "action_find_recently_modified_files"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:

        current_date = datetime.now().isoformat()

        # Connect to the Neo4j database
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))
        with driver.session() as session:
            
            # Find the folder node with the given name
            result = session.run("MATCH (f:Files) RETURN f ORDER BY datetime(f.mtime) DESC LIMIT 1")
            file_node = result.single().get("f")

            if file_node:
                # If the file node is found, extract the file path and send it as a message
                file_path = file_node.get("name")
                dispatcher.utter_message(f"Here's the recently modified file:'{file_path}'")
                return [SlotSet("file_name", file_path)]
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
    
def recent_files_by_format(file_format):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))
    with driver.session() as session:
        # Find the number of files in the given format
        result = session.run("MATCH (file:Files) WHERE file.format = $format RETURN file.name", format=file_format)
        file = result.single().get("file.name")

    return file

class ActionFindRecentlyOpenedPublications(Action):
    def name(self) -> str:
        return "action_find_recently_opened_scientific_publications"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #type wise classification
        try:
            publications = recent_files_by_format("scientific publication")
            if publications:
                response = "Here's the recently opened scientific publication:\n"
                for publication in publications:
                    response += f"- '{publication}'\n"
                dispatcher.utter_message(response)
            else:
                dispatcher.utter_message("No recently opened scientific publications were found.")
        except:
            return [FollowupAction("action_fallback")]


        return []


    
def find_number_of_files_by_format(file_format):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))
    with driver.session() as session:
        # Find the number of files in the given format
        result = session.run("MATCH (file:Files) WHERE file.format = $format RETURN count(file)", format=file_format)
        number = result.single().get("count(file)")
        print("File Format:", file_format, "Count:", number)

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
        return [SlotSet("file_format", file_format)]
    
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai
import json
import re

def extract_code_from_chat_completion(response):
    pattern = r"```(.+?)```"
    matches = re.findall(pattern, response, re.DOTALL)
    if matches:
        return matches[0].strip()
    return None

def extract_paths(string):
    pattern = r"'(/.*?)'"
    paths = re.findall(pattern, string)
    return paths

class ActionFallback(Action):
    def __init__(self):
        # Initialize the ChatGPT model
        #self.chat_model = ChatCompletion("<your_openai_api_key>")
        self.conversation_history = []
        # Load the JSON file
        with open('secret.json') as f:
            secrets = json.load(f)

        # Access the secret key
        openai.api_key = secrets['OpenAI_API']

        self.messages = [
            {"role": "system", "content": '''You are a neo4j community edition 5.5 without apoc cypher query generating assistant with no additional package. 
                                        The graph has 2 nodes. A Files node with name, mtime for modification time, ctime for creation time, atime for last access time (all time properties are in string format. do not use date on ctime, atime, mtime, dbtime directly. convert it to datetime first), dbtime for when the file was added to the folder (Text data cannot be parsed to date with date()), format for file formats, size for file size in kb, numPages if it has pages and node called Keywords with name to hold keywords. 
                                        The Files nodes are connected to Keywords with relationship PER for person, LOC for Location, TYPE for document type, ORG for organization, and MISC for miscellaneous. 
                                        Only Files are connected to Keywords. Files -> Keywords. Help the user in finding a file by writing cypher queries.
                                        Here are 'TYPES' relationship: scientific publication, form, resume. If you encounter TYPES other than the mentioned, match it to scientific publication, form or resume. datetime().week() - duration({weeks: 1}
                                        For scientific jounals or scientific publications accessed last week, the query is MATCH (f:Files)-[:TYPE]->(k:Keywords{name:"scientific publication"}) WHERE datetime(f.atime) > datetime() - duration({weeks: 1}) RETURN f.name
                                        For first modified file, MATCH (f:Files) RETURN f.name ORDER BY datetime(f.mtime) DESC LIMIT 1
                                        For second last accessed file, MATCH (f:Files) RETURN f ORDER BY datetime(f.atime) DESC SKIP 1 LIMIT 1
                                        Return cypher queries within \''' and \''' '''},
            {"role": "system", "content": "If substracting with datetime, use datetime() - duration() to subract."},
            {"role": "system", "content": ""},
            {"role": "system", "content": "for getting files created last week, use datetime() - duration({weeks: 1}) in the cyher query. Do not use datetime().week() "},
            {"role": "system", "content": "Do not use datetime().week() or datetime().month() or datetime().day()"},
            {"role": "system", "content": "Do not use 'AS' while returning in the query"},
            {"role": "system", "content": "Query returned should be inside ``` and ```"},
            {"role": "system", "content": "For files created last week, use MATCH (f:Files) WHERE datetime(f.ctime) > datetime() - duration({weeks: 1}) RETURN f.name, f.format, f.size"},
            
        ]


    def name(self) -> Text:
        return "action_fallback"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user input
        user_input = tracker.latest_message.get('text')
        file_name = tracker.get_slot("file_name")
        query = None
        print("USER INPUT:", user_input)

        if file_name:
            self.messages.append(
                {"role": "system", "content": "Current file: " + str(file_name)},
            )

        if user_input:
            self.messages.append(
                {"role": "user", "content": user_input},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.messages
            )
            reply = chat.choices[0].message.content
            print(f"ChatGPT: {reply}")
            self.messages.append({"role": "assistant", "content": reply})
            query = extract_code_from_chat_completion(reply)


        if query:
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))
            with driver.session() as session:
                
                # Find the folder node with the given name
                try:
                    result = session.run(query)
                    print("result", result)
                    name_values = [record for record in result]

                    print(name_values, "name")
                    name_values = extract_paths(str(name_values))


                    if name_values:
                            # If the file node is found, extract the file path and send it as a message
                         
                            print(len(name_values), name_values)
                            dispatcher.utter_message(f"Here's your result: {name_values}")
                            SlotSet("file_name", name_values)
                            return [SlotSet("file_name", name_values)]
                    else:
                        # If the file node is not found, send a message indicating that the file was not found
                        dispatcher.utter_message(f"No files found: " + str(name_values))
                        return []
                except Exception as e:
                    dispatcher.utter_message(f"There's something wrong with the query. Please rephrase or give more context.")
                    print(e)
                    return []
                    
        dispatcher.utter_message(reply)

        # Add user input to conversation history
        #self.conversation_history.append(user_input)

        # Use ChatGPT to generate a response
        #response = self.generate_chat_response()

        # Send the response to the user
        #dispatcher.utter_message(response)

            


        return []

    def generate_chat_response(self) -> str:
        # Use the ChatGPT model to generate a response based on conversation history
        #response = self.chat_model.complete_conversation(self.conversation_history)
        #chat_response = response['choices'][0]['message']['content']
        chat_response = None

        return chat_response
    
class UtterAskFileName(Action):
    def name(self) -> Text:
        return "utter_ask_file_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Please provide the file name.")
        return []


class ActionSetFileName(Action):
    def name(self) -> Text:
        return "action_set_file_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        file_name = next(tracker.get_latest_entity_values("file_name"), None)
        return [SlotSet("file_name", file_name)]


