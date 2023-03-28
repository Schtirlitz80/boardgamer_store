$(document).ready(function (){
    console.log('j01. document.ready')
    let form = $('#form_buying_product');
    let form2 = $('#nav_basket');


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrf_token = getCookie('csrftoken');


    function basketUpdating(product_id, nmb, is_delete){
        let data = {};  // Данные, которые будем передавать в POST запросе
        data.product_id = product_id;
        data.nmb = nmb;
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data["is_delete"] = true;
        }
        console.log('3data: ', data)

        let url = form.data("action"); // Адрес, на который ajax будет отправлять POST-запрос
        console.log(typeof url)
        if (url == undefined){
            url = form2.data('action');
        };

        // console.log(data)
        $.ajax({
            url: url, // куда отправляем запрос
            type: 'POST', // тип запроса
            data: data,     // данные, которые мы будем отправлять
            cache: true,
            success: function (data) {      // функция, которая вызывается, если получен ответ от сервера
                //TODO: Почему-то одинаковые артикулы в раскрывающемся списке.
                if (data.products_total_nmb || data.products_total_nmb == 0){
                    $('#basket_total_nmb').text('(' + data.products_total_nmb + ')');
                    $('.basket-items ul').html('');
                    $.each(data.products, function (k, v){
                        $('.basket-items ul').append('<li class="basket-items"><a class="dropdown-item" href="#">Арт.'+
                            product_id + ' <b>' + v.name + '</b> - ' + v.nmb + ' шт. * ' + v.price_per_item + ' руб.</a>' +
                            '<button type="button" class="btn-close delete-item" aria-label="Close" data-product_id="' +
                            v.product_id + '"></button></li>')
                    });
                }
            },
            error: function (){
                console.log("error")
            }
        })
    }

    //Срабатывает при нажатии кнопки "Купить" в форме с товаром
    form.on('submit', function (e){
        e.preventDefault();
        let nmb = $('#number').val();
        let submit_btn = $('#submit_btn');
        let product_id = submit_btn.data("product_id");
        let product_name = submit_btn.data("name");
        let product_price = submit_btn.data("price");

        basketUpdating(product_id, nmb, is_delete=false);
    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true);
    });
});