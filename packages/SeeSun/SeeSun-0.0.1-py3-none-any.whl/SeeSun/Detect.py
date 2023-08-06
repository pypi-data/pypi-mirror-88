class seesunObjectDetector():

    def __init__(self):

        import cv2
        import os
        from numpy import argmax

        self.path = os.path.dirname( os.path.abspath( __file__ ) )

        model_config = os.listdir(self.path+'/model_config/')
        self.cfg = self.path+'/model_config/'+[file for file in model_config if file.endswith('.cfg')][0]
        self.weights = self.path+'/model_config/'+[file for file in model_config if file.endswith('.weights')][0]

        self.model = cv2.dnn.readNetFromDarknet(self.cfg,self.weights)

        self.class_dict = {
            '천원':['장','은'],
            '만원':['장','은'],
            '책상':['개','은'],
            '의자':['개','는'],
            '선글라스':['개','는'],
            '병':['개','은'],
            '우산':['개','은'],
            '장난감':['개','은'],
            '수저':['개','는'],
            '자전거':['대','는'],
            '승용차':['대','는'],
            '오토바이':['대','는'],
            '고양이':['마리','는'],
            '개':['마리','는'],
            '사람':['명','은'],
            '트럭':['대','은'],
            '버스':['대','는'],
            '빨간 신호등':['개','은'],
            '초록 신호등':['개','은'],
            '교통표지판':['개','은']}

        self.classes = list(self.class_dict.keys())

        self.get_blob = cv2.dnn.blobFromImage
        self.argmax = argmax
        self.NMS = cv2.dnn.NMSBoxes
        return

    def detect(self,image):

        ht,wt,_ = image.shape

        blob = self.get_blob(image, 1/255,(416,416),(0,0,0),swapRB = True,crop= False)

        self.model.setInput(blob)

        output_layers_name = self.model.getUnconnectedOutLayersNames()

        layerOutputs = self.model.forward(output_layers_name)

        boxes =[]
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                score = detection[5:]
                class_id = self.argmax(score)
                confidence = score[class_id]
                if confidence > 0.3:
                    center_x = int(detection[0] * wt)
                    center_y = int(detection[1] * ht)
                    w = int(detection[2] * wt)
                    h = int(detection[3]* ht)
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    boxes.append([x,y,w,h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        indexes = self.NMS(boxes,confidences,0.5,0.4)

        if not len(indexes): return '검출된 물체가 없어요. 다시 한번 시도해주세요.'

        labels = [ str(self.classes[class_ids[idx]]) for idx in indexes.flatten()]

        obj_dict={}

        for label in labels:
            try:
                obj_dict[label]=obj_dict[label]+1

            except KeyError:
                obj_dict[label]=1

        return_str = '현재 앞에는 '
        
        for key in obj_dict.keys():
                
            return_str+=key+self.class_dict[key][1]+' '+str(obj_dict[key])+self.class_dict[key][0]+','
        
    
        return return_str[:-1]+' 있습니다.'


class seesunTextDetector():

    def __init__(self):

        import os
        import pytesseract
        import numpy as np
        import cv2
        import math
        from typing import Tuple, Union
        from deskew import determine_skew

        # pytesseract path 입력
        #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # 경로 설정 (저장 할경우)
        #self.path = os.path.dirname(os.path.abspath(__file__))
        #self.path_save_img = self.path + "/resource/ocr_orig_image/"
        #self.OrigImgPath = self.path + "/resource/ocr_orig_image/"
        #self.OcrTextPath = self.path + "/resource/ocr_result_txt"
        #self.OutTextPath = self.OcrTextPath

        self.ndarray = np.ndarray
        self.array = np.array
        self.Union = Union
        self.Tuple = Tuple
        self.radians = math.radians
        self.sin , self.cos = np.sin , np.cos
        self.getRotationMatrix2D = cv2.getRotationMatrix2D
        self.warpAffine = cv2.warpAffine
        self.cvtColor = cv2.cvtColor
        self.COLOR_BGR2GRAY = cv2.COLOR_BGR2GRAY
        self.img2str = pytesseract.image_to_string
        self.determine_skew = determine_skew

        return

    #def strTotext(self, txtname, outtext):
    #    with open(txtname + '.txt', 'w', encoding='utf-8') as f:
    #        f.write(outtext)

    #def rotate(self, image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]) -> np.ndarray:
    #    old_width, old_height = image.shape[:2]
    #    angle_radian = math.radians(angle)
    #    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    #    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    #    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    #    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    #    rot_mat[1, 2] += (width - old_width) / 2
    #    rot_mat[0, 2] += (height - old_height) / 2
    #    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

    def rotate(self, image, angle, background):
        
        old_width, old_height = image.shape[:2]
        angle_radian = self.radians(angle)
        width = abs(self.sin(angle_radian) * old_height) + abs(self.cos(angle_radian) * old_width)
        height = abs(self.sin(angle_radian) * old_width) + abs(self.cos(angle_radian) * old_height)

        image_center = tuple(self.array(image.shape[1::-1]) / 2)
        rot_mat = self.getRotationMatrix2D(image_center, angle, 1.0)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return self.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)



    def recognize(self, image):
        grayscale = self.cvtColor(image, self.COLOR_BGR2GRAY)
        angle = self.determine_skew(grayscale)
        rotated = self.rotate(image, angle, (0, 0, 0))
        rotated_gray = self.cvtColor(rotated, self.COLOR_BGR2GRAY)
        outtext = self.img2str(image=rotated_gray, lang='kor+eng',config='--psm 1 -c preserve_interword_space=1')
                                                         
        #print("OCR Extract Result")
        #print(outtext)
        return outtext
