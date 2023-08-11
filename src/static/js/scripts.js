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
                    location.href = "/" + resp.short_url;
                },
                error: (resp) => {
                    $.notify(resp.responseJSON.msg, "error");
                }
            })
        });
    }

    for (let item of document.getElementsByClassName("feather-copy")){
        let short_url = item.getAttribute("data-shorturl");
        $(item).on("click", async () => {
            await navigator.clipboard.writeText(location.origin + "/v/" + short_url);
            $(item).notify("Copied to clipboard!", {"className": "success", "autoHideDelay": 2000 });
        });
    }

    for (let item of document.getElementById("links-list-table").getElementsByClassName("feather-trash-2")){
        let short_url = item.getAttribute("data-shorturl");
        $(item).on("click", () => {
            $.ajax({
                url: `${urls.api.urls}/${short_url}`,
                method: "DELETE",
                success: (resp) => {
                    item.parentElement.parentElement.remove();
                },
                erorr: (resp) => {
                    console.log(resp);
                    $.notify(resp.responseJSON.msg, "error");
                }
            })
        });
    }
});
