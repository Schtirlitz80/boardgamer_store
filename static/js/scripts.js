$(document).ready(function (){
    let form = $('#form_buying_product');
    console.log(form);

    form.on('submit', function (e){
        e.preventDefault();
        let nmb = $('#number').val();
        console.log('Quantity: ', nmb);
        let submit_btn = $('#submit_btn');
        let product_id = submit_btn.data("product_id");
        let product_name = submit_btn.data("name");
        let product_price = submit_btn.data("price");
        console.log('product: ', product_id);
        console.log('product name: ', product_name);
        console.log('product price: ', product_price);

        let data = {};
        data.product_id = product_id;
        data.nmb = nmb;

        let csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        let url = form.attr("action");

    // console.log(data)
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log('OK');
                console.log(data.products_total_nmb);
                if (data.products_total_nmb){
                    $('#basket_total_nmb').text('(' + data.products_total_nmb + ')');
                }
            },
            error: function (){
                console.log("error")
            }
        })

        $('.basket-items ul').append('<li class="basket-items"><a class="dropdown-item" href="#">Арт.'+
            product_id + ' <b>' + product_name + '</b> - ' + nmb + ' шт. * ' + product_price + ' руб.</a>' +
            '<button type="button" class="btn-close delete-item" aria-label="Close"></button></li>')
    });

    $(document).on('click', '.delete-item', function (){
        $(this).closest('li').remove();
    });
});