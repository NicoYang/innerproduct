# -*- coding: utf-8 -*-
import os
import sys
import re
import requests
import datetime

from flask import Flask, request, g, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# configuration
app.config['MONGO_URI'] = os.environ['MONGODB_URI']

# connect to the database
mongo = PyMongo(app)

# handle http status code
@app.errorhandler(400)
def method_400(exception):
    return "",404

@app.errorhandler(404)
def method_404(exception):
    return "",404

@app.errorhandler(405)
def method_405(exception):
    return "",404

@app.errorhandler(500)
def method_500(exception):
    return "",404

# add db connection for each request
@app.before_request
def before_request():
    g.mongo = mongo

@app.route('/info', methods=['GET'])
def info():
    reqLog = g.mongo.db.reqLog
    reqNum = reqLog.find().count()
    errNum = reqLog.find({"reqState":0},{}).count()
    responseData = { "number_of_requests": { "innerproduct": reqNum}, "number_of_errors": { "innerproduct": errNum } }
    return jsonify(responseData), 200

@app.route('/innerproduct', methods=['POST'])
def innerproduct():
    inputData = request.get_json()
    # initiate related attributes
    responseData = { "error": { "type": "format error" } }
    reqState = 0
    nowTime = datetime.datetime.now()
    nowT = nowTime.strftime('%Y-%m-%d %H:%M:%S')
    reqLog = g.mongo.db.reqLog
    if inputData is not None:
        if "x" in inputData and "y" in inputData:
            xArray = inputData["x"]
            yArray = inputData["y"]
            checkResult = checkArray(xArray,yArray)
            if checkResult:
                responseData = {"xTy": innProduct(xArray,yArray)}
                reqState = 1
    reqLog.insert({"reqTime":nowT,"reqResult":responseData,"reqState":reqState})
    
    return jsonify(responseData),200

def checkArray(xArray,yArray):
# check if these two array fulfill the requirements
    # check if array contains numbers
    checkX = all(isinstance(n, int) for n in xArray)
    checkY = all(isinstance(n, int) for n in yArray)
    if checkX == True and checkY == True:
        lenX = len(xArray)
        lenY = len(yArray)
        # check if the length of arrays fulfill the requirements
        if 1 <= lenX <=50 and lenX == lenY:
            return True
    return False

def innProduct(xArray,yArray):
    lenX = len(xArray)
    innResult = 0
    # start calculation
    for i in range(lenX):
        innResult = innResult + (xArray[i]*yArray[i])
    return innResult

if __name__ == '__main__':
	app.run(debug=False)