document.addEventListener("DOMContentLoaded", () => {
    setupDeleteConfirmation();
    setupFormValidation();
    autoDismissAlerts();
});

function setupDeleteConfirmation() {
    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            const confirmed = window.confirm(
                "Are you sure you want to delete this product? This action cannot be undone."
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
}

function setupFormValidation() {
    const forms = document.querySelectorAll(".product-form");

    forms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            const name = form.querySelector("#name");
            const category = form.querySelector("#category");
            const price = form.querySelector("#price");
            const currentStock = form.querySelector("#current_stock");
            const minimumStock = form.querySelector("#minimum_stock");

            let isValid = true;

            [name, category].forEach((field) => {
                if (field && !field.value.trim()) {
                    field.classList.add("invalid");
                    isValid = false;
                } else if (field) {
                    field.classList.remove("invalid");
                }
            });

            [price, currentStock, minimumStock].forEach((field) => {
                if (field && Number(field.value) < 0) {
                    field.classList.add("invalid");
                    isValid = false;
                } else if (field) {
                    field.classList.remove("invalid");
                }
            });

            if (!isValid) {
                event.preventDefault();
            }
        });
    });
}

function autoDismissAlerts() {
    const alerts = document.querySelectorAll(".alert-success");

    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });
}
