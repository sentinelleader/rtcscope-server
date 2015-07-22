# rtcscope-server
API/Dashboard server for [rtcscope.js](https://github.com/samirnaik/rtcscope.js). [rtcscope-server](https://github.com/sentinelleader/rtcscope-server) provides a rest API for the rtcscope clients to inject WebRTC metrics. rtcscope-server also comes with a very basic api for visualizing the real time stats graphs for the ongoing calls (More pretty adhoc graphs/ UI soon ;-) ). rtcscope uses [influxdb](influxdb.com) for storing metrics.

Graphs are rendered and updated in real time(updates automatically when a new call is started or when an ongoing call ends)


# Installation

  InfluxDB

	$ wget http://influxdb.s3.amazonaws.com/influxdb_0.9.1_amd64.deb

	$ sudo dpkg -i influxdb_0.9.1_amd64.deb

	$ /opt/influxdb/influxd -config /etc/opt/influxdb/influxdb.conf

  RTCScope-server

	$ git clone https://github.com/sentinelleader/rtcscope-server

	$ python app.py


# API Endpoints:

```
  /v1/stats/write/  - POST -  Injects Metric onto InfluxDB
  
  /v1/stats/ - GET - Returns JSON metrics for realtime calls
  
  /v1/stats/<call-id>/ - GET - Returns JSON metrics for a particular call id
  
  /demo/  - GET - Returns a webrtc demo page for testing
  
  /graph/<graph-name>/ - GET - Returns raw realtime graph for a particular property
```

# Screenshots

Screenshots of raw rendered graphs


###### Available-Bandwidth

* ```URL  /graph/availableBandwidth/```

![Alt text](/screenshots/availableBandwidth.png?raw=true "Available Bandwidth")


###### Round Trip Delay Time

* ```URL  /graph/rtt/```

![Alt text](/screenshots/rtt.png?raw=true "Round Trip Delay Time")

	
###### Input Level

* ```URL  /graph/inputLevel/```

![Alt text](/screenshots/InputLevel.png?raw=true "Input Level")


###### Packet Lost

* ```URL  /graph/packetsLost/```

![Alt text](/screenshots/PacketLost.png?raw=true "Packet Lost")


# Video


Realtime Rendering/Updating of the graphs - (Links will be added soon)


# TO-DO

  This is not even an alpha version, just an idea made into a prototype. We are working on making this simple prototype into a real usefull product for the WebRTC community :)
