function submit() {
    var un = $("#text_username").val()
    var pd = $("#text_password").val()
    var data = { "username": un, "password": pd }
    $.post("/api/register", JSON.stringify(data))
}