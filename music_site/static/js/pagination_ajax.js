
function ajaxPaginationInit(selector='#ajax-paginated') {
    let page = 1;
    let empty_page = false;
    let block_request = false;

    $(window).scroll(function () {
        let offset = $(document).height() - $(window).height() - 100;

        if ($(window).scrollTop() > offset && !empty_page && !block_request) {
           let request_get = getUrlAsDict();
           let max_items = request_get['max_items'];
           let new_request_get = '?';

           block_request = true;

           if (max_items !== undefined)
               new_request_get += `max_items=${max_items}`;
           new_request_get += `&page=${++page}`;

           $.get(`${getUrlPath()}${new_request_get}`, function (data) {
               if (data && data.length !== 0)
                   $(selector).append(data);
               else
                   empty_page = true;

               block_request = false;
           });
        }
    });
}