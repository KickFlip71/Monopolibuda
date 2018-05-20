var move_player = function(order, position){
  var interval = setInterval(function(){
    var success = move_pawn(order, position)
    if(success)
      clearInterval(interval)
    }, 300)
}

var move_pawn = function(order, position) {
  current_position = $("#player"+order).parent().attr('id').replace( /^\D+/g, '')*1
  if(current_position != position){
    current_position = (current_position + 1) % 24
    $('#player'+order).appendTo("#pos"+current_position)
  }
  return current_position == position
}

var add_player = function(order, position) {
  if($('#player'+order).length==0){
    $("<div class='pointer' id='player"+order+"'></div>").appendTo("#pos"+position)
  }
}

var disable_player = function(player_id){
  $('#player'+player_id).addClass('player_disconnected')
}

var disconnect_player = function(order) {
  $('#player'+order).remove()
}

var set_bought = function(property_set, bought=true){
  property_set.forEach(property => {
    var property_div = $('#pos'+property.card.position)
    if(bought){
      property_div.addClass('bought')
      property_div.find('div.apartments > div').each( function( index, element ){
        if(index<property.buildings){
          $(this).addClass('apartment-bought')
        }
        else{
          $(this).removeClass('apartment-bought')
        }
      })
    }
    else{
      property_div.removeClass('bought')
      property_div.find('.apartment-bought').removeClass('apartment-bought')
    }
  });
}

var winning = function(){
  $.toast({
    
    heading: 'Wygranko!', // Optional heading to be shown on the toast
    
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
    beforeHide: function () {
      window.location.replace("/")
    }, // will be triggered before the toast gets hidden
    afterHidden: function () {}  // will be triggered after the toast has been hidden
  });
}