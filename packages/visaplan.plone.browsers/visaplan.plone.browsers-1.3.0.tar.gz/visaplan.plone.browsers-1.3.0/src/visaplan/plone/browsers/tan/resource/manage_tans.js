function handleSearchSubmit() {
    handleOverLay(true);
    $.post('js-listing-course',
            $('#search-form').serialize(),
            function (data) {
                $('#js-listing-course').html(data);
                $('#delete-groups').hide();
                handleOverLay(false);
            }
    );
}

function deleteGroups() {
    $('#submit-form').attr('action', '/@@groupsharing/delete_groups');
    $('#submit-form').submit();
}

$(document).ready(
    function () {
        $('#delete-groups').live("click", function (e) {
            deleteGroups();
        });

        $('#search-button').live("click", function (e) {
            $('#b_start').attr('value', '0');
            handleSearchSubmit();
            return false;
        });

        $('.group-ids').live("click", function (e) {
            if ($('.group-ids input:checked').length) {
                $('#delete-groups').show();
            } else {
                $('#delete-groups').hide();
            }
        });

        $(document).keypress(function (e) {
            var k = e.keyCode || e.which;
            if (k == 13) {
                $('#b_start').attr('value', '0');
                handleSearchSubmit();
                return false;
            }
         });

         handleSearchSubmit();

    }
);
