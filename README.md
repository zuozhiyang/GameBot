# Gamebot

## Description
A simple web conversation bot where users can ask about video games and returns summary of the games asked. It is built using Flask, Dialogflow, IGDB api, and etc.
Moreover, the bot utilizes Push Channels to enable the feature that that anybody viewing the bot page will see in realtime conversations going on. 

## Framework and Tools
### Frontend:
* HTML
* JavaScripts
* CSS

### Backend:
* Flask/Python
* Pusher


## External APIs:
* DialogueFlow: Natural Language Processing API (I trained a NLP agent specifically for this project thus it can only but well indentify titles of video games.)
* IGDB: RESTful API Database fo Video Game Information 


## Secure Tunneling to Local Host: 
* ngrok

## Prerequisite
1. Python
2. Flask
`pip install Flask`
3. Packages in requirements.txt
`pip install -r requirements.txt`
4. Trained DialogueFlow Agent
5. ngrok for tunneling

## Usage
1. replace public keys in .flaskenv and .env by your own credentials
2. start Flask application `export FLASK_APP=app.py & python -m flask run` (on localhost http://127.0.0.1:5000/ by default)
3. forward your url to your localhost using ngrok.

## Diagram
![arch](https://github.com/zuozhiyang/GameBot/blob/master/Architecture.png)
