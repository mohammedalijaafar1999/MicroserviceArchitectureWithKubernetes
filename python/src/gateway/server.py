import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config['MONGO_URI'] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")
)
channel = connection.channel()

@server.route('/login', methods=['POST'])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

@server.route('/upload', methods=['POST'])
def upload():
    """
    Route for uploading a file.
    
    This function is responsible for handling the HTTP POST request to upload a file. It validates the user's access token, checks if the user has admin privileges, and then uploads the file to the specified location. If the upload is successful, it returns a success message with a status code of 200. If the user is not authorized or if there is an error with the upload, it returns an appropriate error message with the corresponding status code.
    
    Parameters:
    - None
    
    Returns:
    - If the upload is successful, it returns a success message with a status code of 200.
    - If the user is not authorized, it returns an error message with a status code of 403.
    - If there is an error with the upload, it returns an error message with a status code of 400.
    """
    access, err = validate.token(request)
    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Only one file at a time", 400
        
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)
            
            if err:
                return err

        return "File uploaded", 200
    else:
        return "Not authorized", 403
    
@server.route('/download', methods=['GET'])
def download():
    pass

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8080)