import requests
import sys
import time

url = "http://localhost:8888/recognize?"

start_time = time.time()
with open(sys.argv[1], "rb") as jpg:  # "../audios/milk_cf2.jpg"

    files = {"file": jpg}
    # d = {"body": "Foo Bar"}
    req = requests.post(url, files=files)

    print(req.status_code)
    print(req.text)
end_time = time.time()
print(end_time - start_time)