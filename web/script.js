async function search() {

    // 1️⃣ Changer layout : centré → colonnes
    const wrapper = document.getElementById("wrapper");
    const resultsPanel = document.getElementById("results-panel");

    wrapper.classList.remove("mode-center");
    wrapper.classList.add("mode-columns");
    resultsPanel.style.display = "block";

    // Ensuite, appel API comme avant
    let query = document.getElementById("query").value;
    let k = document.getElementById("k").value;
    let author = document.getElementById("author").value;
    let date = document.getElementById("date").value;

    let response = await fetch("http://127.0.0.1:5000/search", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ query, k, author, date })
    });

    let data = await response.json();

    // Injecter résultats
    let html = "<table><tr><th>ID</th><th>Titre</th><th>Score</th></tr>";
    data.forEach(r => {
        html += `<tr>
            <td>${r.id}</td>
            <td>${r.titre}</td>
            <td>${r.score.toFixed(4)}</td>
        </tr>`;
    });
    html += "</table>";

    document.getElementById("results").innerHTML = html;
}

async function loadFilters() {
    let response = await fetch("http://127.0.0.1:5000/filters");
    let data = await response.json();

    // Remplir auteurs
    let authorSelect = document.getElementById("author");
    data.authors.forEach(a => {
        let opt = document.createElement("option");
        opt.value = a;
        opt.textContent = a;
        authorSelect.appendChild(opt);
    });

    // Remplir dates
    let dateSelect = document.getElementById("date");
    data.dates.forEach(d => {
        let opt = document.createElement("option");
        opt.value = d;
        opt.textContent = d;
        dateSelect.appendChild(opt);
    });
}

// Charger les filtres au chargement
loadFilters();
function openTab(tabName) {
    document.querySelectorAll(".tab-content").forEach(div => div.style.display = "none");
    document.querySelectorAll(".tab-button").forEach(btn => btn.classList.remove("active"));

    document.getElementById(tabName).style.display = "block";
    event.target.classList.add("active");
}
async function getEvolution() {

    const mot = document.getElementById("mot-analyse").value;

    let response = await fetch("http://127.0.0.1:5000/evolution", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ mot })
    });

    let data = await response.json();

    const years = data.map(d => d.year);
    const freqs = data.map(d => d.freq);

    if (window.myChart) window.myChart.destroy();

    const ctx = document.getElementById("chart-evolution");
    window.myChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: years,
            datasets: [{
                label: `Fréquence du mot "${mot}"`,
                data: freqs,
                borderColor: "#5a8dee",
                borderWidth: 3,
                fill: false
            }]
        }
    });
}
