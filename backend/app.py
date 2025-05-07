from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_URL = "https://api.themoviedb.org/3"

def fetch_movie_data(movie_name):
    search_url = f"{TMDB_URL}/search/movie"
    response = requests.get(search_url, params={"query": movie_name, "api_key": TMDB_API_KEY})
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie_id = data['results'][0]['id']
            movie_details_url = f"{TMDB_URL}/movie/{movie_id}"
            details_response = requests.get(movie_details_url, params={"api_key": TMDB_API_KEY})
            if details_response.status_code == 200:
                return details_response.json()
        return {"error": "Movie not found"}
    else:
        return {"error": "Unable to fetch movie data from TMDb"}

@app.route("/movie", methods=["GET"])
def get_movie_info():
    movie_name = request.args.get("movie")
    
    if not movie_name:
        return jsonify({"error": "Movie name is required"}), 400
    
    movie_data = fetch_movie_data(movie_name)

    if "error" in movie_data:
        return jsonify(movie_data), 404
    
    return jsonify(movie_data), 200

if __name__ == "__main__":
    app.run(debug=True)
