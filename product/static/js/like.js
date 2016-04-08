$(function() {
  $('.send-like').click(function(e){
    $.post('/like/'+productId,{}, function(data){
      console.log(data.django_messages);})
      .done(function(data) {
        var actionType = '',
            messages =$('.messages');
        $.each(data.django_messages, function (i, item) {
          var tag ='<p class="'+item.extra_tags+'">'+item.message+'</p>';
          actionType = actionType +item.extra_tags;
          messages.html('');
          messages.append(tag);
          $('.messages').show();
        });
        var vote_val = $('#like_for_'+productId);
        if(actionType.indexOf('add') > -1){
          vote_val.html(parseInt(vote_val.text()) + 1);
        } else{
          vote_val.html(parseInt(vote_val.text()) - 1);
        }
      })
      .fail(function(data) {
        $.each(data.django_messages, function (i, item) {
          var tag ='<p class="'+item.extra_tags+'">'+item.message+'</p>';
          $('.messages').append(tag);
        });
      });
    setTimeout(function() {$('.messages').hide()}, 1000);
  });
});