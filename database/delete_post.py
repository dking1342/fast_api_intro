import psycopg2
import psycopg2.extras
from uuid import UUID
from dotenv import load_dotenv
import os

load_dotenv()
psycopg2.extras.register_uuid()


async def delete_post(post_id: UUID):
    """ delete a posts from the posts table """
    sql = """DELETE FROM posts WHERE post_id = %s RETURNING *;"""
    conn = None
    deleted_post = None
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
        cur.execute(sql, (post_id, ))
        # get the generated id back
        post_response = cur.fetchone()
        deleted_post = {
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

    return deleted_post
