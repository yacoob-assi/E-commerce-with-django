$('document').ready(function () {
    let totalCartPrice = parseFloat($("#totalCartPrice").text());


    $('.remove-wish').on("click", function () {

        pid = $(this).data('pid')
        console.log(pid)
        $.ajax({
            url: $(this).data('url'),
            data: { "pid": pid },
            success: function (response) {

                $(`#wish-pro${product.id}`).remove()
                $("#wishIcon").attr("data-notify", response.length);


            }
        })
    })

    $('.delete-cart-button').on("click", function () {

        pid = $(this).data('id')
        price = parseFloat($(this).data('price'))
        total = parseFloat($("#total-price-list").text())
        console.log(total)
        $.ajax({
            url: $(this).data('url'),
            data: { "id": pid, "price": price },
            success: function (response) {
                if (response['data']) {
                    $(`#li-${pid}`).remove()
                    $(".cartIcon").attr("data-notify", response.length)
                    price = total - price

                    $("#total-price-list").html(price.toFixed(2))
                    $(`#addToCartButton-${pid}`).html(`<i class="fas fa-shopping-cart me-2"></i> Add to Cart`)
                }
            }
        })
    })

    $(".changeCart").off("click").on("click", function () {
        $("#updateCardButton").removeClass("added-to-cart");
        $("#updateCardButton").html("UPDATE CART");
        let pid = $(this).data('id');
        let totalEle = $(`#total-price${pid}`);
        let price = parseFloat($(this).data("price"));
        let count = parseFloat($(`#input${pid}`).val());
        let totalPrice = parseFloat(totalEle.text());

        console.log(totalCartPrice)

        let type = $(this).data("type")
        if (type == "m" && totalPrice > 0) {
            totalCartPrice -= price;
            totalPrice -= price;
            count--;


        }
        else if (type == "p") {
            totalCartPrice += price;
            totalPrice += price;
            count++;



        }

        $("#totalCartPrice").html(Math.max(0, totalCartPrice).toFixed(2));
        totalEle.html(Math.max(0, totalPrice).toFixed(2));

        $(`#input${pid}`).val(count)


    })

    $("#updateCardButton").on("click", function () {
        let products = [];

        $(".num-product").each(function () {
            let pid = $(this).data('pid');
            let quntity = $(this).val();
            let totalPrice = $(`#total-price${pid}`).text();
            products.push({ "pid": pid, "quntity": quntity, "totalPrice": totalPrice });
        });
        let url = $(this).data("url");
        $.ajax({
            url: url,
            data: { 'cartProducts': JSON.stringify(products), "totalCartPrice": totalCartPrice }, // Ensure data is correctly serialized
            success: function (response) {
                $("#updateCardButton").addClass("added-to-cart");
                $("#updateCardButton").html("Cart updated");

            }

        });
    });

})