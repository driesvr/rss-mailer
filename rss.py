__author__ = 'dvr'
import feedparser
import time
import calendar
import smtplib
from email.mime.text import MIMEText
import settings

new_articles = []

#checks the current time and date
current_time = time.time()
current_date = time.strftime("%a %d %b %Y", time.gmtime())

#returns age of the article in hours
def get_article_age(time_published):
    article_age_epoch = calendar.timegm(time_published)
    current_time = time.time()
    timediff = current_time - article_age_epoch
    return (timediff/3600)

#collects all new posts from the feeds into new_articles
def collect_new_posts(parsedfeed):
    for item in parsedfeed['entries']:
        time_published = item['updated_parsed']
        if get_article_age(time_published) <= settings.max_article_age:
            new_articles.append({'title':item['title'].replace('\n',' '),'link':item['link']})


#loops over all feeds and process them
for feed in settings.list_of_my_journals:
    parsedfeed = feedparser.parse(feed)
    collect_new_posts(parsedfeed)

#initializes a mail payload
if not new_articles:
    payload = "Sorry! No interesting articles were published in the past 24h.\n"
else:
    payload = "Interesting articles:\n\n"

#attach article info to mail payload
for article in new_articles:
    if 'title' and 'link' in article:
        payload += ((article['title']+'\n'+article['link']+'\n\n'))

#format the mail
msg = MIMEText(payload,'plain',"utf-8")
msg["Subject"] = ("Your articles for {}".format(current_date))
msg["From"] = settings.sender
msg["To"] = settings.receiver

#send the mail
session = smtplib.SMTP_SSL(settings.hostname)
session.login(settings.sender, settings.password)
session.sendmail(settings.sender, [settings.receiver], msg.as_string())
session.quit()
