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

var set_bought = function(property_set){
  property_set.forEach(property => {
    $('#pos'+property.card.position).addClass('bought')
  });
}