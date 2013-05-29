$(document).ready(function()
		  {
		      //Style selects, checkboxes, etc
		      $("select, input:file").uniform();
 
		      //Date and Range Inputs
		      $("#id_deadline").rangeinput()
 
		      $.tools.validator.localize("ru", {
			  '*': 'Пожалуйста, исправьте это значение',
			  ':email': 'Пожалуйста, введите корректный адрес электронной почты',
			  ':number': 'Пожалуйста, введите численное значение',
			  ':url': 'Пожалуйста, ввелите корректный URL адрес',
			  '[max]': 'Пожалуйста, введите значение меньшее чем $1',
			  '[min]': 'Пожалуйста, введите значение большее чем $1',
			  '[required]': 'Пожалуйста, заполните это обязательное поле'
  });
 
		      //Position the error messages next to input labels
		      $.tools.validator.addEffect("labelMate", function(errors, event){
			      $.each(errors, function(index, error){
				      error.input.first().parents('.field').find('.error').remove().end().find('label').after('<span class="error">' + error.messages[0] + '</span>');
				  });
			  if(errors){
			      $('.form-msg').after('<span class="error">Заполните форму</span>');
			  }
 
			  }, function(inputs){
			      inputs.each(function(){
				      $(this).parents('.field').find('.error').remove();
				  });
 
			  });
 
 
		      /**
		       * Handle the form submission, display success message if
		       * no errors are returned by the server. Call validator.invalidate
		       * otherwise.
		       */
 
		      $(".bbform").validator({effect:'labelMate', lang: 'ru'}).submit(function(e){
			      var form = $(this);
 
			      if(!e.isDefaultPrevented()){
				  $.post(form.attr('action'), form.serialize(), function(data){
 
					  if(data.status == 'success'){
					      form.fadeOut('fast', function(){
						      $('.bbform-container').append('<h2 class="success-message">Спасибо за ваше сообщение! С вами свяжутся в кратчайшие сроки.</h2>');
						  });
					      // Redirect on submit:
					      //window.location = 'http://www.example.com/somePage.html';
					  }
					  else validator.invalidate(data.errors);
 
				      }, "json");
				  e.preventDefault();
			      }
 
			      return false;
			  });
 
		      var validator = $('.bbform').data('validator');
 
 
		  });
