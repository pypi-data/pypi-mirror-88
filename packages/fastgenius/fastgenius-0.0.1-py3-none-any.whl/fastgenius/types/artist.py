import pandas as pd
import datetime


class Artist:
    def __init__(self,
                 api_response={},
                 serialized_json={}):
        if api_response:
            self.alternate_names = api_response.get('alternate_names')
            self.api_path = api_response.get('api_path')
            self.description = api_response.get('description', {}).get('plain')
            self.facebook_name = api_response.get('facebook_name')
            self.followers_count = api_response.get('followers_count')
            self.header_image_url = api_response.get('header_image_url')
            self.id = api_response.get('id')
            self.image_url = api_response.get('image_url')
            self.instagram_name = api_response.get('instagram_name')
            self.is_meme_verified = api_response.get('is_meme_verified')
            self.is_verified = api_response.get('is_verified')
            self.name = api_response.get('name')
            self.translation_artist = api_response.get('translation_artist')
            self.twitter_name = api_response.get('twitter_name')
            self.url = api_response.get('url')
        elif serialized_json:
            self.from_json(serialized_json)
        else:
            raise Exception('Artist should receive either an API response, either its JSONized version')

        self.creation_timestamp = round(datetime.datetime.now().timestamp())
        self.songs = []

    def __repr__(self):
        # return json.dumps(self.__dict__, indent = 4)
        return f"Artist({self.name})"

    def to_json(self):
        return {
            'alternate_names': self.alternate_names,
            'api_path': self.api_path,
            'description': self.description,
            'facebook_name': self.facebook_name,
            'followers_count': self.followers_count,
            'header_image_url': self.header_image_url,
            'id': self.id,
            'image_url': self.image_url,
            'instagram_name': self.instagram_name,
            'is_meme_verified': self.is_meme_verified,
            'is_verified': self.is_verified,
            'name': self.name,
            'translation_artist': self.translation_artist,
            'twitter_name': self.twitter_name,
            'url': self.url,
            'creation_timestamp': self.creation_timestamp
        }

    def from_json(self, json):
        self.alternate_names = json.get('alternate_names')
        self.api_path = json.get('api_path')
        self.description = json.get('description')
        self.facebook_name = json.get('facebook_name')
        self.followers_count = json.get('followers_count')
        self.header_image_url = json.get('header_image_url')
        self.id = json.get('id')
        self.image_url = json.get('image_url')
        self.instagram_name = json.get('instagram_name')
        self.is_meme_verified = json.get('is_meme_verified')
        self.is_verified = json.get('is_verified')
        self.name = json.get('name')
        self.translation_artist = json.get('translation_artist')
        self.twitter_name = json.get('twitter_name')
        self.url = json.get('url')
        self.creation_timestamp = json.get('creation_timestamp')

    def to_pandas(self, condensed=False):
        important_columns = []

        attributes_to_export = {k: v for k, v in self.__dict__.items() if k in important_columns or not condensed}

        return pd.DataFrame([attributes_to_export], columns=attributes_to_export.keys())
