# SeeSun package tree

- __\_\_init.py\_\___  
- __model_config__ 
  - model.cfg (모델 구조 파일)
  - model.weights (모델 가중치 파일)
- __Detector.py__ 
  - seesunObjectDetector (class , object)
    - detect (method) : return type =`string` 
  - seesunTextDetector (class , object)
    - recognize(method) : return type = `string` 
- __Speech.py__ 
  - seesunSpeech (class , object)
    - tts (method) : return type = `None` (audio played immediately)
    - stt (method) : return type = `string` 



### Usage



__for object detection__ 

```python
from SeeSun.Detect import seesunObjectDetector
import cv2

detector = seesunObjectDetector()

my_img = cv2.imread('path/to/image/file')
detector.detect(my_img)
```

```shell
OUT : '현재 앞에는 XX는 3개 , OO은 6대 있습니다.'
```

---

​	

__for text detection__ 

```python
from SeeSun.Detect import seesunTextDetector
import cv2

detector = seesunTextDetector()

my_img = cv2.imread('path/to/image/file')
detector.recognize(my_img)
```

```shell
OUT : '코로나 3차 대유행으로 인한 지하철 운행시간 조정 안내 ... '
```

---

​	

__for speech recognition,synthesis__ 

```python
from SeeSun.Speech import seesunSpeech

speech = seesunSpeech()

speech.tts('input_string')
speech.stt('path/to/audio_file')
```

```shell
OUT : None
```

---

