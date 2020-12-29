import xml.etree.ElementTree as ET
import csv
import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('172.20.66.78', 1234)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

#give the station number
print("station:")
station = int(input())


# Wait for a connection and connect
sock.listen(1)
connection, client_address = sock.accept()
print('connection from', client_address)

# Receive the data
while True:
    data = connection.recv(64)
    data1=data.decode('utf-8')
            
    if data:
        print('received: ' + data1)
                
        #make an xml file from the input
        f = open("xmldata.xml", "w")
        f.write(data1)
        f.close()

        #look for data in the xml
        tree = ET.parse('xmldata.xml')
        root = tree.getroot()
        carrier = root[0].text
        print("carrier: " + carrier)
        if int(carrier) == 0:
            print('sending 1000')
            number = 1000
            connection.sendall(number.to_bytes(2, 'little'))
                
        else:
            with open('decoded_data.csv', mode='a', newline='') as decoded_data:
                dataLogging = csv.writer(decoded_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        
                with open('procesing_times_table.csv') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    line_count = 0
                    timeValue = 0

                    #read the process time required
                    for row in csv_reader:
                        if line_count == int(carrier):
                            timeValue = int(row[station])
                            line_count += 1
                        else:
                            line_count += 1
                
                print(timeValue)
                dataLogging.writerow([carrier, timeValue]) #writes the log
            #send value thru TCP
            connection.sendall(timeValue.to_bytes(2, 'little'))








