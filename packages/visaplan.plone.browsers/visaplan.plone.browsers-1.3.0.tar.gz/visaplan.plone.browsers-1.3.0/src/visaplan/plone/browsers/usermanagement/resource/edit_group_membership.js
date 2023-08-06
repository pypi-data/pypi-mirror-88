function handleGroupSearch() {
    handleOverLay(true);
    $.post('js-search-groups-add',
            $(".add-group-membership").serialize(),
            function (data) {
                $('#js-search-groups-add').html(data);
                handleOverLay(false);
            }
    );
}

$(document).ready(
    function () {
        $('.add-group-membership-search-button').live("click", function (e) {
            e.preventDefault();
            handleGroupSearch();
        });

        $(document).keypress(function (e) {
            var k = e.keyCode || e.which;
            if (k == 13) {
                handleGroupSearch();
                return false;
            }
        });

        if ($('.user-management-search-field').attr('value') != '') {
            handleGroupSearch();
        }

});
