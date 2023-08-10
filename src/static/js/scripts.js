window.addEventListener("load", () => {
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
});
