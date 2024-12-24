import webbrowser

from flask import Blueprint, request, jsonify

from ..db.database import session_maker
from ..repository.elastic_statistics import search_multiple_indexes_fuzzy, search_news_fuzzy, search_historic_fuzzy, \
    search_combined_with_date_fuzzy
from ..repository.statistics_repository import get_most_fatal_attack_type, get_mean_fatal_event_for_area, \
    get_most_common_terror_group_by_area, get_event_percentage_change, get_casualties_killers_correlation, \
    get_groups_with_same_target_by_area, get_groups_with_same_attack_by_area, get_top_locations_by_unique_groups, \
    get_groups_in_the_same_attack, get_groups_in_the_same_year_target
from ..service.maps_service import map_for_get_mean_fatal_event_for_country, map_for_most_common_terror_group_by_area, \
    map_for_event_percentage_change, map_for_groups_to_one_target_by_area, map_for_max_unique_groups_by_area, \
    map_for_groups_to_one_attack_by_area, map_for_search_in_elastic
from ..service.pandas_service import calculate_correlation_from_results, calculate_percentage_change_attacks_by_region

terror_data_blueprint = Blueprint("t_data", __name__)


@terror_data_blueprint.route("/most_fatal_attack/<int:limit>", methods=['GET'])
def get_most_fatal_attack(limit):
    try:
        res = get_most_fatal_attack_type(session=session_maker, limit=limit)

        return jsonify(res), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/mean_fatal_event", methods=['POST'])
def map_get_mean_fatal_event_for_area():
    try:
        data = request.get_json()
        res = get_mean_fatal_event_for_area(
            session=session_maker,
            limit=data.get("limit"),
            country=data.get("country"),
            province=data.get("province"),
            region=data.get("region"),
            city=data.get("city"),
        )
        return jsonify({
            "result": res,
            "map": map_for_get_mean_fatal_event_for_country(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/most_common_group", methods=['POST'])
def map_most_common_group_for_area():
    try:
        data = request.get_json()
        res = get_most_common_terror_group_by_area(
            session=session_maker,
            limit=data.get("limit"),
            country=data.get("country"),
            province=data.get("province"),
            region=data.get("region"),
            city=data.get("city"),
        )
        return jsonify({
            "result": res,
            "map": map_for_most_common_terror_group_by_area(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/event_percentage_change", methods=['POST'])
def map_event_percentage_change():
    try:
        data = request.get_json()
        res = get_event_percentage_change(
            session=session_maker,
            limit=data.get("limit"),
            country=data.get("country"),
            province=data.get("province"),
            region=data.get("region"),
            city=data.get("city"),
        )
        res = calculate_percentage_change_attacks_by_region(res)
        return jsonify({
            "result": res,
            'map': map_for_event_percentage_change(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/casualties_killers_correlation", methods=['GET'])
def casualties_killers_correlation():
    try:
        res = get_casualties_killers_correlation(session=session_maker)
        correlation = calculate_correlation_from_results(res, res, "killers_number", "casualties")
        return jsonify(correlation), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/groups_in_the_same_attack", methods=['GET'])
def get_groups_same_attack():
    try:
        res = get_groups_in_the_same_attack(session=session_maker)
        return jsonify(res), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/groups_in_the_same_year_target", methods=['GET'])
def get_groups_same_year_target():
    try:
        res = get_groups_in_the_same_year_target(session=session_maker)
        return jsonify(res), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/groups_with_same_target", methods=['POST'])
def groups_with_same_target():
    try:
        data = request.get_json()
        res = get_groups_with_same_target_by_area(
            session=session_maker,
            limit=data.get("limit"),
            country=data.get("country"),
            province=data.get("province"),
            region=data.get("region"),
            city=data.get("city"),
        )
        return jsonify({
            "result": res,
            "map": map_for_groups_to_one_target_by_area(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/groups_with_same_attack", methods=['POST'])
def groups_with_same_attack():
    try:
        data = request.get_json()
        res = get_groups_with_same_attack_by_area(
            session=session_maker,
            limit=data.get("limit"),
            country=data.get("country"),
            province=data.get("province"),
            region=data.get("region"),
            city=data.get("city"),
        )
        return jsonify({
            "result": res,
            "map": map_for_groups_to_one_attack_by_area(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/unique_groups_for_area", methods=['POST'])
def unique_groups_for_area():
    try:
        data = request.get_json()
        res = get_top_locations_by_unique_groups(
            session=session_maker,
            limit=data.get("limit"),
            country=data.get("country"),
            province=data.get("province"),
            region=data.get("region"),
            city=data.get("city"),
        )
        return jsonify({
            "result": res,
            "map": map_for_max_unique_groups_by_area(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@terror_data_blueprint.route("/search_in_elastic", methods=['POST'])
def search_in_elastic():
    try:
        data = request.get_json()
        res = search_multiple_indexes_fuzzy(
            limit=data.get("limit"),
            keyword=data.get("keyword"),
        )
        return jsonify({
            "result": res,
            "map": map_for_search_in_elastic(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))

@terror_data_blueprint.route("/search_in_elastic_new", methods=['POST'])
def search_in_elastic_new():
    try:
        data = request.get_json()
        res = search_news_fuzzy(
            limit=data.get("limit"),
            keyword=data.get("keyword"),
        )
        return jsonify({
            "result": res,
            "map": map_for_search_in_elastic(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))

@terror_data_blueprint.route("/search_in_elastic_historic", methods=['POST'])
def search_in_elastic_historic():
    try:
        data = request.get_json()
        res = search_historic_fuzzy(
            limit=data.get("limit"),
            keyword=data.get("keyword"),
        )
        return jsonify({
            "result": res,
            "map": map_for_search_in_elastic(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))

@terror_data_blueprint.route("/search_in_elastic_by_dates", methods=['POST'])
def search_in_elastic_by_dates():
    try:
        data = request.get_json()
        res = search_combined_with_date_fuzzy(
            limit=data.get("limit"),
            keyword=data.get("keyword"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
        )
        return jsonify({
            "result": res,
            "map": map_for_search_in_elastic(res)._repr_html_()
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e))