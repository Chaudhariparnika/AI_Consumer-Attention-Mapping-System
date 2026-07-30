// Check Login
const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/login";
}

// Show Logged-in User Name
document.addEventListener("DOMContentLoaded", () => {

    const fullName = localStorage.getItem("full_name");

    console.log("Full Name:", fullName);

    if (fullName) {
        const firstName = fullName.split(" ")[0];
        document.getElementById("welcomeText").textContent =
            `Welcome ${firstName} 👋`;
    }

});
// Logout
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("full_name");
    localStorage.removeItem("role");

    window.location.href = "/login";
});

// Demo Statistics
document.getElementById("totalUsers").textContent = 120;
document.getElementById("storeManagers").textContent = 18;
document.getElementById("retailAnalysts").textContent = 35;
document.getElementById("marketingAnalysts").textContent = 22;

// Demo Table
const users = [
    {
        name: "Rahul",
        email: "rahul@gmail.com",
        role: "Store Manager",
        date: "2026-07-28"
    },
    {
        name: "Neha",
        email: "neha@gmail.com",
        role: "Retail Analyst",
        date: "2026-07-29"
    },
    {
        name: "Amit",
        email: "amit@gmail.com",
        role: "Marketing Analyst",
        date: "2026-07-30"
    }
];

const table = document.getElementById("userTable");

users.forEach(user => {
    table.innerHTML += `
        <tr class="border-b hover:bg-gray-50">
            <td class="p-3">${user.name}</td>
            <td class="p-3">${user.email}</td>
            <td class="p-3">${user.role}</td>
            <td class="p-3">${user.date}</td>
        </tr>
    `;
});

// Pie Chart
new Chart(document.getElementById("pieChart"), {
    type: "pie",
    data: {
        labels: [
            "Store Manager",
            "Retail Analyst",
            "Marketing Analyst"
        ],
        datasets: [{
            data: [18, 35, 22]
        }]
    }
});

// Line Chart
new Chart(document.getElementById("lineChart"), {
    type: "line",
    data: {
        labels: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ],
        datasets: [{
            label: "Users",
            data: [8, 12, 20, 25, 40, 60],
            fill: false
        }]
    }
});