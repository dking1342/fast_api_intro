import psycopg2
import psycopg2.extras
from uuid import UUID
from dotenv import load_dotenv
import os
from app import Post

load_dotenv()
psycopg2.extras.register_uuid()


async def update_post(post_id: UUID, post: Post):
    """ update a posts from the posts table """
    sql = """UPDATE posts SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING *"""
    conn = None
    updated_post = None
    print(post)
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
        cur.execute(sql, (post["title"], post["content"], post["published"], post_id, ))
        # get the generated id back
        post_response = cur.fetchone()
        updated_post = {
            "post_id": post_response[0],
            "title": post_response[1],
            "content": post_response[2],
            "published": post_response[3],
            "created_at": post_response[4]
        }

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_post
