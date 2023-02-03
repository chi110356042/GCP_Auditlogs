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

client = logging.Client()
df = pd.DataFrame()

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

danger_user_query=[]
unique_user=[]
time=[]
count=0



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

#處理timestamp座標
use_time=[]
change=0
for i in range(0,len(time)):
    use_str=time[i]
    use_str=use_str.replace("2023-", "").replace("+08:00", "")
    use_str=use_str.split()
    if i==0:
        use_time.append(use_str[0]+use_str[1])
    else:
        if use_str[1][0]=='0':
            change+=1
            if change==1:
                use_time.append(use_str[0]+use_str[1])
            else:
                use_time.append(use_str[1])
        else:
            use_time.append(use_str[1])

#print dataframe
use={"user": danger_user_query,
      "time": use_time}
data_table=pd.DataFrame(use)
print(data_table)


data = [
    #("YuChi", "v871202@gmail.com"),
    ("Kite", "re102162189@gmail.com"),
    ("Joanne", "jo05240625@gmail.com"),

]

# SMTP server info
smtp_server_str = "smtp.gmail.com"
port = 465
sender_email = "v871202@gmail.com"
password = input("Enter your passowrd: ")


# loop through the data records and send email
with smtplib.SMTP_SSL(smtp_server_str, port) as smtp_server:
    smtp_server.login(sender_email, password)
    for item in data:
        msg = MIMEMultipart()
        msg["Subject"] = f"{yesterday.strftime('%m/%d')} Dangerous user notification" 
        msg["From"] = "胡育騏"
        msg["Cc"] = sender_email
        receiver_email = item[1] 
        msg["To"] = receiver_email  

        if len(unique_user)==0:
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
        if len(unique_user)!=0:
            part1 = MIMEText(html, 'html')
            msg.attach(part1) 

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

plt.title('Danger query last day')
plt.show()
'''


