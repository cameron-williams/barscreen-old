$(document).ready(function(){
    // Initialize datatables
    table = $('#users_table').DataTable();
    channels_table = $('#channels_table').DataTable();
    shows_table = $('#shows_table').DataTable();

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
});
