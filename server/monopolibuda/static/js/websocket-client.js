$(function () {
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/game/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);
    var user_id;

    window.socket = socket;
  
    socket.onmessage = function (message) {
      data = JSON.parse(message.data)
      command = data.command
      if(command == "player_join"){
        user_id = data.payload.user.id;
        $('#balance').html(data.payload.balance);
        debugger;
        data.payload.property_set.forEach(property => {
          $('#properties').append(getPreparedCard(property));
        });
      }
      else if(command=="player_offer"){
          showPreparedPropertyBuyModal(data.payload.offer);
      }
      
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