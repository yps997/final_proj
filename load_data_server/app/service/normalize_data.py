from datetime import date

from ..models import TheDate, City, Country, Region, Province, TargetType, AttackType, Event
from ..utils.normalize_utils import normalize_number


def normalize_date(message):
    year = int(message.get('iyear', 0))
    month = int(message["imonth"]) if int(message["imonth"]) > 0 else 1
    day = int(message["iday"]) if int(message["iday"]) > 0 else 1
    the_date = date(year,month,day)
    return {
        "date": the_date
    }

def normalize_city(message):
    return {
        "city": message['city'] if message['city'] else "Unknown",
        "longitude": float(message['longitude']) if message['longitude'] else None,
        "latitude": float(message['latitude']) if message['latitude'] else None,
    }



def normalize_event(message):
    return {
        "kill_number": float(message['nkill'] if message['nkill'] else 0),
        "wound_number": float(message['nwound'] if message['nwound'] else 0),
        "terror_group": message['gname'] if message['gname'] else "Unknown",
        "killers_number": normalize_number(message['nperps']),
        "is_suicide": bool(int(message['suicide']) if message['suicide'] else False),
        "summary": message['summary'] if message['summary'] else None,
    }


def normalized_message_to_model(message):
    normalized_message = normalize_message(message)

    the_date = TheDate(date=normalized_message['date']['date'])
    city = City(
        city=normalized_message['city']['city'],
        longitude=normalized_message['city']['longitude'],
        latitude=normalized_message['city']['latitude'],
    )
    country = Country(country=normalized_message['country'])
    region = Region(region=normalized_message['region'])
    province = Province(province=normalized_message['province'])
    target_type = TargetType(target_type=normalized_message['target_type'])
    attack_type = AttackType(attack_type=normalized_message['attack_type'])

    event = Event(
        kill_number=normalized_message['event']['kill_number'],
        wound_number=normalized_message['event']['wound_number'],
        terror_group=normalized_message['event']['terror_group'],
        killers_number=normalized_message['event']['killers_number'],
        is_suicide=normalized_message['event']['is_suicide'],
        summary=normalized_message['event']['summary'],
        date=the_date,
        city=city,
        country=country,
        region=region,
        province=province,
        target_type=target_type,
        attack_type=attack_type,
    )
    return event


def normalize_message(message):
    return {
        "date": normalize_date(message),
        "city": normalize_city(message),
        "country": message['country_txt'],
        "region": message['region_txt'],
        "province": message['provstate'],
        "event": normalize_event(message),
        "target_type": message['targtype1_txt'],
        "attack_type": message['attacktype1_txt'],
    }


def normalize_data_for_elastic(row):
    data = {
        "city": row["city"] if not None else None,
        "country": row["country_txt"] if not None else None,
        "latitude": row["latitude"] if not None else None,
        "longitude": row["longitude"] if not None else None,
        "description": row["summary"] if not None else None,
        "date": normalize_date(row)["date"]
    }
    return data