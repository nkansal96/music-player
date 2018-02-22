import sys
import pprint
import json

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

import settings

# if len(sys.argv) > 1:
#   username = sys.argv[1]
# else:
#   print("Usage: %s username" % (sys.argv[0],))
#   sys.exit()

# Old Credentials
# scope = ''
# token = util.prompt_for_user_token(
# 	settings.NATHAN_USERNAME,
# 	scope,
# 	client_id=settings.SPOTIPY_CLIENT_ID,
# 	client_secret=settings.SPOTIPY_CLIENT_SECRET,
# 	redirect_uri=settings.SPOTIPY_REDIRECT_URI
# )

credentials = oauth2.SpotifyClientCredentials(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET)

token = credentials.get_access_token()

if token:
	sp = spotipy.Spotify(auth=token)
	result = sp.search('Coldplay', limit=2, type='track', market='US')
	pprint.pprint(result)
else:
	print("Could not get token")
