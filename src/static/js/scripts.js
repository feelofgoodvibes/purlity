window.addEventListener("load", () => {
    // Remove server messages after 5 seconds
    if (document.getElementById("server-messages")) { setInterval(() => { $("#server-messages").hide('slow', () => { $("#server-messages").remove() }) }, 5000); }
});