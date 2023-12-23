import pika, json

def upload(f, fs, channel, access):
    """
    Uploads a file to a specified channel using the given access credentials.

    Parameters:
        f (File): The file to upload.
        fs (FileSystem): The file system to store the uploaded file.
        channel (Channel): The channel to publish the message to.
        access (dict): The access credentials for the user.

    Returns:
        tuple: A tuple containing the response message and the status code.
               The response message is either "internal server error" if an
               error occurred, or None if the upload was successful.
               The status code is an integer representing the HTTP status code.
    """
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500
        
    messgae = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(messgae),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        fs.delete(fid)
        return "internal server error", 500