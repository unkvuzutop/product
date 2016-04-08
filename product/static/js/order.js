$(function() {
  $('.selectpicker').on('change', function(){
    var selected = $(this).find("option:selected").val();
    window.location.href = '?order_by='+selected;
  });
});