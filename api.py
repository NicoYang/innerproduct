# -*- coding: utf-8 -*-
import os
import sys
import re
import requests
import datetime

from flask import Flask, request, session, g, redirect, url_for, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# configuration
app.config['MONGO_URI'] = 'mongodb://test:800723bridgewell@ds031777.mlab.com:31777/heroku_5rbl3h7w?retryWrites=false'

# connect to the database
mongo = PyMongo(app)

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

@app.before_request
def before_request():
    g.mongo = mongo

@app.route('/info', methods=['GET'])
def info():
    reqLog = g.mongo.db.reqLog
    reqNum = reqLog.find().count()
    errNum = reqLog.find({"reqState":0}).count()
    responseData = { "number_of_requests": { "innerproduct": reqNum}, "number_of_errors": { "innerproduct": errNum } }
    return jsonify(responseData), 200

@app.route('/innerproduct', methods=['POST'])
def innerproduct():
    inputData = request.get_json()
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
    checkX = all(isinstance(n, int) for n in xArray)
    checkY = all(isinstance(n, int) for n in yArray)
    if checkX == True and checkY == True:
        lenX = len(xArray)
        lenY = len(yArray)
        if 1 <= lenX <=50 and lenX == lenY:
            return True
    return False

def innProduct(xArray,yArray):
    lenX = len(xArray)
    result = 0
    for i in range(lenX):
        result = result + (xArray[i]*yArray[i])
    return result

if __name__ == '__main__':
	app.run(debug=False)