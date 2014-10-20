
import re
import math

# constants
miles_to_km = 1.60934

def parse(query): 
    query = query.lower()
    find_number_regex = r'(\d+(\.\d+)?)(\s)?'
    data = {}
    data = {'meters': None, 'seconds': None, 'mps': None, 'units': 'metric'}

    # Distances
    for prefix in ['k', 'km', 'kilometer', 'kilometers']:
        matches = re.findall(find_number_regex + prefix + '(\s)', query)
        if len(matches) > 0: 
            data['meters'] = float(matches[0][0]) * 1000
            data['units'] = 'metric'
    for prefix in ['m', 'meter', 'meters']:
        matches = re.findall(find_number_regex + prefix + '(\s)', query)
        if len(matches) > 0: 
            data['meters'] = float(matches[0][0])
            data['units'] = 'metric'
    
    for prefix in ['mi(\s)', 'miles']:
        matches = re.findall(find_number_regex + prefix, query)
        if len(matches) > 0: 
            data['meters'] = float(matches[0][0]) * 1000 * miles_to_km
            data['units'] = 'imperial'
    
    if 'marathon' in query: 
        data['meters'] = 42195
    if 'half marathon' in query: 
        data['meters'] = 21098

    # Times
    time_seconds = 0
    matches = re.findall(find_number_regex + 'hour', query)
    if len(matches) > 0:
        time_seconds += float(matches[0][0]) * 3600
    matches = re.findall(find_number_regex + 'hr', query)
    if len(matches) > 0:
        time_seconds += float(matches[0][0]) * 3600
    matches = re.findall(find_number_regex + 'min', query)
    if len(matches) > 0:
        time_seconds += float(matches[0][0]) * 60
    matches = re.findall(find_number_regex + 'sec', query)
    if len(matches) > 0:
        time_seconds += float(matches[0][0])

    # Times in hh:mm:ss formats
    if time_seconds == 0: 
        time_regex_2 = r'(\d+):(\d+)'
        matches = re.findall(time_regex_2, query)
        if len(matches) > 0: 
            time_seconds = float(matches[0][0]) * 60 + float(matches[0][1])
        time_regex_3 = r'(\d+):(\d+):(\d+)'
        matches = re.findall(time_regex_3, query)
        if len(matches) > 0: 
            time_seconds = float(matches[0][0]) * 3600 + float(matches[0][1]) * 60 + float(matches[0][2])
    if time_seconds > 0: 
        data['seconds'] = time_seconds
            
            
    # Speeds
    matches = re.findall(find_number_regex + 'km/h', query)
    if len(matches) > 0: 
        data['mps'] = float(matches[0][0]) / 3.6
        data['units'] = 'metric'
    matches = re.findall(find_number_regex + 'kilometers/h', query)
    if len(matches) > 0: 
        data['mps'] = float(matches[0][0]) / 3.6
        data['units'] = 'metric'
    matches = re.findall(find_number_regex + 'mph', query)
    if len(matches) > 0: 
        data['mps'] = float(matches[0][0]) * miles_to_km / 3.6
        data['units'] = 'imperial'


    if 'imperial' in query or 'in miles' in query: 
        print 'here'
        data['units'] = 'imperial'
    if 'metric' in query or 'in kilometers' in query or 'in km' in query: 
        print 'here2'
        data['units'] = 'metric'

    return data

def fill(data): 
    if data['meters'] is None:
        if data['seconds'] is None or data['mps'] is None: 
            return None
        else:
            data['meters'] = 1.0 * data['mps'] * data['seconds'] 
    if data['seconds'] is None:
        if data['meters'] is None or data['mps'] is None: 
            return None
        else:
            data['seconds'] = 1.0 * data['meters'] / data['mps'] 
    if data['mps'] is None:
        if data['seconds'] is None or data['meters'] is None: 
            return None
        else:
            data['mps'] = 1.0 * data['meters'] / data['seconds'] 
    return data

digits = 2
def convert_distance(value, units): 
    if units == 'metric':
        if value > 2000: 
            answer = 1.0 * value / 1000
            return ('{0:.{1}f}'.format(answer, 2), 'kilometers')
        else: 
            answer = value
            return ('{0:.{1}f}'.format(answer, 0), 'meters')
    else: 
        answer = value / 1000 / miles_to_km
        return ('{0:.{1}f}'.format(answer, 2), 'miles')
def convert_time(value, units): 
    minutes = math.floor((value + 0.5) / 60)
    seconds = (value + 0.5) % 60
    return (str(int(minutes)) + ':' + str(int(seconds)).zfill(2), 'minutes')

def convert_speed(value, units): 
    if units == 'metric': 
        answer = value * 3.6
        return ('{0:.{1}f}'.format(answer, digits), 'km/h')
    if units == 'imperial': 
        answer = value * 3.6 / miles_to_km
        return ('{0:.{1}f}'.format(answer, digits), 'miles/hour')

def convert_pace(value, units): 
    if units == 'metric': 
        minute_float = 60.0 / (value * 3.6)
        minutes = math.floor(minute_float)
        seconds = math.floor(60.0 * (minute_float - minutes))
        return (str(int(minutes)) + ':' + str(int(seconds)).zfill(2), 'min/km')
    if units == 'imperial': 
        minute_float = 60 / (value * 3.6 / miles_to_km)
        minutes = math.floor(minute_float)
        seconds = math.floor(60.0 * (minute_float - minutes))
        return (str(int(minutes)) + ':' + str(int(seconds)).zfill(2), 'min/mi')

def calculate_missing(query): 
    parsed = parse(query)
    filled = fill(parsed)
    if filled is None: 
        return {'error_msg': 'Please supply at least two of distance, time, and speed'}
    units = filled['units']

    result = {}
    (result['dist_val'], result['dist_unit']) = convert_distance(filled['meters'], units)
    (result['time_val'], result['time_unit']) = convert_time(filled['seconds'], units)
    (result['pace_val'], result['pace_unit']) = convert_pace(filled['mps'], units)
    (result['speed_val'], result['speed_unit']) = convert_speed(filled['mps'], units)
    return result
