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
      if(command == "playerdata"){
        $('#balance').html(data.balance);
        data.properties.forEach(element => {
          var property = $("<a href='#' class='list-group-item list-group-item-action'>"+ element +"</a>");
          $('#properties').append(property);
        });
      }
      else
        console.log("Got websocket message " + data);
    };
  
    socket.onopen = function () {
        console.log("Connected to socket");
        window.socket.send(JSON.stringify({
            "command": "join",
        }));
    };
    socket.onclose = function () {
      console.log("Disconnected from socket");
    }
  });