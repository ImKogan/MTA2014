from configparser import RawConfigParser

def db_connection(settings):
    '''connection parameters to db
    '''
    config = RawConfigParser()
    config.read(settings)
    DATABASE = {'HOST': config.get('database', 'DATABASE_HOST'),
                'PORT': config.get('database', 'DATABASE_PORT'),
                'NAME': config.get('database', 'DATABASE_NAME'),
                'USER': config.get('database', 'DATABASE_USER'),
                'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
               }
    return DATABASE
