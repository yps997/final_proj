from ..api.groq_api import post_groq_api


def send_to_groq_service(message):
    try:
        res = post_groq_api(message)
        return res
    except:
        return None

def check_if_about_terror(res):
    try:
        if (
            res["groq_response"]["category"]
            == "historical terror attack"
            or res["groq_response"]["category"]
            == "nowadays terror attack"
        ):
            return True
    except:
        return False
def merge_response_with_message(message):
    res = {
        "groq_response": send_to_groq_service(message),
        "title": message["title"],
        "body": message["body"]
    }
    if check_if_about_terror(res):
        return res