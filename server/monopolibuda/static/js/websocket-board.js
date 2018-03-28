$(function () {
  // Correctly decide between ws:// and wss://
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + "/game/stream/";
  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  window.socket = socket;

  socket.onmessage = function (message) {
    debugger
    data = JSON.parse(message.data)
    console.log(data)
    command = data.command
    if(command == "move"){
      //TODO: temporary
      var current_position = $("#player"+data.player_id).parent().attr('id').slice(3);
      var new_position = (parseInt(current_position) + parseInt(data.response)) % 24
      move_pointer(data.player_id, new_position)
    }
    else
      console.log("Got websocket message " + data);
  };

  socket.onopen = function () {
    console.log("Connected to socket");
  };
  socket.onclose = function () {
    console.log("Disconnected from socket");
  }
});