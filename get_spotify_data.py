""" This file gets the spotify data and creates csv files """
import base64
import configparser
import csv
from math import ceil
import requests
import numpy as np
import pandas as pd
from duplicate_song_ids import duplicate_song_ids

CONFIG = configparser.ConfigParser()
CONFIG.read('spotify.config')
CLIENT_ID = CONFIG['spotify_auth']['client_id']
CLIENT_SECRET = CONFIG['spotify_auth']['client_secret']

AUTH_STR = f'{CLIENT_ID}:{CLIENT_SECRET}'
B64_AUTH_STR = base64.b64encode(AUTH_STR.encode()).decode()
TOKEN_AUTH_HEADERS = {
    "Authorization": "Basic " + B64_AUTH_STR,
}
DATA = {
    "grant_type": "client_credentials"
}
TOKEN_RESPONSE = requests.post(
    'https://accounts.spotify.com/api/token', data=DATA, headers=TOKEN_AUTH_HEADERS)

ACCESS_TOKEN = TOKEN_RESPONSE.json()["access_token"]
BEARER_AUTH = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


def get_ids(json_response, with_names=False):
    if with_names:
        return [(item['id'], item['name']) for item in json_response['items']]
    return [item['id'] for item in json_response['items']]


def get_all_album_ids():
    BTS_ARTIST_ID = CONFIG['ids']['bts_artist_id']
    bts_album_endpoint = f'https://api.spotify.com/v1/artists/{BTS_ARTIST_ID}/albums'
    bts_albums_json = requests.get(
        bts_album_endpoint, headers=BEARER_AUTH).json()
    return get_ids(bts_albums_json)


def get_all_tracks():
    album_ids = get_all_album_ids()
    all_album_tracks = []
    all_track_names_and_ids = []
    total_tracks = 0
    for album_id in album_ids:
        tracks_endpoint = f'https://api.spotify.com/v1/albums/{album_id}/tracks?limit=40'
        bts_tracks_json = requests.get(
            tracks_endpoint, headers=BEARER_AUTH).json()
        all_album_tracks.append(get_ids(bts_tracks_json))
        all_track_names_and_ids.append(
            get_ids(bts_tracks_json, with_names=True))
        total_tracks = total_tracks + bts_tracks_json['total']
    all_tracks_flat = [
        tracks for album_tracks in all_album_tracks for tracks in album_tracks]
    all_track_names_and_ids_flat = [
        item for names_and_ids in all_track_names_and_ids for item in names_and_ids]

    print('Total # tracks (all_tracks_flat):', len(all_tracks_flat))
    print('Total # tracks: (total_tracks)', total_tracks)
    if len(all_tracks_flat) != total_tracks:
        raise LookupError('TOTAL TRACKS DON\'T MATCH')
    return all_tracks_flat, all_track_names_and_ids_flat


def remove_duplicate_songs(df):
    df['name_2'] = df['name'].str.strip()
    df['name_2'] = df['name_2'].str.lower()
    df.drop_duplicates(subset='name_2', keep='first', inplace=True)
    return df[~df['spotify_id'].isin(duplicate_song_ids)]


def write_audio_feature_csv_files():
    all_tracks, track_names_and_ids = get_all_tracks()
    split_len = ceil(len(all_tracks) / 100)

    # Split into arrays, Spotify limits the length of ids requested
    all_tracks_split_arr = np.array_split(all_tracks, split_len)

    for index, ids in enumerate(all_tracks_split_arr):
        audio_features_endpoint = f'https://api.spotify.com/v1/audio-features?ids={",".join(ids)}'
        audio_features_json = requests.get(
            audio_features_endpoint, headers=BEARER_AUTH).json()
        csv_columns = audio_features_json['audio_features'][0].keys()

        if index == 0:
            with open('bts_songs_spotify_audio_features.csv', 'w', encoding='utf-8') as new_csv:
                writer = csv.DictWriter(new_csv, fieldnames=csv_columns)
                writer.writeheader()

        try:
            with open('bts_songs_spotify_audio_features.csv', 'a', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerows(audio_features_json['audio_features'])
        except IOError:
            print("Error writing bts_songs_spotify_audio_features csv file")

    name_and_id_df = pd.DataFrame(
        track_names_and_ids, columns=['spotify_id', 'name'])
    name_and_id_df = remove_duplicate_songs(name_and_id_df)
    bts_audio_features = pd.read_csv('bts_songs_spotify_audio_features.csv')

    final_df = pd.merge(name_and_id_df, bts_audio_features,
                        how='left', left_on=['spotify_id'], right_on=['id'])
    # Remove extra id and name column
    final_df.drop(columns=['id', 'name_2'], inplace=True)
    final_df.to_csv('bts-songs-names-and-features-spotify.csv',
                    index=False, encoding='utf-8')


write_audio_feature_csv_files()

# Audio Features - Endpoint MAX 100 ids
# Response example for 'Life Goes On'!
# {
#     'danceability': 0.566,
#     'energy': 0.716, 'key': 1,
#     'loudness': -5.733,
#     'mode': 1,
#     'speechiness': 0.0424,
#     'acousticness': 0.00691,
#     'instrumentalness': 0,
#     'liveness': 0.37,
#     'valence': 0.45,
#     'tempo': 81.068,
#     'type': 'audio_features',
#     'id': '249gnXrbfmV8NG6jTEMSwD',
#     'uri': 'spotify:track:249gnXrbfmV8NG6jTEMSwD',
#     'track_href': 'https://api.spotify.com/v1/tracks/249gnXrbfmV8NG6jTEMSwD',
#     'analysis_url': 'https://api.spotify.com/v1/audio-analysis/249gnXrbfmV8NG6jTEMSwD',
#     'duration_ms': 207481,
#     'time_signature': 4
# }
