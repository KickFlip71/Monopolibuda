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
        //{balance, properties: {[card_id,buildings,deposited,name,cost,apartment_cost,hotel_cost,deposit_value,group,a0,a1,a2,a3,a4,a5]}}
        $('#balance').html(data.balance);
        //data.properties.forEach(element => {
          //var property = $("");
          //$('#properties').append(property);
        //});

        //mockup data:
        $('#properties').append(prepareCard(JSON.parse('{"card_id":2,"buildings":0,"deposited":true,"name":"Budynek B-4","cost":2999,"apartment_cost":500,"hotel_cost":1000,"deposit_value":1000,"group":1,"a0":100,"a1":300,"a2":1000,"a3":3000,"a4":6000,"a5":9000}')));
        $('#properties').append(prepareCard(JSON.parse('{"card_id":4,"buildings":1,"deposited":false,"name":"Budynek A-1","cost":2999,"apartment_cost":500,"hotel_cost":1000,"deposit_value":1000,"group":3,"a0":100,"a1":300,"a2":1000,"a3":3000,"a4":6000,"a5":9000}')));
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

  function prepareCard(property){
    var template = $('.template').clone();
    var cardHeader = template.find('.card-header');
    var title = template.find('.title');
    var cardBody = template.find('.collapse');

    template.removeClass('template');
    cardHeader.addClass('color-group-'+property.group);
    title.html(property.name);
    title.attr('data-target', '.card-'+property.card_id+'.collapse');
    template.attr('id', 'card-'+property.card_id);
    cardBody.addClass('card-'+property.card_id);

    if (property.deposited){
      template.find('.deposited').removeClass('hidden');
    }
    template.find('.buildings').html(property.buildings);
    template.find('.deposit_value').html(property.deposit_value);
    template.find('.apartment_cost').html(property.apartment_cost);
    template.find('.hotel_cost').html(property.hotel_cost);
    template.find('.a0').html(property.a0);
    template.find('.a1').html(property.a1);
    template.find('.a2').html(property.a2);
    template.find('.a3').html(property.a3);
    template.find('.a4').html(property.a4);
    template.find('.a5').html(property.a5);
    template.find('.cost').html(property.cost);
    
    return template;
  }