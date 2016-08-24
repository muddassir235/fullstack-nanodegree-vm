#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
connection = psycopg2.connect("dbname=forum")

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts order by time desc")
    rows = cursor.fetchall()
    posts = [{'content': str(bleach.clean(str(row[0]))), 'time': str(bleach.clean(str(row[1])))} for row in rows]
    cursor.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    cursor = connection.cursor()
    t = time.strftime('%c', time.localtime())
    cursor.execute("INSERT INTO posts (content,time) VALUES (%s,%s)",(str(bleach.clean(content)),t))
    connection.commit()
    cursor.close()


