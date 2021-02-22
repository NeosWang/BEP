class Config(object):
    DEBUG = False
    TESTING = False    
    
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@local/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME="127.0.0.1:5001"
    
class TestingConfig(Config):
    TESTING = True
    