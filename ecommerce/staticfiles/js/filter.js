
$('document').ready(function () {

    $(".addToWishButton").off("click").on("click", function () {
        pid = $(this).data('pid');
        pImage = $(this).data('image');
        pTitle = $(this).data('title');
        pPrice = $(this).data('price');
        console.log(pid);

        let url = $(this).data("url");
        let product = { 'pid': pid, "pImage": pImage, "pTitle": pTitle, "pPrice": pPrice }
        $.ajax({
            url: url,
            data: product,
            success: function (response) {
                $(this).html(`<i class="fa-solid fa-check"></i>`);
                $("#wishIcon").attr("data-notify", response.length);
                // console.log(response.data.length)

            }
        })

        // $(`.cartButton${pid}`).html = "Added to Cart";
    });

    $(".addToWishilist").off("click").on("click", function () {
        pid = $(this).data('pid');
        pImage = $(this).data('image');
        pTitle = $(this).data('title');
        pPrice = $(this).data('price');
        pQuntity = $(this).data('quntity')

        $(this).html("Added To Cart");
        let url = $(this).data("url");
        let product = { 'pid': pid, "pImage": pImage, "pTitle": pTitle, "pPrice": pPrice, "pQuntity": pQuntity }
        $.ajax({
            url: url,
            data: product,
            success: function (response) {
                $(".cartIcon").attr("data-notify", response.data.length);
                // console.log(response.data.length)

            }
        })

        // $(`.cartButton${pid}`).html = "Added to Cart";
    });


    $(".filterProducts, #rangeButton").on("click", function () {

        current_val = $('#customRange').val();

        min_val = $('#customRange').attr('min');
        max_val = $('#customRange').attr('max');




        let filter = {};

        filter['min'] = min_val;
        filter['max'] = max_val;
        filter['current'] = current_val;


        filter['category'] = Array.from(document.querySelectorAll('input[data-filter=category]:checked')).map(function (ele) {
            return ele.value
        });
        filter['vendor'] = Array.from(document.querySelectorAll('input[data-filter=vendor]:checked')).map(function (ele) {
            return ele.value
        });
        $.ajax({
            url: "filter-products/",
            data: filter,
            dataType: "json",
            success: function (response) {
                $("#filterBox").html(response.data)
            }
        })
    })
})