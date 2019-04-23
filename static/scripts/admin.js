$(document).ready(function(){
    // Initialize datatables
    table = $('#users_table').DataTable();
    channels_table = $('#channels_table').DataTable();
    shows_table = $('#shows_table').DataTable();
    content_table = $('#clip_table').DataTable();
    clip_table = $('#clip_dash').DataTable();

    /* Handle button for approving users */
    $("#users_table tbody").on('click', 'button', function() {
        var row_data = table.row($(this).parents('tr')).data();
        if (row_data[2] == "False") {
            $.ajax({
                url: post_url,
                method: "POST",
                data: JSON.stringify({"email": row_data[1]}),
                dataType: "json",
                contentType: "application/json",
                success: function(data){alert("Approved " + row_data[0] + " successfully.")},
                error: function(errMsg){alert("Error approving account: " + errMsg)},
            })
        } else {
            alert("Account already confirmed.")
        }
    });
    /* Adding Loops */

    $("#clip_table tbody").on('click', 'button', function() {
        var row_data = content_table.row($(this).parents('tr')).data();
        var content_name = row_data[1];
        var content_type = row_data[0];
        var content_id = row_data[3];
        var ul = $("#loop_content");
        var tr = $("<tr></tr>").append("<td>"+content_name+"</td><td>"+content_type+"</td><td>"+content_id+"</td>")
        ul.append(tr);
    });

    var array = [];
    var headers = [];
    $(".save_container").on('click', 'button', function() {
        $('#loop_content').has('tr').each(function() {
          var loop_type = $('#loop_content td:nth-child(2)').map(function(){
            return $(this).text();})
          var loop_id = $('#loop_content td:nth-child(3)').map(function(){
            return $(this).text();});
          for (var i=0; i<loop_id.length && i<loop_type.length; i++)
            array[i] = loop_type[i] + loop_id[i];
          console.log(array);
        });
        var loopname = $("#loop_name").val();
        console.log(array);
        console.log("success");
        console.log(loopname);
        $.ajax({
            url: post_url,
            method: "POST",
            data: JSON.stringify({"name": loopname, "playlist": array, "user_id": user_id}),
            dataType: "json",
            contentType: "application/json",
            success: function(data){alert("Sumbited " + loopname + " successfully.")},
            error: function(errMsg){alert("Sorry: " + errMsg)},
        });
    });
});

$(document).on('click','#loop_content tr',function(){
  $(this).remove();
});
