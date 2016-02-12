#!/usr/bin/python

from rauth import OAuth1Service
import os, errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

# if __name__ == "__main__":

def get_session():
    # Create a new consumer at https://bitbucket.org/account/user/{username}/api
    CONSUMER_KEY =raw_input('Enter CONSUMER_KEY here: ')
    CONSUMER_SECRET = raw_input('Enter CONSUMER_SECRET here: ')

    # API URLs from https://confluence.atlassian.com/display/BITBUCKET/oauth+Endpoint
    REQUEST_TOKEN_URL = 'https://api.bitbucket.org/1.0/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.bitbucket.org/1.0/oauth/access_token'
    AUTHORIZE_URL = 'https://api.bitbucket.org/1.0/oauth/authenticate'

    # Create the service
    bitbucket = OAuth1Service(name='bitbucket',
                              consumer_key=CONSUMER_KEY,
                              consumer_secret=CONSUMER_SECRET,
                              request_token_url=REQUEST_TOKEN_URL,
                              access_token_url=ACCESS_TOKEN_URL,
                              authorize_url=AUTHORIZE_URL)


    # Change CALL_BACK to something that listens for a callback
    # with oauth_verifier in the URL params and automatically stores
    # the verifier.
    CALL_BACK = 'http://localhost?dump'

    # Make the request for a token, include the callback URL.
    rtoken, rtoken_secret = bitbucket.get_request_token(params={'oauth_callback': CALL_BACK})

    # Use the token to rquest an authorization URL.
    authorize_url = bitbucket.get_authorize_url(rtoken)

    # Send the user to Bitbucket to authenticate. The CALL_BACK is the
    # URL. The URL is redirected to after success. Normally, your
    # application automates this whole exchange.
    print 'Visit %s in new browser window.' % (authorize_url)

    # You application should also automated this rather than request
    # it from the user.
    oauth_verifier = raw_input('Enter oauth_verifier here: ')

    # Returns a session to Bitbucket using the verifier from above.
    return bitbucket.get_auth_session(rtoken, rtoken_secret, data={'oauth_verifier': oauth_verifier})



if __name__ == '__main__':
    filename=raw_input('Enter file name here: ') # "README.org"
    silentremove(filename)
    session = get_session()

    username = raw_input('Enter username here: ') # 'yu-yuxuan'

    # repo_slug = raw_input('Enter a repository slug: ')
    # git clone git@bitbucket.org:yuyuxuan/bin.git
    git_prefix='git@bitbucket.org:%s/'  % username
    # url = 'https://api.bitbucket.org/1.0/repositories/%s/%s/branches' % (username, repo_slug)
    url = 'https://api.bitbucket.org/1.0/user/repositories'
    resp = session.get(url)
    respfile=resp.json()
    for repo in respfile:
        print repo['slug']
        infomation=str.join('', (git_prefix, repo['slug'],'.git'))
        with open(filename, "a") as myfile:
            myfile.write(infomation+ '\n')
