locs = new Set()

cfg =
  "radius": 5,
  "maxOpacity": .8,
  "scaleRadius": true,
  "useLocalExtrema": true,
  latField: 'lat',
  lngField: 'lng',
  valueField: 'count'

heatmapLayer = new HeatmapOverlay(cfg)

window.locs = locs

redraw = ->
  data = (Array.from locs).map (loc) ->
    {lat: loc.lat, lng: loc.lng, count: 0.3}
  heatmapLayer.setData({data: data})

add_loc = (loc) ->
  locs.add loc
  redraw()
  setTimeout ->
    locs.delete loc
    redraw()
  , 6000

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
