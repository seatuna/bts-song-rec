# bts-song-rec

:construction: This project is still a work in progress. :construction:

BTS song recommendations based on Spotify API data

The goal of this project is to create an app that will give you a BTS song recommendation based on a BTS song you input.
The Spotify API provides data that quantifies audio features for requested tracks. I've pulled this data, saved it to CSV files, which will be uploaded into a SQL database for an API to use.

Current status: Python script to pull data from Spotify and save to CSV is complete.

Next Steps:

- Use cosine similarity to calculate similarity of tracks to each other (functions already written in a gitignored jupyter notebook file, need to run it on a de-duped CSV)
- Save cosine similarity results to a database so they can be accessed in an API function call
- Create API (likely Flask)
- Create front end (currently considering React, styled components, and Vite as a server and build tool, maybe Vitest and Cypress for testing)
- Deploy
