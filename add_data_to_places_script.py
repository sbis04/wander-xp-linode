import csv
import linode_api4


from flask import Flask, request, jsonify
import pymysql
import boto3
import os

# Connect to Linode's managed database
db = pymysql.connect(
    host='lin-16251-9474-mysql-primary-private.servers.linodedb.net',
    user='linroot',
    password=DB_PASSWORD,
    ssl_ca='my-cluster-ca-certificate.crt',
    db='wander_xp',
)


# Open the CSV file
with open('filename.csv', mode='r') as csv_file:
    # Parse the CSV file
    csv_reader = csv.DictReader(csv_file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        data = request.get_json()
        cursor = conn.cursor()
        # Store data in Linode's managed database
        sql = "INSERT INTO places (country, city, zip, image_url) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (row["country"], row["city"], row["zip"], row["image_url"]))
        conn.commit()

