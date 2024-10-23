from os import getenv


HOST = getenv('HTTP_HOST', 'http://localhost:2222')
DB_URL = getenv('DB_URL', 'sqlite+aiosqlite:///./test.db')