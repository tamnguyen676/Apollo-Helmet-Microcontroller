import android, time
droid = android.Android()
droid.startLocating()

while True:
 time.sleep(5)
 loc = droid.readLocation().result
 if loc == {}:
   print("Can't get current location, getting last known location")
   loc = droid.getLastKnownLocation().result
 if loc != {}:
   try:
     n = loc['gps']
   except KeyError:
     print("Can't get GPS location, using network")
     n = loc['network'] 
   la = n['latitude'] 
   lo = n['longitude']
   address = droid.geocode(la, lo).result
   print("lat: {0}, long: {1}".format(la, lo))