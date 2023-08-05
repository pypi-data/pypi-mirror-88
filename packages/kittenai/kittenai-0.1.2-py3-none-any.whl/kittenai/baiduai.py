import requests
import json
import base64
import wave
from io import BytesIO
from random import randrange

format2aue = {
  'wav': 6,
  'pcm': 4,
  'mp3': 3
}

lang2devpid = {
  'zh': 1537,
  'far': 1936,
  'en': 1737,
  'guangdong': 1637,
  'sichuan': 1837,
}

recognizeMap = {
  'object': 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general',
  'ingredient': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/classify/ingredient',
  'plant': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant',
  'dish': 'https://aip.baidubce.com/rest/2.0/image-classify/v2/dish',
  'animal': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/animal',
  'redwine': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/redwine',
  'flower': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/flower',
  'car': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/car',
  'landmark': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/landmark'
}

ocrMap = {
  'common': 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
  'carplate': 'https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate',
  'handwriting': 'https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting',
}

class BaiduAI:

  tokens = {
    'voice': '24.432da7297b04ae007687155f38fd0d82.2592000.1610038801.282335-16328058', 
    'image': '24.a6b968667f98475058d3c2e15f303d37.2592000.1610038801.282335-16726823', 
    'write': '24.ece5c7f397e443c5c35198dd22f9071e.2592000.1610038807.282335-16440024', 
    'talk': '24.b9f5bb06cc551f1995a39349575cbe5b.2592000.1610098146.282335-16726823', 
    'face': '24.b8702b6ef40b5134edfdf355e85a735d.2592000.1610038819.282335-19745302'
    }

  def __init__(self):
    ""
    tokens = requests.get('http://download.kittenbot.cn/baiduai/tokens.json?v={}'.format(randrange(0, 99999))).json()
    self.tokens = tokens
    self.talkcache = {
      'version': '2.0',
      'session_id': '',
      'user_id': randrange(0, 99999),
      'log_id': "ROBOT_{}".format(randrange(0, 99999)),
      'rememberskill': 0
    }

  def text2speech(self, text, lang='zh', per=0, format='wav'):
    
    data ={
      'tex': text,
      'lan': lang,
      'ctp':1,
      'cuid':'kittenai',
      'tok': self.tokens['voice'],
      'per': per,
      'aue': getattr(format2aue, format, 6)
    }
    headers = {
      'Content-Type' : 'application/json; charset=UTF-8'
    }
    resp = requests.post('http://tsn.baidu.com/text2audio', headers=headers, data=data)
    if resp.headers['content-type'] == 'application/json':
      obj = resp.json()
      if obj['err_no'] != 0:
        raise RuntimeError(obj['err_detail'])
    else:
      return resp.content

  def speech2text(self, speech, format='wav', lang="zh", options={}):
    data = {
      "format": format,
      "token": self.tokens['voice'],
      "cuid": "kittenai",
      "dev_pid": getattr(lang2devpid, lang, 1537),
      "speech": base64.b64encode(speech).decode(),
      "len": len(speech)
    }
    if format == 'wav':
      wav = wave.open(BytesIO(speech))
      data['channel'] = wav.getnchannels()
      data['rate'] = wav.getframerate()
      wav.close()

    data = dict(data, **(options))
    url = "http://vop.baidu.com/server_api"
    headers = {
        'Content-Type' : 'application/json; charset=UTF-8'
    }
    resp = requests.post(url,headers=headers,data=json.dumps(data))
    obj = resp.json()
    if obj['err_no'] != 0:
      raise RuntimeError(obj['err_msg'])
    return obj['result'][0]

  def _processImage(self, image):
    data = {}
    if type(image) == str:
      data['image_type'] = 'FACE_TOKEN'
      data['image'] = image
    else:
      data['image_type'] = 'BASE64'
      data['image'] = base64.b64encode(image).decode()
    return data

  def faceOp(self, op, body):
    token = self.tokens['face']
    url = "https://aip.baidubce.com/rest/2.0/face/v3/%s?access_token=%s" %(op,token)
    headers = {
      'Content-Type' : 'application/json; charset=UTF-8'
    }
    resp = requests.post(url,headers=headers,data=body)
    result = resp.json()
    return result

  def faceDetect(self, image):
    data = self._processImage(image)
    
    obj = self.faceOp('detect', data)
    if obj['error_code'] != 0:
      raise RuntimeError(obj['error_msg'])
    return obj['result']['face_list']

  def faceAddGroup(self, image, group, name):
    data = self._processImage(image)
    data['group_id'] = group
    data['user_id'] = name
    obj = self.faceOp('faceset/user/add', data)
    if obj['error_code'] != 0:
      raise RuntimeError(obj['error_msg'])
    return obj['result']

  def faceSearch(self, image, group):
    data = self._processImage(image)
    data['group_id_list'] = group
    obj = self.faceOp('search', data)
    if obj['error_code'] != 0:
      raise RuntimeError(obj['error_msg'])
    return obj['result']

  def recognizeItem(self, image, regType='object', baike=1):
    url = "%s?access_token=%s" %(recognizeMap[regType], self.tokens['image'])
    headers = {
      'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
      "image": base64.b64encode(image).decode(),
      "baike_num": baike
    }
    resp = requests.post(url,headers=headers,data=data)
    result = resp.json()
    if result.get('error_code', 0) != 0:
      raise RuntimeError(result['error_msg'])
    return result['result'][0]

  def ocrRecognize(self, image, ocrType="common"):
    url = "%s?access_token=%s" %(ocrMap[ocrType], self.tokens['image'])
    headers = {
      'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
      "image": base64.b64encode(image).decode(),
    }
    resp = requests.post(url,headers=headers,data=data)
    result = resp.json()
    if result.get('error_code', 0) != 0:
      raise RuntimeError(result['error_msg'])
    return result['words_result']

  def writepoem(self, key, idx=0):
    url = "https://aip.baidubce.com/rpc/2.0/creation/v1/poem?access_token=%s" %self.tokens['write']
    headers = {
      'Content-Type' : 'application/json; charset=UTF-8'
    }
    body = {
      "text": key,
      "index": idx,
    }

    resp = requests.post(url,headers=headers,data=json.dumps(body))
    result = resp.json()
    if result.get('error_code', 0) != 0:
      raise RuntimeError(result['error_msg'])
    return result['poem']

  def writecunlian(self, key, idx=0):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/couplets?access_token=%s" %self.tokens['write']
    headers = {
      'Content-Type' : 'application/json; charset=UTF-8'
    }
    body = {
      "text": key,
      "index": idx,
    }

    resp = requests.post(url,headers=headers,data=json.dumps(body))
    result = resp.json()
    if result.get('error_code', 0) != 0:
      raise RuntimeError(result['error_msg'])
    return result['couplets']

  def talk(self, query, skill="all"):
    req = {
      'log_id': self.talkcache['log_id'],
      'version': '2.0',
      'session_id': self.talkcache['session_id'],
      'request': {
        'query': query,
        'user_id': self.talkcache['user_id']
      }
    }
    
    if skill == 'all':
      req['service_id'] = "S22657" # kitten robot
      if self.talkcache['rememberskill']:
        req['dialog_state'] = {
          "contexts":{"SYS_REMEMBERED_SKILLS":[self.talkcache['rememberskill']]}
        }
    else:
      req['skill_ids'] = [skill]
    
    url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=%s" %self.tokens['talk']
    headers = {
      'Content-Type' : 'application/json; charset=UTF-8'
    }
    resp = requests.post(url,headers=headers,data=json.dumps(req))
    result = resp.json()
    if result.get('error_code', 0) != 0:
      raise RuntimeError(result['error_msg'])
    result = result['result']
    self.talkcache['session_id'] = result['session_id']
    success = []
    failed = []
    if len(result['response_list']):
      for n in result['response_list']:
        for m in n['action_list']:
          if m['action_id'] != 'fail_action':
            success.append((n['origin'], m['say']))
          else:
            failed.append((n['origin'], m['say']))
    if len(success):
      n = randrange(0, len(success))
      result = success[n][1]
      self.talkcache['rememberskill'] = success[n][0]
    else:
      result = failed[0][1]
      self.talkcache['rememberskill'] = failed[0][0]
    return result
