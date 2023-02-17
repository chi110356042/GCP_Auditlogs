import os
from datetime import date, datetime, timedelta, timezone
from google.cloud import logging
import pandas as pd
import pytz
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import email.message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table
import json
import random
import sys
import time
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
client = logging.Client()
df = pd.DataFrame()
danger_user_query=[]
unique_user=[]
time=[]
count=0

today = date.today()
yesterday = date.today() - timedelta(days=1)

start_time = '{}T10:00:00'.format(yesterday)
end_time = '{}T01:00:00'.format(today)

FILTER = 'resource.type=bigquery_dataset AND resource.labels.dataset_id=\"policy_tags_demo\" AND timestamp>\"{}\" AND timestamp<\"{}\"'.format(
        start_time, end_time)

for entry in client.list_entries(filter_=FILTER, page_size=10):
        timestamp = entry.timestamp.isoformat()
        resource = entry.resource.labels
        payload = entry.payload

        timeString = timestamp 
        struct_time = datetime.strptime(
            timeString[:19].replace("T", " "), '%Y-%m-%d %H:%M:%S')  
        
        out_time = struct_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        df = df.append({
            'timestamp': out_time,
            'principalEmail': payload['authenticationInfo']['principalEmail'],
        }, ignore_index=True)

print('Last day ('+yesterday.strftime('%m-%d')+' 18pm to '+today.strftime('%m-%d')+' 9am)\'s result')


'''
iam service account example:
p878198504389-232004@gcp-sa-logging.iam.gserviceaccount.com

principal user email example:
xxxxx@cathayholdings.com.tw
'''
for i in range(0, len(df.index)):
    if "iam.gserviceaccount" not in df["principalEmail"][i]:
        user_name = df["principalEmail"][i].split('@')  
        if user_name[0] not in danger_user_query:   
            count+=1            
            print('danger user email '+str(count)+ ': ', df["principalEmail"][i])
            unique_user.append(df["principalEmail"][i])
        danger_user_query.append(user_name[0]) 
        time.append(str(df["timestamp"][i]))
        
if df.empty==True:
    print("No danger user last night")

else:    
    #處理timestamp
    use_time=[]
    date_time=[]

    for i in range(0,len(time)):
        use_str=time[i]
        '''
        原始格式：
        2023-02-08 23:25:50+08:00
        '''
        use_str=use_str.replace("2023-", "").replace("+08:00", "")
        use_str=use_str.split()
        date_time.append(use_str[0])
        use_time.append(use_str[1])

    #print dataframe
    use={"user": danger_user_query[::-1],
        "date": date_time[::-1],
        "time": use_time[::-1]
        }
    data_table=pd.DataFrame(use)

#change your sender/receiver email info here
data=[
        ("receiver name1", "receiver email1"),
        ("receiver name2", "receiver email2"),
        ("receiver name3", "receiver email3"),
    ]


# SMTP server info
smtp_server_str = "smtp.gmail.com"
port = 465
sender_email = "Enter your sender_email"
#password = input("Enter your passowrd: ")
password = "Enter your password"

# loop through the data records and send email
with smtplib.SMTP_SSL(smtp_server_str, port) as smtp_server:
    smtp_server.login(sender_email, password)
    for item in data:
        msg = MIMEMultipart()
        msg["Subject"] = f"{yesterday.strftime('%m/%d')} Dangerous user notification" 
        msg["From"] = "Your name"
        msg["Cc"] = sender_email
        receiver_email = item[1] 
        msg["To"] = receiver_email  
           
        if df.empty==True:
            txt = f"{item[0]}, \n\nThere are no dangerous user yesterday, thanks.\n"
        else:
            txt = f"{item[0]}, \n\nThe following users need your attention, thanks.\n\n"
            for i in range(0,len(unique_user)):
                txt += f"User {i+1}: {unique_user[i]}\n"
                

            html = """\
            <html>
            <head></head>
            <body>
                {0}
            </body>
            </html>
            """.format(build_table(data_table, 'blue_light'))

        body = MIMEText(txt, "plain")
        msg.attach(body)
        if df.empty!=True:
            part2 = MIMEText(html, 'html')
            msg.attach(part2) 

        smtp_server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )

#pic
'''
    plt.legend(loc='best')
    plt.xlabel('query time') 
    plt.figure(figsize=(10, 8))
    plt.yticks(range(0, len(danger_user_query)), fontsize=8)
    plt.xticks(range(0, len(use_time), 2), rotation=45, color='#f00', fontsize=8)
    plt.scatter(use_time, danger_user_query, color = '#88c999')
    plt.title('Dangerous query last day')
    plt.show()
'''
    
@app.route("/")
def use_func():
    if df.empty==True:
        return "No dangerous user last night"
    else:
        #return data_table.to_html()
        return render_template('index.html', table=data_table)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))