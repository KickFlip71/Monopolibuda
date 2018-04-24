var getPreparedCard = function(property){
    var template = $('.template').clone();
    var cardHeader = template.find('.card-header');
    var title = template.find('.title');
    var cardBody = template.find('.collapse');

    template.removeClass('template');
    template.addClass('property');
    cardHeader.addClass('color-group-'+property.card.group_number);
    title.html(property.card.name);
    title.attr('data-target', '.card-'+property.card.id+'.collapse');
    template.attr('id', 'card-'+property.card.id);
    cardBody.addClass('card-'+property.card.id);

    if (property.deposited){
      template.find('.deposited').removeClass('hidden');
    }
    template.find('.buildings').html(property.buildings);
    template.find('.deposit_value').html(property.card.deposit_value);
    template.find('.apartment_cost').html(property.card.apartment_cost);
    template.find('.hotel_cost').html(property.card.hotel_cost);
    template.find('.a0').html(property.card.charge.zero_apartments);
    template.find('.a1').html(property.card.charge.one_apartments);
    template.find('.a2').html(property.card.charge.two_apartments);
    template.find('.a3').html(property.card.charge.three_apartments);
    template.find('.a4').html(property.card.charge.four_apartments);
    template.find('.a5').html(property.card.charge.five_apartments);
    template.find('.cost').html(property.card.cost);
    
    return template;
  }

  var showPreparedPropertyBuyModal = function(property){
    var modal = $('#cardModal');

    
    modal.find('.deposit_value').html(property.deposit_value);
    modal.find('.apartment_cost').html(property.apartment_cost);
    modal.find('.hotel_cost').html(property.hotel_cost);
    modal.find('.a0').html(property.charge.zero_apartments);
    modal.find('.a1').html(property.charge.one_apartments);
    modal.find('.a2').html(property.charge.two_apartments);
    modal.find('.a3').html(property.charge.three_apartments);
    modal.find('.a4').html(property.charge.four_apartments);
    modal.find('.a5').html(property.charge.five_apartments);
    modal.find('.cost').html(property.cost);
    modal.find('.name').remove();
    modal.find('.table').before("<button class='name btn group text-white color-group-"+property.group_number+"'  type='button'>"+property.name+"   <span class='badge badge-secondary deposited hidden'>Deposited</span></button>")
    if (property.deposited){
      modal.find('.deposited').removeClass('hidden');
    }
    else{
      modal.find('.deposited').addClass('hidden');
    }
    modal.modal('show');
  }

  function updateBalance(money) {
    $('#balance').html(money);
  }

  function updateButtons(move){
    console.log(move)
    if(move == 2){
      $("#dice-button").prop('disabled', false)
      $("#end-round-button").prop('disabled', true)
    }
    else if(move == 1){
      $("#dice-button").prop('disabled', true)
      $("#end-round-button").prop('disabled', false)
    }
    else{
      $("#dice-button").prop('disabled', true)
      $("#end-round-button").prop('disabled', true)
    }

  }

  function findPlayer(players, current_player) {
    var player = null
    $.each(players, function(k,v) {
      if(v.order == current_player){
        player = v
        return false
      }
    })
    return player
  }