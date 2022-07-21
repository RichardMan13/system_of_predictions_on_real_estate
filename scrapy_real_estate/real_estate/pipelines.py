# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import config_database
import psycopg2

class RealEstatePipeline:

    def __init__(self):

        self.DB_HOST = 'localhost' #'127.0.0.1'
        self.DB_NAME = 'postgres'
        self.DB_USER = 'postgres'
        self.DB_PASS = 'postgres'

        self.create_connection()
        self.create_table()

    
    def create_connection(self):
        self.conn = psycopg2.connect(
            dbname=self.DB_NAME, 
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""DROP TABLE IF EXISTS real_estate_ativa""")
        self.cur.execute("""
            CREATE TABLE real_estate_ativa(
                id SERIAL PRIMARY KEY,
                price FLOAT,
                type VARCHAR,
                rooms INT,
                neighborhood VARCHAR,
                suites INT,
                bathrooms INT,
                garages INT,
                private_area FLOAT,
                total_area FLOAT
                );
        """)

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.cur.execute("""
            INSERT INTO real_estate_ativa
                (price,
                neighborhood,
                type,
                rooms,
                suites,
                bathrooms,
                garages,
                total_area,
                private_area)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                item['price'][0],
                item['neighborhood'][0],
                item['type'][0],
                item['rooms'][0],
                item['suites'][0],
                item['bathrooms'][0],
                item['garages'][0],
                item['total_area'][0],
                item['private_area'][0]
            )
        )
        self.conn.commit()