import RPi.GPIO as GPIO
import time
import serial
import sys
import Adafruit_DHT
import sqlite3
import os
import glob
import cgi
import cgitb

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

readFile = open('buttonData.txt','r')
lastData = readFile.readline(1)
#print (lastData)
readFile.close()

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0,1]

sensor = Adafruit_DHT.AM2302
pin = 27

while True:
	#===BUTTON AND POTENTIOMETER STUFF===

	input_state = GPIO.input(17)

	#print('BUTTON INFORMATION:')

	if input_state == False and lastData == '0':
		lastData = '1'
		writeFile = open('buttonData.txt','w')
		writeFile.write(lastData)
		writeFile.close()
		#print('Button Pressed')
	elif input_state == False and lastData == '1':
		#print('Button Still Pressed')
		lastData = '1'
	elif input_state == True and lastData == '1':
		lastData = '0'
		writeFile = open('buttonData.txt','w')
		writeFile.write(lastData)
		writeFile.close()
		#print('Button Not Pressed')
	elif input_state == True and lastData == '0':
		#print('Button Still Not Pressed')
		lastData = '0'
	else:
		#print('Error')
		lastData = '0'

	#print('===================')
	#print('SERIAL INFORMATION:')

	read_serial = ser.readline()
	s[0] = str(int(ser.readline(), 16))
	#print(s[0])
	#print read_serial

	writeFile = open('potentiometerData.txt','w')
	writeFile.write(s[0])
	writeFile.close()

	#===TEMPERATURE READING STUFF===

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	if humidity is not None and temperature is not None:
		conn=sqlite3.connect('/var/www/html/templog.db')
		curs=conn.cursor()

		curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temperature,))

		conn.commit()

		#for row in curs.execute("SELECT * FROM temps"):
		#	print str(row[0])+"	"+str(row[1])

		conn.close
	else:
		print "There was a temperature reading error"

	#===WEBSITE UI STUFF (tempWeb.html)===

		#==CREATE TABLE==
	conn=sqlite3.connect('/var/www/html/templog.db')
	curs=conn.cursor()

	curs.execute("SELECT * FROM temps")

	rows = curs.fetchall()

	conn.close()

	chart_table = ""

	for row in rows[:-1]:
		rowstr="['{0}',{1}],\n".format(str(row[0]),str(row[1]))
		chart_table += rowstr
	row=rows[-1]
	rowstr="['{0}',{1}]\n".format(str(row[0]),str(row[1]))
	chart_table += rowstr

	writeTemp = open('tempWeb.html','w')
	message = """
	<html>
		<head>
			<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
			<script type="text/javascript">

				google.charts.load('current', {'packages':['corechart']});
				google.charts.setOnLoadCallback(drawChart);
				function drawChart() {
					var data = google.visualization.arrayToDataTable([
						['Time','Temperature'],"""+chart_table+"""
					]);

					var options = {
						title: 'Temperature',
						curvetype: 'function',
						legend: { position: 'bottom' }
					};

					var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
					chart.draw(data, options);
				}
			</script>
		</head>
		<body>
			<h2>Temperature Chart</h2>
			<div id="chart_div" style="width:900px; height:500px;"></div>
		</body>


	</html>
	"""
	sys.stdout.flush()

	writeTemp.write(message)
	writeTemp.close()

	#Refresh Rate
	time.sleep(1)

GPIO.cleanup()
