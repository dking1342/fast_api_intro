import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def get_posts():
    """ get all posts from the posts table """
    sql = """SELECT * FROM posts;"""
    conn = None
    post_list = None
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
        cur.execute(sql)
        # get the generated id back
        posts = cur.fetchall()
        post_list = []
        for post in posts:
            post_dict = {
                "post_id": post[0],
                "title": post[1],
                "content": post[2],
                "published": post[3],
                "created_at": post[4]
            }
            post_list.append(post_dict)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return post_list
