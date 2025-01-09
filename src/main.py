from typing import List

import mysql.connector
from datetime import datetime, timedelta
import requests

from src.config import PUSH_BATCH_SIZE, DB_HOST, DB_USER, DB_PASS, DB_NAME, BAIDU_SITE, BAIDU_TOKEN

# Database configuration
db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASS,
    'database': DB_NAME,
}

# Baidu API configuration
API_URL = f"http://data.zz.baidu.com/urls?site={BAIDU_SITE}&token={BAIDU_TOKEN}"
HEADERS = {'Content-Type': 'text/plain'}

def fetch_yesterdays_job_urls() -> List[str]:
    """Fetch jobs published yesterday from the database."""
    yesterday = datetime.now() - timedelta(days=1)
    start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = """
        SELECT slug FROM jobs
        WHERE published_at BETWEEN %s AND %s
    """
    cursor.execute(query, (start_of_yesterday, end_of_yesterday))
    jobs = cursor.fetchall()

    cursor.close()
    connection.close()

    return [f"https://hirelala.com/job/{job[0]}" for job in jobs]

def push_urls_to_baidu(urls):
    """Push URLs to Baidu API."""
    with open('urls.txt', 'w') as file:
        file.write('\n'.join(urls))

    with open('urls.txt', 'rb') as file:
        response = requests.post(API_URL, headers=HEADERS, data=file)

    return response.json()

def main():
    jobs = fetch_yesterdays_job_urls()
    if not jobs:
        print("No jobs published yesterday.")
        return

    batch_size = PUSH_BATCH_SIZE  # Adjust based on your needs
    for i in range(0, len(jobs), batch_size):
        batch = jobs[i:i + batch_size]
        response = push_urls_to_baidu(batch)
        print(f"Batch {i // batch_size + 1} Response: {response}")

        # Check remaining quota
        if response.get("remain", 0) <= 0:
            print("No remaining quota.")
            break


if __name__ == "__main__":
    main()
    print("Done.")
