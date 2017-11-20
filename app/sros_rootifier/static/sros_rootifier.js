$(function() {
    $('#submit_form').click(function() {
        // start showing loading animation
        $.LoadingOverlay("show", {
                        image       : "",
                        fontawesome : "fa fa-cog fa-spin"
                        })
        var data = {}
        data ["cfg"] = $('#raw_config_area').val()
        $.ajax({
            url: window.location.pathname, // url: /int_helpers/conf_rootifier
//            data: $('#raw_config_area').val(),
            data: data,
            type: 'POST',
            success: function(response) {
                $.LoadingOverlay("hide");
                if (response.error != "") {
                    $('#output_div').html(response.error)
                } else {
                    $('#output_config_area').val(response.output_data)
                    $('a[href="#output_cfg_tab"]').tab('show')
                }
            }
        });
    });
});