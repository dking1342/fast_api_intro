import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE posts (
        post_id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        title VARCHAR(255) NOT NULL,
        content VARCHAR(255) NOT NULL,
        published BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMP NOT NULL DEFAULT now()
        )
        """)
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=os.environ.get("HOST_SERVER"),
            database=os.environ.get("DATABASE_NAME"),
            user=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD")
        )
        for command in commands:
            print(command)
        print(commands)
        cur = conn.cursor()
        # create table one by one

        cur.execute(commands)
        # for command in commands:
        #     cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
