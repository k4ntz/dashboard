$('#form').on('submit', function(e){
  e.preventDefault();
  $.ajax({
    url: 'http://127.0.0.1:5000/retrieve_smis/',
    method: 'POST',
    success: function(data) {
      $('#smi_pprocesses').html(data['msg']).css("color", data['color'])
      document.getElementById("refresh_smi").style.display = "none";
    }
  });
});
