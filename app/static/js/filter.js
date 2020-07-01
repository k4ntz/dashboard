$(document).ready(function(){
$(".filter_checkbox").on("click", function() {
name_list = []
$(".process_name").show()
var flag = 1
$("input:checkbox[name=color]").each(function(){
    if ($(this)[0].checked == false){
      flag = 0;
      var value = $(this).val();
        $(".process_name").filter(function() {
            if($(this).context.className.split(/\s+/).indexOf($(value).selector) > -1)
            $(this).hide()
      });
    }
      $(".smi_table tr").each(function() {
         $(this).show();
       });
   });
   $("input:checkbox[name=user]").each(function(){
       if ($(this)[0].checked == false){
        flag = 0;
        var value = $(this).val();
          $(".process_name").filter(function() {
               if($(this).context.className.split(/\s+/).indexOf($(value).selector) > -1)
              $(this).hide()
        });
       }
         $(".smi_table tr").each(function() {
            $(this).show();
          });
       });


 $(".smi_table tr").each(function() {
    // Within tr we find the last td child element and get content
    var j = 0;
    for (var i = 0; i < this.children.length; i++) {
        if($(this.children[i]).is(":visible"))
        j++;
    }
    if(j < 2)
    $(this).hide();
  });
  if(flag == 1)
    $(".process_name").show()
});
});
