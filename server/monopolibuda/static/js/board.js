var new_player = function(player_id) {
  $("<div class='pointer' id='player"+player_id+"'></div>").appendTo("#pos0")
}

var move_pointer = function(id, position){
  $('#player'+id).appendTo("#pos"+position)
}