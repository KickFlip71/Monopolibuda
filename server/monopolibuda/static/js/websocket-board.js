$(function () {
  // Correctly decide between ws:// and wss://
  var current_player = null  
  var code = getUrlParameter('code')
  var game_id = getGameId()
  var websocket_channel = "/game/stream/"+game_id+"/"+code

  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + websocket_channel;
  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  window.socket = socket;

  socket.onmessage = function (message) {
    data = JSON.parse(message.data)
    console.log(data)
    command = data.command
    if(command=="check"){
      data.payload.player_set.forEach(player => {
        add_player(player.order,player.position);
        set_bought(player.property_set)
      });
      $("#start-button").prop('disabled', data.payload.active)
    }
    else if(command=="start"){
      $("#start-button").prop('disabled', data.payload.active)
    }
    else if(command=="board_join"){
      add_player(data.payload.order,data.payload.position);
      set_bought(data.payload.property_set)
    }
    else if(command=="board_move"){
      console.log(data.payload.order)
      move_player(data.payload.order,data.payload.position)
    }
    else if(command=="board_end"){
      disconnect_player(data.payload.order)
      set_bought(data.payload.property_set,bought=false)
    }
    else if(command=="disconnect"){
      remove_player(data.payload.id,data.payload.position)
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

var getUrlParameter = function getUrlParameter(sParam) {
  var sPageURL = decodeURIComponent(window.location.search.substring(1)),
      sURLVariables = sPageURL.split('&'),
      sParameterName,
      i;

  for (i = 0; i < sURLVariables.length; i++) {
      sParameterName = sURLVariables[i].split('=');

      if (sParameterName[0] === sParam) {
          return sParameterName[1] === undefined ? true : sParameterName[1];
      }
  }
};

var getGameId = function(){
  return /\/\d*\//g.exec(window.location.pathname)[0].substr(1).slice(0, -1);
}