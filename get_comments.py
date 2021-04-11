import praw
import time
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode

def bot_login():
    print("Logging in...")
    r = praw.Reddit(username="fkrddt9999",
                    password="rickyy11",
                    client_id="9CzEHluYj8i2xg",
                    client_secret="i9TGDxYUhsqbFXsQxdZc_zt8YIgK6A",
                    user_agent="ricks bot bot")
    print("Logged in!")
    return r

def setup_database():
    conn = sqlite3.connect('reddit_comments.db')
    c = conn.cursor()
    create_comments = ("CREATE TABLE IF NOT EXISTS comments (username INTEGER,date_time INTEGER,comment_id TEXT,comment_karama_local INTEGER,comment_text TEXT,subreddit_posted_in TEXT,comment_sentiment FLOAT)")
    c.execute(create_comments)
    conn.commit()
    conn.close()

# Insert comment data in table
def commit_comments(comments):
    global count
    conn = sqlite3.connect('reddit_comments.db')
    c = conn.cursor()
    sql_statement = 'INSERT INTO comments VALUES (?,?,?,?,?,?,?)'
    c.executemany(sql_statement, comments)
    conn.commit()
    conn.close()
    count = count + 1
    print(str(count) + " comments added")

def run_bot(r):
    analyzer = SentimentIntensityAnalyzer()

    subreddits = r.subreddit("wallstreetbets+stocks+valueinvesting+investing+pennystocks")

    for comment in subreddits.stream.comments(skip_existing=True):
        comment_list = []
        sent_base = analyzer.polarity_scores(unidecode(comment.body))
        sentiment = sent_base['compound']
        comment_list.append(
            [str(comment.author), int(comment.created_utc), str(comment.id), int(comment.score), str(comment.body),
             str(comment.subreddit), float(sentiment)])
        commit_comments(comment_list)
        print("\n\n" + comment.body[0:125] + "..\nSentiment: " + str(sentiment))



r = bot_login()
setup_database()
count = 0

while True:
    try:
        run_bot(r)
    except Exception as e:
        print(e)