const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/login";
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

document.addEventListener("DOMContentLoaded", async () => {
    const fullName = localStorage.getItem("full_name") || "Store Manager";
    if (fullName) {
        const firstName = fullName.split(" ")[0];
        document.getElementById("welcomeText").textContent = `Welcome ${firstName} 👋`;
    }

    try {
        const response = await fetch("/api/dashboard/store/overview", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Unable to load store dashboard");
        }

        const data = await response.json();

        setText("storeName", `${data.store_name} • Store operations`);
        setText("todaysVisitors", data.todays_visitors);
        setText("avgDwellTime", `${data.avg_dwell_time_mins} min`);
        setText("activeCameras", `${data.active_cameras}/${data.total_cameras}`);
        setText("totalShelves", data.total_shelves);
        setText("topShelf", data.top_shelf || "No data");
        setText("attentionFocus", data.attention_focus || "Medium");
        setText("managerName", data.manager_name || "Unassigned");

        const table = document.getElementById("shelfTable");
        table.innerHTML = "";

        if (data.shelf_stats && data.shelf_stats.length) {
            data.shelf_stats.forEach((item) => {
                table.innerHTML += `
                    <tr class="border-b hover:bg-slate-50">
                        <td class="p-3 font-medium">${item.name}</td>
                        <td class="p-3">${item.visitors}</td>
                        <td class="p-3">${item.engagement_score}%</td>
                    </tr>
                `;
            });
        } else {
            table.innerHTML = `<tr><td colspan="3" class="p-4 text-center text-slate-500">No shelf metrics available yet.</td></tr>`;
        }

        if (data.shelf_stats && data.shelf_stats.length) {
            const labels = data.shelf_stats.map((item) => item.name);
            const values = data.shelf_stats.map((item) => item.engagement_score);

            new Chart(document.getElementById("shelfChart"), {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: "Engagement",
                        data: values,
                        backgroundColor: ["#22c55e", "#3b82f6", "#f59e0b", "#8b5cf6"],
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, max: 100 } }
                }
            });
        }
    } catch (error) {
        console.error(error);
        setText("storeName", "Store insights unavailable");
        setText("todaysVisitors", "N/A");
        setText("avgDwellTime", "N/A");
        setText("activeCameras", "N/A");
        setText("totalShelves", "N/A");
        setText("topShelf", "N/A");
        setText("attentionFocus", "N/A");
        setText("managerName", "N/A");
        document.getElementById("shelfTable").innerHTML = `<tr><td colspan="3" class="p-4 text-center text-slate-500">Unable to load store metrics.</td></tr>`;
    }
});

document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("full_name");
    localStorage.removeItem("role");
    window.location.href = "/login";
});