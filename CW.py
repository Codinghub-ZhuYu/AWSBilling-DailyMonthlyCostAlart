import json
import boto3
import datetime
from datetime import datetime, date, timedelta

# As cloud watch cost has a 8 hours delay, please call below function after 16:00 o'clock to get today's data correctly 
def getDatetimeOfToday():
        t = date.today()  #date类型
        dt = datetime.strptime(str(t),'%Y-%m-%d') #date转str再转datetime
        return dt

def getDatetimeOfYesterday():
        today = getDatetimeOfToday() #datetime类型当前日期
        yesterdayDateTime = today + timedelta(days = -1)
        return yesterdayDateTime

def getDatetimeOfTheDayBeforeYesterday():
        today = getDatetimeOfToday() #datetime类型当前日期
        yesterdayDateTime = today + timedelta(days = -2)
        return yesterdayDateTime
        
def getTodayDateTimeForLastMonth():
        t = date.today()  #date类型
        lastMonthSameDate =  datetime(t.year,t.month-1,t.day)
        newdt = datetime.strptime(str(lastMonthSameDate),'%Y-%m-%d %H:%M:%S') #date转str再转datetime '%Y-%m-%d %H:%M:%S
        return newdt
        
def getYesterdayDateTimeForLastMonth():
        t = getTodayDateTimeForLastMonth()  #date类型
        lastMonthSameDate = t + timedelta(days = -1)
        newdt = datetime.strptime(str(lastMonthSameDate),'%Y-%m-%d %H:%M:%S') #date转str再转datetime '%Y-%m-%d %H:%M:%S
        return newdt

def getDateBeforeYesterdayDateTimeForLastMonth():
        t = getYesterdayDateTimeForLastMonth()  #date类型
        lastMonthSameDate = t + timedelta(days = -1)
        newdt = datetime.strptime(str(lastMonthSameDate),'%Y-%m-%d %H:%M:%S') #date转str再转datetime '%Y-%m-%d %H:%M:%S
        return newdt

def getTodayCostForLastMonth():
    return getTodayCost(False)    

def getTodayCostForThisMonth():
    return getTodayCost(True)
    
def getTodayCost(currentMonth):
    client = boto3.client('cloudwatch')
    if currentMonth == True:
        StartTime= getDatetimeOfYesterday()
        EndTime = getDatetimeOfToday()
    else:
        StartTime= getYesterdayDateTimeForLastMonth()
        EndTime = getTodayDateTimeForLastMonth()
    response = client.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions = [
            {
              "Name": "Currency",
              "Value": "CNY"
            }
            ],
        StartTime= StartTime,
        EndTime = EndTime,
        Period = 86400,
        Statistics = ['Maximum']
    )
    todayCost = 0
    if (len(response['Datapoints']) == 1):
        for dp in response['Datapoints']:
            todayCost = dp['Maximum']
    print('start time ' , StartTime, 'end time' , EndTime, 'with today cost ', todayCost)
    return todayCost

def getYesterdayCostForLastMonth():
    return getYesterdayCost(False)    

def getYesterdayCostForThisMonth():
    return getYesterdayCost(True)

def getYesterdayCost(currentMonth):
    client = boto3.client('cloudwatch')
    if currentMonth == True:
        StartTime= getDatetimeOfTheDayBeforeYesterday()
        EndTime = getDatetimeOfYesterday()
    else:
        StartTime= getDateBeforeYesterdayDateTimeForLastMonth()
        EndTime = getYesterdayDateTimeForLastMonth()
    response = client.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions = [
            {
              "Name": "Currency",
              "Value": "CNY"
            }
            ],
        StartTime= StartTime,
        EndTime = EndTime,
        Period = 86400,
        Statistics = ['Maximum']
    )
    YesterdayCost = 0
    if (len(response['Datapoints']) == 1):
        for dp in response['Datapoints']:
            YesterdayCost = dp['Maximum']
    print('start time ' , StartTime, 'end time' , EndTime, 'with yesterday cost ', YesterdayCost)
    return YesterdayCost

