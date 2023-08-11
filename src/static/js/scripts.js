window.addEventListener("load", () => {
    feather.replace();
    // Remove server messages after 5 seconds
    if (document.getElementById("server-messages")) { setInterval(() => { $("#server-messages").hide('slow', () => { $("#server-messages").remove() }) }, 5000); }

    if ($("#logout-btn")){
        $("#logout-btn").on("click", () => {
            $.ajax({
                url: urls.logout,
                method: "POST",
                success: (resp) => {
                    location.href = '/';
                },
                error: (resp) => {
                    $.notify(resp.responseJSON.msg, "error");
                }
            });
        })
    }

    if ($("#land-purify-btn")) {
        $("#land-purify-btn").on("click", () => {
            let url = $("#land-link")[0].value;
            $.ajax({
                url: urls.api.urls,
                method: "POST",
                data: {
                    "url": url
                },
                success: (resp) => {
                    console.log(resp);
                },
                error: (resp) => {
                    $.notify(resp.responseJSON.msg, "error");
                }
            })
        });
    }

    for (let item of document.getElementsByClassName("feather-copy")){
        let href = item.parentElement.querySelector(".short_url").text;
        $(item).on("click", async () => {
            await navigator.clipboard.writeText(location.origin + "/v/" + href);
            $(item).notify("Copied to clipboard!", {"className": "success", "autoHideDelay": 2000 });
        });

    }
});
