import re
from asyncio.events import AbstractEventLoop
from typing import Union, List, Callable
from tqdm.notebook import tqdm
from concurrent.futures import ProcessPoolExecutor
import asyncio
import logging
import warnings
import nest_asyncio

from . import types
from . import api
from . import utils
from . import parser
from .requester import Requester
import pickledb


@utils.all_methods(utils.method_logger)
class Asynchronous:
    """Class containing little async building blocks to make bigger functions. Every method in the Genius class
    has one or more corresponding method(s) here. There are multiple corresponding methods in cases where we want to
    get the same output (eg artist's songs) from different input (eg. artist_name, artist_id), in this case they will
    one method per input type (eg get_artist_songs_from_artist_id, get_artist_song_from_artist_name);

    Args:
        client_access_token (:obj:`str`, optional): API key provided by Genius.
    Attributes:
        asyncio_loop (:class:`AbstractEventLoop`): The asyncio event loop used to run all the coroutines.
        public_api (:class:`PublicAPI`): This attribute gives access to a wrapper for every function implemented by
            the public API (eg. public_api.search_all('Eyes of the Tiger'))
        dev_api (:class:`DeveloperAPI`): This attribute gives access to a wrapper for every function implemented by
            the developer API (eg. public_api.search_all('Eyes of the Tiger'))
        pool (:class:`ProcessPoolExecutor`): Used in asyncio.run_in_executor to run every blocking task in parallel
            processes. Right now it's only used for extracting the lyrics from the HTML page and I am not sure it gives
            great speed improvement.
    """

    pool: ProcessPoolExecutor
    asyncio_loop: AbstractEventLoop
    requester: Requester
    public_api: api.PublicAPI
    dev_api: api.DeveloperAPI

    def __init__(self, client_access_token: str, response_format: str):

        self.asyncio_loop = asyncio.get_event_loop()
        self.requester = Requester(
            asyncio_loop=self.asyncio_loop, client_access_token=client_access_token
        )
        self.public_api = api.PublicAPI(
            requester=self.requester, response_format=response_format
        )
        self.dev_api = api.DeveloperAPI(
            requester=self.requester, response_format=response_format
        )
        self.pool = ProcessPoolExecutor()
        self.db = pickledb.load("test.db", True)

    def run_async(
        self,
        function_to_execute: Callable,
        function_input: Union[List[object], object],
        **kwargs,
    ) -> Union[List[object], object]:
        """Runs the given function(s) asynchronously on a list of element or a single element. We pass a dict
        associating a different function for every input type. It forwards any additional arguments to the function
        it calls.

        Args:
            function_to_execute (function): The function to execute on the object / every object of the list.
            function_input: A list of object or a single object we want to run the function on.
            **kwargs: All the parameters that are going to be forwarded to function_to_execute

        Returns:
            The result of the function called. So it can be anything.

        Examples:
            >>> import fastgenius
            >>> genius = fastgenius.Genius('client_access_token')


            >>> artists = self.asynchronous.run_async(
                genius.asynchronous.get_artist,  # The function to execute on ...
                ['2Pac', 'Madonna'],  # ... each of those objects, asynchronously;
                get_songs=True  # A kwarg that will be passed to asynchronous.get_artist
            )


        """

        # The function that we call in case the input is a list
        async def run_async_for_lists(
            function_to_execute_wrapper, function_input_wrapper, **kwargs_wrapper
        ):
            tasks = [
                function_to_execute_wrapper(element, **kwargs_wrapper)
                for element in function_input_wrapper
            ]
            return await asyncio.gather(*tasks)

        # The function we call in case the input is a single element
        async def run_async_for_single_elements(
            function_to_execute_wrapper, function_input_wrapper, **kwargs_wrapper
        ):
            return await function_to_execute_wrapper(
                function_input_wrapper, **kwargs_wrapper
            )

        if type(function_input) is list:
            wrapper = run_async_for_lists
        else:
            wrapper = run_async_for_single_elements

        # Sometimes we get the error (and warning sometimes) saying "The loop is already running". Since we got the loop
        # with get_event_loop(), that can (in my best knowledge) only happen if we are running the code within a
        # pre-existing event loop like Jupyter. If you have a better fix, happy to discuss it.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            try:
                return self.asyncio_loop.run_until_complete(
                    wrapper(function_to_execute, function_input, **kwargs)
                )
            except RuntimeError:  #  Catching this loop is already running
                nest_asyncio.apply(self.asyncio_loop)
                return self.asyncio_loop.run_until_complete(
                    wrapper(function_to_execute, function_input, **kwargs)
                )

    async def fetch_artist_from_artist_id(self, artist_id: int) -> types.Artist:
        assert artist_id is not None, "artist_id must be specified"
        api_response = await self.dev_api.artist(artist_id)
        artist = types.Artist(api_response=api_response.get("artist", {}))
        return artist

    async def search_artist(self, artist_name) -> types.Artist:
        # db_result = self.db.get(artist_name)
        # if db_result:
        #    return db_result

        assert artist_name, "artist_name must be specified"
        artist_search_response = await self.public_api.search_artists(artist_name)
        found_artist = api.PublicAPI.get_item_from_public_api_search_response(
            response=artist_search_response,
            search_term=artist_name,
            type_="artist",
            result_type="name",
        )
        artist_id = found_artist.get("id", None) if found_artist else None

        # if artist_id:
        #    self.db.set(artist_name, artist_id)

        return types.Artist(api_response=found_artist)

    # Analogue to Genius.get_artist
    async def get_artist(
        self,
        search_term: Union[str, int, types.Artist],
        get_songs=False,
        with_lyrics: bool = True,
        max_nb_songs: int = 1000,
        primary_artist_only: bool = False,
        sort: str = "popularity",
        skip_non_songs: bool = False,
        get_song_full_info: bool = False,
        require_complete_lyrics: bool = True,
        progress_bar=None,
    ) -> Union[None, types.Artist]:
        """Gets the list of songs for the given artist. Used in :meth:`get_artist_songs_from_artist`

        Args:
            primary_artist_only:
            get_songs:
            max_nb_songs:
            sort: If you are not going for the whole discography of the artist you can choose which criteria is going to
                be used to determine which will be the first max_nb_songs
            skip_non_songs: Users can create song pages for whatever they like, for example track listing, some even
                write articles on song pages. If you wish to skip those, set this to True.
            get_song_full_info:
                You can choose to get the full info of each song fetched, this will require an additional request for
                each song. Refer to XXX to see which additional attributes you will get in the full info.
            with_lyrics:
            require_complete_lyrics:
            progress_bar:
            search_term:

        Returns:
            A list of :class:`types.Song`


        """

        search_term_type = type(search_term)
        if search_term_type is str:  # if it's a search term
            artist = await self.search_artist(search_term)
        elif search_term_type is int:  # if it's an artist ID
            artist = await self.fetch_artist_from_artist_id(search_term)
        elif search_term_type is types.Artist:
            artist = search_term
        else:
            logging.warning(
                f"Ignoring {search_term} as it is neither a str, int or types.Artist"
            )
            return None

        if not get_songs:
            return artist

        per_page = min(max_nb_songs, 50)
        nb_request_by_artist_id = (max_nb_songs - 1) // per_page + 1

        artist_songs = []

        coroutines_songs_search = [
            self.dev_api.artist_songs(
                artist_id=artist.id, per_page=per_page, page=page, sort=sort
            )
            for page in range(1, nb_request_by_artist_id + 1)
        ]

        for coro_page in asyncio.as_completed(coroutines_songs_search):
            page = await coro_page

            page_songs = [
                song_info
                for song_info in page.get("songs", [])
                if (
                    parser.Parser.is_song(song_info.get("title", ""))
                    or not skip_non_songs
                )
                and (
                    song_info.get("lyrics_state") == "complete"
                    or not require_complete_lyrics
                )
                and (
                    song_info.get("primary_artist", {}).get("id") == artist.id
                    or not primary_artist_only
                )
            ]

            songs = []
            if get_song_full_info and page_songs:
                coroutines_song_info = [
                    self.get_song_from_song_id(song_info.get("id"))
                    for song_info in page_songs
                    if "id" in song_info
                ]
                if coroutines_song_info:
                    songs = await asyncio.gather(*coroutines_song_info)
            else:
                songs = [types.Song(api_response=song_info) for song_info in page_songs]

            if with_lyrics:
                if songs:
                    coroutines = (self.add_lyrics_to_song(song) for song in songs)
                    songs = await asyncio.gather(*coroutines)

            artist_songs.extend(songs)

        if progress_bar:
            assert isinstance(progress_bar, object)
            progress_bar.update(1)

        artist.songs = artist_songs
        return artist

    async def add_lyrics_to_song(self, song: types.Song) -> types.Song:
        song.lyrics = await self.get_lyrics_from_song_url(song.url)
        return song

    async def fetch_song_from_song_id(self, song_id: int) -> types.Song:
        assert song_id is not None, "song_id must be specified"
        song_info_response = await self.dev_api.song(song_id)
        return types.Song(api_response=song_info_response.get("song", {}))

    async def search_song(self, search_term):
        assert search_term, "search_term must be specified"
        search_response = await self.public_api.search_all(search_term)
        api_response = api.PublicAPI.get_item_from_public_api_search_response(
            search_response, search_term, type_="song", result_type="title"
        )
        if api_response:
            song = types.Song(api_response=api_response)
        else:
            return None
        return song

    # Analogue to Genius.get_song
    async def get_song(
        self,
        search_term: Union[int, str, types.Song],
        get_full_info: bool = False,
        get_annotations: bool = False,
        with_lyrics: bool = True,
        progress_bar: tqdm = None,
    ):
        if type(search_term) is int:
            song: types.Song = await self.fetch_song_from_song_id(search_term)

        elif type(search_term) is str:  # Input is either URL or search term
            if "genius.com" in search_term:  # We are dealing with an URL
                song_page_html = await self.requester.make_request(
                    search_term, web=True
                )
                song_id = utils.get_song_id_from_song_page(song_page_html)
                song = await self.fetch_song_from_song_id(song_id)

            else:  # The input is a genuine term to search
                song: types.Song = await self.search_song(search_term)
                if get_full_info:
                    song: types.Song = await self.fetch_song_from_song_id(song.id)
        elif type(search_term) is types.Song:
            song = search_term

        else:  # Not good type
            raise TypeError(
                f"Type should be either str, int or types.Song, you gave {type(search_term)}"
            )

        if with_lyrics:
            song.lyrics = await self.get_lyrics_from_song_url(song.url)

        if get_annotations:
            referents = await self.dev_api.referents(
                song_id=song.id, text_format="plain"
            )
            annotations = [
                (
                    referent["fragment"],
                    [
                        annotation["body"]["plain"]
                        for annotation in referent["annotations"]
                    ],
                )
                for referent in referents["referents"]
            ]
            song.annotations = annotations

        if progress_bar:
            progress_bar.update(1)

        return song

    async def get_lyrics_from_song_url(
        self, song_url: str, remove_section_headers: bool = True
    ):
        try:
            url_path = re.search(r".*genius\.com/(.*)", song_url).group(1)
        except AttributeError:
            raise Exception(
                "The URL doesn't even seem to contain genius.com in it, it's definitely not a song URL"
            )
        html = await self.requester.make_request(url_path, web=True)
        # We send the blocking task (lyrics scraper) to the process pool so that it doesn't stop the event loop
        return await self.asyncio_loop.run_in_executor(
            self.pool,
            parser.Parser.parse_html_for_lyrics,
            html,
            remove_section_headers,
        )

    async def get_tag_songs_page(self, tag: str, page: int):
        path = f"tags/{tag}/all"
        params = {"page": page}
        return await self.requester.make_request(path, params=params, web=True)

    async def get_songs_from_tag(
        self,
        tag: str,
        max_nb_songs: int = 100,
        get_lyrics: bool = True,
        remove_section_headers: bool = True,
    ):
        """Returns all the songs tagged :param:`tag`

        Args:
            tag:
            max_nb_songs:
            get_lyrics:
            remove_section_headers:

        Returns:

        """
        songs = []
        per_page = min(max_nb_songs, 20)  # 20 is the total number of songs on 1 page
        nb_request = (max_nb_songs - 1) // per_page + 1

        coroutines_songs_search = [
            self.get_tag_songs_page(tag=tag, page=page)
            for page in range(1, nb_request + 1)
        ]

        for coroutine_search_page in asyncio.as_completed(coroutines_songs_search):
            page = await coroutine_search_page

            songs_url = await self.asyncio_loop.run_in_executor(
                self.pool, parser.Parser.parse_html_for_tag_songs, page,
            )

            songs_path = [url.replace("https://genius.com/", "") for url in songs_url]

            coroutines_get_song_page = [
                self.requester.make_request(path, web=True) for path in songs_path
            ]

            for coroutine_song_page in asyncio.as_completed(coroutines_get_song_page):
                html_song_page = await coroutine_song_page

                song_id = await self.asyncio_loop.run_in_executor(
                    self.pool, utils.get_song_id_from_song_page, html_song_page,
                )
                song = await self.fetch_song_from_song_id(song_id)

                if get_lyrics:
                    # We send the blocking task (lyrics scraper) to the process pool so that it doesn't block
                    # the event loop
                    lyrics = await self.asyncio_loop.run_in_executor(
                        self.pool,
                        parser.Parser.parse_html_for_lyrics,
                        html_song_page,
                        remove_section_headers,
                    )
                    song.lyrics = lyrics

                songs.append(song)

        return songs
