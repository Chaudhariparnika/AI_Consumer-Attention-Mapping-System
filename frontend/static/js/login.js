const form = document.getElementById("loginForm");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {

        const response = await fetch("/api/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })

        });

        const result = await response.json();

        console.log("Login Response:", result);

        if (response.ok) {

            // Store JWT token
            localStorage.setItem("access_token", result.access_token);

            // Store user information
            localStorage.setItem("role", result.role);
            localStorage.setItem("full_name", result.full_name);

            console.log("Stored Full Name:", localStorage.getItem("full_name"));

            alert("Login Successful");

            switch (result.role) {

                case "admin":
                    window.location.href = "/admin/dashboard";
                    break;

                case "store_manager":
                    window.location.href = "/store/dashboard";
                    break;

                case "retail_analyst":
                    window.location.href = "/retail/dashboard";
                    break;

                case "marketing_analyst":
                    window.location.href = "/marketing/dashboard";
                    break;

                default:
                    alert("Unknown user role.");
                    break;
            }

        } else {

            alert(result.detail || "Invalid email or password");

        }

    } catch (error) {

        console.error("Login Error:", error);
        alert("Server Error");

    }

});