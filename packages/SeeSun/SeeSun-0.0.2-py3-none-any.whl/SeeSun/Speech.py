class seesunSpeech():
    
    def __init__(self):
        
        import os
        import urllib
        import time
        
        self.request = urllib.request
        self.parse = urllib.parse.quote
        self.get_local = time.localtime
        self.client_id = "xuzazjwgcg"
        self.client_secret = "HAttp1kLDGPgCjcWv1vVAZFkjvsWuKtLJsFilG4t"
        self.speaker = 'nara'
        self.speed = 0
        
        try:
            from playsound import playsound
            
            self.play = playsound
            
        except ImportError as E:
            print('이거 필요해유')
            print(E)
            
        
    def tts(self,input_string):
        text = self.parse(input_string)
        data = "speaker=" + self.speaker + "&speed=" + str(self.speed) + "&text=" + text

        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = self.request.Request(url)

        request.add_header("X-NCP-APIGW-API-KEY-ID", self.client_id)
        request.add_header("X-NCP-APIGW-API-KEY", self.client_secret)

        response = self.request.urlopen(request, data=data.encode('utf-8'))

        if response.getcode() == 200:

            now = self.get_local()
            response_body = response.read()
            file_name = "%04d%02d%02d_%02d%02d%02d" % \
                        (now.tm_year, now.tm_mon, now.tm_mday,
                         now.tm_hour, now.tm_min, now.tm_sec) + "_" + \
                        self.speaker + "_" + str(self.speed) + "_"

            with open(file_name + ".mp3", 'wb') as f:
                f.write(response_body)

            self.play(file_name + ".mp3",block=False)

        else:
             print("Error Code")

    def stt(self):
        
        return
            
