import os, requests

def token(request):
    """
    Tokenizes a request by extracting the authorization token from the headers and validating it.

    Args:
        request: The request object containing the headers.

    Returns:
        A tuple containing the tokenized response if the token is valid, otherwise None and a tuple
        with an error message and status code.

    Raises:
        None
    """
    if not "Authorization" in request.headers:
        return None, ("No credentials provided", 401)

    token = request.headers["Authorization"]
    if not token:
        return None, ("No credentials provided", 401)

    response = requests.post(
        f"{os.environ.get('AUTH_SVC_URL')}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)