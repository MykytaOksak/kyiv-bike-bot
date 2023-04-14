import requests
from io import BytesIO
from PIL import Image
from data import DIRECTIONS_API_ENDPOINT, STATIC_MAPS_API_ENDPOINT, API_KEY

# receives direction url and returns photo preview
def get_photo(path) -> BytesIO:
    # Make a request to the Directions API to get the polyline of the route
    dir_response = requests.get(DIRECTIONS_API_ENDPOINT, params={
        "origin": path['origin'],
        "destination": path['destination'],
        "waypoints": path["waypoints"],
        "key": API_KEY
    })
    dir_response.raise_for_status()

    # Make a request to the Static Maps API to get an image of the route based on the polyline
    polyline_points = dir_response.json()["routes"][0]["overview_polyline"]["points"]
    print(f'polyline_points: {polyline_points}')
    map_response = requests.get(STATIC_MAPS_API_ENDPOINT, params={
        "size": "640x640",
        "maptype": "roadmap",
        "path": f"color:0x0080ffff|weight:5|enc:{polyline_points}",
        "markers": f"{path['origin']}|{path['destination']}",
        "key": API_KEY
    })

    bio = BytesIO()
    bio.name = 'image.png'
    image = Image.open(BytesIO(map_response.content))
    image.save(bio, 'PNG')
    bio.seek(0) # back to the start

    return bio