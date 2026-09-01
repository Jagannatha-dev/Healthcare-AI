// ==========================================
// Search Symptoms
// ==========================================

const search = document.getElementById("searchSymptom");

if (search) {

    search.addEventListener("keyup", function () {

        let value = this.value.toLowerCase();

        document.querySelectorAll(".symptom-item").forEach(function (item) {

            item.style.display = item.innerText.toLowerCase().includes(value)
                ? "block"
                : "none";

        });

    });

}

// ==========================================
// Minimum 4 Symptoms Validation
// ==========================================

const checkboxes = document.querySelectorAll(
    "input[name='symptoms']"
);

const predictBtn = document.getElementById("predictBtn");

function updatePredictButton() {

    let count = 0;

    checkboxes.forEach(function (checkbox) {

        if (checkbox.checked) {

            count++;

        }

    });

    if (count >= 4) {

        predictBtn.disabled = false;

        predictBtn.innerHTML =
            '<i class="bi bi-cpu-fill"></i> Predict Disease';

    }

    else {

        predictBtn.disabled = true;

        predictBtn.innerHTML =
            `<i class="bi bi-cpu-fill"></i> Select ${4 - count} More Symptom(s)`;

    }

}

checkboxes.forEach(function (checkbox) {

    checkbox.addEventListener("change", updatePredictButton);

});

updatePredictButton();