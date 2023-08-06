function handleDownloadSubmit() {
    $('#search-form').attr('action', '/@@usermanagement/download_users');
    $('#search-form').submit();
}

function handleSearchSubmit() {
    handleOverLay(true);
    $.post('js-listing-user',
            $('#search-form').serialize(),
            function (data) {
                $('#js-listing-user').html(data);
                $('#buttons').hide();
                handleOverLay(false);
            }
    );
}


$(document).ready(
    function () {
        $('#getLocked').live("change", function (e) {
            handleSearchSubmit();
        });

        $(document).on('click', '#delete-user', function (e) {
            $('#submit-form').each(function () {
                $(this).attr('action', '/manage_users_delete');
                $(this).submit();
            })
        });

        $(document).on('click', '#lock-users', function (e) {
            $('#submit-form').each(function () {
                $(this).attr('action', '/manage_users_lock');
                $(this).submit();
            })
        });

        $(document).on('click', '#unlock-users', function (e) {
            $('#submit-form').each(function () {
                $(this).attr('action', '/manage_users_unlock');
                $(this).submit();
            })
        });

        $('.sortable-serverside').live("click", function (e) {
            if ($('#sort_on').attr('value') == $(e.target).attr('rel')) {
                if ($('#sort_order').attr('value') == '') {
                    $('#sort_order').attr('value', 'reverse');
                } else {
                    $('#sort_order').attr('value', '');
                }

            } else {
                $('#sort_order').attr('value', '');
            }
            $('#sort_on').attr('value', $(e.target).attr('rel'));
            handleSearchSubmit();
        });


        $('button #appendedInputButton').live("click", function (e) {
            e.preventDefault();
            $('#b_start').attr('value', '0');
            handleSearchSubmit();
            return false;
        });

        $('#user-download').live("click", function (e) {
            handleDownloadSubmit();
            return false;
        });

        $('.user-uids').live("click", function (e) {
            //alle ausgewählt
            if ($(e.target).attr('id') == 'all_users') {
                // Funktion aus select_all.js, Products.CMFPlone:
                toggleSelect(e.target, 'uids:list')
            }
            // mindestens ein Element ausgewählt
            if ($('.user-uids input:checked').length > 0) {
                $('#buttons').show();
            } else {
                $('#buttons').hide();
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
