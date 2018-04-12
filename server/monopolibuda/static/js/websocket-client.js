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
      success = handleError(data['status'])
      if(command == "player_join" && success){
        user_id = data.payload.user.id;
        //{balance, properties: {[card_id,buildings,deposited,name,cost,apartment_cost,hotel_cost,deposit_value,group,a0,a1,a2,a3,a4,a5]}}
        updateBalance(data.payload.balance)        
        data.payload.property_set.forEach(property => {
          $('#properties').append(getPreparedCard(property));
        });
      }
      else if(command=="player_offer" && success){
        showPreparedPropertyBuyModal(data.payload.offer);
      }
      else if(command=="player_move"){
        updateBalance(data.payload.balance)
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
