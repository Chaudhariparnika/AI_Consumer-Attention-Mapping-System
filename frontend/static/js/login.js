const form = document.getElementById("loginForm");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    let apiUrl = "";

    if (window.location.pathname === "/user/login") {
        apiUrl = "/api/user/login";
    }
    else if (window.location.pathname === "/admin/login") {
        apiUrl = "/api/admin/login";
    }

    try {

        const response = await fetch(apiUrl, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email,
                password
            })

        });

        const result = await response.json();

        if (response.ok) {

            localStorage.setItem(
                "access_token",
                result.access_token
            );

            alert(result.message);

            if (window.location.pathname === "/user/login") {
                window.location.href = "/user/dashboard";
            }
            else {
                window.location.href = "/admin/dashboard";
            }

        }
        else {

            alert(result.detail);

        }

    }
    catch (error) {

        console.log(error);

        alert("Server Error");

    }

});