def normalize_data(message):
    data = {
        "city": message["groq_response"]["city"] if not None else None,
        "country": message["groq_response"]["country"] if not None else None,
        "latitude": message["groq_response"]["latitude"] if not None else None,
        "longitude": message["groq_response"]["longitude"] if not None else None,
        "description": message["body"] if not None else None,
        "date": message["groq_response"]["date"] if not None else None,
    }
    return data
