$(function () {
    // Correctly decide between ws:// and wss://
    var current_player = null
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/game/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);
    var user_id;

    window.socket = socket;
  
    socket.onmessage = function (message) {
      data = JSON.parse(message.data)
      command = data.command;
      debugger;
      if(data['command'].slice(0,7) == "player_")
        success = handleError(data['status']);
      if(command == "player_join" && success){
        current_player = data.payload.order;
        user_id = data.payload.user.id;
        //{balance, properties: {[card_id,buildings,deposited,name,cost,apartment_cost,hotel_cost,deposit_value,group,a0,a1,a2,a3,a4,a5]}}
        updateBalance(data.payload.balance);
        updateButtons(data.payload.move);
        data.payload.property_set.forEach(property => {
          $('#properties').append(getPreparedCard(property));
        });
      }
      else if(command=="player_offer" && success){
        showPreparedPropertyBuyModal(data.payload);
      }
      else if(command=="player_move" && success){
        updateBalance(data.payload.balance);
        updateButtons(data.payload.move);
      }
      else if(command=="player_skip" && success){
        player = findPlayer(data.payload.player_set, current_player);
        updateButtons(player.move);
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
