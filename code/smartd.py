import conf,json,time
from boltiot import Bolt,Sms
mybolt = Bolt(conf.API_KEY,conf.DEVICE_ID)
sms = Sms(conf.SID,conf.AUTH_TOKEN,conf.TO_NUMBER,conf.FROM_NUMBER)

old_state = 0     
while True:
   print("Reading value from Bolt")
   response = mybolt.digitalRead('1')
   data = json.loads(response)
   print (data)
   new_state = int(data['value'])   
   if old_state != new_state:  
   #Change in state indicates that the garage door is openend or closed
      try:
         if new_state == 1:    #value of new_state is 1 implies that garage door is open
            print("Making request to twilio to send SMS")   #sending an SMS to the TO NUMBER
            response = sms.send_sms("Garage is open")
            print ("Response received from twilio is:"+str(response))
            print ("Status of SMS at Twilio is :"+str(response.status))

         elif new_state == 0:     #value of new_state is 0 implies that garage door is closed
            print("Making request to twilio to send SMS")   #sending an sms to the TO NUMBER
            response = sms.send_sms("Garage is closed")
            print ("Response received from twilio is:"+str(response))
            print ("Status of SMS at Twilio is :"+str(response.status))

      except Exception as e:
         print("Error occured: Below are the details")
         print (e)
   old_state = new_state   #assign new_state value to the old_state for the next cycle
   time.sleep(20)     #wait for 20 seconds
