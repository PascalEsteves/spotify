import requests
import json
import sqlite3
import base64
from urllib.parse import urlencode

class Database():

    def __init__(self,table=None) -> None:

        self.database = self._db.cursor()
        self.table = table
        self._create_table()

    def _db(self):

        return sqlite3.connect('spotify.db')

    def _create_table(self):

        if self.table:
            pass
        else:
            pass
        
    def _insert_audio(self,table:str,song:dict)->None:

        columns = tuple(list(song.keys()))
        values  = tuple(list(song.values()))

        query = f'insert into {table} {columns} VALUES {values}'

        self.database.execute(query)

    def insert_audio(self,table:str,song:dict)->None:
        """
        Insert song into table 

        Argument: 
        :arg table: Table to insert data
        :arg song: Dict with songs details

        Return:
        Insert validation
        """

        return self._insert_audio(table,song)


    def insert_list_audios(self,table:str,songs:list)->None:

        """

        Insert list of songs into table

        Argument: 
        :arg table : Table to inser data
        :arg songs: list of songs to insert into database

        Return:

        Insert validation
        
        """

        for song in songs:
            self._insert_audio(table,song)

    
    def _delete_song(self,table,song_name):


        cur.execute('''CREATE TABLE IF NOT EXISTS Media(
                id INTEGER PRIMARY KEY, title TEXT, 
                type TEXT,  genre TEXT,
                onchapter INTEGER,  chapters INTEGER,
                status TEXT
                )''')


class API_Request():

    """
    Spotify Connection and Requests 
    """

    def __init__(self,
                config_file:dict) -> None:

        self.client_id = config_file['Client_ID']
        self.client_secret = config_file['Client_Secret']
        self.url = config_file['URL']
        self.token = self._request_token()


    def _request_token(self):

        """
        Get token to authentication
        """

        client_cred = f"{self.client_id}:{self.client_secret}"
        client_cred_64 = base64.b64encode(client_cred.encode())

        header = {
                    "Authorization":f"Basic {client_cred_64.decode()}"
                
                }
        form =  {
                    "grant_type": "client_credentials"
                
                }
        
        token = requests.post(url=self.url,data= form,headers=header)

        if token.ok:

            return token.json()['access_token']

        else:

            raise Exception('Permission Denied - Check URL and credencials')

    def request_data(self,
                    url_=None,
                    look_type:str='',
                    paramms:dict=''):

        """
        Request data to sportify endpoint

        Arguments:

        :arg look_type : endpoint request ex. tracks,search,etc https://developer.spotify.com/documentation/web-api/reference/#/
        :arg params: params to include in request endpoint

        Return:

        Json object with response data

        """

        if url_:

            endpoint = f'{url_}?{urlencode(paramms)}'

        else:

            endpoint = f'https://api.spotify.com/v1/{look_type}{urlencode(paramms)}'

        header = {
                    "Authorization":f"Bearer {self.token}"
                }

        headers = {
            'Accept':'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
}

        r = requests.get(url=endpoint,headers = headers)

        return r.json()

    