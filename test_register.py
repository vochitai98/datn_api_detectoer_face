import requests
import sys

# import cv2
# import base64

url = "http://localhost:8888/register"

# img = cv2.imread(sys.argv[1])
# string_img = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
# req = {"name" : sys.argv[2], "image": string_img}
# print(req["image"])
# res = requests.post(url, json=req)

form_data = {
    'username': 'stephen'
}

# Open the file to upload
with open(sys.argv[1], 'rb') as f:
    files = {'file': f}  # Note the key 'file' should match the key used in the Flask app for file upload

    # Send the POST request with files and form data
    res = requests.post(url, files=files, data=form_data)

print(res)