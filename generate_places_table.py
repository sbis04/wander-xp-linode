import csv

# Define the data to be written to the CSV file
data = [
    {'country': 'USA', 'city': 'New York', 'zip': '10001', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9a/New_York_City_top_view.jpg'},
    {'country': 'USA', 'city': 'Los Angeles', 'zip': '90001', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9d/Los_Angeles%2C_California_%28Unsplash%29.jpg'},
    {'country': 'USA', 'city': 'Chicago', 'zip': '60601', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/e/ee/Chicago_skyline_at_dusk.jpg'},
    {'country': 'Canada', 'city': 'Toronto', 'zip': 'M5V 2A1', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/73/Toronto_skyline_2011.jpg'},
    {'country': 'Canada', 'city': 'Vancouver', 'zip': 'V6B 4Y8', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/8/8d/Vancouver_bc_harbor.jpg'},
    {'country': 'India', 'city': 'Mumbai', 'zip': '400001', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/66/Mumbai_Skyline_with_Banganga_Tank_and_Kapur_Baug.jpg'},
    {'country': 'India', 'city': 'Delhi', 'zip': '110001', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Humayuns_tomb_from_the_charbagh.JPG'},
    {'country': 'Australia', 'city': 'Sydney', 'zip': '2000', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/65/Sydney_Opera_House_and_Harbour_Bridge_Dusk_%2834496014022%29.jpg'},
    {'country': 'Australia', 'city': 'Melbourne', 'zip': '3000', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Melbourne_CBD_skyline_at_dusk_%28cropped%29.jpg'},
    {'country': 'France', 'city': 'Paris', 'zip': '75001', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/4e/Paris_-_Eiffelturm_und_Marsfeld2.jpg'},
    {'country': 'France', 'city': 'Marseille', 'zip': '13001', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9d/Palais_Longchamp_Marseille.jpg'}
    # add more rows here for additional countries and cities
]

# Define the name of the CSV file
filename = 'data.csv'

# Open the CSV file and write the data to it
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['country', 'city', 'zip', 'image_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"CSV file '{filename}' has been generated.")
