# README.md

This repository contains code for a project that involves a middleware, an active checker script, and a RASA server. Follow the instructions below to set up and run the project.

## Prerequisites

- Python 3.x installed on your machine
- NEO4j Server installed and configured
- Access to the OpenAI website to generate an API token

## Instructions

0. Install requirements.

```console
pip install -r requirements.txt
```

1. Clone the repository to your local machine:

```console
cd Middleware
NEO4J-HOME/bin/neo4j start
```

2. Run the activeChecker.py script. Replace <python_command> with the appropriate command for your system.

```console
<python_command> activeChecker.py
```

3. Go to the OpenAI website and generate an API token. Copy the generated token.

4. Go to the NLU folder and create a file named secret.json. Open the file and add the following JSON structure, replacing <api_token> with the token you generated in the previous step:

```json
Copy code
{
  "api_token": "<api_token>"
}
```

5. Start the RASA server by running the actions and endpoint. Replace <rasa_command> with the appropriate command for your system.

```console

<rasa_command> run actions
<rasa_command> run --endpoints endpoints.yml --port 5005
```

6. Run GUI.py inside GUI folder.

```console
<python_command> GUI.py
```

That's it! You have successfully set up and started the project.