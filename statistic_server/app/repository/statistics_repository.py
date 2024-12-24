from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, query
from typing import Callable
from sqlalchemy import func, case, desc, distinct
from ..db.database import session_maker
from ..models import City, Country, Region, Province, Event, AttackType, TargetType, TheDate
from ..service.pandas_service import convert_to_dataframe
from ..service.queries_service import filter_and_return_all, calculate_fatal_event_score, avg_calculator
from toolz import *


def get_most_fatal_attack_type(session, limit):
    with session() as session:
        query = (
            session.query(AttackType.attack_type).join(Event, Event.attack_type_id == AttackType.id)
            .add_columns(calculate_fatal_event_score())
            .order_by(AttackType.attack_type, desc(calculate_fatal_event_score()))
        )
        if limit:
            query = query.limit(limit)
        result = query.all()
        result = [
            {"attack_type": row[0], "fatal_score": row[1]}
            for row in result
        ]
        return result


def get_mean_fatal_event_for_area(
        session: Callable[[], Session],
        limit: int = None, country: Country = None,
        province: Province = None,
        region: Region = None,
        city: City = None):
    with session() as session:
        try:
            from app.models import Province
            results = (
                session.query(
                    Country.country.label("country"),
                    Region.region.label("region"),
                    City.city.label("city"),
                    calculate_fatal_event_score(),
                    City.latitude.label("latitude"),
                    City.longitude.label("longitude")
                )
                .join(Country, Event.country_id == Country.id)
                .join(Region, Event.region_id == Region.id)
                .join(City, Event.city_id == City.id)
                # .group_by(Country.country, Region.region, City.city, City.longitude, City.latitude, Event.wound_number, Event.kill_number)
                .order_by(desc("score"))
            )
            query = filter_and_return_all(limit, country, province, region, city, result=results)
            mean_fatal = [
                {
                    "country": row.country,
                    "region": row.region,
                    "city": row.city,
                    "fatal_avg": avg_calculator(query),
                    "latitude": row.latitude,
                    "longitude": row.longitude,
                    "score": row.score
                }
                for row in query if row.longitude is not None and row.latitude is not None
            ]
            return mean_fatal
        except Exception as e:
            print(f"Error occurred while querying: {e}")


def get_most_common_terror_group_by_area(
        session: Callable[[], Session],
        limit: int = None, country: Country = None,
        province: Province = None,
        region: Region = None,
        city: City = None):
    with session() as session:
        try:
            results = (
                session.query(
                    Event.terror_group,
                    Country.country,
                    Region.region,
                    City.city,
                    City.latitude,
                    City.longitude
                )
                .join(City, Event.city_id == City.id)
                .join(Country, Event.country_id == Country.id)
                .join(Region, Event.region_id == Region.id)
                # .group_by(Event.terror_group, City.city, City.longitude, City.latitude)
                .order_by(desc(Event.terror_group))
                .distinct())

            query = filter_and_return_all(limit, country, province, region, city, result=results)
            mean_fatal = [
                {
                    "latitude": row.latitude,
                    "longitude": row.longitude,
                    "group": row.terror_group,
                    "most_groups": [row.terror_group for row in query][:6],
                }
                for row in query if row.longitude is not None and row.latitude is not None
            ]
            return mean_fatal
        except Exception as e:
            print(f"Error occurred while querying: {e}")


def get_top_terror_groups(session, limit):
    with session() as session:
        results = (
            session.query(Event.terror_group,
                          func.sum(Event.kill_number + Event.wound_number).label('total_victims'))
            .group_by(Event.terror_group)
            .order_by(desc('total_victims'))
        )
        if limit:
            query = results.limit(limit)

        all_groups = query.all()
        top_groups = [
            {"terror_group_name": row.terror_group, "total_victims": float(row.total_victims)}
            for row in all_groups
        ]
        return top_groups


def get_casualties_killers_correlation(session):
    with session() as session:
        result = (
            session.query(
                (func.coalesce(Event.kill_number, 0) + func.coalesce(Event.wound_number, 0)).label("casualties"),
                Event.killers_number
            )
            .group_by(Event.killers_number,
                      (func.coalesce(Event.kill_number, 0) + func.coalesce(Event.wound_number, 0)))
            .all()
        )
        correlation_data = [
            {"killers_number": row.killers_number, "casualties": row.casualties}
            for row in result
        ]
        return correlation_data


def get_event_percentage_change(session: Callable[[], Session],
                                limit: int = None,
                                country: Country = None,
                                province: Province = None,
                                region: Region = None,
                                city: City = None):
    with session_maker() as session:
        results = (
            session.query(
                Country.country,
                Region.region,
                City.city,
                TheDate.date,
                func.count(Event.id).label("attack_count"),
                City.longitude,
                City.latitude
            )
            .join(TheDate, Event.date_id == TheDate.id)
            .join(City, Event.city_id == City.id)
            .join(Country, Event.country_id == Country.id)
            .join(Region, Event.region_id == Region.id)
            .group_by(Country.country, City.city, Region.region, TheDate.date, City.longitude, City.latitude)
            .order_by(Region.region, TheDate.date)
        )
        query = filter_and_return_all(limit, country, province, region, city, result=results)
        return query


def get_groups_with_same_target_by_area(session: Callable[[], Session],
        limit: int = None, country: Country = None,
        province: Province = None,
        region: Region = None,
        city: City = None):
    with session() as session:
        results = (
            session.query(
                Event.terror_group,
                Country.country,
                Region.region,
                City.city,
                City.latitude,
                City.longitude,
                TargetType.target_type
            )
            .join(City, Event.city_id == City.id)
            .join(Country, Event.country_id == Country.id)
            .join(Region, Event.region_id == Region.id)
            .join(TargetType, Event.target_type_id == TargetType.id)
            .order_by(Event.terror_group)
            .distinct()
        )
        query = filter_and_return_all(limit, country, province, region, city, result=results)

        # def is_not_none(*args) -> bool:
        #     return all(x is not None for x in args)

        res = [
            {
                "target": row.target_type,
                "longitude": row.longitude,
                "latitude": row.latitude,
                "groups": list(set([subrow.terror_group for subrow in query if subrow.target_type == row.target_type]))
            }
            for row in query if row.longitude is not None and row.latitude is not None
        ]
        return res

def get_groups_with_same_attack_by_area(session: Callable[[], Session],
        limit: int = None, country: Country = None,
        province: Province = None,
        region: Region = None,
        city: City = None):
    with session() as session:
        results = (
            session.query(
                Event.terror_group,
                Country.country,
                Region.region,
                City.city,
                City.latitude,
                City.longitude,
                AttackType.attack_type
            )
            .join(City, Event.city_id == City.id)
            .join(Country, Event.country_id == Country.id)
            .join(Region, Event.region_id == Region.id)
            .join(AttackType, Event.attack_type_id == AttackType.id)
            .order_by(Event.terror_group)
            .distinct()
        )
        query = filter_and_return_all(limit, country, province, region, city, result=results)
        res = [
            {
                "attack": row.attack_type,
                "longitude": row.longitude,
                "latitude": row.latitude,
                "groups": list(set([subrow.terror_group for subrow in query if subrow.attack_type == row.attack_type]))
            }
            for row in query if row.longitude is not None and row.latitude is not None
        ]
        return res


def get_top_locations_by_unique_groups(session: Callable[[], Session],
           limit: int = None,
           country: Country = None,
           province: Province = None,
           region: Region = None,
           city: City = None):
    with session() as session:
        results = (
            session.query(
                Event.terror_group,
                City.city,
                City.latitude,
                City.longitude,
            )
            .join(City, Event.city_id == City.id)
            .join(Country, Event.country_id == Country.id)
            .join(Region, Event.region_id == Region.id)
            .order_by(Event.terror_group)
            .distinct()
        )
        query = filter_and_return_all(limit, country, province, region, city, result=results)

        res = [
            {
                "city": row.city,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "groups": list(set([subrow.terror_group for subrow in query if subrow.city == row.city]))
            }
            for row in query if row.latitude is not None and row.longitude is not None
        ]
        return res

def get_groups_in_the_same_attack(session: Callable[[], Session]):
    with session() as session:
        try:
            results = (
                session.query(
                    Event.terror_group,
                    Country.country,
                    Region.region,
                    City.city,
                    City.latitude,
                    City.longitude,
                    TargetType.target_type
                )
                .join(City, Event.city_id == City.id)
                .join(Country, Event.country_id == Country.id)
                .join(Region, Event.region_id == Region.id)
                .join(AttackType, Event.attack_type_id == AttackType.id)
                .filter(Event.target_type_id == TargetType.id, Event.city_id == City.id, Event.country_id == Country.id)
            ).all()
            df = convert_to_dataframe(results)
            grouped = df.groupby(
                ["city", "country", "region", "latitude", "longitude", "target_type"]
            )["terror_group"].apply(lambda groups: list(set(groups))).reset_index()
            result = [
                {
                    "city": row["city"],
                    "country": row["country"],
                    "region": row["region"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "target": row["target_type"],
                    "groups": row["terror_group"]
                }
                for index, row in grouped.iterrows()
            ]
            return result
        except SQLAlchemyError as e:
            print(str(e))

def get_groups_in_the_same_year_target(session: Callable[[], Session]):
    with session() as session:
        try:
            results = (
                session.query(
                    Event.terror_group,
                    TheDate.date,
                    Country.country,
                    Region.region,
                    City.city,
                    City.latitude,
                    City.longitude,
                    TargetType.target_type
                )
                .join(City, Event.city_id == City.id)
                .join(Country, Event.country_id == Country.id)
                .join(Region, Event.region_id == Region.id)
                .join(AttackType, Event.attack_type_id == AttackType.id)
                .join(TheDate, Event.date_id == TheDate.id)
                .filter(
                    Event.target_type_id == TargetType.id,
                    Event.city_id == City.id,
                    Event.country_id == Country.id,
                    TheDate.id == Event.date_id
                )
            ).all()
            df = convert_to_dataframe(results)
            import pandas as pd
            df["year"] = pd.to_datetime(df["date"]).dt.year
            grouped = df.groupby(
                ["target_type", "year"]
            )["terror_group"].apply(lambda groups: list(set(groups))).reset_index()
            result = [
                {
                    "target": row["target_type"],
                    "year": row["year"],
                    "groups": row["terror_group"]
                }
                for index, row in grouped.iterrows()
            ]
            return result
        except SQLAlchemyError as e:
            print(str(e))

# def get_attack_type_target_type_correlation(session):
#     with session() as session:
#         result = (
#             session.query(
#                 AttackType.attack_type,
#                 TargetType.target_type,
#             )
#             .join(Event, Event.attack_type_id == AttackType.id)
#             .join(TargetType, Event.target_type_id == TargetType.id)
#             .group_by(AttackType.attack_type, TargetType.target_type)
#             .all()
#         )
#         correlation_data = [
#             {"attack_type": row.attack_type, "target_type": row.target_type}
#             for row in result
#         ]
#         return correlation_data

# def get_event_percentage_change(session: Callable[[], Session],
#             start_year,
#             end_year,
#             limit: int = None,
#             country: Country = None,
#             province: Province = None,
#             region: Region = None,
#             city: City = None,
#         ):
#     with session() as session:
#         try:
#             results = (
#                 session.query(
#                     Event,
#                     Country.country,
#                     Region.region,
#                     TheDate.date,
#                     City.longitude,
#                     City.latitude,
#                     City.city,
#                 )
#                 .join(TheDate, Event.date_id == TheDate.id)
#                 .join(City, Event.city_id == City.id)
#                 .join(Country, Event.country_id == Country.id)
#                 .join(Region, Event.region_id == Region.id)
#
#             )
#             query = check_filters_and_return_all(limit, country, province, region, city, result=results)
#             start_year_counter = Counter([row.city for row in query if row.date.year == start_year])
#             end_year_counter = Counter([row.city for row in query if row.date.year == end_year])
#
#             attacks_for_start_date = start_year_counter[city.city] if city else sum(start_year_counter.values())
#             attacks_for_end_date = end_year_counter[city.city] if city else sum(end_year_counter.values())
#
#             percentage_change = (
#                 0 if attacks_for_start_date == 0 else
#                 (attacks_for_end_date - attacks_for_start_date) * 100.0 / attacks_for_start_date
#             )
#
#             res = [
#                 {
#                     "city": row.city,
#                     "longitude": row.longitude,
#                     "latitude": row.latitude,
#                     "attacks_for_start_date": start_year_counter[row.city],
#                     "attacks_for_end_date": end_year_counter[row.city],
#                     "percentage_change": percentage_change,
#                 }
#                 for row in query if row.longitude is not None and row.latitude is not None
#             ]
#             return res
#         except Exception as e:
#             print(f"Error occurred while querying: {e}")
#             return []
