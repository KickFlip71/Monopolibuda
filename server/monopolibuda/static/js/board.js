var move_player = function(order, position){
  $('#player'+order).appendTo("#pos"+position)
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

var set_bought = function(property_set){
  property_set.forEach(property => {
    $('#pos'+property.card.position).addClass('bought')
  });
}