#rss-mailer
This tiny python script sends a daily email digest of recent scientific articles.

##usage
Settings should be provided in a separate input file, with the following variables:

```
sender                #adress you want to use to send the mail
password              #password for sender
hostname              #hostname for sender
recipient             #adress of the recipient
max_article_age       #maximum age of the articles you want to recover, in hours
list_of_my_journals   #list of the rss feeds for the articles you want to retrieve
```

By default, rss-mailer assumes settings can be found in settings.py.
