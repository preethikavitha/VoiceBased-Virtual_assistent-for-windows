# VoiceBased-Virtual-assistent-for-windows


#### Welcome to Virtual Voice Assisant, a virtual voice assistant that can help you with a variety of tasks. This project utilizes machine learning and natural language processing to create a natural and intuitive experience for users. With Virtual Voice Assistant, you can easily interact with your computer by simply speaking to it.



## Features
Our virtual voice assistant comes packed with a wide range of features, including:
- To Athendicate Users Face to Verify the valid users.
- Bringing a smile to your face with its ability to tell you jokes.
- Keeping you informed with the latest news headlines.
- Telling you your IP address, so you can stay connected.
- Keeping you up-to-date with the latest movies and TV series.
- Providing you with the current weather report of any city you specify, or, if you don't specify a city, it will use your IP address to give you the weather for your current location.
- Testing your internet speed, so you can ensure you're getting the best connection.
- Showing you your system stats, including RAM and CPU usage, battery percent, and system specifications.
- Generating an image from the text you provide.
- Sending emails with an attachments, so you can stay in touch with friends and colleagues.
- send an whatsapp messages
- Performing system operations, including opening, closing, and switching tabs, copying, pasting, deleting, and selecting text, creating new files, minimizing, maximizing, switching, and closing windows.
- Taking screenshots, so you can capture important moments.
- Giving you brief information (3 sentences) on any topic or personality.
- Performing math operations and answering any general queries or GK questions.
- Opening apps and websites, so you can stay productive and connected.
- Taking notes, so you can keep track of important information.
- Saving your chat history, so you can refer back to it later.
- Performing Google search, so you can find the information you need.
- Playing songs and videos on YouTube, so you can enjoy your favorite music and videos.
- Showing maps of any city you specify and calculating the distance between two destinations in Google Maps.<br>

NOTE: Please note that in order for the virtual voice assistant to send emails, the option for "Less secure apps" must be enabled within your Gmail account. To allow access you can click [here](https://myaccount.google.com/lesssecureapps).

## API Keys
To run this program you will require a bunch of API keys. Register your API key by clicking the following links
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Wolframaplha API](https://products.wolframalpha.com/api)
- [News API](https://newsapi.org/)
- [TMDB API](https://developers.themoviedb.org/3/getting-started/introduction)
- [DreamStudio API](https://platform.stability.ai/docs/getting-started/authentication)

## Installation


Please make sure that `Python` and `pip` are installed on your system before proceeding with the installation.

Open a terminal and navigate to your home directory.

Clone the repository by using the command
```
git clone https://github.com/preethikavitha/VoiceBased-Virtual_assistent-for-windows.git
```

Navigate to the project directory using the command
```
cd VoiceBased-Virtual_assistent-for-windows
```

Obtain all necessary API keys and open the file `VoiceBased-Virtual_assistent-for-windows/Data/.env` to insert the keys into the designated placeholder fields.

Run the setup script by using the command
```
python setup.py
```
Install the requirements by using the command
```
pip install -r requirements.txt
```
Navigate to the `VoiceBased-Virtual_assistent-for-windows/Plugins/` directory and run the below command to start the virtual voice assistant.
```
python main.py
```

You're all set! The virtual voice assistant should be up and running now.

## Code Structure

    ├── VoiceBased-Virtual_assistent-for-windows
        ├── Data                              
            ├── .env                          # Stores the API keys, email and password.
            ├── chat_model                    # Directory that stores the trained model used to understand user's intent
            ├── chats.db                      # Database file that stores the chat history
            ├── intents.json                  # Data on which the model is trained
            ├── label_encoder.pickle          # Converts text labels into numerical values
            └── tokenizer.pickle              # Splits the text into individual tokens
        ├── Plugins
            ├── API_functionalities.py        # Contains functions that interact with different APIs
            ├── browsing_functionalities.py   # Contains functions for web browsing
            ├── database.py                   # Contains functions for interacting with the chat history database
            |__ whatsapp.py                   # Contains functions for send an whatsapp messages
            |
            ├── gmail.py                      # Contains functions for sending emails with an attachment
            ├── image_generation.py           # Contains functions for generating images from text
            ├── main.py                       # It is the entry point of the virtual voice assistant
            ├── model_training.py             # Contains functions for training the intent recognition model
            ├── system_operations.py          # Contains functions for performing system operations
            └── websites.py                   # Contains a list of websites that the virtual voice assistant can open
        ├── requirements.txt                  # Lists the dependencies required for the project
        └── setup.py                          # Contains code for setting up the virtual voice assistant




