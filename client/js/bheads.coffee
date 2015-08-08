$ ->
  tileLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  })

  cfg =
    "radius": 5,
    "maxOpacity": .8,
    "scaleRadius": true,
    "useLocalExtrema": true,
    latField: 'lat',
    lngField: 'lng',
    valueField: 'count'

  heatmapLayer = new HeatmapOverlay(cfg)

  map = L.map('map', {
    center: new L.LatLng(51.505, -0.09)
    zoom: 2
    layers: [tileLayer, heatmapLayer]
  })

  ws = new WebSocket 'ws://localhost:8765'
  ws.onmessage = (e) ->
    loc = JSON.parse e.data
    console.log loc
    # L.marker([loc.lat, loc.lng]).addTo(map)
    heatmapLayer.addData([{lat: loc.lat, lng: loc.lng, count: 1}])
