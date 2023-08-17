import subprocess

#using check_output to retrieve the required data
devices = subprocess.check_output(['netsh','wlan','show','network','mode=BSSID'])

#decoding it to string
devices = devices.decode('ascii')
devices = devices.replace("\r","")
  
#recording decoded data in text file
file = open('Wifi_info.txt','w')
file.write(devices)
file.close()
