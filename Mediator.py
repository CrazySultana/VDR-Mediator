import serial
import pynmea2
import requests
from csv import writer
import csv
from cryptography.fernet import Fernet
import json

 
# Define the serial port and baud rate 
ser = serial.Serial('COM10', 4800)  # Change 'COM1' to the appropriate serial port on your system
fields=["Sensor","Reading"] 

with open('VDRData.csv', 'w', newline='') as file:
    # creating a csv dict writer object
    writer = csv.DictWriter(file, fieldnames=fields)

    # writing headers (field names)
    writer.writeheader()
    file.close()


try: 
    while True: 
        # Read a line from the serial port 
        line = ser.readline()

        # url = 'http://localhost:3001/ship-navigation-system'
        url = 'http://localhost:3001/api/data'
        

        # I create a session
       # Session = requests.Session()
        # I get the page from witch I'm going to post the url
       # Session.get(url)


        # Print the line read from the serial port 
        print(line) 
        print(type(line))

        # Define new data to create
        my_json = line.decode('utf8')
        print(my_json)
        print('- ' * 20)


        # Encrypt Data
        key = Fernet.generate_key()
        
        # Instance the Fernet class with the key
        
        fernet = Fernet(key)
        
        # then use the Fernet class instance 
        # to encrypt the string string must
        # be encoded to byte string before encryption
        encMessage = fernet.encrypt(my_json.encode())
        

        # Open our existing CSV file in append mode
        # Create a file object for this file
        with open('VDRData.csv', 'a') as f_object:
        
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = csv.writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(["Sensor",encMessage])
        
            # Close the file object
            f_object.close()
            
        msg = pynmea2.parse(my_json)
        #print(repr(msg.sentence_type))
        print(repr(msg.data))
        
        VdrData =msg.sentence_type + " " + ' '.join(msg.data)
        #DataMsg = json.loads(V)
        print(VdrData)
        result = requests.post(url, data=VdrData, headers={'Content-Type': 'text/plain'})
        
        if result.status_code == requests.codes.ok:
            print("Request Successful")
        else:
            print ("Error")
        
        '''# Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)

        #new_data = json.loads(line)

        # The API endpoint to communicate with
        url_post = 'http://garmin1.atwebpages.com/index.html?macbook-pro-16%22-1'
    
        # A POST request to tthe API
        post_response = requests.post(url_post, data=my_json)
         post_response.raise_for_status()  # raises exception when not a 2xx response
        if post_response.status_code != 204:
            print( post_response.json() )
        
        # Print the response
        post_response_json = post_response.json()
        print(post_response_json)
        
        

        print("original string: ", my_json)
        print("encrypted string: ", encMessage)
        # Save decrypted data in a file
        '''
        

 
except KeyboardInterrupt: 
    # Close the serial port when the program is interrupted 
    ser.close() 


