import configparser
from flask import Flask
import numpy as np
import pandas as pd

CONFIG = configparser.ConfigParser()
CONFIG.read("app.config")
HOST = CONFIG["dev"]["host"]
PORT = CONFIG["dev"]["port"]

app = Flask(__name__)


@app.route("/<string:id>", methods=["GET"])
def get_song_data(song_id):
    """Get song"""
    bts_songs = pd.read_csv("data/bts-songs-names-and-features-spotify.csv")
    song = bts_songs.loc(song_id).to_json()
    return song


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
