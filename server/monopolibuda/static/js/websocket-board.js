$(function () {
  // Correctly decide between ws:// and wss://
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + "/game/stream/";
  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  window.socket = socket;

  socket.onmessage = function (message) {
    data = JSON.parse(message.data)
    command = data.command

    if(command=="check"){
      data.payload.player_set.forEach(player => {
        console.log(player);
        add_player(player.id,player.position);
      });
    }
    else if(command=="board_join"){
      add_player(data.payload.id,data.payload.position);
    }
    else if(command=="board_move"){
      move_player(data.payload.id,data.payload.position)
    }
    else if(command=="disconnect"){
      move_player(data.payload.id,data.payload.position)
    }
  };

  socket.onopen = function () {
    console.log("Connected to socket");
    window.socket.send(JSON.stringify({
      "command": "check",
  }));
  };
  socket.onclose = function () {
    console.log("Disconnected from socket");
  };
});