$(function () {
  var move = function(id, position){
    $('#player'+id).appendTo("#pos"+position)
  }

  window.move = move;
});