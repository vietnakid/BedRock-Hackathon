import requests
import base64
import json

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
    return r.json()


def base64_file(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


def convert_data(json_text):
    responses = json_text['responses']
    result = list()
    for response in responses:
        pages = response['fullTextAnnotation']['pages']
        for page in pages:
            blocks = page['blocks']
            for block in blocks:
                bl = dict()
                boundingBox = block['boundingBox']
                bl['boundingBox'] = boundingBox
                paragraphs = block['paragraphs']
                _text = ""
                for paragraph in paragraphs:
                    words = paragraph['words']
                    for word in words:
                        symbols = word['symbols']
                        for symbol in symbols:
                            text = symbol['text']
                            _text = _text + text
                            if symbol.get('property') and 'detectedBreak' in symbol.get('property'):
                                _text = _text + " "
                bl['text'] = _text
                result.append(bl)
    return result