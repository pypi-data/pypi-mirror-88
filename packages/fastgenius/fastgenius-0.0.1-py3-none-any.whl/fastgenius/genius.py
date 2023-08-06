import logging
from tqdm.notebook import tqdm
from typing import Union, List, Dict
import os
from contextlib import ExitStack

from . import types
from . import asynchronous
from . import utils

logging.getLogger("fastgenius").addHandler(logging.NullHandler())


class Genius:
    """User-level interface with the Genius.com API and public API.

    Args:
        client_access_token (:obj:`str`, optional): API key provided by Genius. If you don't pass it at initialization,
            make sure that it is in the GENIUS_ACCESS_TOKEN environment variable.
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        verbose (:obj:`bool`, optional): Turn printed messages on or off.

    Attributes:
        verbose (:obj:`bool`): Turn printed messages on or off.
        asynchronous (:class:`asynchronous.Asynchronous`): Contains function for individual elements.
        progress_bar (:obj:`bool`): Set to true to display a progress bar, handy to keep track of the progress
            when fetching 1000's of songs.

    Returns:
        :class:`Genius`

    Note:
        Set the environment variable by typing this in your shell: export GENIUS_ACCESS_TOKEN="my_access_token_here"
        Default excluded terms are the following regular expressions:
        :obj:`track\\s?list`, :obj:`album art(work)?`, :obj:`liner notes`,
        :obj:`booklet`, :obj:`credits`, :obj:`interview`, :obj:`skit`,
        :obj:`instrumental`, and :obj:`setlist`.

    """

    def __repr__(self):
        return "Genius Instance"

    def __init__(
        self,
        client_access_token: str = None,
        response_format: str = "plain",
        verbose: bool = False,
        progress_bar: bool = False,
    ):

        if not client_access_token:
            client_access_token = os.environ.get("GENIUS_ACCESS_TOKEN", None)
            assert client_access_token, (
                "You should either pass an API token in Genius, like "
                "Genius(client_access_token=aeECVGlYppnGqeuhIUHhiihuihDUVIt),"
                " either have it as an environment variable under the name "
                "GENIUS_ACCESS_TOKEN"
            )

        self.response_format = response_format
        self.asynchronous = asynchronous.Asynchronous(
            client_access_token=client_access_token, response_format=response_format
        )
        self.verbose = verbose
        self.progress_bar = progress_bar

    @utils.method_logger
    def get_artist(
        self,
        search_term: Union[List[Union[int, str, types.Artist]], str, int, types.Artist],
        get_songs: bool = False,
        with_lyrics: bool = True,
        max_nb_songs: int = 1000,
        primary_artist_only: bool = False,
        get_song_full_info: bool = False,
        skip_non_songs: bool = False,
        require_complete_lyrics: bool = True,
    ) -> Union[Dict[Union[int, str, types.Artist], types.Artist], types.Artist]:
        """Get artist(s), optionally including the artist(s)' song(s) and their lyrics.

        Args:
            search_term (list of str, int and/or Artist or single str, int or Artist):
                Used to get search results from genius if you pass a string. You can also pass :class:`types.Artist` 
                or Genius artist ID. You can pass a list mixing those types or a single element.
            get_songs: Populates the songs attribute of the resulting artist with the number of songs defined by 
                max_nb_songs
            with_lyrics (bool, optional): Set this to True if you want to get the lyrics of the songs you fetch. 
                You can get the lyrics of the first song like this: artist.songs[0].lyrics
            max_nb_songs (int, optional):
                The function is going to fetch up to this number of songs by artist. 1000, the default value, should
                get you the whole discography from most artists.
            primary_artist_only (bool, optional):
                Set this to true if you only want songs where the artist you looked for is the primary artist. **Note**:
                we fetch max_nb_songs where the artist appears, and then filter out the songs where they are not the
                primary artist. If you ask for 50 songs where the artist is primary, you might get < 50 songs.
            get_song_full_info (bool, optional):
                Check XXX to see which song attributes only come in the full info. Getting the full info of a song
                takes one more HTTP request to the developer API, the execution will therefore be faster when
                set to False. Default is False.
            skip_non_songs (bool, optional):
                If set to True, we will only return what we believe are lyrics, and not something else.
            require_complete_lyrics:
                Lyrics on Genius are tagged complete if all the lyrics of a song have been transcribed, it's tagged as
                incomplete otherwise. You can choose to ignore songs that have incomplete lyrics by setting this
                parameter to True.

        Returns:
            dict with your search term / id / artist as keys and list of :class:`types.Song` as values

        Examples:
            >>> import fastgenius
            >>> genius = fastgenius.Genius('client_access_token')

            You can fetch one song, searching for the title:\n
            >>> genius.get_artist('Madonna')
            Artist(Madonna)

            Be sure to check the results if you are not sure your iinput is correct, here is something that can happen
            when misspelling:\n
            >>> genius.get_artist('Madona')
            Artist(Madona (D’Lamotta))

            You can also fetch multiple ones:\n
            >>> genius.get_artist(['Madonna', 'TuPac'])
            {'Madonna': Artist(Madonna), 'TuPac': Artist(2Pac)}

            By default we won't fetch the songs of the song:\n
            >>> artists = genius.get_artist(['Madonna', 'TuPac'])
            >>> artists['Madonna'].songs
            []

            You can fetch the songs by setting get_songs=True:\n
            >>> artists = genius.get_artist(['Madonna', 'TuPac'], get_songs=True)
            >>> artists['Madonna'].songs
            [Song(Madonna - Into the Groove (Extended Remix)),
             Song(Leo The Kind - Material Girl),
             Song(Madonna - Masterpiece - MDNA World Tour / Live 2012),
             Song(Genius Polska Tłumaczenia - Madonna & Quavo - Future),...

            You can get the lyrics from those songs by default:\n
            >>> artists['Madonna'].songs[0].lyrics
            "\\nAnd you can dance\\nFor inspiration\\nCome on\\nI'm waiting\\nCome, ..."

            You can ask the function to filter out songs where the artist is not the main artist (they call it primary
            artist, and you can get their name in song.primary_artist_name). For example, Big Syke wrote a lot for other
            rappers, mainly 2Pac, so his songs count changes dramatically when considering only the ones where he
            actually raps:\n
            >>> big_syke = genius.get_artist('Big Syke', get_songs=True)
            >>> len(big_syke.songs)
            78
            >>> big_syke = genius.get_artist('Big Syke', get_songs=True, primary_artist_only=True)
            >>> len(big_syke.songs)
            17

        Note:
            Sometimes genius's search is wrong, for example if you search 'La F' a french rapper, it will return
            the 'Travis Scott' :class:`types.Artist`object. Make sure to check the output and to use the artist_id
            if you know it as this will directly fetch the artist and not use search.

        """
        search_term = utils.remove_nones(search_term)

        with ExitStack() if not self.progress_bar else tqdm(
            total=utils.get_object_len(search_term), ncols="100%"
        ) as progress_bar:
            progress_bar = progress_bar if isinstance(progress_bar, tqdm) else None
            artists = self.asynchronous.run_async(
                self.asynchronous.get_artist,
                search_term,
                get_songs=get_songs,
                with_lyrics=with_lyrics,
                max_nb_songs=max_nb_songs,
                primary_artist_only=primary_artist_only,
                skip_non_songs=skip_non_songs,
                get_song_full_info=get_song_full_info,
                require_complete_lyrics=require_complete_lyrics,
                progress_bar=progress_bar,
            )

        if type(search_term) is list:
            return dict(zip(search_term, artists))
        else:
            return artists

    def get_song(
        self,
        search_term: Union[List[Union[int, str, types.Song]], int, str, types.Song],
        with_lyrics: bool = True,
        get_full_info: bool = False,
        get_annotations: bool = False,
    ) -> Union[Dict[Union[int, str], types.Song], types.Song]:
        """Get song(s) optionally with lyrics and full metadata.

        Args:
            search_term (:obj:`int`, :obj:`str` or :obj:`list` of :obj:`int` and/or :obj:`str`):
                The song search term, Song ID or song URL. You can fetch multiple results by giving list mixing those
                3 types. A search term could be the artist name followed by the song title
                (eg. "Michael Jackson Beat it") or just the song title (eg. "Beat it")
            with_lyrics: If set to true the songs objects returned will contain the lyrics of the song in the lyrics
                attribute, you can then access the lyrics by executing song.lyrics
            get_full_info: You can choose to get the full info of the song, this will only make a difference if you used
                a search term and not the song's id. It takes 1 more request per song, you can check here XXX what
                additional attribute this will get you.
            get_annotations (bool, optional): If set to yes, we will fetch the song's annotations and put it in the
                annotations attribute that you can access like so: song.annotations. The format is a list of tuples,
                with a tuple looking like : ('piece of lyrics that is annotated', 'annotation')

        Returns:
            A dictionary with the search term as the key and the found song as the value.

        Examples:
            >>> import fastgenius
            >>> genius = fastgenius.Genius('client_access_token')

            You can fetch one song, searching for the title:\n
            >>> genius.get_song('La isla bonita')
            Song(Madonna - La Isla Bonita)

            You can also fetch multiple ones, note that you can pass th artist name if you know it to help the search.\n
            >>> genius.get_song(['La isla bonita', '2Pac all eyes on mi'])
            {'La isla bonita': Song(Madonna - La Isla Bonita),
             'all eyes on mi': Song(2Pac - All Eyes on Me)}

            By default we will fetch the lyrics of the song:\n
            >>> songs = genius.get_song(['La isla bonita', 'all eyes on mi'])
            >>> songs['La isla bonita'].lyrics
            "\\n¿Cómo puede ser verdad?\\nLast night I dreamt of San Pedro\\nJust ..."

            You can choose to get the full info on the song, to get the release date for example:\n
            >>> song = genius.get_song('La isla bonita', get_full_info=True)
            >>> song.release_date
            '1986-06-30'

            You can mix types: using search terms but also URL and IDs:\n
            >>> genius.get_song(['https://genius.com/Madonna-la-isla-bonita-lyrics', 6576], get_full_info=True)
            {'https://genius.com/Madonna-la-isla-bonita-lyrics': Song(Madonna - La Isla Bonita),
             6576: Song(2Pac - All Eyez on Me)}

            You can learn about french champagne by looking at people annotations on the song:\n
            >>> song = genius.get_song('all eyez on me 2pac', get_annotations=True)
            >>> song.annotations[-2]
            ('Devoted to servin’ this Moët and pay checks',
            ['Moët & Chandon is a prominent French champagne brand.'])

        Note:
            We use genius.com's search to find the song, results can sometimes be off, it is strongly advised to
            have a process checking that the return song is the one you expected.

        """
        search_term = utils.remove_nones(search_term)

        with ExitStack() if not self.progress_bar else tqdm(
            total=utils.get_object_len(search_term), ncols="100%"
        ) as progress_bar:
            progress_bar = progress_bar if isinstance(progress_bar, tqdm) else None
            songs = self.asynchronous.run_async(
                self.asynchronous.get_song,
                search_term,
                progress_bar=progress_bar,
                with_lyrics=with_lyrics,
                get_full_info=get_full_info,
                get_annotations=get_annotations,
            )

        if type(search_term) is list:
            return dict(zip(search_term, songs))
        else:
            return songs

    def get_songs_from_tag(
        self, tag: str, max_nb_songs: int = 100, get_lyrics: bool = True
    ):
        """Gets songs belonging to a tag, which most of the time a music genre.

        Args:
            tag (str): The tag you want to get songs for. To find a list of existing tags, check XXX.
            max_nb_songs (int, optional): The number of songs you want to get for this tag.
            get_lyrics (bool, optional): By default we will fetch lyrics, this involves an additional request per song
                if you only need the songs' metadata you better set this to False.

        Returns:
            list of songs.

        """
        song_list = self.asynchronous.run_async(
            self.asynchronous.get_songs_from_tag,
            tag,
            max_nb_songs=max_nb_songs,
            get_lyrics=get_lyrics,
        )
        return song_list
