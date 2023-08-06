import unicodedata
import re
from string import punctuation
from bs4 import BeautifulSoup
from functools import wraps
import logging
import spacy
import time

regexes_song_id_in_page = [
    re.compile('\\\\"songId\\\\":([0-9]+)'),
    re.compile('\{"name":"song_id","values":\["([0-9]+)"\]'),
    re.compile('"genius://songs/([0-9]+)"'),
]


def all_methods(decorator):
    @wraps(decorator)
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def get_song_id_from_song_page(html_raw):
    for regex in regexes_song_id_in_page:
        try:
            return re.search(regex, html_raw).group(1)
        except AttributeError:
            pass
    return None



def method_logger(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        # Iterate over all args, convert them to str, and join them
        args_str = ",".join([str(arg)[:100] for arg in args])
        kwargs_str = ",".join(
            f"{str(k)[:100]}={str(v)[:100]}" for k, v in kwargs.items()
        )
        logging.debug(
            f"processing {method.__name__}({','.join([args_str, kwargs_str])})"
        )
        start_time = time.time()
        method_results = method(*args, **kwargs)
        end_time = time.time()
        logging.info(
            f"processing {method.__name__}({','.join([args_str, kwargs_str])}) took {end_time - start_time}"
        )
        return method_results

    return wrapper


def clean_str(s):
    """Cleans a string to help with string comparison.
    Removes punctuation and returns
    a stripped, NFKD normalized string in lowercase.
    Args:
        s (:obj:`str`): A string.
    Returns:
        :obj:`str`: Cleaned string.
    """
    assert type(s) is str, "clean_str should receive a string"
    punctuation_ = punctuation + "’"
    string = s.translate(str.maketrans("", "", punctuation_)).strip().lower()
    return unicodedata.normalize("NFKD", string)


def get_object_len(object_):
    if type(object_) is list:
        return len(object_)
    else:
        return 1


def remove_nones(function_input, ignore_nones=True):
    if type(function_input) is list:
        none_count = sum(item is None for item in function_input)
        if none_count > 0:
            if ignore_nones:
                print(f"Ignoring {none_count} None's from the list")
                return [item for item in function_input if item is not None]
            else:
                raise Exception(f"There are {none_count} in the list passed")
    else:
        assert function_input is not None, "You passed None to the function"

    return function_input


def verify_and_get_type(list_to_check, list_of_allowed_types):
    error_message = f'You should pass any of {", ".join(map(str, list_of_allowed_types))} lists, but you passed a list that either contains mixed types or a type that is not supported'
    assert any(
        [all(isinstance(x, t) for x in list_to_check) for t in list_of_allowed_types]
    ), error_message
    return type(list_to_check[0])


def listify(list_or_not):
    return list_or_not if type(list_or_not) is list else [list_or_not]


def return_list_or_element(list_or_not):
    return list_or_not[0] if len(list_or_not) == 1 else list_or_not


class LanguageDetectorWrapper:
    def __init__(self):
        self.nlp = spacy.load("en")
        self.nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

    def detect_lang(self, text: str):
        results = self.nlp(text)._.language
        return results["language"], results["score"]

    def is_fr(self, text: str, strict=False) -> bool:
        lang, score = self.detect_lang(text)
        assert score is not None, "score is none"
        return lang == "fr" or (score < 0.2 and not strict)


def _result_is_lyrics(self, song):
    """Returns False if result from Genius is not actually song lyrics.
    Sets the :attr:`lyricsgenius.Genius.excluded_terms` and
    :attr:`lyricsgenius.Genius.replace_default_terms` as instance variables
    within the Genius class.
    Args:
        song_title (:obj:`str`, optional): Title of the song.
    Returns:
        :obj:`bool`: `True` if none of the terms are found in the song title.
    Note:
        Default excluded terms are the following: 'track\\s?list',
        'album art(work)?', 'liner notes', 'booklet', 'credits',
        'interview', 'skit', 'instrumental', and 'setlist'.
    """
    if song["lyrics_state"] != "complete":
        return False

    expression = r"".join(["({})|".format(term) for term in self.excluded_terms])
    expression = expression.strip("|")
    regex = re.compile(expression, re.IGNORECASE)
    return not regex.search(clean_str(song["title"]))


def extract_lyrics_from_html(html_raw, remove_section_headers=True):
    html = BeautifulSoup(html_raw.replace("<br/>", "\n"), "html.parser")
    # Determine the class of the div
    div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
    if div is None:
        return None

    lyrics = div.get_text()

    # Remove [Verse], [Bridge], etc.
    if remove_section_headers:
        lyrics = re.sub(r"(\[.*?\])*", "", lyrics)
        lyrics = re.sub("\n{2}", "\n", lyrics)  # Gaps between verses

    return lyrics


def clean_content(content):
    """
    Clean input content from the API lowering case and removing non needed characters.
    :param content: Input content to clean.
    :return: String representation of the cleaned content.
    """
    content = content.lower()
    # Removes spaces on both sides
    content = content.strip()
    # Removes funny character including accents (french people love that)
    content = unidecode.unidecode(content)
    # Remove headers and such eg [Verse] or (Ademo)
    content = re.sub(r"\n*[(\[{].*?[)\]}]\n*", ".\n", content)
    # Removing all weird characters
    content = re.sub(r'[/\\\(\)\[\]\{\}\'"]', "", content)
    # Remove any punctuation at the start of the line
    content = re.sub(r"^[!?,;:\.]+", "", content, flags=re.MULTILINE)
    # Finish the document with a dot
    content = content + "."
    # Remove spaces around punctuations as well as taking the last punctuation when
    # there are multiple ones following each other
    content = re.sub(r"(\s*([!?;:\.,])(\s)*)+", r"\2\3", content)

    # Replacing jumps of 2 lines or more by 1 line jump
    content = re.sub(r"([\n\r]+|\s{2,}|(\s+\n))", r"\n", content)

    # Interpret going to the next line as being a comma (not always right)
    content = re.sub(r"([^\n,.;?!])$", r"\1,", content, flags=re.MULTILINE)
