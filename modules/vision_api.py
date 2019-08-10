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


def convert_data(resp):
    responses = resp['responses']
    result = list()
    for response in responses:
        pages = response['fullTextAnnotation']['pages']
        for page in pages:
            blocks = page['blocks']
            for block in blocks:
                bl = dict()
                boundingBox = block['boundingBox']
                bl['position'] = normalize_data(boundingBox['vertices'])
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
    return json.dumps(result)

def normalize_data(resp):
    max_x = 0
    min_x = 99999
    max_y = 0
    min_y = 99999
    result = {}
    for res in resp:
        x = res['x']
        y = res['y']
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    result['x'] = min_x
    result['y'] = min_y
    result['width'] = max_x - min_x
    result['height'] = max_y - min_y
    return result