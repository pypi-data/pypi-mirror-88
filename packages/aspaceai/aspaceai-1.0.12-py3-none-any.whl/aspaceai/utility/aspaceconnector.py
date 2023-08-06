import requests



def createJSONPostRequest(aspace_url,json_payload):
    headers = {
        'Content-Type': 'application/json'
    }
    aspace_response = requests.post(aspace_url,headers=headers, data = json_payload, verify=False)
    return(aspace_response)

def createMultipartPostRequest(aspace_url,file_path,json_payload):

    files = {'file': open(file_path, 'rb')}
    aspace_response = requests.post(aspace_url, files=files, data=json_payload, verify=False)
    return(aspace_response)

