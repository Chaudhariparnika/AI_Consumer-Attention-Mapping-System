const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/login";
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

document.addEventListener("DOMContentLoaded", () => {
    const fullName = localStorage.getItem("full_name") || "Marketing Analyst";
    if (fullName) {
        const firstName = fullName.split(" ")[0];
        document.getElementById("welcomeText").textContent = `Welcome ${firstName} 👋`;
    }

    const campaignRows = [
        { campaign: "Weekend Promo", audience: "Young Adults", results: "+18% uplift" },
        { campaign: "Holiday Bundle", audience: "Families", results: "+12% uplift" },
        { campaign: "New Arrival", audience: "Tech Savvy", results: "+9% uplift" }
    ];

    const table = document.getElementById("campaignTable");
    table.innerHTML = "";
    campaignRows.forEach((row) => {
        table.innerHTML += `
            <tr class="border-b hover:bg-slate-50">
                <td class="p-3 font-medium">${row.campaign}</td>
                <td class="p-3">${row.audience}</td>
                <td class="p-3">${row.results}</td>
            </tr>
        `;
    });

    setText("peakAudience", "Evening Shoppers");
    setText("engagementLift", "18%");
    setText("campaignReach", "24.8k");
    setText("conversionTrend", "Rising");
    setText("bestSegment", "Young Adults");
    setText("recommendation", "Focus on digital bundles");

    new Chart(document.getElementById("trendChart"), {
        type: "bar",
        data: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            datasets: [{
                label: "Engagement",
                data: [55, 62, 70, 74, 81, 88],
                backgroundColor: ["#f59e0b", "#fbbf24", "#fcd34d", "#fde68a", "#f59e0b", "#d97706"],
                borderRadius: 8
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