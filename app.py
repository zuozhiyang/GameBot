from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
from igdb_api_python.igdb import igdb

app = Flask(__name__)
api_key = os.getenv('IGDB_API_KEY')
api_url = "https://api-endpoint.igdb.com/"
pusher_client = pusher.Pusher(
        app_id=os.getenv('PUSHER_APP_ID'),
        key=os.getenv('PUSHER_KEY'),
        secret=os.getenv('PUSHER_SECRET'),
        cluster=os.getenv('PUSHER_CLUSTER'),
        ssl=True)
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get_game_detail', methods=['POST'])
def get_game_detail():
    data = request.get_json(silent=True)
    game = data['queryResult']['parameters']['game']
    print(game)
    db = igdb(api_key)
    game_detail = db.games({
        'search': game,
        'fields': 'name'
    }).body
    game_detail =  db.games(int(game_detail[0]['id'])).body[0]
    summary = "None"
    if 'summary' in game_detail:
        summary = game_detail['summary']
    response = """
                Title : {0}
                Summary: {1}
                """.format(game_detail['name'],summary)
    reply = {
        "fulfillmentText": response,
    }
    return jsonify(reply)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    socketId = request.form['socketId']
    pusher_client.trigger('gamebot', 'new_message',
                          {'human_message': message, 'bot_message': fulfillment_text},
                          socketId)
    return jsonify(response_text)

def getRequest(url):
    headers = {
        'user-key': api_key,
        'Accept': 'application/json'
    }
    r = requests.get(api_url + url, headers=headers)
    r.body = json.loads(r.text)
    return r

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

if __name__ == '__main__':
    app.run()
