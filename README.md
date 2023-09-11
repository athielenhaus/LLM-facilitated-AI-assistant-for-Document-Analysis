# AI Document ChatBot

A project description can be found on the main branch of the repository.

__To test the live app:__
- go here: https://acc-check.streamlit.app/
- NOTE: the app may be deactivated during longer periods of inactivity. You can also run the app locally (see below).


__Running the App locally:__  
First, fork the repository and / or copy the repo files to a folder on your computer. Then you have two options:

- Option 1: you can run the app by installing the relevant libraries on your system:
    - create a virtual environment, activate it and install all the Python libraries from the requirements.txt file
    - with the virtual environment activated, use a terminal to navigate to the directory with the project files, and run the following command: python -m streamlit run acc_checkerUI.py

- Option 2: you can run the app using Docker (note: you must have Docker installed). To do this:
    - build the docker image - with a terminal, navigate to the directory containing the files and run the following command to build the Docker image (don't forget the period at the end of the command): docker build -t accchatbot .
    - once the previous step was successfully completed, run the following command: docker run -e "OPENAI_API_KEY=<insert your OpenAI API key here>" -p 8501:8501 accchatbot. NOTE: the web app will open even if you do not insert an OpenAI API key, but the embedding and chatbot functions will not work




