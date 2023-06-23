import configparser
from flask import Flask, jsonify, abort, request
import numpy as np
import pandas as pd

CONFIG = configparser.ConfigParser()
CONFIG.read("app.config")
HOST = CONFIG["dev"]["host"]
PORT = CONFIG["dev"]["port"]

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    """Return generic 404 error"""
    return jsonify(error=str(e)), 404


@app.route("/song/<string:song_id>", methods=["GET"])
def get_song_data(song_id):
    """Get song"""
    bts_songs = pd.read_csv("data/bts-songs-names-and-features-spotify.csv")
    song = bts_songs.loc[bts_songs["spotify_id"] == song_id]

    if song.empty:
        abort(404, description="Song not found")

    print(song)
    print(song.index[0])
    return jsonify(song.reset_index().to_dict(orient="records")[0])


@app.route("/song/<string:song_id>/similar", methods=["GET"])
def get_similar_songs(song_id):
    """Get first five similar songs"""
    bts_songs = pd.read_csv("data/bts-songs-names-and-features-spotify.csv")
    song = bts_songs.loc[bts_songs["spotify_id"] == song_id]

    if song.empty:
        abort(404, description="Song not found")

    index = song.index[0]
    cos_sim = np.load("data/bts-song-cos-sim.npy")
    similar_songs = list(enumerate(cos_sim[index]))

    # First 5 similar songs
    sorted_similar_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)[1:6]
    index_list = [value[0] for value in sorted_similar_songs]

    # Retrieve songs from songs df
    similar_songs_df = bts_songs.iloc[index_list]

    return jsonify(similar_songs_df.reset_index().to_dict(orient="records"))


@app.route("/song/search", methods=["GET"])
def search_song():
    """Search for song title and return ids"""
    args = request.args
    query = args.get("query")
    print(query)

    bts_songs = pd.read_csv("data/bts-songs-names-and-features-spotify.csv")
    filtered_songs = bts_songs[bts_songs["name"].str.lower().str.contains(query)]
    search_results_list = filtered_songs[["name", "spotify_id"]].to_dict(
        orient="records"
    )

    return jsonify(search_results_list)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
