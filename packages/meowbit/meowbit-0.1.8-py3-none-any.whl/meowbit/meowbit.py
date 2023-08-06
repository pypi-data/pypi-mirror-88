import sys, os, platform
import re
from functools import wraps
import serial.tools.list_ports as list_ports
import time
from random import randint
from .SerialCom import serialList, serialCom
from .pyboard import Pyboard, PyboardError


def func_wrap(func):
  @wraps(func)
  def f(*args, **kwargs):
    print(func, args[0].ctx)
    return func(*args, kwargs)
  return f


initCode = '''
import gc,os
gc.enable()
from meowbit import *
from meowbit import Ultrasonic as MeowUltrasonic
'''


buzzAPI = ['tone', 'note', 'rest', 'melody', 'stop']
displayAPI = ['scroll', 'show', 'pix', 'clear']
sensorAPI = ['getTemp', 'getLight', 'accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ', 'pitch', 'roll', 'gesture', 'btnValue']
screenAPI = ['refresh', 'pixel', 'setColor', 'textSize', 'text', 'textCh', 'showText', 'fill', 'clear', 'pixel', 'line', 'drawLine', 'rect', 
              'drawRect', 'triangle', 'circle', 'drawCircle', 'loadBmp', 'loadgif', 'polygon', 'drawPolygon']
ledAPI = ['on', 'off', 'toggle', 'intensity']

meowpinAPI = ['getAnalog', 'getDigital', 'read', 'setDigital', 'write', 'setAnalog', 'set_pulse_width']
ultrasonicAPI = ['distance']
neopixelAPI = ['setColor', 'setColorAll', 'setAllOff', 'setColorLight', 'update']
robotbitAPI = ['set_pwm_freq', 'set_pwm', 'pulse_width', 'servo', 'geekServo9g', 'geekServo2kg', 'motor', 'setStepper', 'stopMotor', 'motorStopAll', 'stepperDegree', 'stepperDual']

colorGesAPI = ['mode', 'read', 'ledpwm', 'led', 'distance', 'gesture']
dhtAPI = ['measure']
dht11API = ['humidity', 'temperature']
rfidAPI = ['probe','status','uuid','read','write','stop']
mp3API = ['operate', 'vol','playIndex','playName']

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class DummyClass(object):

  def __init__(self, context):
    self.ctx = context

class MeowBit():

  def _getter(self, key):
    ret = self._eval(key)
    return self.processOutput(ret)

  def _setter(self, key, value):
    self._exec('%s = %s' %(key, value))

  def __init__(self):
    self.pyb = None
    self.funcPre = {"screen.textCh": self.textChPre}
    self.createApi(buzzAPI, 'buzzer')
    self.createApi(displayAPI, 'display')
    self.createApi(sensorAPI, 'sensor')
    self.createApi(screenAPI, 'screen')
    self.createApi(ledAPI, 'led1')
    self.createApi(ledAPI, 'led2')

    self.createClass(meowpinAPI, 'MeowPin')
    self.createClass(ultrasonicAPI, 'Ultrasonic')
    self.createClass(neopixelAPI, 'NeoPixel')
    self.createClass(robotbitAPI, 'RobotBit', 'from robotbit import *')
    self.createClass(colorGesAPI, 'ColorGes')
    self.createClass(dhtAPI, 'DHTBase')
    self.createClass(dht11API, 'DHT11')
    self.createClass(rfidAPI, 'RFID')
    self.createClass(mp3API,'MP3')
    
    self.fontfd = open(os.path.join(os.path.dirname(__file__), 'font_12x16.bin'), 'rb')
    
    setattr(getattr(self, "Class_screen"), 'sync', property(
      lambda self: self.getter('screen.sync'), 
      lambda self,value: self.setter('screen.sync', value)
    ))

  def __del__(self):
    self.fontfd.close()

  def textChPre(self, args, kwargs):
    fontDict = {}
    for n in range(len(args[0])):
      unicode = ord(args[0][n])
      self.fontfd.seek(unicode*24)
      fontDict[str(unicode)] = list(bytes(self.fontfd.read(24)))

    kwargs['font'] = fontDict
    return (args, kwargs)

  def classInit(self, *args, **kwargs):
    ins = args[0]
    args = args[1:]
    importer = getattr(ins, 'importer', None)
    if importer:
      self._exec(importer)
    proxyName = "tmp_{}".format(randint(0,999))
    setattr(ins, 'proxy', proxyName)
    argCode = self._processArgs(args, kwargs)
    code = "{} = {}({})".format(proxyName, ins.namespace, argCode)
    self._exec(code)
    for n in getattr(ins, 'api', []):
      setattr(ins, n, self.makefunc(proxyName+'.'+n))

  def createClass(self, api, namespace, importer=None):
    methods = {
      'namespace': namespace,
      'proxy': None,
      'importer': importer,
      'api': api,
      '__init__': lambda *args, **kwargs: self.classInit(*args, **kwargs)
    }
    setattr(self, namespace, type(namespace, (DummyClass,), methods))

  def createApi(self, api, namespace):
    # setattr(self, namespace, DummyClass(self))
    setattr(self, "Class_%s" %namespace, type(namespace, (DummyClass,), {"getter": self._getter, "setter": self._setter}))
    setattr(self, namespace, getattr(self, "Class_%s" %namespace)(self))
    for n in api:
      f = self.makefunc(namespace+'.'+n)
      setattr(getattr(self, namespace), n, f)

  def processOutput(self, ret):
    try:
      ret = ret.decode()
      if ret.isnumeric():
        return int(ret)
      elif isfloat(ret):
        return float(ret)
      elif ret == 'True' or ret == 'true' or ret == '1':
        return True
      elif ret == 'False' or ret == 'false' or ret == '0':
        return False
      else:
        return ret
    except:
      return ret

  def _processArgs(self, args, kwargs):
    tmpArgs=""
    for n in args:
      if type(n) == str:
        tmpArgs+='"%s",' %n
      else:
        tmpArgs+=str(n)+','
    if len(kwargs):
      for key, value in kwargs.items():
        tmpArgs += '%s=%s,' %(key,value)
    return tmpArgs

  def makefunc(self, callsign):
    def f(*args, **kwargs):
      # print(callsign, args, kwargs)
      if callsign in self.funcPre:
        (args, kwargs) = self.funcPre[callsign](args, kwargs)
      argCode = self._processArgs(args, kwargs)
      code = "%s(%s)" %(callsign, argCode)
      ret = self._eval(code)
      return self.processOutput(ret)
    return f

  def _exec(self, code):
    if self.pyb:
      return self.pyb.exec_(code)
    else:
      print("Exec >>", code)

  def _eval(self, code):
    if self.pyb:
      return self.pyb.eval(code)
    else:
      print("Eval >>", code)

  def commRx(self, msg, dt):
    if msg == None and dt == -1:
      print("Error comm close")
    else:
      print(msg)
      'do port command parse'

  def connect(self, port=None, baud=115200):
    if not port:
      port = serialList()
      if len(port) == 0:
        raise Exception("Cannot find port for board")
      port = port[0]['peripheralId']
    self.comm = serialCom(self.commRx)
    self.comm.connect(port, baud)
    self.pyb = Pyboard(self.comm)
    self.comm.setPybMutex(True)
    self.pyb.enter_raw_repl()
    self.pyb.exec_(initCode)
    time.sleep(0.2)
