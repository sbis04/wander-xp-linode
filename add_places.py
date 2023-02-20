import pymysql
import os

data = [
    {'country': 'USA', 'city': 'New York', 'zip': '10001', 'image_path': 'https://image.cnbcfm.com/api/v1/image/106268734-1574876711571gettyimages-1059614218.jpeg'},
    {'country': 'USA', 'city': 'San Francisco', 'zip': '90001', 'image_path': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSan_Francisco&psig=AOvVaw35To-7JGk-Mj5GqmoS0tUT&ust=1676881763161000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCPCgr8uVof0CFQAAAAAdAAAAABAM'},
    {'country': 'USA', 'city': 'San Diego', 'zip': '90001', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft3.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcRqoa2VT7qUY6EFnxZS8ijdxmfEVEkeJVRBmHDFer8UJnYhIZaXZTm2fAIUptecb_2i&psig=AOvVaw35To-7JGk-Mj5GqmoS0tUT&ust=1676881763161000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCPCgr8uVof0CFQAAAAAdAAAAABAI'},
    {'country': 'USA', 'city': 'Seattle', 'zip': '60601', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft1.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcTZbjYBZTtuNzB88WIhYa84YvjWBCDHrlt_Fk7q0kgQUEJuPXyjz85xvMGmNxgggnZN&psig=AOvVaw35To-7JGk-Mj5GqmoS0tUT&ust=1676881763161000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLjOyY6Wof0CFQAAAAAdAAAAABAE'},
    {'country': 'Canada', 'city': 'Toronto', 'zip': 'M5V 2A1', 'image_path': 'https://cdn.britannica.com/93/94493-050-35524FED/Toronto.jpg'},
    {'country': 'Canada', 'city': 'Vancouver', 'zip': 'V6B 4Y8', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft2.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcS90WWUwmFLBdKppM1kZywD52_tuJ38QlRLTQAe9jTs3tsbR5wRhcgh2nXlNywMb7fY&psig=AOvVaw2U6_GETaZ4h89STVnkZcJh&ust=1676881946411000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLjOk6CWof0CFQAAAAAdAAAAABAE'},
    {'country': 'Canada', 'city': 'Victoria', 'zip': 'V6B 4Y8', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft0.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcRp7kyKmnM5Lrf8fBUNtE1NsGnrmorV96ImVEOjvRRRtDCdRqS7qtHpDXlXYPatwszv&psig=AOvVaw2U6_GETaZ4h89STVnkZcJh&ust=1676881946411000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLjOk6CWof0CFQAAAAAdAAAAABAI'},
    {'country': 'India', 'city': 'Mumbai', 'zip': '400001', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft2.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcRCHq5sfoZSceeJhBJOlt2YPx6umIaxsHFPTXSMIgqR86RwMXerY7Z4rPL_cKgtf-KH&psig=AOvVaw2R4B5gsgaK7QXOK1vEFUkG&ust=1676882039654000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCPCu48OWof0CFQAAAAAdAAAAABAE'},
    {'country': 'India', 'city': 'Delhi', 'zip': '110001', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft3.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcRfcK-yQI7bvI7TbYddJcWOFX4x7WxvTxvxDJvMEHzdTBWe1Dfb1tN9lcHrbILdpplN&psig=AOvVaw2R4B5gsgaK7QXOK1vEFUkG&ust=1676882039654000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCPCu48OWof0CFQAAAAAdAAAAABAI'},
    {'country': 'India', 'city': 'Bengaluru', 'zip': '', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft3.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcTCLo_orZbk5wQyKhcMBGTw-9Ms3N49_RFB2OliAJGxiDARTQpkm20fN9hihDXEUKK6&psig=AOvVaw2R4B5gsgaK7QXOK1vEFUkG&ust=1676882039654000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCPCu48OWof0CFQAAAAAdAAAAABAM'},
    {'country': 'Australia', 'city': 'Sydney', 'zip': '2000', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft1.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcRFEGuHElSkb18430ojFaA4iCAus5XYfQuhwJ531_vmI6AoRDn829re2yqUqwq9u8C1&psig=AOvVaw3UNcZF5ws1k7JM6AKp-_4P&ust=1676881592817000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCJCT2-6Uof0CFQAAAAAdAAAAABAE'},
    {'country': 'Australia', 'city': 'Melbourne', 'zip': '3000', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft1.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcTEv9gdycEKSYtq4KTlbZt-Ekp-Aq9u9xzjQu9qiSFw31eSDBKRM_0wGPWAemXCcMyi&psig=AOvVaw3UNcZF5ws1k7JM6AKp-_4P&ust=1676881592817000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCJCT2-6Uof0CFQAAAAAdAAAAABAI'},
    {'country': 'Australia', 'city': 'Brisbane', 'zip': '', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft2.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcReLhtYOyzGw5Ep-pz-NccH8JwYGfJQ8nLCH_ct4upnvde5taZxl6ynVIX_FwAkpJFv&psig=AOvVaw3UNcZF5ws1k7JM6AKp-_4P&ust=1676881592817000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLCq-qqVof0CFQAAAAAdAAAAABAE'},
    {'country': 'France', 'city': 'Paris', 'zip': '75001', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft3.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcQ1oS-DeKDIgvicoSyoD8KKoIAinTTDeC6VO7erBHEsAggFjaZYZ6YP1HkFahtlKTb_&psig=AOvVaw2mIx_WLd1VADZDf6YTBXhq&ust=1676881477966000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCKig_LeUof0CFQAAAAAdAAAAABAI'},
    {'country': 'France', 'city': 'Marseille', 'zip': '', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft3.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcQ6-OUl5YRCuUrG7j-RnhO-gJjJgOX29YoJXz0oCTxTDepRQkRBlbdLDCQ-H602pzUU&psig=AOvVaw2mIx_WLd1VADZDf6YTBXhq&ust=1676881477966000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLjRtpeVof0CFQAAAAAdAAAAABAE'},
    {'country': 'France', 'city': 'Bordeaux', 'zip': '', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft1.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcQYBPdeeQ34uOStqa9VX_5TSfr3634gXIUyVuZh2m6RmzQIqqt3TGWey8rYC1_ECno7&psig=AOvVaw0-QK5_c4Rtca2YIER3O096&ust=1676881328870000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCKCx7vCTof0CFQAAAAAdAAAAABAE'},
    {'country': 'France', 'city': 'Lyon', 'zip': '', 'image_path': 'https://www.google.com/url?sa=i&url=http%3A%2F%2Ft0.gstatic.com%2Flicensed-image%3Fq%3Dtbn%3AANd9GcQ94OEZPuwT3AEOGRN6ILlk0cpboutA_wKHmkbOBTUXffMWKghUGnKPEANvCUvUfNT_&psig=AOvVaw2mIx_WLd1VADZDf6YTBXhq&ust=1676881477966000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCKig_LeUof0CFQAAAAAdAAAAABAE'},
]

DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Connect to Linode's managed database
db = pymysql.connect(
    host='lin-16251-9474-mysql-primary-private.servers.linodedb.net',
    user='linroot',
    password=DB_PASSWORD,
    ssl_ca='my-cluster-ca-certificate.crt',
    db='wander_xp',
)

def add_places(data):
    cursor = db.cursor()
    for row in data:
        sql = "INSERT INTO places (city, country, image_path) VALUES (%s, %s, %s)"
        cursor.execute(sql, (row["city"], row["country"], row["image_path"]))
        db.commit()

add_places(data)
