"""
Mission planning based on station and parameter filess

Reads in a YAML-format parameter file containing parameters and a list of events.
Details on this file are given in the subroutine "read_param_file()"

The parameter file can also specify a "station file" containing the names,
latitudes and longitudes of the stations.  All of these stations will be
plotted on the map and if one of the events has the same name and no specified
latitude and longitude.

Outputs a table of events with predicted (or specified) times, in HTML and
RestructuredText formats.

Miscellaneous additional features:
  * Crosses out visited stations (departure_time before datetime.now()

  * Changes the color of the ship's track at every "NEWLEG" action

  * Plots a color bathymetric image if you specify map:bathy_map as:
    * a string: a NetCDF file at the given path
    * True: A low-res global image
"""
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import math as m

import yaml
import docutils.core

from .sea_plot import plot_map
from .sea_print import event_table, print_used_stations
from .validate_json import validate


def main(debug=False):
    """
    Create an at-sea deployment plan
    """
    # Read from command line
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('parameter_file', metavar='PARAM_FILE',
                        help='YAML file containing all parameters')
    parser.add_argument('--no_map', action='store_true',
                        help="Don't print/save map")
    args = parser.parse_args()

    # Read in parameters and station positions
    validate(args.parameter_file)
    params, events = read_param_file(args.parameter_file)
    orig_stations = read_station_file(params['station_file'])

    # Set up variables
    total_hours = 0
    used_stations = []
    if debug:
        print(orig_stations)
    stations = orig_stations.copy()

    # Setup "past" information
    events[0]['dist_from_previous'] = 0
    prev_event = events[0].copy()
    prev_event, _ = _handle_existence(prev_event, stations, params)

    if 'depart_time' in prev_event:
        depart_base = datetime.strptime(prev_event['depart_time'],
                                        '%Y-%m-%dT%H:%M')
    else:
        depart_base = datetime.strptime(prev_event['arrive_time'],
                                        '%Y-%m-%dT%H:%M')

    # Loop over events
    for event in events:
        # Handle pre-existence of stations
        event, stations = _handle_existence(event, stations, params)
        if event_station(event, orig_stations):
            used_stations.append(event['station'])
        # Calculate distance from previous event
        event['dist_from_previous'] = distance(event, prev_event)
        # Update leg # on "NEWLEG" event action
        if 'action' in event:
            if event['action'] == "NEWLEG":
                iLeg += 1
        # Calculate time on station, latency, and total times
        event, total_hours = calc_times(event, params['timing'], depart_base,
                                        total_hours)
        prev_event = event.copy()
    # Print and save event table
    t = event_table(events, args.parameter_file, params, 'RST')
    print(t)
    outfname = Path(args.parameter_file).with_suffix('.rst')
    with open(outfname, 'w') as f:
        f.write(t)
    htmlfname = Path(args.parameter_file).with_suffix('.html')
    # s=docutils.core.publish_string(
    #     t,
    #     destination_path=htmlfname,
    #     writer_name="html")
    # s=docutils.core.publish_string(t, writer_name="html")
    # print(s)
    #with open(htmlfname, 'w') as f:
    #    f.write(str(s))
    docutils.core.publish_file(
        source_path=outfname,
        destination_path=htmlfname,
        writer_name="html")

    # Print list of CSV-file stations used
    print_used_stations(orig_stations, used_stations)

    # Make a map
    if not args.no_map:
        plot_map(events, orig_stations, params)


def _handle_existence(event, stations, params):
    """
    Handle pre-existence of a station for an event
    """

    # If the event is at an existing station, modify/complete the information
    event = event_from_station(event, stations, params)

    # If the event is not at an existing station, save its lat and lon
    if not event_station(event, stations):
        try:
            stations[event['station']] = dict(lat=event['lat'],
                                              lon=event['lon'])
        except:
            print(f'Error, event "{event["station"]}" has no coordinates')
            sys.exit(2)
    return event, stations


def read_param_file(parameter_file):
    """
    READ IN PARAMETERS AND SEQUENTIAL LIST OF EVENTS FROM YAML FILE

    Variables that can be provided in the parameter files are
    (default in [braces]):
    stations:
        file(str): CSV (semicolon-separated) file of
                   station;Lat;Lon;Type;Comment
        times: {type1: hours, type2:hours, ...}  # Hours to deploy one station
                                                 # of given type
    map:
        show_plot: Show the map of positions and tracks [False]
        bounds: [left, right, bottom, top]  Decimal degrees    [MANDATORY if
                plot_map==True]
        bathy (str): netCDF file to plot as background image on the map
              (True): Plot an etopo image as background
              (False): No background map
        plot_past_tracks: Plot past ship tracks [True]
    printout:
        show_comments : Show comments in output [False]
        print_past : Print out past events [False]
        print_waypoints: Print out waypoints (events with 0 time) [True]
    timing:
        ignore_arrive_depart: Ignore arrive_time and depart_time to test time
                              predictions [False]
        ship_speed.kn_i: Cruising speed of the ship in knots [10.]
        ship_latency: Hours lost getting to speed from stopped [0.5]
        event_list: Sequential list of events to perform [MANDATORY].
                    Each item must have a "station" key (str) and may have the
                    following keys:
                        action(str): the action to perform ("deploy",
                                     "recover","survey","waypt"...)
                        lat (float): site latitude  [station.lat or 0]
                        lon (float): site longitude  [station.lat or 0]
                        arrive_time (ISO):  [previous depart_time + transit
                                             + latency]
                        depart_time (ISO):  [arrive_time + hours]
                        hours (float): hours expected for operation  [0 or
                                       stations[type].times]
                        comment (str): comments
                        speed (float): speed between previous and given site
                                      [ship_speed.kn_i]
    """
    stream = open(parameter_file, 'r')
    p = yaml.load(stream)
    stream.close()
    event_list = p['events']

    # SET DEFAULT VALUES
    params = {'file': parameter_file,
              'station_file': {'name': False, 'field_separator': ';'},
              'printout': {'show_comments': False,
                           'print_past': False,
                           'print_waypoints': True},
              'timing': {'ignore_depart_arrive_times': False,
                         'ship_speed.kn_i': 10,
                         'ship_latency.h': 0.5,
                         'action_times.h': {}},
              'map': {'show_plot': False,
                      'bounds': [],
                      'grid': {'x': 1, 'y': 1},
                      'bathy_map': False,
                      'plot_past_tracks': True}}
    # UPDATE WITH ENTERED VALUES
    for key in params.keys():
        if key in p['variables']:
            params[key].update(p['variables'][key])

    return params, event_list


def _verify_fields(field_order):
    if 'name' not in field_order:
        print('Error: no "name" in 1st line of csv file')
        print(field_order)
        sys.exit(1)
    if 'lon' not in field_order:
        if not ('lond' in field_order and 'lonm' in field_order):
            print('Error: no "lon" or "lond"&"lonm" in 1st line of csv file')
            sys.exit(1)
    if 'lat' not in field_order:
        if not ('latd' in field_order and 'latm' in field_order):
            print('Error: no "lat" or "latd"&"latm" in 1st line of csv file')
            sys.exit(1)


def _deg_min_to_deg(degrees, minutes):
    return m.sign(float(degrees)) * (m.abs(float(degrees))
                                     + m.abs(float(minutes)/60.))


def read_station_file(station_file, debug=False):
    """  READ STATION POSITONS FROM CSV FILE  """
    stations = dict()
    if station_file['name']:
        with open(station_file['name']) as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=station_file['field_separator'])
            field_order = next(reader)
            field_order = [x.lower() for x in field_order]
            _verify_fields(field_order)

            for row in reader:
                i = 0
                # Read into appropriate fields
                temp = dict()
                for field in field_order:
                    temp[field] = row[i]
                    i += 1
                if debug:
                    print(temp.keys())
                if 'lat' not in temp:
                    temp['lat'] = _deg_min_to_deg(temp['latd'], temp['latm'])
                if 'lon' not in temp:
                    temp['lon'] = _deg_min_to_deg(temp['lond'], temp['lonm'])

                # Fill station dictionary
                station = dict(lat=float(temp['lat']), lon=float(temp['lon']))
                station['type'] = temp.get('type', '')
                station['comment'] = temp.get('comment', '')

                # Put into stations dictionary
                stations[temp['name']] = station
    else:
        stations = dict()
    return stations


def _degrees_to_kilometers(degrees, radius=6371):
    """
    Convenience function to convert (great circle) degrees to kilometers
    assuming a perfectly spherical Earth.  Taken from obspy

    :type degrees: float
    :param degrees: Distance in (great circle) degrees
    :type radius: int, optional
    :param radius: Radius of the Earth used for the calculation.
    :rtype: float
    :return: Distance in kilometers as a floating point number.

    .. rubric:: Example

    >>> _degrees_to_kilometers(1)
    111.19492664455873
    """
    return degrees * (2.0 * radius * m.pi / 360.0)


def _locations_to_degrees(lat1, long1, lat2, long2):
    """
    Convenience function to calculate the great circle distance between two
    points on a spherical Earth.

    This method uses the Vincenty formula in the special case of a spherical
    Earth. Taken from obspy.

    :type lat1: float
    :param lat1: Latitude of point 1 in degrees
    :type long1: float
    :param long1: Longitude of point 1 in degrees
    :type lat2: float
    :param lat2: Latitude of point 2 in degrees
    :type long2: float
    :param long2: Longitude of point 2 in degrees
    :rtype: float or :class:`numpy.ndarray`
    :return: Distance in degrees as a floating point number

    .. rubric:: Example

    >>> _locations_to_degrees(5, 5, 10, 10)
    7.0397014191753815
    """
    # Convert to radians.
    lat1 = m.radians(lat1)
    lat2 = m.radians(lat2)
    long1 = m.radians(long1)
    long2 = m.radians(long2)
    long_diff = long2 - long1
    gd = m.degrees(
        m.atan2(
            m.sqrt((
                m.cos(lat2) * m.sin(long_diff)) ** 2 +
                (m.cos(lat1) * m.sin(lat2) - m.sin(lat1) *
                    m.cos(lat2) * m.cos(long_diff)) ** 2),
            m.sin(lat1) * m.sin(lat2) + m.cos(lat1) * m.cos(lat2) *
            m.cos(long_diff)))
    return gd


def distance(site1, site2):
    """
    Distance in nautical miles between two sites

    Sites must have 'lat' and 'lon' keys and values in decimal degrees
    """
    # Why are these two cases?  In case nothing was entered?  Should be None!
    # if (site1['lat'] == 0 and site1['lon'] == 0)
    #         return 0
    # if (site2['lat'] == 0 and site2['lon'] == 0):
    #         return 0
    degrees = _locations_to_degrees(site1['lat'], site1['lon'],
                                    site2['lat'], site2['lon'])
    nm = _degrees_to_kilometers(degrees) / 1.852
    return nm


def _default_hours(event, params):
    if 'timing' in params:
        if 'action_times.h' in params['timing']:
            at_h = params['timing']['action_times.h']
            if 'action' in event:
                if event['action'] in at_h:
                    action = event['action']
                    if 'type' in event:
                        if event['type'] in at_h[action]:
                            return at_h[action][event['type']]
                        else:
                            return at_h[action].get('default', 0.)
                    else:
                        return at_h[action].get('default', 0.)
    return 0.


def event_from_station(event, stations, params):
    """
    Find the station corresponding to event['station']
    """
    station = event_station(event, stations)
    if station:
        if 'lat' in event:
            print(f'"{event["station"]}" latitude ignored, using previously '
                  'specified value')
        elif 'lon' in event:
            print(f'"{event["station"]}" longitude ignored, using previously '
                  'specified value')
        event['lat'] = station['lat']
        event['lon'] = station['lon']
        event['type'] = event.get('type', station.get('type', ''))
        event['hours'] = event.get('hours', _default_hours(event, params))
        event['comment'] = add_comments(event.get('comment', ''),
                                        station.get('comment', ''))
    else:
        event['hours'] = event.get('hours', 0.)
        if event['hours'] == 0:
            event['type'] = event.get('type', 'Waypoint')
        else:
            event['type'] = event.get('type', 'Operation')
        event['comment'] = add_comments(event.get('comment', ''), '')
    return event


def event_station(event, stations, debug=True):
    """ Find the station corresponding to event['station'] """
    if event['station'] in stations:
        return stations[event['station']]
    return None


def choose_time(input_time, forced_time, ignore_forced_times):
    """
    Return the time to associate with an arrival or departure

    input_time :    a calculated time
    forced_time : a hand-entered time (may be empty)
    ignore_forced times: whether to used the forced time or not
    """
    if forced_time and not ignore_forced_times:
        return dict(time=datetime.strptime(forced_time, '%Y-%m-%dT%H:%M'),
                    forced=True)
    return dict(time=input_time, forced=False)


def calc_times(event, tparams, depart_base, total_hours):
    """ Calculate arrival and departure times

    :type event: dict (should it become a class?)
    :param event: seaplan event
    :type tparams: dict
    :param tparams: timing parameters
    :type depart_base: datetime
    :param depart_base: base depart time
    :type total_hours: float
    :param total_hours: total hours for the event
    :rtype: dict
    :return: Event with recalculated times
    """
    time_on_station = event['hours']
    if time_on_station == 0:
        latency = 0
    else:
        latency = tparams['ship_latency.h']
    ship_speed = event.get('speed', tparams['ship_speed.kn_i'])
    imposed_arrive_time = event.get('arrive_time', False)
    imposed_depart_time = event.get('depart_time', False)
    event['transit_hours'] = event['dist_from_previous'] / ship_speed + latency
    arrival = depart_base + timedelta(seconds=3600 *
                                      (total_hours + event['transit_hours']))
    event['arrival'] = choose_time(arrival, imposed_arrive_time,
                                   tparams['ignore_depart_arrive_times'])
    departure = event['arrival']['time'] + timedelta(seconds=3600
                                                     * time_on_station)
    event['departure'] = choose_time(departure, imposed_depart_time,
                                     tparams['ignore_depart_arrive_times'])

    dt = event['departure']['time'] - depart_base
    total_hours = dt.days * 24 + dt.seconds/3600.

    return event, total_hours


def add_comments(event_comment, station_comment):
    """Combine event and station comments"""

    if station_comment and event_comment:
        # Put "e:" before the event_comment and "s:" before the station_comment
        return f'e:{event_comment}; s:{station_comment}'
    elif station_comment:
        return station_comment
    elif event_comment:
        return event_comment
    else:
        return ''


if __name__ == '__main__':
    sys.exit(main())
