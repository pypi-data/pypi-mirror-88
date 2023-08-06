# roland-gamos

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



### Usage
````python
import fastgenius
genius = fastgenius.Genius()
artist_name_list = ['Kekra', 'La F']
artist_name = 'Kekra'

genius.get_artist_id(artist_name_list)
genius.get_artist_id(artist_name)
genius.get_artist_info(artist_name_list)
genius.get_artist_info(artist_name)
genius.get_artist_songs(artist_name)
genius.get_artist_songs(artist_name_list)
genius.get_song_info('Kekra Ailleurs')
genius.get_song_info(['Kekra ailleurs', 'kekra laisse les faire'])
genius.get_artist_lyrics(artist_name)
genius.get_songs_from_tag('rock', max_nb_songs=100) # takes a lot of time
````