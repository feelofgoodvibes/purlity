window.addEventListener("load", () => {
    if ($("#authform[type='login']")[0]){
        $("#authform-submit").on("click", () => {
            let username = $("input[name='username']")[0].value;
            let password = $("input[name='password']")[0].value;

            $.ajax({
                url: urls.login,
                method: "POST",
                data: {
                    "username": username,
                    "password": password},
                success: (resp) => {
                    location.href = '/';
                },
                error: (resp) => {
                    $.notify(resp.responseJSON.msg, "error");
                }
            });
        });
    }

    else if ($("#authform[type='registration']")[0]){
        $("#authform-submit").on("click", () => {
            let username = $("input[name='username']")[0].value;
            let password = $("input[name='password']")[0].value;
            
            $.ajax({
                url: urls.register,
                method: "POST",
                data: {
                    "username": username,
                    "password": password},
                success: (resp) => {
                    location.href = '/';
                },
                error: (resp) => {
                    $.notify(resp.responseJSON.msg, "error");

                }

            });
        });
    }
});