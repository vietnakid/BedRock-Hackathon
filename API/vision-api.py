import requests
import base64

def detect_text(path):
    url = 'https://vision.googleapis.com/v1/images:annotate'
    key = 'AIzaSyBmLShzB8n-ykMQeOMRjc08Rk96QTfj9JI'
    _url = url + '/?key=' + key
    b64_file = base64_file(path)
    data = {
        "requests": [
            {
            "image": {
                "content": b64_file
            },
            "features": [
                {
                "type": "TEXT_DETECTION"
                }
            ]
            }
        ]
    }

    r = requests.post(_url, json = data)
    print r.json()


def base64_file(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

detect_text("/Users/trananhduc/Desktop/BedRock/crop-image.jpg")