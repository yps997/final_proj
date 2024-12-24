import folium
from folium.plugins import HeatMap
import matplotlib.colors as mcolors

def get_marker_color(fatal_avg, score):
    if fatal_avg - score > 0.5:
        return "green"
    elif fatal_avg - score < -0.5:
        return "red"
    else:
        return "orange"

def get_color_for_unique_groups(value, min_value, max_value):
    norm = (value - min_value) / (max_value - min_value)
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["green", "yellow", "red"])
    rgb = cmap(norm)
    return mcolors.rgb2hex(rgb)

def get_marker_color_for_percentage(percentage):

    if percentage > 0:
        return "red"
    elif percentage < 0:
        return "green"
    else:
        return "blue"


def map_for_get_mean_fatal_event_for_country(res: list):
    main_map = folium.Map(location=[0, 0], zoom_start=2)
    for loc in res:
        marker_color = get_marker_color(loc["fatal_avg"], loc["score"])
        folium.Marker(
            location=[loc["latitude"], loc["longitude"]],
            tooltip=(
                f"Country: {loc['country']},"
                f" Region: {loc['region']},"
                f" City: {loc['city']},"
                f" Fatal Avg: {loc['fatal_avg']},"
                f" Score: {loc['score']},"
            ),
            popup=f"Fatal Avg: {loc['fatal_avg']}",
            icon=folium.Icon(color=marker_color),
        ).add_to(main_map)
    main_map.save("static/mean_fatal_event.html")

    return main_map


def map_for_most_common_terror_group_by_area(res: list):
    main_map = folium.Map(location=[0, 0], zoom_start=2)
    for loc in res:
        folium.Marker(
            location=[loc["latitude"], loc["longitude"]],
            tooltip=(
                loc["group"]
            ),
            popup=f"most common terror group: {loc['most_groups']}",
            icon=folium.Icon(color="red"),
        ).add_to(main_map)
    main_map.save("static/most_common_group.html")

    return main_map


def map_for_event_percentage_change(res: list):
    main_map = folium.Map(location=[0, 0], zoom_start=2)
    for loc in res:
        folium.Marker(
            location=[loc["latitude"], loc["longitude"]],
            tooltip=(
                loc["percentage_change"]
            ),
            popup=(f"Country: {loc['country']},"
                    f" Region: {loc['region']},"
                    f" City: {loc['city']}"
            ),
            icon=folium.Icon(color=get_marker_color_for_percentage(loc["percentage_change"])),
        ).add_to(main_map)
    main_map.save("static/event_percentage_change.html")

    return main_map


def map_for_groups_to_one_target_by_area(res: list):
    main_map = folium.Map(location=[0, 0], zoom_start=2)
    max_group = max([data for data in res], key=lambda x: len(x['groups']))
    folium.Marker(
        location=[max_group["latitude"], max_group["longitude"]],
        tooltip=(
            max_group["target"]
        ),
        popup=(f"terror_groups: {max_group['groups']},"
                f" target: {max_group['target']},"
        ),
        icon=folium.Icon(color="blue"),
    ).add_to(main_map)
    main_map.save("static/groups_to_one_target.html")

    return main_map


def map_for_groups_to_one_attack_by_area(res: list):
    main_map = folium.Map(location=[0, 0], zoom_start=2)
    max_group = max([data for data in res], key=lambda x: len(x['groups']))
    folium.Marker(
        location=[max_group["latitude"], max_group["longitude"]],
        tooltip=(
            max_group["attack"]
        ),
        popup=(f"terror_groups: {max_group['groups']},"
                f" attack: {max_group['attack']},"
        ),
        icon=folium.Icon(color="blue"),
    ).add_to(main_map)
    main_map.save("static/groups_to_one_attack.html")

    return main_map


def map_for_max_unique_groups_by_area(res: list):
    main_map = folium.Map(location=[0, 0], zoom_start=2)
    max_group = max([data for data in res], key=lambda x: len(x['groups']))
    min_group = min([data for data in res], key=lambda x: len(x['groups']))
    for loc in res:
        folium.Marker(
            location=[loc["latitude"], loc["longitude"]],
            tooltip=(
                f"number of unique groups for this area: {str(len(loc['groups']))}"
            ),
            popup=(
                f"terror_groups: {loc['groups']},"
                f" city: {loc['city']},"
            ),
            icon=folium.Icon(
                color=get_color_for_unique_groups(
                    len(loc["groups"]), len(min_group["groups"]), len(max_group["groups"])
                )),
        ).add_to(main_map)
    main_map.save("static/max_unique_groups.html")
    return main_map

def map_for_search_in_elastic(res: list):
    main_map = folium.Map(location=[0, 0], zoom_start=2)
    for loc in res:
        folium.Marker(
            location=[loc["latitude"], loc["longitude"]],
            tooltip=(
                loc["city"]
            ),
            popup=(f"country: {loc['country']},"
                   f" city: {loc['city']},"
                   f" description: {loc['description']}"
                   ),
            icon=folium.Icon(color="blue"),
        ).add_to(main_map)
