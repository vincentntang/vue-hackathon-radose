import pyrebase
import time
import serial
from datetime import date

config = {
  "apiKey": "AIzaSyB0FVJJS-coorTDpHi5pL4quPi_9cE_fLg",
  "authDomain": "team-zero-3a430.firebaseapp.com",
  "databaseURL": "https://team-zero-3a430.firebaseio.com",
  "storageBucket": "team-zero-3a430.appspot.com"
}

config_id = {
  "apiKey": "AIzaSyB0FVJJS-coorTDpHi5pL4quPi_9cE_fLg",
  "authDomain": "team-zero-3a430.firebaseapp.com",
  "databaseURL": "https://team-zero-3a430-2395a.firebaseio.com/",
  "storageBucket": "team-zero-3a430.appspot.com"
}


firebase = pyrebase.initialize_app(config)
firebase_id = pyrebase.initialize_app(config_id)

ser_rad = serial.Serial('COM7' , 9600)
ser_id = serial.Serial('COM6', 9600)
ser_id_exit = serial.Serial('COM19', 9600)
db = firebase.database()
db_id = firebase_id.database()

facility = "Dempster Hall"
count = 0
calculate = False
while True:
    
    raw_data = ser_rad.readline()
    
    radiation = raw_data.decode().strip('\r\n')
    cpm = float(radiation) /0.00812
    time_stamp = time.ctime()
    time_code = int(time.time())
    print(str(radiation)+" uSv/h")
    
    if ser_id.in_waiting:
        raw_id = ser_id.readline()
        id_rad = raw_id.decode().strip('\r\n')
        rec_name = db.child(id_rad).get()
        patient_name = rec_name.val()
        entry_time = time.ctime()
        data = {
            "Time of Entry" : str(time_code),
        }
        db_id.child(str(patient_name)).set(data)

    if ser_id_exit.in_waiting:
        raw_id_exit = ser_id_exit.readline()
        id_rad_exit = raw_id.decode().strip('\r\n')
        rec_name_exit = db.child(id_rad).get()
        patient_name_exit = rec_name.val()
        entry_time_exit = time.ctime()
        data = {
            "Time of Exit" : str(time_code),
        }
        db_id.child(str(patient_name)).update(data)
        calculate = True

    count = count + 1
    if count > 1:
        
        data = {
            "Facility ID" : "98765",
            "Room Number": "140 S",
            "Time Stamp" : str(time_stamp),
            "Radiation" : str(radiation)+" uSv/h",
            "CPM (Counts per Minute)" : int(cpm)
        }
        db.child(facility).child(str(time_code)).set(data)

    if calculate == True:
        TOEN = db_id.child(str(patient_name)).child("Time of Entry").shallow().get().val()
        TOEXT = db_id.child(str(patient_name)).child("Time of Exit").shallow().get().val() 
        num_of_entry = (int(TOEXT) - int(TOEN))/10
        #print(i)

        rad_array = []

        for i in range (0,int(num_of_entry)):
            
            time_get = int(TOEXT)
            temp_rad = db.child("Dempster Hall").child(str(time_get)).child("CPM (Counts per Minute)").shallow().get().val()
            rad_array.append (int(temp_rad))
            TOEXT = int(time_get) - 10
        
        total_rad = sum(rad_array)
        average_rad = total_rad / num_of_entry
        print(average_rad)
            
            
        
        calculate = False

