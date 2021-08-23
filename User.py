import re
import json
from DataBase import DataBase
from werkzeug.datastructures import ImmutableMultiDict

from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
 
 ################## DONT FORGET TO ACCEPT NOTHING BUT THE THINGS SENT TO YOU

def length_funcfn(string):
    valid = 1<=len(string)<=25 
    if(valid):
        return {"error":False, "message":""} 
    return {"error": True, "message": "Your first name must be between 1 and 25 characters!"}

def length_funcln(string):
    valid = 1<=len(string)<=25 
    if(valid):
        return {"error":False, "message":""} 
    return {"error": True, "message": "Your last name  must be between 1 and 25 characters!"}


def email_func(email):
    print("in the email func")
    
    value = DataBase.emailExists(email)
    
    if(value["error"]):
        return {"error": True, "message":value["message"]}
     
    if(re.search(regex,email)):
        print("Valid Email")
        return {"error":False, "message":""}
       
    else:
        print("Invalid Email")
        return {"error": True, "message": "Your e-mail should look like an e-mail!"}
       


def pass_func(password):
    valid = 8<=len(password)<=20 
    if(valid):
        return {"error":False, "message":""} 
    return {"error": True, "message": "Your password length must be between 20 and 8!"}

  
#######################################################





register_model = {
    "fname": [length_funcfn],
    "lname": [length_funcln],
    "email": [email_func],
    "password":[pass_func]
}
      
def registerValidate(json_input):
    for key in register_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        else:
            for requirement in register_model[key]:                    
                value = json_input[key]
                
                if(requirement(value)["error"]):
                     return {"error":True, "message": requirement(value)["message"]}
         
                else:
                     succ = json_input["email"]
                     return {"error":False, "message": f"User registered with unique e-mail {succ}", "newpw": bcrypt.generate_password_hash(json_input["password"])}
         
#######################################################


signin_model = {
    "email": [],
    "password":[]
}

#so2al: required brdo fel signin wala la2?


def signinValidate2(json_input):
    for key in signin_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        else:
            value = DataBase.loginDB(json_input)

            if(value["error"]):
                return {"error": True, "message": value["message"]}
     
    return {"error":False, "message":""}



def signinValidate(json_input):
     for key in signin_model:
        if(key not in json_input and key != "rides"):
            return {"error": True, "message": f"{key} not found"}
        else:
                value = DataBase.loginDB(json_input)
                
                if value["error"]:
                         return  {"error":True, "message":value["message"]}
                else:
                    if bcrypt.check_password_hash(value["pass"], json_input["password"]):                   
                        return  {"error":False, "message": "Logged in seccessfully"}
                    return {"error": True, "message": "password is incorrect!"}
     
     return  {"error":True, "message": "Email does not exist"}
     
    # succ = json_input["email"]
     #return {"error":False, "message": f"User logged in with unique e-mail {succ}", "newpw": bcrypt.generate_password_hash(json_input["password"])}
     

#######################################################

passwordChange_model = {
    "email":[],
    "password": [pass_func],
    "newpassword":[pass_func]
}


def changePassword(json_input):
    for key in passwordChange_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        else:
            for requirement in passwordChange_model[key]:                    
                value = json_input[key]
                if(requirement(value)["error"]):
                    return  requirement(value)
                else:                    
                    value = DataBase.loginDB(json_input)
                    if value["error"]:
                         return  {"error":False, "message":value["message"]}
                    else:
                        if bcrypt.check_password_hash(value["pass"], json_input["password"]):
                            #password is correct
                            newpw = {"newpw":bcrypt.generate_password_hash(json_input["newpassword"])}
                            changeIT = DataBase.changePW(json_input, newpw)
                            
                            if changeIT["error"]:    
                                return  {"error":True, "message": changeIT["message"]}  
                            return  {"error":False, "message": "Password changed successfully"}
                        return {"error": True, "message": "passwords do not match"}
     
        
    return {"error":False, "message":""}
 ######################################################
             
emailCheck_model = {
    "email":[email_func]
}

 
def emailCheck(json_input):
    for key in emailCheck_model:
        if(key not in json_input):
            return {"error": True, "message": "E-mail not found"}
        else:
            value = DataBase.checkEmail(json_input)
            if(value["error"]):
                return {"error": True, "message": "E-mail is taken!"}
            return {"error": False, "message": ""}
                

def getNumbers(json_input):
    value = DataBase.getnum(json_input)
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}
    



   
def validNumber(phone_number):
    if len(phone_number) != 11:
        return {"error": True, "message": "This doesn't look like a phone number"}
    #for i in range(12):
       # if i in [3,7]:
       #     if phone_number[i] != '-':
      #          return {"error": True, "message": "This doesn't look like a phone number"}
     #   elif not phone_number[i].isalnum():
    #        return {"error": True, "message": "This doesn't look like a phone number"}
    return {"error": False, "message": ""}
                


phoneCheck_model = {
    "numbers":[validNumber]
}
                
     

    
def addNum(json_input):
    for key in phoneCheck_model:
        for requirement in phoneCheck_model[key]:
                      
            value = json_input[key]
            
            if(requirement(value)["error"]):
                return  requirement(value)
            
        value = DataBase.addRaqam(json_input)
        
        if(value["error"]):
            return {"error": True, "message": value["message"]}
    
    return {"error": False, "message": "DONE THANK GOD!"}
    

def validEmail(email):
    if(re.search(regex,email["email"])):
        print("Valid Email")
        return {"error":False, "message":""}
       
    else:
        print("Invalid Email")
        return {"error": True, "message": "Your e-mail should look like an e-mail!"}


#_______________________________________________
#_______________________________________________


editNumber_model = {
    "numbers":[validNumber],
    "numbers2":[validNumber],
    "email":[]
}
    

def editNum(json_input):
    for key in editNumber_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        else:
            for requirement in editNumber_model[key]:                    
                value = json_input[key]
                if(requirement(value)["error"]):
                    return  requirement(value)
                else:
                    value = DataBase.editNumber(json_input)
                    if(value["error"]):
                        return {"error": True, "message": value["message"]}
                    return {"error":False, "message":""}
    return {"error":False, "message":""}


removeNumber_model = {
    "numbers":[validNumber],
    "email":[]
}

def removeNum(json_input):
    for key in removeNumber_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        else:
            value = DataBase.removeNumber(json_input)
            if(value["error"]):
                return {"error": True, "message": value["message"]}
            return {"error":False, "message":""}
    return {"error":False, "message":""}

#_______________________________________________
#_______________________________________________

createRide_model = {
    "email",
    "history",
    "startDate",
    "endDate",
    "startTime",
    "endTime"
}


def createRideDB(json_input):
    for key in createRide_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        else:
            value = DataBase.createRideNOW(json_input)
            if(value["error"]):
                return {"error": True, "message": value["message"]}
            return {"error":False, "message":""}
    return {"error":False, "message":""}


def getRides(email):
    value = DataBase.getRidesDB(email)
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}


updateBikeID_model = {
    "email",
    "bikeID"
}


def bikeID(json_string):
    for key in updateBikeID_model:
        if(key not in json_string):
            return {"error": True, "message": f"{key} not found"}
        else:
            value = DataBase.updateBikeID(json_string)
            if(value["error"]):
                return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}
    
updateTempBikeID_model = {
    "email",
    "tempBikeID"
}
def tempBikeID(json_string):
    for key in updateTempBikeID_model:
        if(key not in json_string):
            return {"error": True, "message": f"{key} not found"}
        else:
            value = DataBase.updateTempBikeID(json_string)
            if(value["error"]):
                return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}


removeBikeID_model = {
    "email"
}

def remBikeID(json_string):
    for key in removeBikeID_model:
        if(key not in json_string):
            return {"error": True, "message": f"{key} not found"}
        else:
            value = DataBase.removeBikeID(json_string)
            if(value["error"]):
                return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}
    




def getCommand(json_input):
    value = DataBase.getcmd(json_input)
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}
    

removeRide_model = {
    "email",
    "rideNo"
}


def removeRideDB(json_input):
    for key in removeRide_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        
    value = DataBase.removeRideNOW(json_input)
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    return {"error":False, "message":value["message"]}



def getUserBike(json_input):
    value = DataBase.getUserB(json_input)
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}



    
def getUserTempBike(json_input):
    value = DataBase.getUserTempB(json_input)
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}

#____________________________________________________________
#____________________FORGOT PASSWORD STUFF___________________

def forgotPassword(json_string, code):
    for key in emailCheck_model:
        if(key not in json_string):
            return {"error": True, "message": f"{key} not found"}
        else:
           # code = bcrypt.generate_password_hash(code)
            code = bcrypt.generate_password_hash(code)
            
            value = DataBase.forgotPassWord(json_string, code)
            if(value["error"]):
                return {"error": True, "message": value["message"]}
    #return {value["lool"]}
    return {"error": False, "message": value["message"]}
       

def removeCode(json_input):
    for key in emailCheck_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        
    value = DataBase.removeCodeNOW(json_input)
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    return {"error":False, "message":value["message"]}


codeCheck_model = {
    "email":[email_func],
    "code":[]
}



def checkCode(json_input):
    for key in codeCheck_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        
    value = DataBase.checkCodeNOW(json_input)
    
    if(value["error"]):
        return {"error": True, "message": value["message"]}
    else:
        if(value["code"] == ""):
            return {"error":True, "message":"You have not requested a code yet!"}
        else:
            if bcrypt.check_password_hash(value["code"], json_input["code"]):
                #DataBase.removeCodeNOW(json_input)
                return {"error":False, "message":"DONE!!"}
            else:
                return {"error":True, "message":"The code is  incorrect, recheck your email!"}
            


changePwEz_model = {
    "email": [],
    "newpassword":[pass_func]
}


def changePwEz(json_input):
    for key in changePwEz_model:
        if(key not in json_input):
            return {"error": True, "message": f"{key} not found"}
        
        newpw = {"newpw":bcrypt.generate_password_hash(json_input["newpassword"])}
        changeIT = DataBase.changePW(json_input, newpw)
                            
        if changeIT["error"]:    
            return  {"error":False, "message": changeIT["message"]}  
        return  {"error":False, "message": "Password changed successfully"}
    