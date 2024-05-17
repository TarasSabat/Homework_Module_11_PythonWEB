class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = "sqlite:///example.db"
    SECRET_KEY = "your_secret_key"

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "sqlite:///dev.db"

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "sqlite:///test.db"

class ProductionConfig(Config):
    DATABASE_URI = "postgresql://user:password@localhost/prod_db"
    SECRET_KEY = "your_production_secret_key"


