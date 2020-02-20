$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#agregarUsuarios').modal('show');
			},
			success: function(data){
				$('#agregarUsuarios.modal-content').html(data.html_form);
			}
		});
	};
})