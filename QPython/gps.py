import android, time
droid = android.Android()
droid.startLocating()
  
while True:
 time.sleep(5)
 loc = droid.readLocation().result
 if loc = {}:
   loc = getLastKnownLocation().result
 if loc != {}:
   try:
     n = loc['gps']
   except KeyError:
     n = loc['network'] 
   la = n['latitude'] 
   lo = n['longitude']
   address = droid.geocode(la, lo).result
   print("lat: {0}, long: {1}".format(la, lo)