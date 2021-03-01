#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# get_ipython().system('pip uninstall pysftp && pip install pysftp==0.2.8')
# get_ipython().system('pip install requests')
from config import *
import base64
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
import pandas as pd
import pysftp

now = datetime.now()


class SpotifyAPI(object):
    access_token = None
    access_token_expires = now
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret is None or client_id is None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    @staticmethod
    def get_token_data():
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def search(self, query, search_type='artist'):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)  # .json()
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_resource(self, lookup_id, resource_type='artists', version='v1', target='related-artists'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}/{target}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_related_artist(self, _id):
        return self.get_resource(_id, resource_type='artists', target='related-artists')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists', target='albums')


# spotify = SpotifyAPI(client_id, client_secret)

spotify = SpotifyAPI(client_id, client_secret)


def getRelatedArtist(artist_name, id):
    # id='4Awgi8rHD631aMJCXLf21D'   ###uncomment for testing
    related_artists = []
    related_artist_cnt = len(spotify.get_related_artist(id)['artists'])
    # print("related_artist_cnt",related_artist_cnt)
    rank = 0
    JSON_Data = spotify.get_related_artist(id)['artists']  # ('4Awgi8rHD631aMJCXLf21D')

    if related_artist_cnt > 0:
        for x in range(0, related_artist_cnt):
            rank = rank + 1
            genres_cnt = 0
            image_cnt = 0
            genres_cnt = len(JSON_Data[x]['genres'])
            image_cnt = len(JSON_Data[x]['images'])

            # derive metadata
            RelatedArtist_Name = JSON_Data[x]['name']
            external_urls__spotify = JSON_Data[x]['external_urls']['spotify']
            ##followers__href           = JSON_Data[x]['followers']['href']
            followers__total = JSON_Data[x]['followers']['total']
            if genres_cnt > 0:
                genres__001 = JSON_Data[x]['genres'][0]
            else:
                genres__001 = ''

            if genres_cnt > 1:
                genres__002 = JSON_Data[x]['genres'][1]
            else:
                genres__002 = ''

            if genres_cnt > 2:
                genres__003 = JSON_Data[x]['genres'][2]
            else:
                genres__003 = ''

            if genres_cnt > 3:
                genres__004 = JSON_Data[x]['genres'][3]
            else:
                genres__004 = ''

            if genres_cnt > 4:
                genres__005 = JSON_Data[x]['genres'][4]
            else:
                genres__005 = ''

            ##href                      = JSON_Data[x]['href']
            id = JSON_Data[x]['id']

            ## if image_cnt>0:
            ##     images__height_1          = JSON_Data[x]['images'][0]['height']
            ## else:
            ##     images__height_1          =''

            if image_cnt > 0:
                Large_image = JSON_Data[x]['images'][0]['url']
            else:
                Large_image = ''

            ##if image_cnt>0:
            ##  images__width_1           = JSON_Data[x]['images'][0]['width']
            ##else:
            ##  images__width_1           =''

            ## if image_cnt>1:
            ##   images__height_2          = JSON_Data[x]['images'][1]['height']
            ##else:
            ##  images__height_2          =''

            if image_cnt > 1:
                Medium_image = JSON_Data[x]['images'][1]['url']
            else:
                Medium_image = ''

            ## if image_cnt>1:
            ##   images__width_2           = JSON_Data[x]['images'][1]['width']
            ##else:
            ##  images__width_2           =''

            ##if image_cnt>2:
            ##  images__height_3          = JSON_Data[x]['images'][2]['height']
            ##else:
            ##  images__height_3          =''

            if image_cnt > 2:
                Small_image = JSON_Data[x]['images'][2]['url']
            else:
                Small_image = ''

            ##if image_cnt>2:
            ##  images__width_3           = JSON_Data[x]['images'][2]['width']
            ##else:
            ##  images__width_3           =''

            popularity = JSON_Data[x]['popularity']
            type = JSON_Data[x]['type']
            ##uri                       = JSON_Data[x]['uri']

            ## artist = [artist_name,RelatedArtist_Name,rank,external_urls__spotify,followers__href,followers__total
            ##         ,genres__001,genres__002,genres__003,genres__004,genres__005
            ##         ,href,id
            ##         ,images__height_1,images__url_1,images__width_1
            ##         ,images__height_2,images__url_2,images__width_2
            ##         ,images__height_3,images__url_3,images__width_3
            ##         ,popularity,type,uri]

            artist = [artist_name, RelatedArtist_Name, rank, external_urls__spotify, followers__total
                , genres__001, genres__002, genres__003, genres__004, genres__005
                , id
                , Large_image
                , Medium_image
                , Small_image
                , popularity, type]

            related_artists.append(artist)

    return related_artists

try:
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection succesfully stablished ... \n")

        # print("Before", cnopts.hostkeys)
        # Obtain structure of the remote directory '/var/www/vhosts'
        # Print data
        artist_names = {}
        try:
            temp = open(FileName)
        except FileNotFoundError:
            sftp.get('/Export/' + FileName)

        artists = pd.read_csv(FileName, encoding='UTF-16', sep="|", error_bad_lines=False, nrows=10)

        artist_names = artists[['Artist_Name']].drop_duplicates()
        artist_names['FULL_NAME'] = artist_names['Artist_Name']
        print(artist_names)

        artist_list = []

        for artist in artist_names['FULL_NAME']:
            # print(artist)
            result = spotify.search(artist, search_type='artist')['artists']['items']
            # print(result)
            try:
                if not result:
                    continue
                else:
                    id_val = result[0]['id']
                    artist_name = artist

                    Artist = [artist_name, id_val]
                    # print(id_val)
                    artist_list.append(Artist)
            except:
                print('no data')

        print(artist_list)

        Full_Related_Artists = []
        print('Starting data load')

        for i in range(len(artist_list)):
            # time.sleep(.5)
            getRelatedArtist(artist_list[i][0], artist_list[i][1])
            Artists = getRelatedArtist(artist_list[i][0], artist_list[i][1])  # getRelatedArtist(related_artist[i])
            for Artist in Artists:
                Full_Related_Artists.append(Artist)

        # create dataset
        df = pd.DataFrame(Full_Related_Artists,
                          columns=['artist_name', 'RelatedArtist_Name', 'rank', 'external_urls__spotify', 'followers__total'
                              , 'genres__001', 'genres__002', 'genres__003', 'genres__004', 'genres__005'
                              , 'id', 'Large_image', 'Medium_image', 'Small_image', 'popularity', 'type', ])

        FinalOutputFileName = OutputFileName + now.strftime('%Y-%m-%d') + '.csv'
        df.to_csv(FinalOutputFileName, sep=',')

        print('Operation completed')

        remotepath = r'/Import/Spotify/'+FinalOutputFileName
        localpath = FinalOutputFileName

        o_var = sftp.put(localpath, remotepath, confirm=False)
        print('o_var:', o_var)
        sftp.close()
        print("File uploaded... \n")
    # In[ ]:
except Exception as e1:
    print('[Error-1]:', e1)

exit(200)
