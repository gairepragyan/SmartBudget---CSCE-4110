
document.addEventListener("DOMContentLoaded", function () {

    // STORE EXPENSES
    const expenses = [];

    // GET HTML ELEMENTS
    const expenseForm = document.getElementById("expenseForm");
    const expenseList = document.getElementById("expenseList");
    const optimizeButton = document.getElementById("optimizeButton");

    const budgetInput = document.getElementById("budgetInput");
    const expenseName = document.getElementById("expenseName");
    const expenseCost = document.getElementById("expenseCost");
    const expensePriority = document.getElementById("expensePriority");
    const algorithmSelect = document.getElementById("algorithmSelect");

    // UPDATE BUDGET DISPLAY
    function updateBudget() {
        const budget = Number(budgetInput.value) || 0;

        document.getElementById("budgetDisplay").textContent =
            "$" + budget.toLocaleString();

        document.getElementById("remainingLabel").textContent =
            "$" + budget.toLocaleString() + " remaining";
    }

    budgetInput.addEventListener("input", updateBudget);


    // ADD EXPENSE
    expenseForm.addEventListener("submit", function (event) {

        // STOP PAGE REFRESH
        event.preventDefault();

        const name = expenseName.value.trim();
        const cost = Number(expenseCost.value);
        const priority = Number(expensePriority.value);

        if (
            !name ||
            !Number.isInteger(cost) ||
            cost <= 0
        ) {
            alert("Please enter valid expense information.");
            return;
        }

        // SAVE EXPENSE
        expenses.push({
            name: name,
            cost: cost,
            priority: priority
        });

        // UPDATE LIST
        renderExpenses();

        // CLEAR ONLY EXPENSE INPUTS
        expenseName.value = "";
        expenseCost.value = "";
        expensePriority.value = "10";

        expenseName.focus();
    });


    // DISPLAY EXPENSES
    function renderExpenses() {

        expenseList.innerHTML = "";

        // EMPTY LIST
        if (expenses.length === 0) {
            expenseList.innerHTML = `
                <div class="empty-state">
                    <span>◇</span>
                    <p>No expenses added yet.</p>
                    <small>Add an expense to get started.</small>
                </div>
            `;
        }

        // DISPLAY EACH EXPENSE
        expenses.forEach((expense, index) => {

            const item = document.createElement("div");
            item.className = "expense-item";

            const details = document.createElement("div");

            const name = document.createElement("strong");
            name.textContent = expense.name;

            const information = document.createElement("p");
            information.textContent =
                "$" + expense.cost +
                " | Priority: " + expense.priority;

            details.appendChild(name);
            details.appendChild(information);

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.textContent = "Remove";

            removeButton.addEventListener("click", function () {
                expenses.splice(index, 1);
                renderExpenses();
            });

            item.appendChild(details);
            item.appendChild(removeButton);

            expenseList.appendChild(item);
        });

        // UPDATE EXPENSE COUNT
        document.getElementById("expenseCount").textContent =
            expenses.length;

        document.getElementById("expenseBadge").textContent =
            expenses.length + " items";

        // UPDATE BUDGET INFORMATION
        const budget = Number(budgetInput.value) || 0;

        const totalCost = expenses.reduce(
            (sum, expense) => sum + expense.cost,
            0
        );

        document.getElementById("spentLabel").textContent =
            "$" + totalCost + " planned";

        document.getElementById("remainingLabel").textContent =
            "$" + (budget - totalCost) + " remaining if all purchased";

        const percentage = budget > 0
            ? Math.min((totalCost / budget) * 100, 100)
            : 0;

        document.getElementById("budgetProgress").style.width =
            percentage + "%";
    }

    budgetInput.addEventListener("input", renderExpenses);


    // OPTIMIZE BUDGET
    optimizeButton.addEventListener("click", async function () {

        const budget = Number(budgetInput.value);
        const algorithm = algorithmSelect.value;

        if (!Number.isInteger(budget) || budget < 1 || budget > 10000) {
            alert("Please enter a budget between $1 and $10,000.");
            return;
        }

        if (expenses.length === 0) {
            alert("Please add at least one expense.");
            return;
        }

        optimizeButton.disabled = true;
        optimizeButton.textContent = "Optimizing...";

        try {

            // SEND DATA TO FLASK
            const response = await fetch("/optimize", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    budget: budget,
                    algorithm: algorithm,
                    expenses: expenses
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Optimization failed."
                );
            }

            // GO TO RESULTS PAGE
            window.location.href = data.redirect;

        } catch (error) {

            alert(error.message);

            optimizeButton.disabled = false;
            optimizeButton.textContent = "✦ Optimize My Budget";
        }
    });


    // INITIAL DISPLAY
    updateBudget();
    renderExpenses();

});
