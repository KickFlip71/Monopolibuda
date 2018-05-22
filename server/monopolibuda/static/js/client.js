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

var showPreparedPropertyBuyModal = function(property, rebuy=false){
  if(rebuy){
    var modal = $('#cardModal').clone()
    modal.removeAttr('id')
    $('.modal-rebuy-offer').remove()
    modal.addClass('modal-rebuy-offer')
    var real_property = property
    property = property.card
  }
  else{
    var modal = $('#cardModal')
  }
  

  
  modal.find('.deposit_value').html(property.deposit_value);
  modal.find('.apartment_cost').html(property.apartment_cost);
  modal.find('.hotel_cost').html(property.hotel_cost);
  modal.find('.a0').html(property.charge.zero_apartments);
  modal.find('.a1').html(property.charge.one_apartments);
  modal.find('.a2').html(property.charge.two_apartments);
  modal.find('.a3').html(property.charge.three_apartments);
  modal.find('.a4').html(property.charge.four_apartments);
  modal.find('.a5').html(property.charge.five_apartments);
  
  if(rebuy){
    modal.find('.cost').html(real_property.selling_price)
    modal.find('.buildings').html(real_property.buildings)
    modal.find('.hidden-card-id').html(property.id)
    modal.find('#buy-card-button').remove()
    modal.find('.hidden').removeClass('hidden')
  }
  else{
    modal.find('.cost').html(property.cost)
  }
  modal.find('.name').remove();
  modal.find('.table').before("<button class='name btn group text-white color-group-"+property.group_number+"'  type='button'>"+property.name+"   <span class='badge badge-secondary deposited hidden'>Deposited</span></button>")
  if(rebuy){
    if (real_property.deposited){
      modal.find('.deposited').removeClass('hidden')
    }
  }
  modal.modal('show')
  if(rebuy){
    $('#cardModal').before(modal)
  }
}

function updateBalance(money) {
  $('#balance').html(money)
}

function fixBalance(money) {  // i am also ashamed
  var temp = $('#balance').text()
  var temp2 = parseInt(temp)+money
  $('#balance').html(temp2)
}

function updateBuildingsCount(card_id, new_value){
  $('#card-'+card_id+' .buildings').html(new_value)
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

var chance = function(chance){
  $.toast().reset('all')
  $.toast({
    heading: chance.description, // Optional heading to be shown on the toast
    text: chance.value,
    showHideTransition: 'fade', // fade, slide or plain
    allowToastClose: true, // Boolean value true or false
    hideAfter: false, // false to make it sticky or number representing the miliseconds as time after which toast needs to be hidden
    stack: false, // false if there should be only one toast at a time or a number representing the maximum number of toasts to be shown at a time
    position: 'mid-center', // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values
    
    bgColor: '#444444',  // Background color of the toast
    textColor: '#eeeeee',  // Text color of the toast
    textAlign: 'center',  // Text alignment i.e. left, right or center
    loader: true,  // Whether to show loader or not. True by default
    loaderBg: '#9EC600',  // Background color of the toast loader
    beforeShow: function () {}, // will be triggered before the toast is shown
    afterShown: function () {}, // will be triggered after the toat has been shown
    beforeHide: function () {}, // will be triggered before the toast gets hidden
    afterHidden: function () {}  // will be triggered after the toast has been hidden
  })
}