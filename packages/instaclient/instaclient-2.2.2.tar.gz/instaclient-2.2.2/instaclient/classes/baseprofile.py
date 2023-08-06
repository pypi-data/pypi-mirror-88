import requests, logging
from instaclient.errors.common import InvalidInstaRequestError, InvalidInstaSchemaError
from instaclient.client.urls import GraphUrls
from instaclient.classes.instaobject import InstaBaseObject
from instaclient.utilities import get_url

logger = logging.getLogger(__name__)

class BaseProfile(InstaBaseObject):
    def __init__(self, id:str, viewer:str, username:str, name:str):
        try:id = id.replace('profilePage_', '')
        except: pass
        
        super().__init__(id=id, viewer=viewer, type=self.GRAPH_PROFILE)
        self.username = username
        try: self.name = name.split('\\')[0]
        except: self.name = name

    def __repr__(self) -> str:
        return f'BaseProfile<{self.username}>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, BaseProfile):
            return False
        try:
            self_id = self.get_id()
            o_id = o.get_id()
            return self_id == o_id
        except:
            return self.username == o.username

    def from_username(username:str, proxy:str=None, scraperapi_key:str=None):
        url = GraphUrls.GRAPH_USER.format(username)
        request = get_url(url, scraperapi_key)
        if proxy:
            proxyDict = { 
              "http"  : proxy, 
              "https" : proxy, 
              "ftp"   : proxy
            }
            result = requests.get(request, proxies=proxyDict)
        else:
            result = requests.get(request)
            
        try:
            data = result.json()
            try:
                user = data['graphql']['user']
                profile = BaseProfile(
                    id=user['id'],
                    viewer=None,
                    username=user['username'],
                    name=user['full_name']
                )
                return profile
            except:
                raise InvalidInstaSchemaError(__name__)
        except:
            logger.error(f'Invalid request. Data: {result.raw}')
            raise InvalidInstaRequestError(request)

    
    def username_profile(username:str):
        return BaseProfile(
            id=None,
            viewer=None,
            username=username,
            name=None
        )
        

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name