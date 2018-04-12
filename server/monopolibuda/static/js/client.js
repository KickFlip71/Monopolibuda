var getPreparedCard = function(property){
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

  var showPreparedPropertyBuyModal = function(property){
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