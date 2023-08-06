from .__version__ import __version__
import os

API_URL = "https://3.basecampapi.com/"

OAUTH_URL = "https://launchpad.37signals.com"

OAUTH_LOCAL_BIND_PORT = 33333
"""A web server will bind to this port on localhost when authorizing your oauth tokens in `bc3 configure`"""

DEFAULT_REDIRECT_URI = "http://localhost:%d" % OAUTH_LOCAL_BIND_PORT
"""The default Redirect URI recommended for your Basecamp 3 OAuth2 integration."""

AUTHORIZE_URL = "%s/authorization/new?" \
                "client_id={client_id}&redirect_uri={redirect_uri}&type=web_server" % OAUTH_URL
"""Confirms you want to allow an app (identified by client_id) to have access to your Basecamp 3 account"""

AUTHORIZATION_JSON_URL = "%s/authorization.json" % OAUTH_URL

ACCESS_TOKEN_URL = "%s/authorization/token?type=web_server&client_id={client_id}&" \
                       "redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}" % OAUTH_URL
"""Using the code received during initial authentication, obtain access and refresh tokens."""

REFRESH_TOKEN_URL = "%s/authorization/token?type=refresh&refresh_token={0.refresh_token}&" \
                    "client_id={0.client_id}&redirect_uri={0.redirect_uri}&client_secret={0.client_secret}" % OAUTH_URL
"""Using a saved refresh token, apply for new access token."""

DEFAULT_CONFIG_FILE = os.path.expanduser(os.path.join("~", ".config", "basecamp.conf"))

DOCK_NAME_CAMPFIRE = 'chat'
DOCK_NAME_MESSAGE_BOARD = 'message_board'
DOCK_NAME_TODOS = 'todoset'
DOCK_NAME_SCHEDULE = 'schedule'
DOCK_NAME_CHECKIN = 'questionnaire'
DOCK_NAME_VAULT = 'vault'
DOCK_NAME_FORWARDS = 'inbox'

RATE_LIMIT_REQUESTS = 50
RATE_LIMIT_PER_SECONDS = 10

VERSION = __version__

USER_AGENT = "BasecamPY3 {version} (https://github.com/phistrom/basecampy3)".format(version=VERSION)
