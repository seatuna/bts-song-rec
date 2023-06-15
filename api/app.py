import configparser
from flask import Flask
import json
import numpy as np
import pandas as pd

CONFIG = configparser.ConfigParser()
CONFIG.read("app.config")
HOST = CONFIG["dev"]["host"]
PORT = CONFIG["dev"]["port"]

app = Flask(__name__)


@app.route("/song/<string:song_id>", methods=["GET"])
def get_song_data(song_id):
    """Get song"""
    bts_songs = pd.read_csv("data/bts-songs-names-and-features-spotify.csv")
    song = bts_songs.loc[bts_songs["spotify_id"] == song_id]
    print(song.index[0])
    return json.loads(song.reset_index().to_json(orient="records"))[0]


@app.route("/song/<string:song_id>/similar", methods=["GET"])
def get_similar_songs(song_id):
    """Get first five similar songs"""
    bts_songs = pd.read_csv("data/bts-songs-names-and-features-spotify.csv")
    song = bts_songs.loc[bts_songs["spotify_id"] == song_id]
    index = song.index[0]

    cos_sim = np.load("data/bts-song-cos-sim.npy")
    similar_songs = list(enumerate(cos_sim[index]))
    # First 5 similar songs
    sorted_similar_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)[1:6]
    index_list = [value[0] for value in sorted_similar_songs]

    # Retrieve songs from songs df
    similar_songs_df = bts_songs.iloc[index_list]

    return json.loads(similar_songs_df.reset_index().to_json(orient="records"))


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
