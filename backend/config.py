'''
This module defines the configuration class for the application. 

The configuration parameters are loaded from the environment variables. 
If the environment variables are not defined, default values are used.

Environment Variables:
- SECRET_KEY: The secret key for the application, used in session management and CSRF protection.
- DATABASE_URL: The URL of the SQL database to use for the application.
- JWT_SECRET_KEY: The secret key used for encoding and decoding JWT tokens.
- SQLALCHEMY_TRACK_MODIFICATIONS: Flag to enable or disable SQLAlchemy event system. 

Note: It is recommended to set the environment variables for security reasons. 
Default values should only be used for testing and development purposes.
'''

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    '''
    The Config class encapsulates the configuration parameters of the application.

    Attributes:
    - SECRET_KEY: The secret key for session management and CSRF protection.
    - SQLALCHEMY_DATABASE_URI: The URL of the SQL database to use for the application.
    - JWT_SECRET_KEY: The secret key used for encoding and decoding JWT tokens.
    - SQLALCHEMY_TRACK_MODIFICATIONS: Flag to enable or disable SQLAlchemy event system. 
    '''
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')
    JWT_ALGORITHM=os.getenv('JWT_ALGORITHM')
    CORS_HEADERS=os.getenv('CORS_HEADERS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    raw_origins = os.getenv('ALLOWED_ORIGINS', '')
    ALLOWED_ORIGINS = raw_origins.split(',') if raw_origins else []

class DevelopmentConfig(Config):
    '''
    The TestConfig class encapsulates the test configuration parameters of the application.

    Attributes:
    - SQLALCHEMY_DATABASE_URI: The URL of the SQL database to use for the application. 
    '''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite3')

class ProductionConfig(Config):
    '''
    The DevelopmentConfig class encapsulates the development configuration parameters of the application.

    Attributes:

    '''
    DEVELOPMENT = True