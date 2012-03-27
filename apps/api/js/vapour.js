
jQuery.fn.vapour = function() {

    var form = $(this);

    form.validate({
        rules: {
            uri: {
                required: true,
                url: true
            }
        }
    });

    form.submit(function() {
        if ($(this).valid()) {
            var uri = $("input#uri").val();
            alert(uri);
            return false;
        } else {
            return false;
        }
    });

}

