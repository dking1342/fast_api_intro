import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def insert_post(post):
    """ insert a new post into the posts table """
    sql = f"""INSERT INTO posts(title,content)
             VALUES(%s,%s) RETURNING *;"""
    conn = None
    post_id = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=os.environ.get("HOST_SERVER"),
            database=os.environ.get("DATABASE_NAME"),
            user=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD")
        )
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (post["title"], post["content"],))
        # get the generated id back
        post_id = cur.fetchone()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return post_id


# if __name__ == '__main__':
#     # insert one vendor
#     insert_post("new post", "beaches are sandy")