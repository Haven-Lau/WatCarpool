#from geotext import GeoText    
#import geograpy
from datetime import datetime, timedelta
from datetime import date
import parsedatetime as pdt
import os
import sys
import re
import requests
import loc_scan

weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
nextdays = ['today', 'tomorrow', 'tonight']
link = 'https://graph.facebook.com/v2.6/372772186164295/feed?access_token=EAACEdEose0cBAKLzm2QjYxZAvMxVXg15gHWldA1ZBQWSnobIsLwJtwPMMYnDiCypeNe0mCU6RNpywrm6BoQlqSZAwXRUXZA0xx2CZA7BnHRMumuG0lfFId8ajZBxkm8j0US34g21bUAwphCrtn8iI7IQhZA4ZBpQ6aEXCRc1k7d6dwZDZD'
cal = pdt.Calendar()
now = datetime.now()
breaking = False
while True:
    response = requests.get(link)
    for entry1 in response.json()['data']:

        weekday_date = None
        nextday_date = None
        message_date = None
        price = 0
        
        # Sanitize 'ish' that people sometimes like to use
        raw_message = entry1["message"].lower().replace("ish", "")

        #places = GeoText(titled_message)
        #url = 'http://www.bbc.com/news/world-europe-26919928'
        #places = geograpy.get_place_context(text=entry1['message'])

        time_string = entry1["updated_time"]
        time_string = time_string[:10]+' '+time_string[11:-5]
        message_time = cal.parseDT(time_string, now)[0]
        message_time = message_time - timedelta(hours=5)
        print "message time: "+ str(message_time)
        if now - timedelta(days=1) > message_time:
            breaking = True
            break
        #print("Post date:\t%s" % message_time)
        # Recognition precedence: Weekday == Relation > Date Time
        # Weekday scan
        for weekday in weekdays:
            if weekday in raw_message:
                raw_message = raw_message.replace(weekday,'')
                weekday_date = cal.parseDT(weekday, message_time)[0]
                message_date = weekday_date.date()
                #print ("Weekday found:\t%s\t%s" % (weekday,weekday_date))
                break

        # Relation scan
        for nextday in nextdays:
            if nextday in raw_message:
                raw_message = raw_message.replace(nextday,'')
                nextday_date = cal.parseDT(nextday, message_time)[0]
                message_date = nextday_date.date()
                #print ("Relation found:\t%s\t%s" % (nextday,nextday_date))
                break

        # Check if day matches relation
        if (nextday_date is not None and weekday_date is not None):
            if (nextday_date.date() == weekday_date.date()):
                message_date = nextday_date.date()
                print ("Relation and Weekday matches")
            else:
                print ("Relation and Weekday DO NOT MATCH!!")

        # Remaining message datetime scan
        final_datetime = cal.parseDT(raw_message, message_time)[0]
        #print("Remaining msg:\t%s\t%s" % (raw_message,final_datetime))

        if (message_date is not None):
            final_datetime = final_datetime.replace(year=message_date.year,month=message_date.month,day=message_date.day)

        # Location Scan
        location_dict = loc_scan.location_scan(entry1["message"])

        # Price 
        for entry in entry1["message"].split():
            if '$' in entry:
                price = entry


        # Outputs
        print ("Final date: %s" % (final_datetime))
        print ("From: %s" % (location_dict['From']))
        print ("To: %s" % (location_dict['To']))
        print ("Price: %s" % price)
    link = response.json()['paging']['next']
    if breaking:
        break

