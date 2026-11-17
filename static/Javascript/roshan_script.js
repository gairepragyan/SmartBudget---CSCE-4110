
document.addEventListener("DOMContentLoaded", function () {

    const STORAGE_KEYS = {
        expenses: "smartbudget_expenses",
        budget: "smartbudget_budget",
        algorithm: "smartbudget_algorithm"
    };

    const expenseForm = document.getElementById("expenseForm");
    const expenseList = document.getElementById("expenseList");
    const optimizeButton = document.getElementById("optimizeButton");
    const clearAllButton = document.getElementById("clearAllButton");

    const budgetInput = document.getElementById("budgetInput");
    const expenseName = document.getElementById("expenseName");
    const expenseCost = document.getElementById("expenseCost");
    const expensePriority = document.getElementById("expensePriority");
    const algorithmSelect = document.getElementById("algorithmSelect");

    const budgetDisplay = document.getElementById("budgetDisplay");
    const spentLabel = document.getElementById("spentLabel");
    const remainingLabel = document.getElementById("remainingLabel");
    const budgetProgress = document.getElementById("budgetProgress");
    const expenseCount = document.getElementById("expenseCount");
    const expenseBadge = document.getElementById("expenseBadge");

    function loadSavedExpenses() {
        try {
            const saved = localStorage.getItem(STORAGE_KEYS.expenses);

            if (!saved) return [];

            const parsed = JSON.parse(saved);

            if (!Array.isArray(parsed)) return [];

            return parsed.filter(function (expense) {
                return (
                    expense &&
                    typeof expense.name === "string" &&
                    expense.name.trim().length > 0 &&
                    expense.name.length <= 60 &&
                    Number.isInteger(expense.cost) &&
                    expense.cost > 0 &&
                    Number.isInteger(expense.priority) &&
                    expense.priority >= 0
                );
            }).slice(0, 50);

        } catch (error) {
            console.error("Could not load saved expenses:", error);
            return [];
        }
    }

    let expenses = loadSavedExpenses();

    function saveExpenses() {
        try {
            localStorage.setItem(
                STORAGE_KEYS.expenses,
                JSON.stringify(expenses)
            );
        } catch (error) {
            console.error("Could not save expenses:", error);
            alert("Could not save expenses in this browser.");
        }
    }

    const savedBudget = localStorage.getItem(STORAGE_KEYS.budget);

    if (savedBudget !== null) {
        budgetInput.value = savedBudget;
    }

    const savedAlgorithm = localStorage.getItem(STORAGE_KEYS.algorithm);

    if (savedAlgorithm === "tabulation" || savedAlgorithm === "memoization") {
        algorithmSelect.value = savedAlgorithm;
    }

    function formatMoney(amount) {
        return "$" + amount.toLocaleString("en-US");
    }

    function updateBudget() {
        const budget = Number(budgetInput.value) || 0;

        const totalCost = expenses.reduce(function (sum, expense) {
            return sum + expense.cost;
        }, 0);

        budgetDisplay.textContent = formatMoney(budget);
        spentLabel.textContent = formatMoney(totalCost) + " planned";

        const remaining = budget - totalCost;

        remainingLabel.textContent =
            formatMoney(remaining) + " remaining if all purchased";

        const percentage = budget > 0
            ? Math.min((totalCost / budget) * 100, 100)
            : 0;

        budgetProgress.style.width = percentage + "%";
    }

    budgetInput.addEventListener("input", function () {
        localStorage.setItem(STORAGE_KEYS.budget, budgetInput.value);
        updateBudget();
    });

    algorithmSelect.addEventListener("change", function () {
        localStorage.setItem(
            STORAGE_KEYS.algorithm,
            algorithmSelect.value
        );
    });

    function validExpense(name, cost, priority) {
        if (!name || name.length > 60) {
            alert("Please enter a valid expense name.");
            return false;
        }

        if (!Number.isInteger(cost) || cost <= 0) {
            alert("Expense cost must be a positive whole number.");
            return false;
        }

        if (!Number.isInteger(priority) || priority < 0) {
            alert("Priority must be a nonnegative whole number.");
            return false;
        }

        return true;
    }

    expenseForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = expenseName.value.trim();
        const cost = Number(expenseCost.value);
        const priority = Number(expensePriority.value);

        if (!validExpense(name, cost, priority)) return;

        if (expenses.length >= 50) {
            alert("You can add a maximum of 50 expenses.");
            return;
        }

        expenses.push({ name, cost, priority });

        saveExpenses();
        renderExpenses();

        expenseName.value = "";
        expenseCost.value = "";
        expensePriority.value = "10";
        expenseName.focus();
    });

    function editExpense(index) {
        const expense = expenses[index];

        if (!expense) return;

        const newName = prompt("Edit expense name:", expense.name);
        if (newName === null) return;

        const newCost = prompt("Edit expense cost ($):", expense.cost);
        if (newCost === null) return;

        const newPriority = prompt("Edit priority score:", expense.priority);
        if (newPriority === null) return;

        const name = newName.trim();
        const cost = Number(newCost);
        const priority = Number(newPriority);

        if (newCost.trim() === "" || newPriority.trim() === "") {
            alert("Cost and priority cannot be empty.");
            return;
        }

        if (!validExpense(name, cost, priority)) return;

        expenses[index] = { name, cost, priority };

        saveExpenses();
        renderExpenses();
    }

    function removeExpense(index) {
        if (index < 0 || index >= expenses.length) return;

        expenses.splice(index, 1);

        saveExpenses();
        renderExpenses();
    }

    clearAllButton.addEventListener("click", function () {
        if (expenses.length === 0) {
            alert("There are no expenses to clear.");
            return;
        }

        const confirmed = confirm(
            "Are you sure you want to remove all expenses? " +
            "This will delete all saved expenses from this browser."
        );

        if (!confirmed) return;

        expenses.length = 0;

        saveExpenses();
        renderExpenses();

        expenseName.value = "";
        expenseCost.value = "";
        expensePriority.value = "10";
    });

    function renderExpenses() {
        expenseList.innerHTML = "";

        if (expenses.length === 0) {
            const emptyState = document.createElement("div");
            emptyState.className = "empty-state";

            const symbol = document.createElement("span");
            symbol.textContent = "◇";

            const message = document.createElement("p");
            message.textContent = "No expenses added yet.";

            const description = document.createElement("small");
            description.textContent = "Add an expense to get started.";

            emptyState.append(symbol, message, description);
            expenseList.appendChild(emptyState);
        }

        expenses.forEach(function (expense, index) {
            const item = document.createElement("div");
            item.className = "expense-item";

            const details = document.createElement("div");

            const name = document.createElement("strong");
            name.textContent = expense.name;

            const information = document.createElement("p");
            information.textContent =
                formatMoney(expense.cost) + " | Priority: " + expense.priority;

            details.appendChild(name);
            details.appendChild(information);

            const editButton = document.createElement("button");
            editButton.type = "button";
            editButton.className = "edit-expense-button";
            editButton.textContent = "Edit";
            editButton.setAttribute("aria-label", "Edit " + expense.name);

            editButton.addEventListener("click", function () {
                editExpense(index);
            });

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.className = "remove-expense-button";
            removeButton.textContent = "Remove";
            removeButton.setAttribute("aria-label", "Remove " + expense.name);

            removeButton.addEventListener("click", function () {
                removeExpense(index);
            });

            const actions = document.createElement("div");
            actions.className = "expense-actions";

            actions.appendChild(editButton);
            actions.appendChild(removeButton);

            item.appendChild(details);
            item.appendChild(actions);

            expenseList.appendChild(item);
        });

        expenseCount.textContent = expenses.length;

        expenseBadge.textContent =
            expenses.length + (expenses.length === 1 ? " item" : " items");

        clearAllButton.disabled = expenses.length === 0;

        updateBudget();
    }

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

        saveExpenses();

        localStorage.setItem(STORAGE_KEYS.budget, budgetInput.value);
        localStorage.setItem(STORAGE_KEYS.algorithm, algorithm);

        optimizeButton.disabled = true;
        optimizeButton.textContent = "Optimizing...";

        try {
            const response = await fetch("/optimize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    budget,
                    algorithm,
                    expenses
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Budget optimization failed.");
            }

            if (!data.redirect) {
                throw new Error("Results page URL was not returned.");
            }

            window.location.href = data.redirect;

        } catch (error) {
            console.error("SmartBudget optimization error:", error);
            alert(error.message);

        } finally {
            optimizeButton.disabled = false;
            optimizeButton.textContent = "✦ Optimize My Budget";
        }
    });

    renderExpenses();

    console.log(
        "SmartBudget loaded successfully.",
        expenses.length,
        "saved expenses restored."
    );
});
