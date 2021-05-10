import requests
import threading
import time
from plyer import notification

def foo():
    print(time.ctime())
    
def GetAppoint():
    url = "http://www.google.com"
    timeout = 5
    Flag=0
    try:
        request = requests.get(url, timeout=timeout)
        Flag=0
    except (requests.ConnectionError, requests.Timeout) as exception:
        Flag=1
        print('Retrying to connect to the internet')
    if Flag:
        return {0}
    else:
        comlist=[]
        num=581  #141-150 Delhi
        date=['10-05-2021','18-05-2021','24-05-2021','1-06-2021']
        for d in range(len(date)):
            url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'.format(num,date[d])
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
            result = requests.get(url, headers=headers)
            x=result.json()
            #print(x)
            for i in range(len(x["centers"])):
                for j in range(len(x["centers"][i]["sessions"])):
                    if x["centers"][i]["sessions"][j]["min_age_limit"]==18 and  x["centers"][i]["sessions"][j]["available_capacity"]>=0:
                        comlist.append(x["centers"][i]["sessions"][j])
                    
        #print(comlist)
        return comlist


WAIT_TIME_SECONDS = 60
title='Slot Available'


K=GetAppoint()
#print(len(str(K)))
if len(str(K))<5:
    Message='Script Start\n Null'
else:
    Message=''
    for p in range(len(K)):
        if K[int(p)]['available_capacity']>=1:
            Message='available_capacity: '+str(K[int(p)]['available_capacity'])+"\nvaccine: "+str(K[int(p)]['vaccine'])+'\n'+str(K[int(p)]['date'])+'\n'
            notification.notify(title=title,message=Message,app_icon= 'C:/Users/jhawa/OneDrive/Desktop/CoWin/1.ico',timeout=10,toast=False)
    #print(Message)
#print(K)
ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    foo()
    AlertMe=GetAppoint()
    if len(str(AlertMe))<5:
        print(str(AlertMe))
    else:
        Message=''
        for p in range(len(AlertMe)):
            if AlertMe[int(p)]['available_capacity']>=1:
                Message='available_capacity: '+str(AlertMe[int(p)]['available_capacity'])+"\nvaccine: "+str(AlertMe[int(p)]['vaccine'])+'\n'+str(AlertMe[int(p)]['date'])
                #print(Message)
                notification.notify(title=title,message=Message,app_icon= 'C:/Users/jhawa/OneDrive/Desktop/CoWin/1.ico',timeout=10,toast=True)
                print('##--------------------##')
                print('Available capacity is {} || Notification is pushed'.format(AlertMe[int(p)]['available_capacity']))
                print('##--------------------##')
            else:
                print('Available capacity is 0 || No notification is pushed')
        
         