from flask import Flask, request, jsonify
from flask_cors import CORS
import AppleMusicWebScrape
import SpotifyAPI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/convert', methods=['POST'])

def process_data():
    try:
        data = request.get_json()
        if not data or 'inputValue' not in data:
            return jsonify({"error": "Invalid request"}), 400

        url = data.get('inputValue')
        songs, name = AppleMusicWebScrape.web_scrape(url)
        result = SpotifyAPI.create_playlist(songs, name)
   
        response = jsonify(result)
        return response

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=8000)