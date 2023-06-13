import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def calculate_and_save_cos_sim():
    """Calculates the cosine similarity of songs based on the CSV file containing audio feature data and saves the results"""
    bts_songs_and_audio_features = pd.read_csv(
        'data/bts-songs-names-and-features-spotify.csv')

    # key, loudness, tempo are wildly different values, probably need to normalize. Removed from features.
    audio_features = bts_songs_and_audio_features[[
        'danceability', 'energy', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']]

    # calculate cosine similarity and save
    cos_similarity = cosine_similarity(audio_features)
    np.save('data/bts-song-cos-sim.npy', cos_similarity)
    print('cosine similarity calculated and saved to bts-song-cos-sim.npy')


calculate_and_save_cos_sim()
