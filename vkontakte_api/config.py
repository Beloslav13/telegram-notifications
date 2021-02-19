import os


DEBUG = True

BASE_URL = 'https://api.vk.com/method/{}?{}&v=5.52&access_token={}'
TIME_OUT = 3

if DEBUG:
    from probe import TOKEN_DEBUG, ID_DEBUG
    TOKEN_VK = TOKEN_DEBUG
    ID = ID_DEBUG
else:
    TOKEN_VK = os.environ.get("TOKEN_VK", None)
    ID = os.environ.get("ID", None)
