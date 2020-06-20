import json
import SNSOps as sns
import os
import CW as cw

def lambda_handler(event, context):
    print("Started process daily cost for current month")
    yesterdayTotalCost = cw.getYesterdayCostForThisMonth()
    todayTotalcost = cw.getTodayCostForThisMonth()
    lastmonthTodaycost = cw.getTodayCostForLastMonth()
    if (todayTotalcost - yesterdayTotalCost > float(os.environ['DailyBudget'])):
        todaycost =  todayTotalcost - yesterdayTotalCost
        dailybudget = os.environ['DailyBudget']
        DailyWarningMsg = 'Today cost is ' + str(todaycost) + ' which is more than the daily budge plan '  + str(dailybudget)
        print('Warning:', DailyWarningMsg)
        SNSARN = os.environ['SNSARN']
        sns.sendNotification(SNSARN, str(DailyWarningMsg))
    if (todayTotalcost > lastmonthTodaycost) and (todayTotalcost - lastmonthTodaycost)/(lastmonthTodaycost/100) > float(os.environ['MonthlyGrowthRate']):
        growthRate =os.environ['MonthlyGrowthRate']
        MonthlyGrowthRate = (todayTotalcost - lastmonthTodaycost)/(lastmonthTodaycost/100)
        GrowthRateWarningMes = 'Monthly growth Rate is ' + str(MonthlyGrowthRate) +  ' which is more than the the max growth rate ' + str(growthRate)
        SNSARN = os.environ['SNSARN']
        print('Warning:', GrowthRateWarningMes)
        sns.sendNotification(SNSARN, GrowthRateWarningMes)