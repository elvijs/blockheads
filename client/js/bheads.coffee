$ ->
  map = L.map('map').setView([51.505, -0.09], 13)

  window.L = L
  window.map = map

  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  }).addTo(map)

  ws = new WebSocket 'ws://localhost:8765'
  ws.onmessage = (e) ->
    loc = JSON.parse e.data
    console.log loc
    L.marker([loc.lat, loc.lng]).addTo(map)
