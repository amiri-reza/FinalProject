$(function() {
    var username = "{{ user.first_name }}";
    $('.chatbot-btn').on('click', function() {
      $('#chatbot-modal').modal('show');
    });
  
    $('#chatbot-modal').on('hidden.bs.modal', function () {
      $(this).find('.chat-area').empty();
      $('.modal-backdrop').remove();
    });
  
    $('#chatbot-form').submit(function(event) {
      event.preventDefault();
      var ticker = $('#ticker').val();
      var statement = $('#statement').val();
      send_message(ticker, statement);
      $('#ticker').val('');
      $('#statement').val('');
    });
  
    function send_message(ticker, statement) {
      console.log('send_message called');
      $.ajax({
        url: '/home/chatbot/',
        type: 'POST',
        data: {
          'ticker': ticker,
          'statement': statement,
          'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        dataType: 'json',
        success: function(data) {
          display_message(username, statement);
          display_message('Trado', data.response);
        },
        error: function(xhr, status, error) {
          console.log('Error: ' + error.message);
        }
      });
    }
  
    function display_message(sender, message) {
      var chat_area = $('.chat-area');
      var message_div = $('<div>', {'class': 'message'});
      var sender_div = $('<div>', {'class': 'message-sender'});
      var text_div = $('<div>', {'class': 'message-text'});
      sender_div.text(sender + ':');
      text_div.text(message);
      message_div.append(sender_div).append(text_div);
      chat_area.append(message_div);
      chat_area.scrollTop(chat_area.prop('scrollHeight'));
    }
  });