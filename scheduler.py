import deliver
import schedule
import time
from datetime import datetime, timezone
import userlist
import pytz
import json

def sched():
    
    nowt = datetime.now
    for x in range(0, len(userlist.read())):
        try:
            usr = userlist.loadUser(userlist.read()[x]['phone'])
            t = usr.time
            if t == '':
                t = '06:30'
            tz = pytz.timezone(usr.timezone)
            localt = str(nowt(tz).strftime("%H:%M"))
            
            if t == localt:
                deliver.sendWeather(usr.phone)
            
        except Exception as e:
            err = nowt(pytz.timezone('America/New_York')).strftime("%b %d at %I:%M%p: User: {} {} {}: ").format(usr.phone, usr.first, usr.last) + str(e)
            print (err)
            with open('logs/errors.json', 'a', encoding = 'utf-8') as f:
                json.dump(err, f, ensure_ascii = False, indent=4)
                f.write('\n')
            
schedule.every().minute.at(":00").do(sched)

while True:
    schedule.run_pending()
    time.sleep(1)
