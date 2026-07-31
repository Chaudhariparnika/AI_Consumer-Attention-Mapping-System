const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/login";
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

document.addEventListener("DOMContentLoaded", () => {
    const fullName = localStorage.getItem("full_name") || "Retail Analyst";
    if (fullName) {
        const firstName = fullName.split(" ")[0];
        document.getElementById("welcomeText").textContent = `Welcome ${firstName} 👋`;
    }

    const sampleRows = [
        { shelf: "Shelf A", visitors: 182, engagement: 91 },
        { shelf: "Shelf B", visitors: 146, engagement: 84 },
        { shelf: "Shelf C", visitors: 128, engagement: 76 }
    ];

    const table = document.getElementById("insightTable");
    table.innerHTML = "";
    sampleRows.forEach((row) => {
        table.innerHTML += `
            <tr class="border-b hover:bg-slate-50">
                <td class="p-3 font-medium">${row.shelf}</td>
                <td class="p-3">${row.visitors}</td>
                <td class="p-3">${row.engagement}%</td>
            </tr>
        `;
    });

    setText("topProduct", "Fresh Drinks");
    setText("engagementScore", "91%");
    setText("avgDwellTime", "6.4 min");
    setText("trackedCameras", "4");
    setText("attentionZone", "Front Left Corner");
    setText("conversionSignal", "Strong");

    new Chart(document.getElementById("attentionChart"), {
        type: "line",
        data: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            datasets: [{
                label: "Attention",
                data: [72, 78, 85, 81, 90, 91],
                borderColor: "#8b5cf6",
                backgroundColor: "rgba(139, 92, 246, 0.15)",
                tension: 0.35,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });
});

document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("full_name");
    localStorage.removeItem("role");
    window.location.href = "/login";
});