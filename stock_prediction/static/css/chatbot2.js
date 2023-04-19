$(document).ready(function () {
    // Open the chatbot modal when the chatbot button is clicked
    $('#chatbot-btn').on('click', function () {
      $('#chatbot-modal').modal('show');
    });

    // Handle the chatbot modal close event
    $('#chatbot-modal').on('hidden.bs.modal', function () {
      // Remove the chat area messages
      $(this).find('.chat-area').empty();

      // Manually remove the modal-open class and fix the scrolling issue
      $('body').removeClass('modal-open');
      $('body').css('padding-right', '');
      $('body').css('overflow', '');
    });
  });