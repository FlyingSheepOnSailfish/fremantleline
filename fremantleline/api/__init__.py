# -*- coding: utf-8 -*-
#
# Fremantle Line: Transperth trains live departure information
# Copyright (c) 2009-2013 Matt Austin
#
# Fremantle Line is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fremantle Line is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

from __future__ import absolute_import, unicode_literals
from datetime import datetime
from fremantleline.api.useragent import URLOpener
from urllib import urlencode
import lxml.html


class Operator(object):
    """Operating company.

    """

    name = 'Transperth Trains'
    stations = None
    url = 'http://www.transperth.wa.gov.au/TimetablesMaps/LiveTrainTimes.aspx'

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, unicode(self))

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return self.name

    def _get_html(self):
        url_opener = URLOpener()
        response = url_opener.open(self.url)
        html = lxml.html.parse(response).getroot()
        return html

    def _parse_stations(self, html):
        options = html.xpath('.//*[@id="EntryForm"]//select/option')
        stations = []
        for option in options:
            data = urlencode({'stationname': option.attrib['value']})
            name = '{0}'.format(option.attrib['value']).rsplit(' Stn', 1)[0]
            url = '{0}?{1}'.format(self.url, data)
            stations += [Station(name, url)]
        return stations

    def get_stations(self):
        """Returns list of Station instances for this operator."""
        if self.stations is None:
            html = self._get_html()
            self.stations = self._parse_stations(html)
        return self.stations


class Station(object):
    """Train station.

    """

    departures = None

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, unicode(self))

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return self.name

    def _get_html(self):
        url_opener = URLOpener()
        response = url_opener.open(self.url)
        html = lxml.html.parse(response).getroot()
        return html

    def _parse_departures(self, html):
        rows = html.xpath(
            '//*[@id="dnn_ctr1608_ModuleContent"]//table//table/tr')[1:-1]
        return [Departure(self, row) for row in rows]

    def get_departures(self):
        """Returns Departure instances for this station."""
        if self.departures is None:
            html = self._get_html()
            self.departures = self._parse_departures(html)
        return self.departures


class Departure(object):
    """Departure information.

    """

    def __init__(self, station, row_data):
        self.station = station
        self._cols = row_data.xpath('td')

    def __repr__(self):
        return '<{class_name}: {time} {destination} {status}>'.format(
            class_name=self.__class__.__name__, time=self.time,
            destination=self.destination, status=self.status)

    @property
    def description(self):
        return self._cols[3].text_content().strip()

    @property
    def destination(self):
        return self._cols[2].text_content().strip().split('To ', 1)[-1]

    @property
    def line(self):
        return self._cols[0].xpath('img')[0].attrib['title']

    @property
    def status(self):
        return self._cols[5].text_content().strip()

    @property
    def time(self):
        return datetime.strptime(self._cols[1].text_content().strip(),
                                 '%H:%M').time()

transperth = Operator()
