# Public endpoint of szurubooru
SZURU_ENDPOINT = 'https://booru.tld'

# Credentials - must have the permission to add tags
SZURU_USERNAME = 'user'
SZURU_PASSWORD = 'password'

# IQDB sometimes can't find an exact enough match
# This option allows it to fall back on the "Possible" match
ALLOW_POSSIBLE_MATCH = True

# How long to wait between IQDB queries, this is to avoid possible IP rate limits/blocks*
# *never happened to me, but better be safe than sorry.
SLEEP_TIME = 10
