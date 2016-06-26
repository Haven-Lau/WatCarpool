from datetime import datetime
from datetime import date
#from geotext import GeoText  
#import geograpy
import parsedatetime as pdt
import os
import sys
import re
import loc_scan

weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
nextdays = ['today', 'tomorrow', 'tonight']

entry1 = {
      "message": '''
      Driving Richmond Hill -> Waterloo Sunday 4pm
$15 - Richmond Hill, Ontario
'''
      ,"updated_time": "2016-06-25T23:33:21+0000","id": "372772186164295_1023771491064358"
}

cal = pdt.Calendar()
now = datetime.now()

weekday_date = None
nextday_date = None
message_date = None

# Sanitize 'ish' that people sometimes like to use
raw_message = entry1["message"].lower().replace("ish", "")

#places = GeoText(titled_message)
#url = 'http://www.bbc.com/news/world-europe-26919928'
#places = geograpy.get_place_context(text=entry1['message'])

time_string = entry1["updated_time"]
time_string = time_string[:10]+' '+time_string[11:-5]
message_time = cal.parseDT(time_string, now)[0]
message_time = message_time.replace(hour=(message_time.hour-5))
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
print("Final date:\t%s" % (final_datetime))

# Location Scan
loc_scan.location_scan(entry1["message"])
