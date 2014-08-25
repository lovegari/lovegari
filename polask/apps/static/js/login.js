function fblogin() {
    var name;
    var img_url;
    FB.api('/me', function (response) {
        name = response.name;
        FB.api('/me/picture?width=35&height=35', function (response) {
            img_url = response.data.url;
            $.ajax({
                url: "/fblogin",
                dataType: 'JSON',
                data: {
                    name_data: name,
                    img_url: img_url
                },
                success: function (data) {
                    url = '/chat/' + data.chat_id;
                    location.replace(url);
                }
            });
        });
    });
}

$(document).ready(function () {
		$('#facebook-btn').click(function () {
			FB.login(function (response) {
				fblogin();
			});
		});
});