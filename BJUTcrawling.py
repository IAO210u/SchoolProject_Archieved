##@@ Parsing settings
import requests
url = 'http://www.bjut.edu.cn'
rqg = requests.get(url)
print("Status:", rqg.status_code)

import chardet
print('Encoding:', rqg.encoding)
print('Detection Result:', chardet.detect(rqg.content))
# rqg.encoding = chardet.detect(rqg.content)['encoding']
print('Encoding After:', rqg.encoding)


##@@ MySQL settings
import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='4BEAR', db='db_crawl', charset='utf8')

cursor = conn.cursor()
## table
cursor.execute("drop table bjut_notice")  # uncomment it if you want to reset table
sql_tb = """Create table if not exists BJUT_notice(
title varchar(255) not null,
date varchar(255),
text text not null,
url varchar(255) primary key) CHARACTER SET utf8mb4"""  # avoid duplicate news
cursor.execute(sql_tb)
cursor.execute("show tables")

## store data
def dump_data(thumbnail, text, date, url):
    insert = "insert into BJUT_notice(title, text, date, url) values (%s, %s, %s, %s)"
    cursor.execute(insert, (thumbnail, text, date, url))
    conn.commit()



##@@ Parsing by xml
from lxml import etree
html = rqg.content.decode('utf-8')
html = etree.HTML(html,parser=(etree.HTMLParser(encoding='utf-8')))

# test if accessible, delete if not necessary
target = html.xpath('//div[@class="list2"]/ul/li/a/text()')
print(target)
target_url = html.xpath('//div[@class="list2"]/ul/li/a/@href')
print(target_url, '\n\n')



box = []  # comment it after first run
for i in range(len(target_url)):
    # detect and parse settings
    news_url = "http://www.bjut.edu.cn/" + target_url[i]
    rqg = requests.get(news_url)
        # print('Detection:', chardet.detect(rqg.content))
    rqg.encoding = chardet.detect(rqg.content)['encoding']
        # print('Charset is:', chardet.detect(rqg.content))
    html = rqg.content.decode('utf-8')
    html = etree.HTML(html, parser=(etree.HTMLParser(encoding='utf-8')))

    # finding text and store into mysql
    news_date = html.xpath('//p[@class="vsbcontent_end"]/text()')  # return a list of 'etree._ElementUnicodeResult' em
    #@print('datetype:', type(news_date[0]), news_date)
    title = html.xpath('//div[@class="content-title"]/h3/text()')  # return a list of 'etree._ElementUnicodeResult' em
    #@print('titletype:', type(title))
    tagt = html.xpath('//div[@class="v_news_content"]')
    #@print('tagt', type(tagt))
    content = tagt[0].xpath('string(.)').strip()
    try:
        dump_data(title,content,news_date,news_url)
        # alternatively, dump_data(title[0], content, news_date[0], news_url)
    except:
        pass

    # email notifications
    notice = target[i] + ' ' + news_url
    if notice not in box:
        box.append(notice)


## out of loop
conn.close()  # disconnect from mysql
# del box [0:5]  # delete news that had been sent, uncomment it after first run
print('News to be sent:', box, '\n\n')


# auto-sending notification
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
##@@ settings
msg = MIMEMultipart()
sender_info = 'BurBur <renyi@qq.com>'  # any name or name with email like: bur <wyyx@163.com>, only name is not recommend
receiver_email = 'bur_wyyx@163.com'

from_addr = 'bur_wyyx@163.com'  # real address to send email
passwd = 'RDKUWHTOUVBOHQDI'

msg['From'] = sender_info
msg['To'] = receiver_email
msg['Subject'] = '这次可以了'
msg['Cc'] = '自己发的'
##@@ email content
# sending an html version
html_add = """\
<html>
  <body>
    <p><br> <strong> Hi there! here's the latest news:</strong>\n"""
# adding news into body
for news in box:
    slices = news.rsplit(" ", 1)
    html_add += "       <br>{} <a href=\"{}\">{}</a>\n".format(slices[0], slices[1], slices[1])
html_tail = """<br>And this is HTML!
    </p>
  </body>
</html>
"""

html = html_add + html_tail
print(html)
body = MIMEText(html, 'html', 'utf-8')
# attaching parts
msg.attach(body)
# sending email
smtp_server = 'smtp.163.com'
server = smtplib.SMTP_SSL(smtp_server, 465)  # SSL connection
# server = smtplib.SMTP(smtp_server, 465)  # normal connection
server.login(from_addr, passwd)
server.sendmail(from_addr, receiver_email, msg.as_string())
server.quit()  # end connection
