#!/usr/bin/env python3
"""
Plotting routines for seaplan
"""
import math
from datetime import datetime

import numpy as np
from scipy.io import netcdf
from matplotlib import pyplot as plt
# from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
from cartopy.feature import GSHHSFeature
from pylab import cm

from .bathy_map import BathyMap

# CONSTANTS
font_size = 7
text_offset = 0.02  # degrees from station
text_bbox = dict(boxstyle="round", pad=0.1, edgecolor='none',
                 facecolor='white', alpha=0.5)


def plot_map(events, orig_stations, params):
    """
    Plot basemap

    :param orig_stations: stations in CSV file(?)
    :param params: seaplan parameter dictionary
    """
    mp = params['map']
    m = BathyMap(mp['bounds'], mp.get('bathy_map', False), mp['grid']['x'],
                 mp['grid']['y'])
    if 'bathy_map' in mp:
        if isinstance(mp['bathy_map'], str):
            m.plot_image(pastel=True, shaded=True)
            m.plot_contours()
        elif mp['bathy_map'] is True:
            m.ax.stock_img()
            
    m.plot_coastlines('high')
    
    for name, station in orig_stations.items():
        ms = 5
        if station['type'] == 'WayPoint':
            sym = 'k.'
        elif station['type'] == 'Operation':
            continue
        elif station['type'] == 'Survey':
            continue
        elif station['type'] == 'BB':
            sym = 'r+'
            ms = 10
        else:
            sym = 'r+'
        m.plot(station['lon'], station['lat'], sym, markersize=ms)
        # m.plot(event['lon'],event['lat'],'k+',latlon=True)
        # x, y = m(station['lon'] + text_offset, station['lat'])
        plt.text(station['lon']+ text_offset, station['lat'],
                 name, fontsize=font_size, va='center', color='gray')

    iLeg = 0
    # COLOR FOR EVERY "NEWLEG"
    legSyms = ['k-', 'r-', 'b-', 'g-', 'm-', 'c-', 'k--', 'r--', 'b--']
    prev_event = events[0].copy()
    for event in events:
        if event['station'] in orig_stations:
            cross_visited_stations(m, event)
        # Update leg # on "NEWLEG" event action
        if 'action' in event:
            if event['action'] == "NEWLEG":
                iLeg += 1
        if (params['map']['plot_past_tracks'] or
                (event['arrival']['time'] > datetime.now())):
            plot_track(m, event, prev_event, legSyms[iLeg % len(legSyms)])
        plot_event(m, event)
        prev_event = event.copy()
    dt = events[-1]['arrival']['time'] - events[0]['departure']['time']
    fig, base_name = close_map(params, dt)
    fig.savefig(f'{base_name}.png', dpi=150)



def plot_track(m, event, prev_event, sym):
    """
    Plot ship track
    """
    if event['dist_from_previous'] > 0:
        m.plot([event['lon'], prev_event['lon']],
                 [event['lat'], prev_event['lat']], sym)
        m.arrow(prev_event['lon'], prev_event['lat'],
                  .6 * (event['lon'] - prev_event['lon']),
                  .6 * (event['lat'] - prev_event['lat']),
                  head_width=0.015, length_includes_head=True)


def cross_visited_stations(m, event):
    """
    plot a cross if departure_time is specified & before current time
    """
    if 'depart_time' in event:
        if (datetime.strptime(event['depart_time'], '%Y-%m-%dT%H:%M')
                < datetime.now()):
            # x, y = m(event['lon'], event['lat'])
            m.plot(event['lon'], event['lat'], 'kx', markersize=12, linewidth=3)


def plot_event(m, event, debug=False):
    """
    Plot one mission event

    :param m: global coordinate system
    :param event: event dictionary
    """
    if debug:
        print("In plot_event()")
    if event['type'] == 'Operation':
        m.plot(event['lon'], event['lat'], 'r+', markersize=8, lw=5.0)
        # x, y = m(event['lon'], event['lat'] - text_offset)
        m.text(event['lon'], event['lat'], event['station'],
               fontsize=font_size, va='top', ha='center', color='red',
               bbox=text_bbox)
    else:
        # Station or WayPoint
        if event['type'] == 'WayPoint':
            m.plot(event['lon'], event['lat'], '+', markersize=5, lw=3.0)
        else:
            m.plot(event['lon'], event['lat'], 'ro', markersize=5, lw=3.0)
        if event['hours'] != 0:
            m.text(event['lon'] + text_offset, event['lat'],
                   event['station'], fontsize=font_size, va='center',
                    color='black', bbox=text_bbox)


def close_map(params, timedelta_total):
    """
    Saves map to a file

    :param params: seaplan parameters
    :param timedelta_total: total time spent (datetime.timedelta)
    :returns: figure object, base_name of output file
    """
    base_name = params['file'].split('.')[0]
    plt.title('{}: {:.0f} days {:.0f}h (speed={:g}, latency={:g}h)'.format(
              base_name, timedelta_total.days,
              timedelta_total.seconds / 3600.,
              params['timing']['ship_speed.kn_i'],
              params['timing']['ship_latency.h']),
              fontsize=12)
    fig1 = plt.gcf()    # Needed to save after "show" (which creates new fig)
    if params['map']['show_plot']:
        plt.show()
    return fig1, base_name
