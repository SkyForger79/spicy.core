function process_response(api_response){
    if (api_response.code == 'error'){
	Growl.error({title:"Error!", text: api_response.errors.join('<br/>')});
    } else if (api_response.code == 'success'){
	Growl.success({title:"Success!", text: api_response.messages.join('<br/>')});
    }
}

function post_form(form_id){
    var form = $(form_id);
    
    $.post(form.attr('action'), form.serialize(), function(data){                
	    process_response(data);
        });
}    

function call_method(url){	
    $.get(url, function(data){                
	    process_response(data);
        });
}