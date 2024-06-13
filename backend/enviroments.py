from dotenv import dotenv_values

# Bot token can be obtained via https://t.me/BotFather
CONFIG = dict(dotenv_values(".env"))
DB_NAME = CONFIG['DB_NAME']
DB_USER = CONFIG['DB_USER']
DB_HOST = CONFIG['DB_HOST']
DB_PORT = CONFIG['DB_PORT']
DB_PASSWORD = CONFIG['DB_PASSWORD']
