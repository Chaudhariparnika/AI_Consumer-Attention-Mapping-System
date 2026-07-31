const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/login";
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

function buildCharts(data) {
    const visitorCtx = document.getElementById("visitorChart");
    const cameraCtx = document.getElementById("cameraChart");

    if (visitorCtx) {
        new Chart(visitorCtx, {
            type: "line",
            data: {
                labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                datasets: [{
                    label: "Visitors",
                    data: [1200, 1400, 1350, 1600, 1750, 2200, 2100],
                    borderColor: "#3b82f6",
                    backgroundColor: "rgba(59, 130, 246, 0.2)",
                    tension: 0.35,
                    fill: true,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    if (cameraCtx) {
        new Chart(cameraCtx, {
            type: "doughnut",
            data: {
                labels: ["Online", "Offline"],
                datasets: [{
                    data: [data.active_ai_cameras || 0, Math.max((data.total_cameras || 0) - (data.active_ai_cameras || 0), 0)],
                    backgroundColor: ["#22c55e", "#f59e0b"],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: "bottom" } }
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const fullName = localStorage.getItem("full_name");

    if (fullName) {
        const firstName = fullName.split(" ")[0];
        document.getElementById("welcomeText").textContent = `Welcome ${firstName} 👋`;
    }

    try {
        const response = await fetch("/api/dashboard/overview", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }

        const data = await response.json();

        setText("totalUsers", data.total_users);
        setText("totalStores", data.total_stores);
        setText("totalCameras", data.total_cameras);
        setText("totalProducts", data.total_products);
        setText("totalShelves", data.total_shelves);
        setText("totalVisitors", data.todays_visitors);
        setText("averageDwellTime", `${data.avg_dwell_time_mins} min`);
        setText("mostViewedProduct", data.product_engagement_score ? `${data.product_engagement_score}%` : "N/A");
        setText("activeAiCameras", data.active_ai_cameras || 0);
        setText("engagementScore", data.product_engagement_score ? `${data.product_engagement_score}%` : "N/A");
        setText("attentionFocus", (data.product_engagement_score || 0) > 80 ? "High" : "Medium");

        buildCharts(data);

    } catch (error) {
        console.error(error);
        setText("totalUsers", "N/A");
        setText("totalStores", "N/A");
        setText("totalCameras", "N/A");
        setText("totalProducts", "N/A");
        setText("totalShelves", "N/A");
        setText("totalVisitors", "N/A");
        setText("averageDwellTime", "N/A");
        setText("mostViewedProduct", "N/A");
    }

    try {
        const usersResponse = await fetch("/api/users", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!usersResponse.ok) {
            throw new Error("Failed to load users");
        }

        const users = await usersResponse.json();
        const table = document.getElementById("userTable");

        table.innerHTML = "";

        users.slice(0, 5).forEach((user) => {
            table.innerHTML += `
                <tr class="border-b hover:bg-gray-50">
                    <td class="p-3">${user.full_name || user.name || "N/A"}</td>
                    <td class="p-3">${user.email || "N/A"}</td>
                    <td class="p-3">${user.role || "N/A"}</td>
                    <td class="p-3">${user.created_at ? new Date(user.created_at).toLocaleDateString() : "N/A"}</td>
                </tr>
            `;
        });
    } catch (error) {
        console.error(error);
        document.getElementById("userTable").innerHTML = `
            <tr>
                <td colspan="4" class="p-3 text-center text-sm text-slate-500">No user data available</td>
            </tr>
        `;
    }
});

document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("full_name");
    localStorage.removeItem("role");
    window.location.href = "/login";
});