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

if __name__ == '__main__':
    import sys
    import os
    settings = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.ini')
    conn = db_connection(settings)
    print(conn['NAME'])
    sys.exit(0)
