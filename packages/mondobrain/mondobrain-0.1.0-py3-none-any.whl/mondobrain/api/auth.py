from .requestor import APIRequestor


def auth_test(error: str = None, **kwargs):
    """Tests the ability to connect to the API
    """
    params = {}
    if error:
        params["error"] = error

    requestor = APIRequestor(**kwargs)

    return requestor.request("post", "auth.test", params=params)
