function handleToGroupSearch() {
    handleOverLay(true);
    $.post('js-search-to-groups-add',
            $(".add-group-membership").serialize(),
            function (data) {
                $('#js-search-to-groups-add').html(data);
                handleOverLay(false);
            }
    );
}

// (editTimeRange und saveTimeRange verschoben nach ../../../skins/unitracc_resource/custom.js;
// mittelfristig ersetzen durch vernünftige API-Lösung)

$(document).ready(
    function () {
        $('.add-to-group-search-button').live("click", function (e) {
            $('#b_start').attr('value', '0');
            handleToGroupSearch();
        });

        $(document).keypress(function (e) {
            var k = e.keyCode || e.which;
            if (k == 13) {
                handleToGroupSearch();
                return false;
            }
        });

        if ($('.user-management-search-field').attr('value') != '') {
            handleToGroupSearch();
        }
});
