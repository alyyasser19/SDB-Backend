from routes import app
from flask import Response
from User import registerValidate

from User import signinValidate
from User import emailCheck
from User import getNumbers

from User import editNum
from User import removeNum

from User import createRideDB

from User import getUserBike
from User import getCommand

from User import removeCode


from User import remBikeID

from User import bikeID


from User import getRides

from User import validEmail

from User import forgotPassword

from User import addNum

from User import changePassword

from User import removeRideDB

from User import tempBikeID

from User import getUserTempBike

from User import checkCode

from User import changePwEz

from flask_bcrypt import Bcrypt


#from flask_mail import Mail
#, Message

import random
import string

import json

from flask import jsonify, request
import jwt
import datetime
import os
from functools import wraps
app.config['SECRET_KEY'] = os.urandom(24)


from DataBase import DataBase
db = DataBase()

bcrypt = Bcrypt(app)




#@app.route('/users/<id>', methods=['GET'])
#def getUser(id):
    #return id


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            txt = {"Action": 'Token is missing', "date": datetime.datetime.utcnow()}
  #          jsontxt = json.dumps(txt)
            jsonFile = open("log.json", 'w')
          #  jsonFile.write(jsontxt)
            jsonFile.close()

            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"])
            print(data)
        except:
            txt = {"Action": 'Token is Invalid', "date": datetime.datetime.utcnow()}
            #jsontxt = json.dumps(txt)
            jsonFile = open("log.json", 'w')
            #jsonFile.write(jsontxt)
            jsonFile.close()
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated



@app.route('/')
def welcome():
    return "Welcome to the app!"

@app.route('/users/sendemail', methods=['POST'])
def sendEmail():
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'bikeroonsApp@gmail.com'
    app.config['MAIL_PASSWORD'] = "Ll1234567"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    
  #  mail = Mail(app)

  #  msg = Message('Hello', sender = 'BikeroonsApp@gmail.com', recipients = ['lydiay711@gmail.com'])
   # msg.body = "This is the email body"
   # mail.send(msg)
    return "Sent"



@app.route('/users/register', methods=['POST'])
def createUser():
    
    val = db.emailExists(request.form)
    
    if not val["error"]:
            
        validated = registerValidate(request.form)
        
        error = validated["error"]
        message = validated["message"]
        
        if(not error):
    
            hashedpw = validated["newpw"]
            #info = {"fname": request.form['fname'], "lname": request.form['lname'], "email": request.form['email'],"password": request.form['password'],"bikeID":None,"numbers":[],"rides":[{"rideNo":0},{"history":[]},{"startDate":""},{"endDate":""},{"startTime":""},{"endTime":""}]}
            #info = {"fname": request.form['fname'], "lname": request.form['lname'], "email": request.form['email'],"password": request.form['password'],"bikeID":None,"numbers":[],"rides":[]}
            info = {"fname": request.form['fname'], "lname": request.form['lname'], "email": request.form['email'], "password": hashedpw, "bikeID":"","tempBikeID":"","numbers":[],"rides":[], "numberOfRides":0, "code":""}
            
            db.araf(info)
            
        
            #app.config['MAIL_SERVER']='smtp.gmail.com'
            #app.config['MAIL_PORT'] = 465
            #app.config['MAIL_USERNAME'] = 'bikeroonsApp@gmail.com'
            #app.config['MAIL_PASSWORD'] = "Ll1234567"
            #app.config['MAIL_USE_TLS'] = False
            #app.config['MAIL_USE_SSL'] = True
            
            #mail = Mail(app)
        
            #msg = Message('Welcome to Bikeroons!', sender = 'BikeroonsApp@gmail.com', recipients = [request.form['email']])
            #msg.body = f"We are thrilled to have you become a member of the Bikeroons community\nYour Login information is:\n\nE-mail: {request.form['email']}\nPassword: {request.form['password']} "
            #mail.send(msg)
            #return "Sent"
            
            
            
            return Response(
                response=json.dumps(message),
                
                #response=json.dumps(request.form),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({
                    "message": validated["message"]
                }),
                status=500,
                mimetype="application/json"
            )
    else:
        return Response(
                response=json.dumps({
                    "message": val["message"]
                }),
                status=500,
                mimetype="application/json"
            )



@app.route('/users/getuserbike/<email>', methods=['GET'])
def getUserbike(email):
    validated = getUserBike(email)
    
    error = validated["error"]
    #message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            #response=json.dumps(request.form),
            
            status=500,
            mimetype="application/json"
        )
    

@app.route('/users/getusertempbike/<email>', methods=['GET'])
def getUserTemBike(email):
    validated = getUserTempBike(email)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    

@app.route('/users/getcommand', methods=['GET'])
def getCMD():
    validated = getCommand(request.form)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    





@app.route('/users/updatebikeid', methods=['POST'])
def updateBikeID():
    validated = bikeID(request.form)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
@app.route('/users/updatetempbikeid', methods=['POST'])
def updateTempBikeID():
    validated = tempBikeID(request.form)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
      
    
    
@app.route('/users/nullifybikeid', methods=['POST'])
def nullifyBikeID():
    validated = remBikeID(request.form)
    
    error = validated["error"]
    message = validated["message"]
    if(not error):
        
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
    
    


# EMERGENCY NUMBERS
@app.route('/users/addnumber', methods=['POST'])
def n5alas():
    validated = addNum(request.form)
    error = validated["error"]
    message = validated["message"]
    
    if(not error):
        return Response(
            response=json.dumps(message),
            #response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
@app.route('/users/editnumber', methods=['POST'])
def editNumber():
    validated = editNum(request.form)
    error = validated["error"]
    
    if(not error):
        
        return Response(
            response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
@app.route('/users/removenumber', methods=['POST'])
def removeNumber():
    validated = removeNum(request.form)
    error = validated["error"]
    
    if(not error):
        
        return Response(
            response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
    
@app.route('/users/gimmenums/<email>', methods=['GET'])
def getEmergencyNumbers(email):
    dic = {"email":email}
    validated = getNumbers(dic)
    error = validated["error"]
    message = validated["message"]
    
    if(not error):
        
        return Response(
            response=json.dumps(message),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )

    
# EMERGENCY NUMBERS   
    
    
    

# RIDE ROUTES

    # create a new ride with (ride number, history, startDate, endDate, startTime, endTime)
@app.route('/users/createRide', methods=['POST'])
def createRide():
    #email_func
    validated = createRideDB(request.form)
    error = validated["error"]
    
    if(not error):
        return Response(
            response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
    
@app.route('/users/removeride', methods=['POST'])
def removeRide():
    #email_func
    validated = removeRideDB(request.form)
    error = validated["error"]
    
    if(not error):
        return Response(
            response=json.dumps("Ride removed! "),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
    
        
    # get all rides    
@app.route('/users/getrides/<email>', methods=['GET'])
@token_required
def getRide(email):
    #email_func
    dic = {"email":email}
    validated = getRides(dic)
    error = validated["error"]
    
    if(not error):
        return Response(
            response=json.dumps({"message":validated["message"]}),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    # get 1 ride with rideNo
    
# RIDE ROUTES



@app.route('/users/checkemail', methods=['POST'])
def checkEmail():
    #email_func
    validated = emailCheck(request.form)
    error = validated["error"]
    
    if(not error):
        return Response(
            response=json.dumps(validated["message"]),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )




@app.route('/users/emailVal', methods=['POST'])
def emailVall():
    validated = validEmail(request.form)
    error = validated["error"]
    
    if(not error):
        return Response(
            response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )

###############################################################################################
#################################### FORGOT PASSWORD STUFF ####################################

@app.route('/users/forgotpassword', methods=['POST'])
def forgotPW():
    
    letters = string.ascii_letters
    code = ''.join(random.choice(letters) for i in range(4))
           
    validated = forgotPassword(request.form, code)
    error = validated["error"]
    
    if(not error):
                 
        print(code)
        
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'bikeroonsApp@gmail.com'
        app.config['MAIL_PASSWORD'] = "Ll1234567"
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        
     #  mail = Mail(app)
    
      #  msg = Message('Code to change password', sender = 'BikeroonsApp@gmail.com', recipients = [request.form['email']])
     #   msg.body = "You have requested to change your password. To proceed with the process, enter the following code in the space provided in Bikeroons: "+code
      #  mail.send(msg)
        
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )

@app.route('/users/checkcode', methods=['POST'])
def checkcode():
    
    #bta5od email wel entered code mn el user
    
    validated = checkCode(request.form)
    error = validated["error"]
    
    if(not error):
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )


@app.route('/users/changepwez', methods=['POST'])
def changePWEZ():
    
    #bta5od email wel entered code mn el user
    
    validated = changePwEz(request.form)
    error = validated["error"]
    
    if(not error):
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )


###############################################################################################
################################## END FORGOT PASSWORD STUFF ##################################

@app.route('/users/removecode', methods=['POST'])
def removecode():
    validated = removeCode(request.form)
    error = validated["error"]
    
    if(not error):
        
        return Response(
            response=json.dumps(request.form),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    



@app.route('/users/login', methods=['POST'])
def login():
    validated = signinValidate(request.form)
    error = validated["error"]
    
    message = validated["message"]
    auth = request.form["email"]
    if(not error):
        
        token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
        txt = {"Action": 'Token was authorized', "User": auth}
        #jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        #jsonFile.write(jsontxt)
        jsonFile.close()
        return jsonify({'token': token})
        
        return Response(
            response=json.dumps(message),
            status=200,
            mimetype="application/json"
        )
    else:
        
        txt = {"Action": 'Token could not be verified'}
        #jsontxt = json.dumps(txt)
        jsonFile = open("log.json", 'w')
        #jsonFile.write(jsontxt)
        jsonFile.close()        
        
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )
    
    
    

@app.route('/users/changepw', methods=['POST'])
def changepw():
    validated = changePassword(request.form)
    error = validated["error"]
    msg = validated["message"]
    if(not error):
        
        #return "Sent"
            
        
        return Response(
            response=json.dumps("Password has changed"),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            response=json.dumps({
                "message": validated["message"]
            }),
            status=500,
            mimetype="application/json"
        )




#@app.route('/users/getspeed', methods=['GET'])
#def getSpeed():
 #   validated = loginValidate(request.form)
  #  error = validated["error"]
   # if(not error):
    #    return Response(
     #       response=json.dumps(request.form),
      #      status=200,
       #     mimetype="application/json"
        #)
    #else:
     #   return Response(
      #      response=json.dumps({
       #         "message": validated["message"]
        #    }),
         #   status=500,
         #   mimetype="application/json"
        #)