
document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // SMARTBUDGET - FINAL JAVASCRIPT
    // AUTOMATIC LOCAL STORAGE
    // ==========================================

    const STORAGE_KEYS = {
        expenses: "smartbudget_expenses",
        budget: "smartbudget_budget",
        algorithm: "smartbudget_algorithm"
    };

    // ==========================================
    // GET HTML ELEMENTS
    // ==========================================

    const expenseForm = document.getElementById("expenseForm");
    const expenseList = document.getElementById("expenseList");
    const optimizeButton = document.getElementById("optimizeButton");

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

    // ==========================================
    // LOAD SAVED EXPENSES
    // ==========================================

    function loadSavedExpenses() {
        try {
            const saved = localStorage.getItem(STORAGE_KEYS.expenses);

            if (!saved) {
                return [];
            }

            const parsed = JSON.parse(saved);

            if (!Array.isArray(parsed)) {
                return [];
            }

            // Only restore valid expenses.
            return parsed.filter(function (expense) {
                return (
                    expense &&
                    typeof expense.name === "string" &&
                    expense.name.trim().length > 0 &&
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

    // ==========================================
    // SAVE EXPENSES
    // ==========================================

    function saveExpenses() {
        try {
            localStorage.setItem(
                STORAGE_KEYS.expenses,
                JSON.stringify(expenses)
            );
        } catch (error) {
            console.error("Could not save expenses:", error);
        }
    }

    // ==========================================
    // LOAD SAVED BUDGET
    // ==========================================

    const savedBudget = localStorage.getItem(STORAGE_KEYS.budget);

    if (savedBudget !== null) {
        budgetInput.value = savedBudget;
    }

    // ==========================================
    // LOAD SAVED ALGORITHM
    // ==========================================

    const savedAlgorithm = localStorage.getItem(
        STORAGE_KEYS.algorithm
    );

    if (
        savedAlgorithm === "tabulation" ||
        savedAlgorithm === "memoization"
    ) {
        algorithmSelect.value = savedAlgorithm;
    }

    // ==========================================
    // FORMAT MONEY
    // ==========================================

    function formatMoney(amount) {
        return "$" + amount.toLocaleString("en-US");
    }

    // ==========================================
    // UPDATE BUDGET DISPLAY
    // ==========================================

    function updateBudget() {

        const budget = Number(budgetInput.value) || 0;

        const totalCost = expenses.reduce(
            function (sum, expense) {
                return sum + expense.cost;
            },
            0
        );

        budgetDisplay.textContent = formatMoney(budget);

        spentLabel.textContent =
            formatMoney(totalCost) + " planned";

        const remaining = budget - totalCost;

        remainingLabel.textContent =
            formatMoney(remaining) +
            " remaining if all purchased";

        // Show planned spending, capped at 100%.
        const percentage = budget > 0
            ? Math.min((totalCost / budget) * 100, 100)
            : 0;

        budgetProgress.style.width = percentage + "%";
    }

    // ==========================================
    // SAVE BUDGET WHEN CHANGED
    // ==========================================

    budgetInput.addEventListener("input", function () {

        localStorage.setItem(
            STORAGE_KEYS.budget,
            budgetInput.value
        );

        updateBudget();
    });

    // ==========================================
    // SAVE ALGORITHM WHEN CHANGED
    // ==========================================

    algorithmSelect.addEventListener("change", function () {

        localStorage.setItem(
            STORAGE_KEYS.algorithm,
            algorithmSelect.value
        );
    });

    // ==========================================
    // ADD NEW EXPENSE
    // ==========================================

    expenseForm.addEventListener("submit", function (event) {

        // Prevent browser page refresh.
        event.preventDefault();

        const name = expenseName.value.trim();
        const cost = Number(expenseCost.value);
        const priority = Number(expensePriority.value);

        // Validate expense.
        if (!name || name.length > 60) {
            alert("Please enter a valid expense name.");
            return;
        }

        if (!Number.isInteger(cost) || cost <= 0) {
            alert("Expense cost must be a positive whole number.");
            return;
        }

        if (!Number.isInteger(priority) || priority < 0) {
            alert("Please enter a valid priority.");
            return;
        }

        if (expenses.length >= 50) {
            alert("You can add a maximum of 50 expenses.");
            return;
        }

        // Add expense to the list.
        expenses.push({
            name: name,
            cost: cost,
            priority: priority
        });

        // Automatically save it.
        saveExpenses();

        // Update the page.
        renderExpenses();

        // Clear only the expense fields.
        expenseName.value = "";
        expenseCost.value = "";
        expensePriority.value = "10";

        // Keep the budget unchanged.
        expenseName.focus();
    });

    // ==========================================
    // DISPLAY ALL EXPENSES
    // ==========================================

    function renderExpenses() {

        expenseList.innerHTML = "";

        // ======================================
        // SHOW EMPTY MESSAGE
        // ======================================

        if (expenses.length === 0) {

            const emptyState = document.createElement("div");
            emptyState.className = "empty-state";

            const symbol = document.createElement("span");
            symbol.textContent = "◇";

            const message = document.createElement("p");
            message.textContent = "No expenses added yet.";

            const description = document.createElement("small");
            description.textContent =
                "Add an expense to get started.";

            emptyState.append(
                symbol,
                message,
                description
            );

            expenseList.appendChild(emptyState);
        }

        // ======================================
        // DISPLAY SAVED EXPENSES
        // ======================================

        expenses.forEach(function (expense, index) {

            const item = document.createElement("div");
            item.className = "expense-item";

            const details = document.createElement("div");

            const name = document.createElement("strong");
            name.textContent = expense.name;

            const information = document.createElement("p");

            information.textContent =
                formatMoney(expense.cost) +
                " | Priority: " +
                expense.priority;

            details.appendChild(name);
            details.appendChild(information);

            // ==================================
            // REMOVE EXPENSE BUTTON
            // ==================================

            const removeButton = document.createElement("button");

            removeButton.type = "button";
            removeButton.textContent = "Remove";

            removeButton.addEventListener("click", function () {

                // Remove from the array.
                expenses.splice(index, 1);

                // Update saved expenses.
                saveExpenses();

                // Refresh the expense list.
                renderExpenses();
            });

            item.appendChild(details);
            item.appendChild(removeButton);

            expenseList.appendChild(item);
        });

        // ======================================
        // UPDATE EXPENSE COUNT
        // ======================================

        expenseCount.textContent = expenses.length;

        expenseBadge.textContent =
            expenses.length +
            (expenses.length === 1 ? " item" : " items");

        // ======================================
        // UPDATE BUDGET INFORMATION
        // ======================================

        updateBudget();
    }

    // ==========================================
    // OPTIMIZE MY BUDGET
    // ==========================================

    optimizeButton.addEventListener("click", async function () {

        const budget = Number(budgetInput.value);
        const algorithm = algorithmSelect.value;

        // ======================================
        // VALIDATE BUDGET
        // ======================================

        if (
            !Number.isInteger(budget) ||
            budget < 1 ||
            budget > 10000
        ) {

            alert(
                "Please enter a budget between $1 and $10,000."
            );

            return;
        }

        // ======================================
        // VALIDATE EXPENSE LIST
        // ======================================

        if (expenses.length === 0) {

            alert("Please add at least one expense.");

            return;
        }

        // Save the latest values before optimizing.
        saveExpenses();

        localStorage.setItem(
            STORAGE_KEYS.budget,
            budgetInput.value
        );

        localStorage.setItem(
            STORAGE_KEYS.algorithm,
            algorithm
        );

        // ======================================
        // DISABLE BUTTON WHILE PROCESSING
        // ======================================

        optimizeButton.disabled = true;
        optimizeButton.textContent = "Optimizing...";

        try {

            // ==================================
            // SEND DATA TO FLASK
            // ==================================

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

            // ==================================
            // CHECK RESPONSE
            // ==================================

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Budget optimization failed."
                );
            }

            if (!data.redirect) {
                throw new Error(
                    "Results page URL was not returned."
                );
            }

            // ==================================
            // GO TO RESULTS PAGE
            // ==================================

            window.location.href = data.redirect;

        } catch (error) {

            console.error(
                "SmartBudget optimization error:",
                error
            );

            alert(error.message);

        } finally {

            // Re-enable the button if navigation
            // has not completed.
            optimizeButton.disabled = false;

            optimizeButton.textContent =
                "✦ Optimize My Budget";
        }
    });

    // ==========================================
    // RESTORE SAVED DATA WHEN PAGE OPENS
    // ==========================================

    renderExpenses();

    console.log(
        "SmartBudget loaded successfully.",
        expenses.length,
        "saved expenses restored."
    );

});
