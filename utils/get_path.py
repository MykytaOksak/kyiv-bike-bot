import urllib.parse
import re

# gets google maps direction url and returns path from it
def get_path(url) -> dict:
    url = urllib.parse.unquote(url).replace(" ", "")
    
    # get waypoints after 'data='
    url_data = url[url.find("data="):]
    pattern = r'1d(-?\d+\.\d+)!2d(-?\d+\.\d+)'
    matches = re.findall(pattern, url_data)
    coordinates = [(f"{float(match[1])}, {float(match[0].replace('!2d', ','))}") for match in matches]

    # get waypoint after 'dir/'
    pattern1 = r'(?<=dir\/)(.*)(?=\/)'
    coordinates1 = re.search(pattern1, url).group(1)
    coordinates1 = coordinates1.split('/')[0:-1]
    if coordinates1[-1] != 'z' and len(coordinates1[-1]) == 1: 
        coordinates1[-2] = coordinates1[-2] + '/' + coordinates1[-1]
        coordinates1 = coordinates1[0:-1]

    print(f'coordinates1: {coordinates1}')
    print(f'coordinates: {coordinates}')    

    # if there are less waypoints after 'data=' than after 'dir/'
    if len(coordinates1) > len(coordinates):
        coordinates1[0] = coordinates[0]
        coordinates1[-1] = coordinates[-1]
        coordinates = coordinates1

    origin = coordinates[0]
    waypoints = '|'.join(coordinates[1:-1])
    destination = coordinates[-1]

    path = {
        "origin": origin,
        "waypoints": waypoints,
        "destination": destination        
    }

    print(f'path: {path}')

    return path