function startSimulation() {
    let pages = document.getElementById("pages").value.trim();
    let frames = document.getElementById("frames").value;
    let algorithm = document.getElementById("algorithm").value;

    if (!pages || !frames || isNaN(frames) || frames <= 0) {
        alert("Please enter a valid page reference string and a positive number of frames.");
        return;
    }

    fetch('/simulate', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pages: pages, frames: frames, algorithm: algorithm })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displaySimulation(data.history, data.faults,algorithm);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
}

function displaySimulation(history, faults,algorithm) {
    let container = document.getElementById("simulation-container");
    container.innerHTML = `<h3>${algorithm} - Total Page Faults: ${faults}</h3>`; // Display page fault count

    history.forEach((frameSet, index) => {
        let row = document.createElement("div");
        row.classList.add("frame-row");

        frameSet.forEach((frame, idx) => {
            let div = document.createElement("div");
            div.classList.add("frame");
            div.textContent = frame;

            // Highlight new pages (page faults)
            if (index === 0 || history[index - 1][idx] !== frame) {
                div.classList.add("fault");
                div.style.animation = "fadeIn 0.5s";
            }

            row.appendChild(div);
        });

        container.appendChild(row);
    });
}
