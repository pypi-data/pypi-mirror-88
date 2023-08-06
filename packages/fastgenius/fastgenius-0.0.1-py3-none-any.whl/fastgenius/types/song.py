import pandas as pd
import datetime


class Song:
    """A song from the Genius.com database.

    Attributes:
        annotation_count (:obj:`int`)
        api_path (:obj:`str`)
        full_title (:obj:`str`)
        header_image_thumbnail_url (:obj:`str`)
        header_image_url (:obj:`str`)
        id (:obj:`int`)
        lyrics (:obj:`str`)
        lyrics_owner_id (:obj:`int`)
        lyrics_state (:obj:`str`)
        path (:obj:`str`)
        primary_artist_name (:class:`Artist`)
        pyongs_count (:obj:`int`)
        song_art_image_thumbnail_url (:obj:`str`)
        song_art_image_url (:obj:`str`)
        stats (:class:`Stats`)
        title (:obj:`str`)
        title_with_featured (:obj:`str`)
        url (:obj:`str`)

    """

    def __init__(self, api_response={}, lyrics=""):
        self.annotation_count = api_response.get("annotation_count")
        self.api_path = api_response.get("api_path")
        self.apple_music_id = api_response.get("apple_music_id")
        self.apple_music_player_url = api_response.get("apple_music_player_url")
        self.embed_content = api_response.get("embed_content")
        self.featured_video = api_response.get("featured_video")
        self.full_title = api_response.get("full_title")
        self.header_image_thumbnail_url = api_response.get("header_image_thumbnail_url")
        self.header_image_url = api_response.get("header_image_url")
        self.id = api_response.get("id")
        self.lyrics_owner_id = api_response.get("lyrics_owner_id")
        self.lyrics_placeholder_reason = api_response.get("lyrics_placeholder_reason")
        self.lyrics_state = api_response.get("lyrics_state")
        self.path = api_response.get("path")
        self.pyongs_count = api_response.get("pyongs_count")
        self.recording_location = api_response.get("recording_location")
        self.release_date = api_response.get("release_date")
        self.release_date_for_display = api_response.get("release_date_for_display")
        self.song_art_image_thumbnail_url = api_response.get(
            "song_art_image_thumbnail_url"
        )
        self.song_art_image_url = api_response.get("song_art_image_url")
        self.title = api_response.get("title")
        self.title_with_featured = api_response.get("title_with_featured")
        self.url = api_response.get("url")

        self.description = api_response.get("description", {}).get("plain")

        stats = api_response.get("stats", {})
        self.stats_accepted_annotations = stats.get("accepted_annotations")
        self.stats_contributors = stats.get("contributors")
        self.stats_iq_earners = stats.get("iq_earners")
        self.stats_transcribers = stats.get("transcribers")
        self.stats_unreviewed_annotations = stats.get("unreviewed_annotations")
        self.stats_verified_annotations = stats.get("verified_annotations")
        self.stats_concurrents = stats.get("concurrents")
        self.stats_hot = stats.get("hot")
        self.stats_pageviews = stats.get("pageviews")

        custom_performances = api_response.get("custom_performances")
        self.custom_performances = (
            {
                perf["label"]: artist.get("id")
                for perf in custom_performances
                for artist in perf["artists"]
            }
            if custom_performances
            else None
        )

        self.featured_artists = [
            artist.get("id") for artist in api_response.get("featured_artists", [])
        ]
        self.media = api_response.get("media")
        self.primary_artist_id = api_response.get("primary_artist", {}).get("id")
        self.primary_artist_name = api_response.get("primary_artist", {}).get("name")
        self.producer_artists = [
            artist.get("id") for artist in api_response.get("producer_artists", [])
        ]

        self.lyrics = lyrics
        self.annotations = []

        self.creation_timestamp = round(datetime.datetime.now().timestamp())

    def __repr__(self):
        return f"Song({self.primary_artist_name} - {self.title})"

    # +album: {...},
    # +song_relationships: [...],
    # +writer_artists: [...]

    def to_pandas(self, condensed=False):
        important_columns = [
            "full_title",
            "header_image_thumbnail_url",
            "header_image_url",
            "id",
            "lyrics_state",
            "path",
            "release_date",
            "release_date_for_display",
            "song_art_image_thumbnail_url",
            "song_art_image_url",
            "title",
            "title_with_featured",
            "url",
            "desciption",
            "featured_artists",
            "media",
            "primary_artist",
            "producer_artists",
            "lyrics",
        ]

        attributes_to_export = {
            k: v
            for k, v in self.__dict__.items()
            if k in important_columns or not condensed
        }

        return pd.DataFrame([attributes_to_export], columns=attributes_to_export.keys())
