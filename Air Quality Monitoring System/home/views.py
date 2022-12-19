from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse
import requests
import threading
from datetime import datetime
import time
import pandas as pd
global temp,hum,feellike,aqi,aqi_int,aircode,colour_aqi,pm,co,co2,nh,last,recommend

def things():
    threading.Timer(30,things).start()
    global temp,hum,feellike,aqi,aqi_int,aircode,colour_aqi,recommend
    url = 'https://api.thingspeak.com/channels/1469958/fields/2/last.json?api_key=6VZFKVYO23I7TCXP'
    response = requests.get(url)
    storage = response.json()
    temp=storage["field2"]
    url_hum = 'https://api.thingspeak.com/channels/1469958/fields/3/last.json?api_key=6VZFKVYO23I7TCXP'
    response_hum = requests.get(url_hum)
    storage_hum = response_hum.json()
    hum=storage_hum["field3"]
    url_feel = 'https://api.thingspeak.com/channels/1469958/fields/7/last.json?api_key=6VZFKVYO23I7TCXP'
    response_feel = requests.get(url_feel)
    storage_feel = response_feel.json()
    feellike=storage_feel["field7"]
    url_aqi = 'https://api.thingspeak.com/channels/1469958/fields/1/last.json?api_key=6VZFKVYO23I7TCXP'
    response_aqi = requests.get(url_aqi)
    storage_aqi = response_aqi.json()
    aqi=storage_aqi["field1"]
    aqi_int=int(aqi)
    if(0<aqi_int<=50):
        aircode="Good"
        colour_aqi="rgb(0, 255, 0);"
        recommend="The level of Air Quality might have Minimal Impact."
    elif(50<aqi_int<=100):
        aircode="Satisfactory"
        colour_aqi="rgb(255, 255, 0);"
        recommend="The level of Air Quality might cause minor breathing discomfort to sensitive people"
    elif(100<aqi_int<=200):
        aircode="Moderate"
        colour_aqi="rgb(255, 165, 0);"
        recommend="The level of Air Quality might cause breathing discomfort to the people with lung disease such as asthma and discomfort to people with heart disease, children and older adults."
    elif(200<aqi_int<=300):
        aircode="Poor"
        colour_aqi="rgb(255,0, 0);"
        recommend="The level of Air Quality might cause breathing discomfort to people on prolonged exposure and discomfort to people with heart disease with short exposure."
    elif(300<aqi_int<=400):
        aircode="Very Poor"
        colour_aqi="rgb(153, 0, 0);"
        recommend="The level of Air Quality might cause respiratory illness to the people on prolonged exposure. Effect may be more pronounced in people with lung and heart diseases."
    else:
        aircode="Severe"
        colour_aqi="rgb(142, 1, 17);"
        recommend="The level of Air Quality might cause respiratory effects even on healthy people and serious health impacts on people with lung/heart diseases. The health impacts may be experienced even during light physical activity."



# Create your views here.
def index(request):
    now = datetime.now()
    current_time = now.strftime("%d %b %H:%M")
    print("Current Time =", current_time)
    global temp,hum,feellike,aqi,aqi_int,aircode,colour_aqi
    things()
    context={
        "temperature":temp,
        "humidity":hum,
        "feels":feellike,
        "aqi":aqi,
        "colour_aqi":colour_aqi,
        "air":aircode,
        "time":current_time

    }
    

    return render(request,'base.html',context)



def aqi_conc():
    threading.Timer(30,aqi_conc).start()
    global pm,co,co2,nh,last
    url_pm = 'https://api.thingspeak.com/channels/1469958/fields/8/last.json?api_key=6VZFKVYO23I7TCXP'
    response = requests.get(url_pm)
    storage = response.json()
    pm=storage["field8"]
    url_co2 = 'https://api.thingspeak.com/channels/1469958/fields/5/last.json?api_key=6VZFKVYO23I7TCXP'
    response_co2 = requests.get(url_co2)
    storage_co2 = response_co2.json()
    co2=storage_co2["field5"]
    url_co = 'https://api.thingspeak.com/channels/1469958/fields/4/last.json?api_key=6VZFKVYO23I7TCXP'
    response_co = requests.get(url_co)
    storage_co = response_co.json()
    co=storage_co["field4"]
    url_nh = 'https://api.thingspeak.com/channels/1469958/fields/6/last.json?api_key=6VZFKVYO23I7TCXP'
    response_nh = requests.get(url_nh)
    storage_nh = response_nh.json()
    nh=storage_nh["field6"]
    my_date =datetime.utcnow()
    my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
    my_currentutctime = time.mktime(currentutctime)
    y=(storage["created_at"])
    my_createdtime= time.strptime(y, '%Y-%m-%dT%H:%M:%SZ')
    created_time = time.mktime(my_createdtime)
    time_diff=my_currentutctime-created_time
    minutes = int((time_diff) / 60 )
    hours=int((time_diff) / 3600) 
    if(minutes<=2):
        last="now"
    elif(hours<=1):
        minutes=str(minutes)
        last=minutes+" minutes ago"
    elif(hours>1 and hours<=24):
        hours=str(hours)
        last=hours+" hours ago"
    else:
        last=" long time ago"
    

def charts():
    threading.Timer(30,charts).start()
    url_temp_100 = 'https://api.thingspeak.com/channels/1469958/fields/2.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_temp_100 = requests.get(url_temp_100)
    storage_temp_100 = response_temp_100.json()
    mylist_temp_100=[]
    time_temp_100=[]
    for i in range(1,len(storage_temp_100["feeds"])):
        x=(storage_temp_100["feeds"][i]["field2"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_temp_100["feeds"][(len(storage_temp_100["feeds"])-1)]["created_at"])
        y_time=(storage_temp_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M:%S')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_temp_100.append(float(x))
            time_temp_100.append(minutes)
    return(mylist_temp_100,time_temp_100)

def charts_co():
    threading.Timer(30,charts_co).start()
    url_co_100 = 'https://api.thingspeak.com/channels/1469958/fields/4.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_co_100 = requests.get(url_co_100)
    storage_co_100 = response_co_100.json()
    mylist_co_100=[]
    time_co_100=[]
    for i in range(1,len(storage_co_100["feeds"])):
        x=(storage_co_100["feeds"][i]["field4"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_co_100["feeds"][(len(storage_co_100["feeds"])-1)]["created_at"])
        y_time=(storage_co_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M:%S')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_co_100.append(float(x))
            time_co_100.append(minutes)
    return(mylist_co_100,time_co_100)

def charts_co_2():
    threading.Timer(30,charts_co_2).start()
    url_co2_100 = 'https://api.thingspeak.com/channels/1469958/fields/5.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_co2_100 = requests.get(url_co2_100)
    storage_co2_100 = response_co2_100.json()
    mylist_co2_100=[]
    time_co2_100=[]
    for i in range(1,len(storage_co2_100["feeds"])):
        x=(storage_co2_100["feeds"][i]["field5"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_co2_100["feeds"][(len(storage_co2_100["feeds"])-1)]["created_at"])
        y_time=(storage_co2_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M:%S')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_co2_100.append(float(x))
            time_co2_100.append(minutes)
    return(mylist_co2_100,time_co2_100)

def charts_nh_3():
    threading.Timer(30,charts_nh_3).start()
    url_nh_100 = 'https://api.thingspeak.com/channels/1469958/fields/6.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_nh_100 = requests.get(url_nh_100)
    storage_nh_100 = response_nh_100.json()
    mylist_nh_100=[]
    time_nh_100=[]
    for i in range(1,len(storage_nh_100["feeds"])):
        x=(storage_nh_100["feeds"][i]["field6"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_nh_100["feeds"][(len(storage_nh_100["feeds"])-1)]["created_at"])
        y_time=(storage_nh_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M:%S')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_nh_100.append(float(x))
            time_nh_100.append(minutes)
    return(mylist_nh_100,time_nh_100)
def charts_aqi():
    threading.Timer(30,charts_aqi).start()
    url_aqi_100='https://api.thingspeak.com/channels/1469958/fields/1.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_aqi_100 = requests.get(url_aqi_100)
    storage_aqi_100 = response_aqi_100.json()
    mylist_aqi_100=[]
    time_aqi_100=[]
    for i in range(1,len(storage_aqi_100["feeds"])):
        x=(storage_aqi_100["feeds"][i]["field1"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_aqi_100["feeds"][(len(storage_aqi_100["feeds"])-1)]["created_at"])
        y_time=(storage_aqi_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_aqi_100.append(float(x))
            time_aqi_100.append(minutes)
    return(mylist_aqi_100,time_aqi_100)
def charts_temp():
    threading.Timer(30,charts_temp).start()
    url_temp_100='https://api.thingspeak.com/channels/1469958/fields/2.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_temp_100 = requests.get(url_temp_100)
    storage_temp_100 = response_temp_100.json()
    mylist_temp_100=[]
    time_temp_100=[]
    for i in range(1,len(storage_temp_100["feeds"])):
        x=(storage_temp_100["feeds"][i]["field2"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_temp_100["feeds"][(len(storage_temp_100["feeds"])-1)]["created_at"])
        y_time=(storage_temp_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_temp_100.append(float(x))
            time_temp_100.append(minutes)
        mynewlist_temp_100 = [z for z in mylist_temp_100 if pd.isnull(z) == False]
    return(mynewlist_temp_100,time_temp_100)

def charts_temp_index():
    threading.Timer(30,charts_temp_index).start()
    url_heat_100='https://api.thingspeak.com/channels/1469958/fields/7.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_heat_100 = requests.get(url_heat_100)
    storage_heat_100 = response_heat_100.json()
    mylist_heat_100=[]
    time_heat_100=[]
    for i in range(1,len(storage_heat_100["feeds"])):
        x=(storage_heat_100["feeds"][i]["field7"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_heat_100["feeds"][(len(storage_heat_100["feeds"])-1)]["created_at"])
        y_time=(storage_heat_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_heat_100.append(float(x))
            time_heat_100.append(minutes)
    mynewlist_heat_100 = [z for z in mylist_heat_100 if pd.isnull(z) == False]
    mynewlist_heat_100 = [i for i in mynewlist_heat_100 if i != 0]
    return(mynewlist_heat_100)


def charts_pm():
    threading.Timer(30,charts_pm).start()
    url_pm_100='https://api.thingspeak.com/channels/1469958/fields/8.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_pm_100 = requests.get(url_pm_100)
    storage_pm_100 = response_pm_100.json()
    mylist_pm_100=[]
    time_pm_100=[]
    for i in range(1,len(storage_pm_100["feeds"])):
        x=(storage_pm_100["feeds"][i]["field8"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_pm_100["feeds"][(len(storage_pm_100["feeds"])-1)]["created_at"])
        y_time=(storage_pm_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None):
            mylist_pm_100.append(float(x))
            time_pm_100.append(minutes)
    return(mylist_pm_100)

def charts_hum():
    threading.Timer(30,charts_hum).start()
    url_hum_100='https://api.thingspeak.com/channels/1469958/fields/3.json?api_key=6VZFKVYO23I7TCXP&results=100'
    response_hum_100 = requests.get(url_hum_100)
    storage_hum_100 = response_hum_100.json()
    mylist_hum_100=[]
    time_hum_100=[]
    for i in range(1,len(storage_hum_100["feeds"])):
        x=(storage_hum_100["feeds"][i]["field3"])
        my_date =datetime.utcnow()
        my_datetime=my_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentutctime= time.strptime(my_datetime, '%Y-%m-%dT%H:%M:%SZ') # Current Time in floating values
        my_currentutctime = time.mktime(currentutctime)
        y=(storage_hum_100["feeds"][(len(storage_hum_100["feeds"])-1)]["created_at"])
        y_time=(storage_hum_100["feeds"][i]["created_at"])
        d = datetime.fromisoformat(y_time[:-1])
        d_time=d.strftime('%H:%M')
        my_createdtime= time.strptime(y_time, '%Y-%m-%dT%H:%M:%SZ')
        created_time = time.mktime(my_createdtime)
        time_diff=my_currentutctime-created_time
        minutes = int((time_diff) / 60)
        if(minutes<=60*1 and x!=None and x!="nan"):
            mylist_hum_100.append(float(x))
            time_hum_100.append(minutes)
    mynewlist_hum_100 = [z for z in mylist_hum_100 if pd.isnull(z) == False]
    return(mynewlist_hum_100)
def prediction_aqi():
    url_pqi = 'https://api.thingspeak.com/channels/1408468/fields/1/last.json?api_key=C9LRRAUC90L2JW3T'
    response_pqi = requests.get(url_pqi)
    storage_pqi = response_pqi.json()
    x=storage_pqi["field1"]
    print(x)
    x=int(x)
    mylist=[]
    if(0<x<50):
        predicted_aqi="Good"
        predicted_aqi_range="1-50"
        colour_pqi="rgb(0, 255, 0);"
    elif(50<=x<100):
        predicted_aqi="Satisfactory"
        predicted_aqi_range="51-100"
        colour_pqi="rgb(255, 255, 0);"
    elif(100<=x<200):
        predicted_aqi="Moderate"
        predicted_aqi_range="101-200"
        colour_pqi="rgb(255, 165, 0);"
    elif(201<=x<300):
        predicted_aqi="Poor"
        predicted_aqi_range="201-300"
        colour_pqi="rgb(255,0, 0);"
    elif(301<=x<400):
        predicted_aqi="Very Poor"
        predicted_aqi_range="301-400"
        colour_pqi="rgb(153, 0, 0);"
    else:
        predicted_aqi="Severe"
        predicted_aqi_range="401-500"
        colour_pqi="rgb(142, 1, 17);"
    mylist.append(predicted_aqi)
    mylist.append(predicted_aqi_range)
    mylist.append(colour_pqi)

    return(mylist)


def airquality(request):
    aqi_conc()
    things()
    mylist=prediction_aqi()
    mylist_aqi_100,time_aqi_100=charts_aqi()
    mylist_temp_100,time_temp_100=charts()
    mylist_co_100,time_co_100=charts_co()
    mylist_co2_100,time_co2_100=charts_co_2()
    mylist_nh_100,time_nh_100=charts_nh_3()
    mylist_pm_100=charts_pm()
    global aircode
    context={
        "pm":pm,
        "co2":co2,
        "co":co,
        "nh":nh,
        "last":last,
        "air":aircode,
        "aqi":aqi,
        "recommend":recommend,
        "chart_temp":mylist_temp_100,
        "time_co":time_co_100,
        "chart_co":mylist_co_100,
        "chart_co2":mylist_co2_100,
        "chart_nh3":mylist_nh_100,
        "chart_aqi":mylist_aqi_100,
        "aqi_time":time_aqi_100,
        "chart_pm":mylist_pm_100,
        "predicted_aqi":mylist[0],
        "predicted_aqi_range":mylist[1],
        "colour_pqi":mylist[2],


    }

    return render(request,'aqi.html',context)


def weather(request):
    aqi_conc()
    things()
    global temp
    mylist_temp_100,time_temp_100=charts_temp()
    mylist_heat_100=charts_temp_index()
    mylist_hum_100=charts_hum()
    print(mylist_hum_100)
    now = datetime.now()
    current_hour=int(now.strftime("%H"))
    print(current_hour)
    current_time = now.strftime("%I:%M")
    current_date = now.strftime("%A, %d %B %Y")
    day_night=now.strftime("%p")
    global aircode
    temp=float(temp)
    if(current_hour>=0 and current_hour<=6):
        feel="Clear"
        image="https://images.unsplash.com/photo-1495430288918-03be19c7c485?ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8bmlnaHR8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=60"
        colour="white"
    elif(temp>=30 and current_hour>6 and current_hour <=12):
        feel="Clear"
        image="https://images.unsplash.com/photo-1609881142760-298c2e76725b?ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8Y2xvdWR5JTIwc2t5fGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=60"
        colour="black"
    elif(temp<30 and current_hour>6 and current_hour <=12):
        feel="Cloudy"
        image="https://images.unsplash.com/photo-1509023464722-18d996393ca8?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=750&q=80"
        colour="white"
    elif(temp>=30 and current_hour>12 and current_hour <15):
        feel="Sunny"
        image="https://images.unsplash.com/photo-1602798415471-595a19ef43e0?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=401&q=80"
        colour="black"
    elif(temp<30 and current_hour>12 and current_hour <15):
        feel="Partly Cloudy"
        image="https://images.unsplash.com/photo-1597621864521-93dfdb10c6b1?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1188&q=80"
        colour="black"
    elif(temp>=30 and current_hour>=15 and current_hour <=18):
        feel="Clear"
        image="https://images.unsplash.com/photo-1586866811088-9e0c914bec1a?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MzB8fHN1bm55JTIwc2t5fGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=60"
        colour="black"
    elif(temp<30 and current_hour>=15 and current_hour <=18):
        feel="Cloudy"
        image="https://images.unsplash.com/photo-1595736516846-c9fe0cb86f7c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=334&q=80"
        colour="black"
    elif(current_hour>18 and current_hour <=23):
        feel="Partly Cloudy"
        image="https://images.unsplash.com/photo-1507759709536-db5a2dadf022?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1050&q=80"
        colour="white"
    else:
        feel="Clear"
        image="https://images.unsplash.com/photo-1521303833147-3c0dc0be5816?ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8c3ByaW5nJTIwY2xpbWF0ZXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=60"
        colour="black"
    
    
    context={
        "temperature":temp,
        "humidity":hum,
        "feels":feellike,
        "time":current_time,
        "date":current_date,
        "am_pm":day_night,
        "feel":feel,
        "image":image,
        "chart_temp":mylist_temp_100,
        "time_temp":time_temp_100,
        "chart_heat":mylist_heat_100,
        "chart_hum":mylist_hum_100,
        "colour":colour,

    }
    return render(request,'weather.html',context)