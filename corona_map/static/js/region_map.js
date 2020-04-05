var dayList = null
var playButton = null;
var timestampElement = null;
var activeMarker = [];
var index = 0;
var activeMarker = [];
var max_Cases = 0;
var max_Radius = 4800;
var oldDayEntrys = []

var mymap;

window.onload = function () {

    timestampElement = document.getElementById('timestamp');
    playButton = document.getElementById('play-button');


    mymap = L.map('mapid')//.setView([50.623596,12.924983099999999], 10);

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



        max_Cases = Math.max.apply(Math, res['data'].map(function(o) { return o.Anzahl; }));
        res['data'].forEach(element => {
            var circle = getMarker(element);


            circle.bindPopup(`<b>${element['Region']}</b><br>Anzahl: ${element['Anzahl']}`)

            activeMarker.push(circle)
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

    console.log('Play')
    console.log('Daylist: ', dayList)


    //Start the script
    if (dayList.length > 0) {
        showDay(index)
        index ++;
    }

    const interval = setInterval(function() {
        showDay(index)

        index++
        if (index >= dayList.length) {
            clearInterval(interval);
        }
    }, 3000)
}

function showDay(_index){
    const day = dayList[_index];

    showDateStamp(day.day);
    day.list.forEach(element => {
        var foundedEntrys = oldDayEntrys.filter(x => x['Region'] == element['Region']);
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
        oldDayEntrys.push(element);
    });
}

function showDateStamp(date) {
    timestampElement.innerText = date.toLocaleDateString();
    timestampElement.style.visibility = 'visible';
}

function getMarker(element) {
    return L.circle([element['lat'], element['lon']], {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.3,
                radius: element['Anzahl'] / max_Cases * max_Radius
            }).addTo(mymap);
}