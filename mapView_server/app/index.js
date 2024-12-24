
const BASE_URL = `http://localhost:5002`

const fetchData = async (additionUrl = "", method = "POST", body = {}) => {
    const response = await fetch(`${BASE_URL}/${additionUrl}`, {
        method,
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    return await response.json()
}

const setImage = async () => {
    const inputs = [
        'end-date', 'start-date', 'city',
        'country', 'region', 'province',
        'limit',
        'question',
        'key_word'
    ]
    const values = inputs.reduce((obj, id) => {
        const value = document.getElementById(id).value
        return value == '' ? obj : { ...obj, [id]: value }
    }, {})
    const selectedQuestion = values['question'];

    const apiEndpoints = {
        'avg_fatal_event': '/api/mean_fatal_event',
        'most_common_group_for_area': '/api/most_common_group',
        'event_percentage_change': '/api/event_percentage_change',
        'groups_with_same_target': '/api/groups_with_same_target',
        'groups_with_same_attack': '/api/groups_with_same_attack',
        'top_locations_by_unique_groups': '/api/unique_groups_for_area',
        'search_new_in_elastic': '/api/search_in_elastic_new',
        'search_old_in_elastic': '/api/search_in_elastic_historic',
        'search_in_elastic_by_dates': '/api/search_in_elastic_by_dates',
        'search_in_elastic': '/api/search_in_elastic'
    };

    try {
        const { map } = await fetchData(apiEndpoints[selectedQuestion], "POST", values);
        document.getElementById("map").innerHTML = map;
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("An error occurred while fetching data. Please try again.");
    }
}


