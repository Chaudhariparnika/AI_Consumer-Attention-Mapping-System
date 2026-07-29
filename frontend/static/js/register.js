const form = document.getElementById("registerForm");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const full_name = document.getElementById("full_name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone_no = document.getElementById("phone_no").value.trim();
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;

    if (password !== confirm_password) {
        alert("Passwords do not match.");
        return;
    }

    const userData = {
        full_name: full_name,
        email: email,
        phone_no: phone_no,
        password: password
    };

    // Detect whether this is Admin or User registration
    const isAdmin = window.location.pathname.includes("admin");

    // Select API endpoint
    const apiUrl = isAdmin
        ? "/api/admin/register"
        : "/api/user/register";

    try {
        console.log("Current Page:", window.location.pathname);
        console.log("API URL:", apiUrl);
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (response.ok) {
            alert(
                isAdmin
                    ? "Admin Registration Successful!"
                    : "User Registration Successful!"
            );

            // Redirect after successful registration
            window.location.href = isAdmin
                ? "/admin/login"
                : "/user/login";

        } else {
            alert(result.detail || "Registration Failed");
        }

    } catch (error) {
        console.error(error);
        alert("Server Error");
    }
});