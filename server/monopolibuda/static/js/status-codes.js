var status_codes = 
{
  1000: 'OK',
  1001: 'Joined',
  1002: 'Leave',
  1003: 'Skip Turn',
  1004: 'Move',
  2000: 'Unspecified Error',
  2001: 'Game not found',
  2002: 'Player not found',
  2003: 'User not found',
  2004: 'Player already exists',
  2005: 'Card not found',
  2006: 'Card is occupied',
  2007: 'Property does not exist',
  2010: 'Cannot skip',
  2011: 'Cannot move',
  2012: 'Player cannot afford',
  2014: 'Max buildings reached',
  2015: 'Min buildings reached',
  2016: 'Property is deposited'
}

var handleError = function(status) {
  status = String(status)
  if(status.length != 4)
    return false 
  
  var success = status[0] == '1'
  
  if(!success) {
    $.toast({
      heading: 'Error',
      text: status_codes[status],
      position: 'bottom-center',
      stack: false,
      icon: 'error',
      loader: false,
      hideAfter: 2000
    })
  }
  else { //TODO: DEBUG ONLY
    $.toast({
      heading: 'Success',
      text: status_codes[status],
      position: 'bottom-center',
      stack: false,
      icon: 'success',
      loader: false,
      hideAfter: 100
    })
  }

  return success
}