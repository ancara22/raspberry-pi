import requests
import os


def sendData(web_service_url, fileName, fileType):
    if(fileType == "image"):
        fileName = "/home/rig/Documents/App/main/images/" + fileName


    with open(fileName, 'rb') as data:
        files = {fileType: (data)}
        response = requests.post(web_service_url, files=files)
        os.remove(fileName)

        if response.status_code == 200:
           print('Data sent successfully to the web service')
        else:
           print('Failed to send the data to the web service')
           exit()



def sendGSR(data, web_service_url):
    try:
        response = requests.post(web_service_url, json={'gsr_data': data})

        if response.status_code == 200:
            pass
        else:
            print(f'Failed to send GSR data. Status code: {response.status_code}')
    except Exception as e:
        print(f'Error while sending GSR data: {str(e)}')
    
