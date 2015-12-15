__author__ = 'dvr'
import feedparser
import time
import calendar
import smtplib
from email.mime.text import MIMEText
import settings

#journals currently following:
#J Med Chem, Med Chem Lett, Nature Rev DD, J Chemical biology,
#J Chem Inf Model, Practical Fragments

new_articles = []
currentdate = time.strftime("%a %d %b %Y", time.gmtime())


def get_article_age(time_published):
    article_age_epoch = calendar.timegm(time_published)
    current_time = time.time()
    timediff = current_time - article_age_epoch
    return (timediff/3600)

def collect_new_posts(parsedfeed):
    for item in parsedfeed['entries']:
        time_published = item['updated_parsed']
        if get_article_age(time_published) <= settings.max_article_age:
            new_articles.append({'title':item['title'].replace('\n',' '),'link':item['link']})

list_of_my_journals = ['http://feeds.feedburner.com/acs/jmcmar',
'http://feeds.nature.com/nrd/rss/aop',
'http://feeds.feedburner.com/acs/acbcct',
'http://feeds.feedburner.com/acs/amclct',
'http://feeds.feedburner.com/acs/jcisd8',
'http://practicalfragments.blogspot.com/feeds/posts/default']

current_time = time.time()


for feed in list_of_my_journals:
    parsedfeed = feedparser.parse(feed)
    collect_new_posts(parsedfeed)

if not new_articles:
    payload = "Sorry! No interesting articles were published in the past 24h.\n"
else:
    payload = "Interesting articles:\n\n"


for article in new_articles:
    if 'title' and 'link' in article:
        payload += ((article['title']+'\n'+article['link']+'\n\n'))


#Send mails

msg = MIMEText(payload,'plain',"utf-8")

msg["Subject"] = ("Your articles for {}".format(currentdate))
msg["From"] = settings.sender
msg["To"] = settings.receiver

session = smtplib.SMTP_SSL(settings.hostname)
session.login(settings.sender, settings.password)
session.sendmail(settings.sender, [settings.receiver], msg.as_string())
session.quit()
