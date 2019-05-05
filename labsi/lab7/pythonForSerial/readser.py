import time
import serial

foo = open("scriptout", "w")
ser = serial.Serial("/dev/ttyAMA0", timeout=0)

def ble(ser): 
	c=ser.read()
	if(c and (not c.isspace())):
		foo = open("scriptout", "a")
		foo.write(c)
		if(c == ';'):
			timestamp = str(time.time())
			foo.write(timestamp)
			foo.write('!')			
		foo.close()


while(1):
	ble(ser)
	time.sleep(.5)
#with open("scriptout", "rb") as fin:
#	content = json.load(fin)
#fin.close()
#with open("scriptout", "rb") as fout:
#	json.dump(content, fout, indent=1)
#fout.close()
