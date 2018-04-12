var move_player = function(player_id, position){
  $('#player'+player_id).appendTo("#pos"+position)
}

var add_player = function(player_id, position) {
  if($('#player'+player_id).length==0){
    $("<div class='pointer' id='player"+player_id+"'></div>").appendTo("#pos"+position)
  }
}

var disable_player = function(player_id){
  $('#player'+player_id).addClass('player_disconnected')
}

