$ ->
  map = L.map('map').setView([51.505, -0.09], 13)

  window.L = L
  window.map = map

  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  }).addTo(map)

  ws = new WebSocket 'wss://localhost'
  ws.onmessage = (e) ->
    tx = JSON.parse e.data
    console.log tx
    L.marker([tx.lat, tx.lon]).addTo(map)
