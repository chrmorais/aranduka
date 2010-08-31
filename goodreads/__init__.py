import urlparse
import urllib
import time
import oauth2 as oauth

# class to connect to goodreads.com
class GoodReadsClient():
    url = 'http://www.goodreads.com'
    request_token_url = '%s/oauth/request_token/' % url
    authorize_url = '%s/oauth/authorize/' % url
    access_token_url = '%s/oauth/access_token/' % url
    
    def __init__(self, key, secret, token=None, token_secret=None):
        self.key = key
        self.secret = secret

        self.consumer = oauth.Consumer(self.key, self.secret)
        self.client = oauth.Client(self.consumer)

        # get access token
        if token and token_secret:
            self.token = oauth.Token(token, token_secret)
        else:
            # get authorize link
            print self.authorize_link()
            time.sleep(10)
            self.token = self.access_token()
        # get client with user's access allowed
        self.client = oauth.Client(self.consumer, self.token)

    def authorize_token(self):
        response, content = self.client.request(self.request_token_url, 'GET')
        if response['status'] != '200':
            raise Exception('Invalid response: %s' % response['status'])

        self.request_token = dict(urlparse.parse_qsl(content))
        print self.request_token['oauth_token']
        print self.request_token['oauth_token_secret']
        return self.request_token['oauth_token']

    def authorize_link(self):
        return '%s?oauth_token=%s' % (self.authorize_url, self.authorize_token())

    def access_token(self, token=None, token_secret=None):
        if not token and not token_secret:
            token = self.request_token['oauth_token']
            token_secret = self.request_token['oauth_token_secret']
        token = oauth.Token(token, token_secret)

        client = oauth.Client(self.consumer, token)
        response, content = client.request(self.access_token_url, 'POST')
        if response['status'] != '200':
            raise Exception('Invalid response: %s' % response['status'])
        
        access_token = dict(urlparse.parse_qsl(content))
        
        # this is the token you should save for future uses
        token = oauth.Token(access_token['oauth_token'],
                            access_token['oauth_token_secret'])
        return token

    def authors_books(self, id, page=1):
        """Get an xml file with a paginated list of an authors books.
        
        url: http://www.goodreads.com/author/list.xml   (sample url)
        http method: GET
        params:
        * page: 1-N (default 1)
        * id: Goodreads Author id (required)"""

        body = urllib.urlencode({'key': self.key,
                                 'id': id,
                                 'page': page})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response, content = self.client.request('%s/author/list.xml' % self.url,
                                                'GET', body, headers)
        if response['status'] != '200':
            raise Exception('Cannot create resource: %s' % response['status'])
        else:
            return response, content
