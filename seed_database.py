"""Script to seed database."""

import os
import json
from random import choice, randint

import crud
import model
import server

os.system('dropdb visualplaylist')
os.system('createdb visualplaylist')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/playlists.json') as f:
    playlist_data = json.loads(f.read())

playlists_in_db = []

for playlist in playlist_data:

    url = playlist["title"]
    playlist_name = playlist["overview"]
    playlist_tracks = playlist["tracks"]

    db_playlist = crud.create_playlist
    playlists_in_db.append(db_playlist)


model.db.session.add_all(playlists_in_db)
model.db.session.commit()


for n in range(5):
    username = f'user{n}'
    password = 'test'

    user = crud.create_user(username, password)
    model.db.session.add(user)

model.db.session.commit()