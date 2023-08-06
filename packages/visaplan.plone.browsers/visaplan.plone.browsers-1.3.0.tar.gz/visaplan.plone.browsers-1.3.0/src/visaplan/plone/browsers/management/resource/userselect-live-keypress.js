function handle_user_search() {
    handleOverLay(true);
    dict_ = {}
    dict_['SearchableText'] = $('#user_id_search').attr('value');
    dict_['sort_on'] = 'getUserId';

    $.post('js_management_userselection',
           dict_,
           function (data) {
               $('#user_id_search_results').html(data);
               handleOverLay(false);
           }
    );
}

$(document).ready(function () {
    $("#user_id_search").live("click", function (event) {
        event.preventDefault()  // ?
        // $("#user_id_search").attr('value', '');
        $('#user_id_search_results').html('');
        $('#user_id_selected').show();
    });

    $(".user-select").live("click", function (event) {
        value_=$(event.target).attr('rel');
        $('#user_id').attr('value', value_);
        $.fn.show_status_message(_('Changes saved.'));
    });

    $("#user_id_search").live("keypress", function (event) {
        var code = (event.keyCode ? event.keyCode : event.which);
        if (code == 13) {
            handle_user_search();
        }
    });

    $("#user_id_search").live("click", function (event) {
        value_=$(event.target).attr('rel');
        $('#user_id').attr('value', value_);

    });

    $(document).keypress(function (e) {
        if (e.which == 13) {
            handle_user_search();
        return false;  // XXX hier oder nach dem Block?!
        }
    });

});
