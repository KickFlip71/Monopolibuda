$(function () {
  // Correctly decide between ws:// and wss://
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + "/game/stream/";
  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  window.socket = socket;

  socket.onmessage = function (message) {
    console.log("Got websocket message " + message.data);
  };

  socket.onopen = function () {
    console.log("Connected to chat socket");
  };
  socket.onclose = function () {
    console.log("Disconnected from chat socket");
  }
});