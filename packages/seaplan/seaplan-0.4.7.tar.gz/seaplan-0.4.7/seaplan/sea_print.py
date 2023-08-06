#!/usr/bin/env python3
"""
Printing routines for seaplan
"""
# STANDARD LIBRARIES
from datetime import datetime
import math
# from obspy import UTCDateTime
# CONSTANTS
comment_len = 40


def event_table(event_list, parameter_file, params, format="RST"):
    """
    Print a table in MultiMarkDown or reStructuredText
    
    :param event_list: list of Events
    :param parameter_file:
    :param params:
    :param format: 'RST' or 'MMD'

    Should add HTML output
    """
    assert format in ['RST', 'MMD']
        
    show_comments = params['printout']['show_comments']
    t = _table_header(parameter_file, params, format)
    prev_arrival = event_list[0]['arrival']['time']
    day_mesg = make_day_mesg(prev_arrival, show_comments, format, True)
    trans_accum = dict(h=0., nm=0.)
    for event in event_list:
        if event['hours'] or params['printout']['print_waypoints']:
            arrival = event['arrival']['time']
            departure = event['departure']['time']
            if arrival.day != prev_arrival.day:
                day_mesg = make_day_mesg(arrival, show_comments, format)
            if (params['printout']['print_past']
                or (departure > datetime.now())):
                    if day_mesg:
                        t += day_mesg
                        day_mesg = ''
                    t += _table_row(event, trans_accum, show_comments, format)
            prev_arrival = arrival
            trans_accum = dict(h=0., nm=0.)
        else:
            trans_accum['h'] += event['transit_hours']
            trans_accum['nm'] += event['dist_from_previous']
    t += _table_footer(show_comments, format)
    return t


# def _parse_rst(text: str) -> docutils.nodes.document:
#     parser = docutils.parsers.rst.Parser()
#     components = (docutils.parsers.rst.Parser,)
#     settings = docutils.frontend.OptionParser(components=components).\
#         get_default_values()
#     document = docutils.utils.new_document('<rst-doc>', settings=settings)
#     parser.parse(text, document)
#     return document


def make_day_mesg(the_time, show_comments, form="multimarkdown", no_top=False):
    if form == "multimarkdown":
        t = "|||||| {:63s}   ||".format(the_time.strftime("*%A, %d %B*"))
    else:
        # reStructuredText
        if show_comments:
            if no_top:
                t = ""
            else:
                t = "+---------+----------+-----------+-----------+--------------+-----------+-----------+-" + comment_len*"-" + "-|\n"
            t += "|    {:77s}    ".format(the_time.strftime("*%A, %d %B*"))\
                + comment_len*" " + " |\n"
        else:
            if no_top:
                t = ""
            else:
                t = "+---------+----------+-----------+-----------+--------------+-----------+-----------+\n"
            t += "|    {:77s}  |\n".format(the_time.strftime("*%A, %d %B*"))
    return t


def _table_header(parameter_file, params, form='multimarkdown'):
    t = f"- **Created on**: {datetime.now().strftime('%Y-%m-%d %H:%M local')}\n"
    t += f'- **Station file**: "{params["station_file"]["name"]}"\n'
    t += f'- **Parameter file**: "{parameter_file}"\n'
    t += f'\n'
    t += '  - **Boat speed (kts)**: {:d}\n'.format(params['timing']['ship_speed.kn_i'])
    t += '  - **Boat latency (h)**: {:g}\n'.format(params['timing']['ship_latency.h'])
    t += '  - **Default Action "hours"**:\n'
    t += '\n'
    for action, values in params['timing']['action_times.h'].items():
        t += f'    - **{action}**: '
        for name, hours in values.items():        
            t += f'"{name}": {hours}, '
        t += '\n'
    t += '\n'
    if params['timing']['ignore_depart_arrive_times']:
        t += '\nIGNORING ALL "arrival_time"S AND "departure_time"S IN PARAMETER FILE!!!\n'
    if form == 'multimarkdown':
        if not params['printout']['show_comments']:
            t += "\n"
            t += "|    EVENT       ||  POSITION           ||   TRANSIT   |STATION TIME (Z)||\n"
            t += " Station | Action |   Lat    |   Lon    | hours(nmiles)| Arrive | Depart \n"
            t += "---------|--------|---------:|---------:|-------------:|:------:|:------:\n"
        else:
            t += "\n"
            t += "|    EVENT       ||        POSITION     ||    TRANSIT  |STATION TIME (Z)|| COMMENTS\n"
            t += " Station | Action |   Lat    |   Lon    | hours(nmiles)| Arrive | Depart | \n"
            t += "---------|--------|---------:|---------:|-------------:|:------:|:------:|---------------------\n"
    else:
        # reStructuredText
        if not params['printout']['show_comments']:
            t += "\n"
            t += "+--------------------+-----------------------+--------------+-----------------------+\n"
            t += "| EVENT              | POSITION              | TRANSIT      | STATION TIME          |\n"
            t += "+---------+----------+-----------+-----------+--------------+-----------+-----------+\n"
            t += "| Station | Action   | Lat       | Lon       | hours(nmiles)| Arrive    | Depart    |\n"
            t += "+=========+==========+===========+===========+==============+===========+===========+\n"
        else:
            t += "\n"
            t += "+--------------------+-----------------------+--------------+-----------------------+-"+comment_len*"-"+"-+\n"
            t += "| EVENT              | POSITION              | TRANSIT      | STATION TIME          | COMMENTS "+(comment_len-9)*" "+" |\n"
            t += "+---------+----------+-----------+-----------+--------------+-----------+-----------+-"+comment_len*"-"+"-+\n"
            t += "| Station | Action   | Lat       | Lon       | hours(nmiles)| Arrive    | Depart    | "+comment_len*" "+" |\n"
            t += "+=========+==========+===========+===========+==============+===========+===========+="+comment_len*"="+"=+\n"
    return t


def _table_row(event, trans_accum, show_comments, form="multimarkdown",
               debug=False):
    sta = event['station']
    act = event.get('action', '')
    lat = __deg_as_degmin(event['lat'])
    lon = __deg_as_degmin(event['lon'])
    trn = event['transit_hours'] + trans_accum['h']
    dst = event['dist_from_previous'] + trans_accum['nm']
    arr = time_str(event['arrival'])
    dep = time_str(event['departure'])
    cmt = event['comment']
    if debug:
        print(f"comment={event['comment']}")
    if form == "multimarkdown":
        if not show_comments:
            return "{:9.9s}| {:6.6s} |{:>9s} |{:>9s} | {:4.1f} ({:5.1f}) |{:^7s}|{:^7s}\n".format(
                 sta, act, lat, lon, trn, dst, arr, dep)
        else:
            return "{:9.9s}| {:6.6s} |{:>9s} |{:>9s} | {:4.1f} ({:5.1f}) |{:^7s}|{:^7s} | {}\n".format(
                 sta, act, lat, lon, trn, dst, arr, dep, cmt)
    else:
        # reStructuredText
        if not show_comments:
            t = "+---------+----------+-----------+-----------+--------------+-----------+-----------+\n"
            t += "| {:7.7s} | {:8.8s} | {:>9s} | {:>9s} | {:4.1f} ({:5.1f}) | {:^9s} | {:^9s} |\n".format(
                 sta, act, lat, lon, trn, dst, arr, dep)
            return t
        else:
            t = "+---------+----------+-----------+-----------+--------------+-----------+-----------+-"+comment_len*"-"+"-+\n"
            t += "| {:7.7s} | {:8.8s} | {:>9s} | {:>9s} | {:4.1f} ({:5.1f}) | {:^9s} | {:^9s} | {:" + f"{comment_len:d}.{comment_len:d}s"+"} |\n"
            return t.format(sta, act, lat, lon, trn, dst, arr, dep, cmt)


def _table_footer(show_comments, form="multimarkdown"):
    if form == "multimarkdown":
        t = "\n"
        t += "To make the above table pretty, convert to HTML using MMD and\n"
        t += "replace the <table> tag in the resulting HTML file with:\n"
        t += '<table border="1" width="100%" cellspacing="0" cellpadding=6>\n'
        t += "\n"
    else:
        if show_comments:
            t = "+---------+----------+-----------+-----------+--------------+-----------+-----------+-" + 40*"-" + "-+\n"
        else:
            t = "+---------+----------+-----------+-----------+--------------+-----------+-----------+\n"
    return t


def time_str(the_time):
    """
    return time string

    The output text has different emphasis based on whether it is
    the input time (normal), a forced time in the future (**bold**),
    or a forced time in the past (*italic*)
    """
    emphasis = ''
    if the_time['forced']:
        if the_time['time'] < datetime.now():  # Already passed, no big deal
            emphasis = '*'
        else:                            # Not yet passed, **CONSTRAINT**
            emphasis = '**'
    time_s = emphasis+the_time['time'].strftime("%H:%M") + emphasis
    return time_s


def print_used_stations(stations, used_stations):
    """
    Print information about which stations were used

    I think this is inefficiently written (no need for sta_dict?)
    :param stations: list of station dictionaries
    :param used_stations: list of the stations visited, in order
    """
    sta_dict = dict()
    for us in used_stations:
        sta_dict[us] = sta_dict.get(us, 0) + 1
    print('{:d} of {:d} stations in the station file were used:'.format(
        len(sta_dict), len(stations)))

    # List used stations
    print("Used:")
    __print_by_cols(sorted(sta_dict))
    # List unused stations
    print("Unused:")
    unused = []
    for name in stations.keys():
        if name not in sta_dict.keys():
            unused.append(name)
    if len(unused) == 0:
        print("  None")
    else:
        __print_by_cols(sorted(unused))

    # If multiple occurences of a station or stations, warn and inform
    iRepeated = 0
    for sta_name in sorted(sta_dict.keys()):
        if sta_dict[sta_name] > 1:
            iRepeated += 1
    if iRepeated:
        if iRepeated == 1:
            print('1 repeated used station:')
        else:
            print('{:d} of the stations were repeated:'.format(iRepeated))
        for sta_name in sorted(sta_dict.keys()):
            if sta_dict[sta_name] > 1:
                print("  {} : {:d} times".format(sta_name, sta_dict[sta_name]))
    else:
        print("No repeated used stations")
    print('')


def __print_by_cols(list, ncols=10):
    " print given list as rows of a given number of columns (10 by default) "
    i = 1
    for obj in list:
        if i == 1:
            print('  ', end='')
        print('{:>6s},'.format(obj), end='')
        i += 1
        if i > ncols:
            print("")
            i = 1
    if i != 1:
        print("")


def __deg_as_degmin(degrees, precision=1):
    """
    Return text string containing degrees and minutes

    precision is number of digits after the decimal place to return
    for the minutes field
    """
    if not isinstance(precision, int):
        print('PRECISION IS NOT AN INTEGER')
        return
    if precision < 0:
        print('PRECISION < 0!')
        return
    deg_int = math.trunc(degrees)
    deg_min = abs(60 * (degrees - deg_int))
    field_width = precision + 3
    if precision == 0:
        field_width = 2
    else:
        field_width = precision + 3
    fmt_str = "{:d}d{:0" + "{:d}.{:d}".format(field_width, precision) + "f}m"
    return fmt_str.format(deg_int, deg_min)
