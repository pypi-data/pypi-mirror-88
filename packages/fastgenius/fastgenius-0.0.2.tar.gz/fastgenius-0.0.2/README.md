[![fastgenius](./images/fastgenius_logo_with_namev3.png)](https://github.com/theomart/fastgenius)  
  
<br>
<br>


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


### Installation

````shell
pip install fastgenius
````

### Usage
````python
>>> import fastgenius
>>> genius = fastgenius.Genius('client_access_token')

>>> genius.get_artist('Madonna')
Artist(Madonna)

>>> genius.get_artist('Madona')
Artist(Madona (D’Lamotta))

>>> genius.get_artist(['Madonna', 'TuPac'])
{'Madonna': Artist(Madonna), 'TuPac': Artist(2Pac)}

>>> artists = genius.get_artist(['Madonna', 'TuPac'])
>>> artists['Madonna'].songs
[]

>>> artists = genius.get_artist(['Madonna', 'TuPac'], get_songs=True)
>>> artists['Madonna'].songs
[Song(Madonna - Into the Groove (Extended Remix)),
 Song(Leo The Kind - Material Girl),
 Song(Madonna - Masterpiece - MDNA World Tour / Live 2012),
 Song(Genius Polska Tłumaczenia - Madonna & Quavo - Future),
 ...]

>>> artists['Madonna'].songs[0].lyrics
"\\nAnd you can dance\\nFor inspiration\\nCome on\\nI'm waiting\\nCome, ..."

>>> big_syke = genius.get_artist('Big Syke', get_songs=True)
>>> len(big_syke.songs)
78

>>> big_syke = genius.get_artist('Big Syke', get_songs=True, primary_artist_only=True)
>>> len(big_syke.songs)
17

````