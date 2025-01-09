import os

DB_HOST=os.getenv('DB_HOST', 'localhost')
DB_PORT=os.getenv('DB_PORT', '3006')
DB_USER=os.getenv('DB_USER', 'root')
DB_PASS=os.getenv('DB_PASS', '12345678')
DB_NAME=os.getenv('DB_NAME', 'hirelala')

BAIDU_SITE=os.getenv('BAIDU_SITE', 'https://www.hirelala.com')
BAIDU_TOKEN=os.getenv('BAIDU_TOKEN')

PUSH_BATCH_SIZE=5