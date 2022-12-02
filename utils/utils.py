import random
from selenium.webdriver.common.by import By

TEN_USERS = 10
FORTY_USERS = 40

THREE_SECONDS = 3
FIVE_SECONDS = 5
TEN_SECONDS = 10
TWENTY_SECONDS = 20

LOGIN_PAGE = "https://www.okcupid.com/login/"
WHO_YOU_LIKED_PAGE = 'https://www.okcupid.com/who-you-like?cf=likesIncoming'


def generate_id():
    #  Adding a generated number in case we get 2 users with the same name
    return str(random.randint(1, 100))
