import re
from bs4 import BeautifulSoup, SoupStrainer
from .utils import all_methods, method_logger, clean_str
from typing import Union, List


@all_methods(method_logger)
class Parser:
    non_lyrics_flagging_regexs: List[str] = [
        "track\\s?list",
        "album art(work)?",
        "liner notes",
        "booklet",
        "credits",
        "interview",
        "skit",
        "instrumental",
        "setlist",
        "livret",
        "translation",
        "traduzione",
        "deutsch",
    ]

    expression = "|".join([f"({term})" for term in non_lyrics_flagging_regexs])
    regex_for_is_lyrics = re.compile(expression, re.IGNORECASE)

    regex_lyrics_div = re.compile("^lyrics$|Lyrics__Root")
    regex_header_section = re.compile("(\[.*?\])*")
    regex_gap_between = re.compile("\n{2,}")

    @classmethod
    def is_song(cls, song_title: str):
        return not cls.regex_for_is_lyrics.search(clean_str(song_title))

    @classmethod
    def parse_html_for_lyrics(cls, html_raw, remove_section_headers=True):

        html = BeautifulSoup(
            html_raw.replace("<br/>", "\n"), "lxml"  # SoupStrainer("a")
        )

        # Determine the class of the div
        div = html.find("div", class_=cls.regex_lyrics_div)
        if div is None:
            return None

        lyrics = div.get_text()

        # Remove [Verse], [Bridge], etc.
        if remove_section_headers:
            lyrics = re.sub(cls.regex_header_section, "", lyrics)
            lyrics = re.sub(cls.regex_gap_between, "\n", lyrics)  # Gaps between verses

        return lyrics

    @classmethod
    def parse_html_for_tag_songs(cls, html_raw):

        soup = BeautifulSoup(html_raw, "lxml")

        ul = soup.find("ul", class_="song_list")
        urls = []
        for li in ul.find_all("li"):
            url = li.a.attrs["href"]

            urls.append(url)

        return urls
