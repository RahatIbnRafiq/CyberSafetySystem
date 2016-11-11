'''
Created on Nov 10, 2016

@author: RahatIbnRafiq
'''

import unirest
import vinepy

class VineAPIClass:
    
    
    def __init__(self):
        self.rootPath = "C:\\Users\\RahatIbnRafiq\\workspace\\CyberSafetySystem\\"
        self.letters = ['a','b','c','d','e','f','h',
           'i','j','k','l','m','n','o',
           'p','q','r','s','t','u','v',
           'w','x','y','z']
        self.password = "123456789"
    
    
    def collectSessionKeys(self):
        keyMap = dict()
        response = None
        for c in self.letters:
            email = str(c)+"@rahat.com"
            response = unirest.post("https://community-vineapp.p.mashape.com/users/authenticate",
                      headers={
                        "X-Mashape-Key": "gxShFmp7TCmshoB0O4PP8ya9QQfcp1pKUeBjsnzWJltjpv0o7B",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json"
                      },
                      params={
                        "password": self.password,
                        "username": email
                      }
                    )
            try:
                keyMap[email] = response.body["data"]["key"]
            except Exception:
                continue
        #writing the keys to the file
        f = open(self.rootPath+"TextFiles\\vine_api_keys.txt","w")
        for email in keyMap.keys():
            f.write(str(email)+","+str(self.password)+","+str(keyMap[email])+"\n")
        f.close()
    
    
    def getVineAPIList(self):
        self.collectSessionKeys()
        vineList = []
        f = open(self.rootPath+"TextFiles\\vine_api_keys.txt","r") # getting the keys
        for line in f:
            line = line.strip()
            data = line.split(",")
            username = str(data[0])
            password = str(data[1])
            sessionid = str(data[2])
            vine = vinepy.API(username=username, password=password,session_id=sessionid) # get api for the keys
            vineList.append(vine)
        f.close()
        return vineList #return the api list
