// Fremantle Line: Transperth trains live departure information
// Copyright (c) 2009-2013 Matt Austin
//
// Fremantle Line is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Fremantle Line is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/

import QtQuick 1.1
import Sailfish.Silica 1.0


Page {

    id: stationPage

    SilicaListView {

        id: stationList
        anchors.fill: parent
        model: station_list

        header: PageHeader {
            title: 'Perth Trains'
        }

        PullDownMenu {
            id: pullDownMenu
            MenuItem {
                text: 'About'
                onClicked: {
                    pullDownMenu.close();
                    aboutDialog.open();
                }
            }
            MenuItem {
                text: 'Project homepage'
                onClicked: {Qt.openUrlExternally(projectUrl)}
            }
        }

        ViewPlaceholder {
            enabled: station_list.fetching
            text: 'Loading...'
            Behavior on opacity {}
        }

        delegate: BackgroundItem {
            width: stationList.width
            Label {
                text: model.title
                color: parent.down ? theme.highlightColor : theme.primaryColor
                anchors.verticalCenter: parent.verticalCenter
                x: theme.paddingLarge
            }
            onClicked: {
                departure_list.station = model.station;
                pageStack.push(departurePage);
            }
        }

        VerticalScrollDecorator {}

    }

}
