var dayList = null
var playButton = null;
var timestampElement = null;
var maxValueElement = null;
var activeMarker = [];
var index = 0;
var max_Cases = 0;
var max_Radius = 66000;
var oldDayEntrys = [];

var regions = [];

var mymap;

function markerRadius(amount) {
    return (amount / max_Cases * (max_Radius*10)) / Math.pow(mymap.getZoom(),2);
}
function perc2color(perc) {
    perc = Math.min(perc, 100);
	var r, g, b = 0;
	if(perc < 50) {
		g = 255;
		r = Math.round(5.1 * perc);
	}
	else {
		r = 255;
		g = Math.round(510 - 5.10 * perc);
	}
	var h = r * 0x10000 + g * 0x100 + b * 0x1;
	return '#' + ('000000' + h.toString(16)).slice(-6);
}


window.onload = function () {

    timestampElement = document.getElementById('timestamp');
    playButton = document.getElementById('play-button');
    maxValueElement = document.getElementById('max_value');


    mymap = L.map('mapid')//.setView([50.623596,12.924983099999999], 10);

    mymap.on('zoomend', function() {
        activeMarker.forEach(marker => {
            marker.setRadius(markerRadius(marker._amount));
        })
    });

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia3JlbG91IiwiYSI6ImNrOGxscXRldTA1ZmQzZW9jdmp0dnFncGwifQ.fVy2oaejPmtfmhEWhqbPwg', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 14,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1Ijoia3JlbG91IiwiYSI6ImNrOGxscXRldTA1ZmQzZW9jdmp0dnFncGwifQ.fVy2oaejPmtfmhEWhqbPwg'
    }).addTo(mymap);




    var url_parts = window.location.href.split('/')
    var region = url_parts[url_parts.length -1]

    //Load Current - Data
    $.ajax({
        url: `/data/${region}/total`
    }).done(function(res) {

        center_lat = res['map']['lat']
        center_lon = res['map']['lon']
        mymap.setView([center_lat, center_lon], 10)

        var latest_day_unix = Math.max.apply(Math, res['data'].map(function (o) {return o['latest-record']}));
        const date = new Date(latest_day_unix)
        showDateStamp(date);

        //max_Cases = Math.max.apply(Math, res['data'].map(function(o) { return o.Anzahl; }));
        max_Cases = res['range']['max'];
        maxValueElement.innerText = '>= ' + max_Cases;
        res['data'].forEach(element => {
            if (element['Polygon'].length > 4) {
                var polygon = getPolygon(element);
                regions.push(polygon);
            } else {
                var marker = L.marker([element['lat'], element['lon']]).addTo(mymap);
                marker.bindTooltip(`<b>${element['Region']}</b><br>Anzahl: ${element['Anzahl']}`).addTo(mymap);
            }

            //var circle = getMarker(element);
            //circle.bindPopup(`<b>${element['Region']}</b><br>Anzahl: ${element['Anzahl']}`)
            //activeMarker.push(circle)
        })
    });


    // Load Historical Information
    $.ajax({
        url: `/data/${region}/daily`
    }).done(function(response) {
        const list = response['data']

        var times = list.map(x => x.date);
        times = [... new Set(times)]

        var dayOverview = [];

        times.forEach(time => {
            const day_Entrys = list.filter(x => x['date'] === time);
            const day = new Date(time);
            dayOverview.push({
                day: day,
                list: day_Entrys
            });
        });
        dayList = dayOverview;

        //Show DayList only if more than 1 day
        if (dayList.length > 1) {
            playButton.style.visibility = 'visible';
        }
    })
}

function onPlayStart() {
    //Reset Pre-Run
    index = 0;
    activeMarker.forEach(marker => marker.remove());
    oldDayEntrys = [];

    resetRegions();


    //Start the script
    if (dayList.length > 0) {
        showDay(index)
        index ++;
    }

    if (dayList.length > 1) {
        var wait_time = 60 / dayList.length;
        wait_time = Math.max(wait_time, 2);
        wait_time = Math.min(wait_time, 3);
    }

    const interval = setInterval(function() {
        showDay(index, wait_time * 1000);

        index++
        if (index >= dayList.length) {
            clearInterval(interval);
        }
    }, wait_time * 1000)
}

function resetRegions() {
    regions.forEach(region => {
        setPolygonColor(region, 0);
        region._amount = 0;
    })
}

function setPolygonColor(polygon, percentage) {
    polygon.setStyle({fillColor: perc2color(percentage), color: perc2color(percentage)});
}

function showDay(_index, timeoutTime){
    const day = dayList[_index];

    showDateStamp(day.day);
    day.list.forEach(element => {
        var region = regions.filter(x => x._municipality == element['Region']);
        if (region.length > 0) {
            region = region[0];

            region._amount += element['Anzahl'];
            setPolygonColor(region, region._amount / max_Cases * 100);
            var lat = region._center._lat;
            var lon = region._center._lon;
            const location = [lat, lon];
            var popup = L.popup().setLatLng(location).setContent(`<b>${element['Region']}</b><br>+ ${element['Anzahl']}`);
            popup.options.autoClose = false;
            popup.openOn(mymap);

            setTimeout(() => {
                mymap.closePopup(popup);
            }, timeoutTime);
        }
        /*var foundedEntrys = oldDayEntrys.filter(x => x['Region'] == element['Region']);
        const existingEntry = foundedEntrys[foundedEntrys.length - 1];
        if (existingEntry) {
            element['Anzahl'] += existingEntry['Anzahl']
            const index = oldDayEntrys.indexOf(existingEntry);
            oldDayEntrys.slice(index, 1);
        }

        if (activeMarker.length > 0) {
            var oldMarker = activeMarker.filter(x => x._latlng.lat == element['lat'] && x._latlng.lng == element['lon']);
            oldMarker.forEach(marker => mymap.removeLayer(marker));
        }

        const marker = getMarker(element);
        marker.bindPopup(`<b>${element['Region']}</b><br>Anzahl: ${element['Anzahl']}`)
        activeMarker.push(marker);
        oldDayEntrys.push(element);*/
    });
}

function showDateStamp(date) {
    timestampElement.innerText = date.toLocaleDateString();
    timestampElement.style.visibility = 'visible';
}

function getPolygon(element) {
    var latlngs = Array.from(element['Polygon'])
    myColor =perc2color(element['Anzahl'] / max_Cases * 100)
    var polygon = L.polygon(latlngs, {color: myColor});
    polygon._municipality = element['Region'];
    polygon._center = {_lat: element['lat'], _lon: element['lon']}
    polygon.addTo(mymap);
    polygon.bindTooltip(`<b>${element['Region']}</b><br>Anzahl: ${element['Anzahl']}`).addTo(mymap);

    return polygon;
}

function getMarker(element) {
    var per = element['Anzahl'] / max_Cases * 100;
    var marker =  L.circle([element['lat'], element['lon']], {
                color: perc2color(per),
                fillColor: perc2color(per),
                fillOpacity: 0.3,
                radius: markerRadius(element['Anzahl'])
            }).addTo(mymap);
    marker._amount = element['Anzahl'];
    return marker;
}