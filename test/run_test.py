import requests
import os

for file in os.listdir("./test/examples"):
    path = os.path.join("./test/examples", file)


    with open(path, "rb") as xml_file:
        xml_content = xml_file.read()
        
    url = "http://127.0.0.1:5000/nfe/xml"
    files = {"xml_file": xml_content}
    response = requests.post(url, files=files)

    print("code:", response.status_code)
    print("message:", response.text)
