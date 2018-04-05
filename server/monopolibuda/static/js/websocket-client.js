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
      if(command == "playerdata"){
        user_id = data.payload.user.id;
        //{balance, properties: {[card_id,buildings,deposited,name,cost,apartment_cost,hotel_cost,deposit_value,group,a0,a1,a2,a3,a4,a5]}}
        $('#balance').html(data.payload.balance);
        
        data.payload.property_set.forEach(property => {
          $('#properties').append(getPreparedCard(property));
        });

        //mockup data:
      //   $('#properties').append(getPreparedCard({"card_id":2,"buildings":0,"deposited":true,"name":"Budynek B-4","cost":2999,"apartment_cost":500,"hotel_cost":1000,"deposit_value":1000,"group":1,"a0":100,"a1":300,"a2":1000,"a3":3000,"a4":6000,"a5":9000}));
      //   $('#properties').append(getPreparedCard({"card_id":4,"buildings":1,"deposited":false,"name":"Budynek A-1","cost":2999,"apartment_cost":500,"hotel_cost":1000,"deposit_value":1000,"group":3,"a0":100,"a1":300,"a2":1000,"a3":3000,"a4":6000,"a5":9000}));
      //   showPreparedPropertyBuyModal({"card_id":4,"buildings":1,"deposited":false,"name":"Budynek A-1","cost":2999,"apartment_cost":500,"hotel_cost":1000,"deposit_value":1000,"group":3,"a0":100,"a1":300,"a2":1000,"a3":3000,"a4":6000,"a5":9000});
      }
      else if(command=="offer"){
        showPreparedPropertyBuyModal(data.payload.offer);
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

  function getPreparedCard(property){
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

  function showPreparedPropertyBuyModal(property){
    var modal = $('#cardModal');

    
    modal.find('.deposit_value').html(property.deposit_value);
    modal.find('.apartment_cost').html(property.apartment_cost);
    modal.find('.hotel_cost').html(property.hotel_cost);
    modal.find('.a0').html(property.a0);
    modal.find('.a1').html(property.a1);
    modal.find('.a2').html(property.a2);
    modal.find('.a3').html(property.a3);
    modal.find('.a4').html(property.a4);
    modal.find('.a5').html(property.a5);
    modal.find('.cost').html(property.cost);
    modal.find('.name').remove();
    modal.find('.table').before("<button class='name btn group text-white color-group-"+property.group+"'  type='button'>"+property.name+"   <span class='badge badge-secondary deposited hidden'>Deposited</span></button>")
    if (property.deposited){
      modal.find('.deposited').removeClass('hidden');
    }
    else{
      modal.find('.deposited').addClass('hidden');
    }
    modal.modal('show');
  }