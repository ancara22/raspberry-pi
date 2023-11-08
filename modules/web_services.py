import requests
import os

#Send the data to the server. Image and Audio
def sendData(web_service_url, fileName, fileType):
    #If it is image, set the path
    if(fileType == "image"):
        fileName = "/home/rig/Documents/App/main/data/images/" + fileName

    #Open and read the saved file
    with open(fileName, 'rb') as data:
        files = {fileType: (data)}
        response = requests.post(web_service_url, files=files)   #Send the file, POST
        os.remove(fileName)    #Remove the file

        #Check the status
        if response.status_code == 200:
           print('Data sent successfully to the web service')
        else:
           print('Failed to send the data to the web service')
           exit()

#Send GSR data in json format
def sendGSR(data, web_service_url):
    try:
        response = requests.post(web_service_url, json={'gsr_data': data})   #Send the data

        #Check the status
        if response.status_code == 200:
            pass
        else:
            print(f'Failed to send GSR data. Status code: {response.status_code}')
    except Exception as e:
        print(f'Error while sending GSR data: {str(e)}')
    
