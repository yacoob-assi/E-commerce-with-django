$("#reviewForm").submit(function (e) {
    e.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        method: $(this).attr('method'),
        data: $(this).serialize(),
        dataType: "json",
        success: function (response) {
            console.log(response);
            let html = `<div class="col-md-4 review-card">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex">
                                <img src="https://www.w3schools.com/w3images/avatar2.png" alt="User Image" class="review-img">
                                <div class="ms-3">
                                    <h5 class="card-title">${response.context.user.username}</h5>
                                    <p class="stars">`;
            let stars = ``;
            for (let i = 0; i < response.context.rating; i++) {
                stars += '★';
            }
            for (let i = 0; i < (5 - response.context.rating); i++) {
                stars += `☆`;

            }
            html += ` ${stars}</p>
                                    <p class="card-text">${response.context.review}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
            $('#reviews-container').append(html);
            $('#review-text').val("");
            let reviewsData = {
                1: response.context.star1,
                2: response.context.star2,
                3: response.context.star3,
                4: response.context.star4,
                5: response.context.star5,
            }
            let total_reviews = reviewsData[1] + reviewsData[2] + reviewsData[3] + reviewsData[4] + reviewsData[5];
            let stat = 0;



            for (let i = 1; i <= 5; i++) {

                stars = ``;
                for (let j = 0; j <= i; j++) {
                    stars += '★';
                }
                for (let j = 0; j < (5 - i); j++) {
                    stars += `☆`;

                }

                stat = (reviewsData[i] / total_reviews) * 100;

                stat = Math.round(stat);


                $('#stat-' + i).html(`${stars}${stat}%`);


            }
        },

    });
});
