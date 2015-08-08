locs = new Set()

cfg =
  "radius": 7,
  "maxOpacity": .8,
  "scaleRadius": true,
  "useLocalExtrema": true,
  latField: 'lat',
  lngField: 'lng',
  valueField: 'count'

heatmapLayer = new HeatmapOverlay(cfg)

redraw = ->
  data = (Array.from locs).map (loc) ->
    amount = Math.log(loc.amount + 3);
    {lat: loc.lat, lng: loc.lng, count: amount}
  heatmapLayer.setData({data: data})

add_loc = (loc) ->
  locs.add loc
  redraw()
  setTimeout ->
    locs.delete loc
    redraw()
  , 50000

$ ->
  tileLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  })

  map = L.map('map', {
    center: new L.LatLng(51.505, -0.09)
    zoom: 2
    layers: [tileLayer, heatmapLayer]
  })

  ws = new WebSocket 'ws://localhost:8765'
  ws.onmessage = (e) ->
    loc = JSON.parse e.data
    add_loc loc
