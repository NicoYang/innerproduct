# -*- coding: utf-8 -*-
"""
This is a module developed for a simple API server.

Author:
    Nico Yang

Paths:
    /innerProduct - for user, read two array and return their inner product.
    /info - for admin, return the statics of requests for innerProduct.

Other methods:
    checkArray(xArray,yArray)
    innProduct(xArray,yArray)

Database:
    MongoDB (if need, change the driver and related code to adapt for other database)
"""
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

@app.before_request
def before_request():
    """
    This is a method to initiate variables for each request.
    """
    # add db connection
    g.mongo = mongo

@app.route('/info', methods=['GET'])
def info():
    """
    This is a method for admins to get the statics of requests for innerProduct.

    Parameters:
        None

    Returns:
        The number of times the path /innerproduct/ has been called and returned with an error.
        The result is wrapped as a JSON Object with the following format: 
        { "number_of_requests": { "innerproduct": <number> }, "number_of_errors": { "innerproduct": <number> } } .
        Example: { "number_of_requests": { "innerproduct": 3 }, "number_of_errors": { "innerproduct": 1 } }
    """
    reqLog = g.mongo.db.reqLog
    # query db and count for the result
    reqNum = reqLog.find().count()
    errNum = reqLog.find({"reqState":0},{}).count()
    responseData = { "number_of_requests": { "innerproduct": reqNum}, "number_of_errors": { "innerproduct": errNum } }
    return jsonify(responseData), 200

@app.route('/innerproduct', methods=['POST'])
def innerproduct():
    """
    This is a method for users to get the inner product of two array.

    Parameters:
        A JSON Object with the following format:
        { "x": <array>, "y": <array> }
        These two array should have the same length and should contain numbers, 
        the length of the array should be at least 1 and not exceed 50 (1 <= Length <= 50).

    Returns:
        If the input does not meet the above criteria the following JSON message should be returned:
        { "error": { "type": "format error" } }
        Otherwise, return the inner product of the two vectors x and y with the following format: 
        { "xTy": <number> } .
    """
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
    # insert the result into db
    reqLog.insert({"reqTime":nowT,"reqResult":responseData,"reqState":reqState})
    
    return jsonify(responseData),200

def checkArray(xArray,yArray):
    """
    This is a method to check the two array fulfill the criteria.

    Parameters:
        xArray - the array sent by user.
        yArray - the array sent by user.
        These two array should have the same length and should contain numbers, 
        the length of the array should be at least 1 and not exceed 50 (1 <= Length <= 50).

    Returns:
        If the input does not meet the above criteria, return False.
        Otherwise, return True.
    """
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
    """
    This is a method to calculate the inner product of two array.

    Parameters:
        xArray - the array sent by user.
        yArray - the array sent by user.

    Returns:
        innResult - the inner product of two array.
    """
    lenX = len(xArray)
    innResult = 0
    # start calculation
    for i in range(lenX):
        innResult = innResult + (xArray[i]*yArray[i])
    return innResult

if __name__ == '__main__':
	app.run(debug=False)