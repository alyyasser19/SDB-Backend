import pymongo
from flask_bcrypt import Bcrypt
import re
import random
import string


#add ride array
#add all this to the project
# 1) login/logout/register
# 2) change password
# 3) QR code
#

bcrypt = Bcrypt()

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
 

class DataBase:

    def __init__(self):
        #client = pymongo.MongoClient(f"mongodb+srv://{Config.DB_USER}:{urllib.parse.quote(Config.DB_PASS)}@cluster0.ibr9d.mongodb.net/{Config.DB_NAME}?retryWrites=true&w=majority")
        #client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.6tb2n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.6tb2n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        
        self.db = client.users
        print("connected to the DB!")


    def araf(self,params):
        #return self.mongo.db.posts.insert(params, safe=True)
        #return {"error": True, "message": ""}
        self.db.users.insert(params)
        return {"error": False, "message": "User created!"}
    
    
    def emailExists(self,params):
        if self.db.users.find({'email': params["email"]}).limit(1).count() > 0:
            return {"error": True, "message": "This e-mail is already registered!"}
        else:
              if(re.search(regex, params["email"])):
                print("Valid Email")
                return {"error":False, "message":""}
               
              else:
                print("Invalid Email")
                return {"error": True, "message": "Your e-mail should look like an e-mail!"}
               
        return {"error": False, "message": ""}
         
            
    def loginDB(self,params):
       #hashedpw = fernet.encrypt(params['password'].encode())
       cursor1= self.db.users.find()
       for record in cursor1:
                if record['email'] == params['email']:
                    hashedpw = record["password"]
                    return {"error": False, "message": "Email found", "pass":hashedpw}     
       return {"error": True, "message": "Email not found"}



    def changePW2(self,params, newpw, oldpw):
        if self.db.users.find({'email': params['email'], 'password': oldpw['oldpw']}).limit(1).count() > 0:
            
            cursor1= self.db.users.find()
            
            for record in cursor1:
                if record['email'] == params['email'] and record["password"] == oldpw['oldpw']:
                    
                    loool = {"password":newpw['newpw']}
                    loool2 = {"$set":loool}
                        
                    self.db.users.update(record, loool2)
                    return {"error": False, "message": ""}
                else:
                    return {"error": True, "message": "Pas changed!"}
        return {"error": True, "message": "Password cannot be changed!"}




    def changePW(self,params, newpw):
       cursor1= self.db.users.find()
       for record in cursor1:
                if record['email'] == params['email']:
                    
                    self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"password": newpw["newpw"]}},upsert=True)
                   
                    return {"error": False, "message": "Password changed!"}   
       return {"error": True, "message": "Email does not exist!"}
        
        


    def checkEmail(self,params):
        cursor1= self.db.users.find()            
        for record in cursor1:            
            if record['email'] == params['email']:    
                return {"error": True, "message": ""}                
        return {"error": False, "message": ""}
        
    
    
    
    def getnum(self,params):
        cursor1= self.db.users.find()            
        for record in cursor1:   
            if record['email'] == params['email']: 
                result = record["numbers"]
                
                return {"error": False, "message":result}                
        return {"error": True, "message": "E-mail not found"}





    def addRaqam(self,params):
        cursor1= self.db.users.find()            
        for record in cursor1:
            
            if record['email'] == params['email']:
               
               target = record['numbers']
               
               isThere = False
               
               for key in target:
                   if key == params['numbers']:
                       isThere = True
                       
               if not isThere:
                      
                   target.append(params['numbers'])
                   self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"numbers": target}},upsert=True)
                   return {"error": False, "message":"Done!"}  
               else:
                   return {"error": True, "message": "Number already added!"}
                             
        return {"error": True, "message": "E-mail not found"}





    def editNumber(self,params):
        cursor1= self.db.users.find()            
        for record in cursor1:
            
            if record['email'] == params['email']:
               
               target = record['numbers']
               
               isThere = False
               
               for key in target:
                   if key == params['numbers']:
                       isThere = True
                       
               if not isThere:
                   target.remove(params["numbers2"])
                   target.append(params['numbers'])
                   self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"numbers": target}},upsert=True)
                   return {"error": False, "message":"Done!"}  
               else:
                   return {"error": True, "message": "Number already added!"}
                             
        return {"error": True, "message": "E-mail not found"}





    def removeNumber(self,params):
        cursor1= self.db.users.find()            
        for record in cursor1:
            
            if record['email'] == params['email']:
               
               target = record['numbers']
               
               isThere = False
               
               for key in target:
                   if key == params['numbers']:
                       isThere = True
                       
               if isThere:
                   target.remove(params["numbers"])
                   self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"numbers": target}},upsert=True)
                   return {"error": False, "message":"Done!"}  
               else:
                   return {"error": True, "message": "Number already removed!"}
                             
        return {"error": True, "message": "E-mail not found"}


    def createRideNOW(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:
            if record['email'] == params['email']:
               
               target = record['rides']
               size = len(target)
               rideNo = size+1
               
               newRide = [{"rideNo":rideNo}, {"history":params["history"]}, {"startDate":params["startDate"]}, {"endDate":params["endDate"]}, {"startTime":params["startTime"]}, {"endTime":params["endTime"]}]
               
               target.append(newRide)
               
               self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"rides": target}},upsert=True)
               return {"error": False, "message": "Ride successfully created"}
        else:
            return {"error": True, "message": "Email not found"}
        
              
    def getRidesDB(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:   
            if record['email'] == params['email']: 
                result = record["rides"]
                return {"error": False, "message":result}                
        return {"error": True, "message": "E-mail not found"}

    
    def updateBikeID(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:   
            if record['email'] == params['email']: 
                
                self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"bikeID": params["bikeID"]}},upsert=True)
                
                return {"error": False, "message":"Bike ID updated"}                
        return {"error": True, "message": "E-mail not found"}

    def updateTempBikeID(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:   
            if record['email'] == params['email']: 
                
                self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"tempBikeID": params["tempBikeID"]}},upsert=True)
                
                return {"error": False, "message":"Temp bike ID updated"}                
        return {"error": True, "message": "E-mail not found"}


    def removeBikeID(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:   
            if record['email'] == params['email']: 
                
                self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"bikeID": ""}},upsert=True)
                
                return {"error": False, "message":"Bike ID updated"}                
        return {"error": True, "message": "E-mail not found"}


    def removeTempBikeID(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:   
            if record['email'] == params['email']: 
                
                self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"tempBikeID": ""}},upsert=True)
                
                return {"error": False, "message":"Temp bike ID updated"}                
        return {"error": True, "message": "E-mail not found"}



    def getcmd(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:   
            if record['email'] == params['email']: 
                result = record["command"]
                return {"error": False, "message":result}                
        return {"error": True, "message": "E-mail not found"}



    def removeRideNOW(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:
            
            if record['email'] == params['email']:
               
               target = record['rides']
               
               for key in target:
                   
                   if str(key[0]) == str({'rideNo':int(params['rideNo'])}):
                       target.remove(key)
                       self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"rides": target}},upsert=True)
                       return {"error": False, "message":"Done!"}  
               else:
                    return {"error": True, "message": "Number already removed!"}
                             
        return {"error": True, "message": "E-mail not found"}

    

    def getUserB(self, params):
        #cursor1= self.db.users.find()            
        #for record in cursor1:
            
      #  if self.db.users.find({'email': params["email"]}).limit(1).count() > 0:
            
            cursor1= self.db.users.find()
            
            for record in cursor1:
                if record["email"] == params:
                    
                    result = record["bikeID"]
                    return {"error": False, "message": result}

            return {"error": True, "message": "Error"}

    
    def getUserTempB(self, mail):
        cursor1= self.db.users.find()            
        for record in cursor1:
            if record['email'] == mail: 
                result = record["tempBikeID"]
                return {"error": False, "message":result}                
        return {"error": True, "message": "E-mail not found"}
    
    
    
    def forgotPassWord(self, params, code):
        cursor1= self.db.users.find()            
        for record in cursor1:
            if record['email'] == params['email']: 
                
                #letters = string.ascii_letters
                #code = ''.join(random.choice(letters) for i in range(4))
            
                self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"code": code}},upsert=True)
               
                
                return {"error": False, "message":"Code sent successfully"}                
        return {"error": True, "message": "Code not sent"}
    
    
    
    def removeCodeNOW(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:
            
            if record['email'] == params['email']:
               
               self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"code": ""}},upsert=True)
               return {"error": False, "message":"Done!"}  
               
        return {"error": True, "message": "E-mail not found"}


    def checkCodeNOW(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:
        
            if (record['email'] == params['email']):
                
            
              # code = bcrypt.generate_password_hash(params["code"])
             #  if bcrypt.check_password_hash(record['code'], params["code"]):
    
                self.db.users.find_one_and_update({"email" : params['email']},{"$set":{"code": ""}},upsert=True)
                return {"error": False, "message":"Done!", "code":record['code']}  
               
        return {"error": True, "message": "Email not found!"}



    def getName(self, email):
        cursor1= self.db.users.find()            
        for record in cursor1:
            if record['email'] == email: 
                return {"error": False, "firstName":record["fname"], "lastName":record["lname"]}                
        return {"error": True, "message": "E-mail not found"}
    

    def getBalance(self, mail):
        cursor1= self.db.users.find()            
        for record in cursor1:
            if record['email'] == mail: 
                return {"error": False, "balance":record["balance"]}                
        return {"error": True, "message": "E-mail not found"}
    
    
    def getSharedBike(self, email):
        cursor1= self.db.users.find()            
        for record in cursor1:
            if record['email'] == email: 
                return {"error": False, "message":record["tempBikeID"]}
        return {"error": True, "message": "E-mail not found"}
    
    
  
    def addToBalance(self, params):
        cursor1= self.db.users.find()            
        for record in cursor1:
        
            if (record['bikeID'] == params['Name']):
                
              # code = bcrypt.generate_password_hash(params["code"])
             #  if bcrypt.check_password_hash(record['code'], params["code"]):
                
                if record["balance"]=="":
                    newBalance =  float(params["money"])
                else:
                    newBalance = float(record['balance']) + float(params["money"])
                    #return {"error": False, "message":newBalance}  
    
                self.db.users.find_one_and_update({"email" : record["email"]},{"$set":{"balance": newBalance}},upsert=True)
                return {"error": False, "message":record["balance"]}  
               
        return {"error": True, "message": "Bike not linked to any user!"}
    
    def __del__(self):
        self.db.close()
        
        
        