import linode_api4
import csv

# Connect to the Linode API
client = linode_api4.LinodeClient("key")

# Get the Linode Database Service
db_service = client.db

# Get the Linode Database
db = db_service.instances("16251")

# Open the CSV file
with open('data.csv', mode='r') as csv_file:
    # Parse the CSV file
    csv_reader = csv.DictReader(csv_file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Create a new record with the data from the CSV row
        new_record = {
            "country": row["country"],
            "city": row["city"],
            "zip": row["zip"],
            "image_url": row["image_url"]
        }

        # Add the new record to the database
        db.add_row(new_record)
