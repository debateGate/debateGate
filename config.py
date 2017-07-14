""" Contains all config data for the application. """


class Auth:
    """ Contains Google Project credentials. """
    CLIENT_ID = ('google id'
                 '.apps.googleusercontent.com')
    CLIENT_SECRET = 'secrets'
    REDIRECT_URI = 'https://www.debategate.net/gCallBack' # change this to localhost:5000 in dev
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


class Config:
    """
    Contains config that should be shared by both DevConfig and ProdConfig.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_NAME = "debateGate"
    SECRET_KEY = "change-this-before-production-lol"
    SQLALCHEMY_MIGRATE_REPO = './db_repo'

    # pagination
    POSTS_PER_PAGE = 3

    # time for mode switches
    TIME_DELTA = 1

    #email
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '465'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    ADDRESS = "addressfortotallynotspammingpeople@gmail.com"
    PASSWORD = "passwordiguess"


class DevConfig(Config):
    """ Config class for dev servers only. """
    DEBUG = True
    use_reloader = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///name'


class ProdConfig(Config):
    """ Config class for production servers only. """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///othername'


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
}
