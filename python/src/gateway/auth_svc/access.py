import os, requests

def login(request):
    """
    Authenticates the user login credentials and returns the response.

    Args:
        request (Request): The request object containing the user login details.

    Returns:
        tuple: A tuple containing the response text and status code if the login is successful, 
               otherwise a tuple containing None and the error response text and status code.
    """
    auth = request.authorization
    if not auth:
        return 'Could not verify your login details', 401, {'WWW-Authenticate': 'Basic realm="Login required"'}

    basicAuth = (auth.username, auth.password)
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)