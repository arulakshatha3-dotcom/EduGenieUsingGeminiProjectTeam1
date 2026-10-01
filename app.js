const taskSelect = document.getElementById("task");
const userInput = document.getElementById("inputText");
const submitButton = document.getElementById("submitBtn");

const levelContainer = document.getElementById("level-container");
const levelSelect = document.getElementById("level");

const resultContainer = document.getElementById("result");
const loading = document.getElementById("loading");


// Show / hide learning level
function updateTaskUI() {
    if (taskSelect.value === "learn") {
        levelContainer.style.display = "block";
    } else {
        levelContainer.style.display = "none";
    }
}


// Show loading
function setLoading(isLoading) {
    if (isLoading) {
        loading.style.display = "block";
        resultContainer.innerHTML = "Generating response...";
        submitButton.disabled = true;
    } else {
        loading.style.display = "none";
        submitButton.disabled = false;
    }
}


// Escape HTML
function escapeHTML(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// Send request to FastAPI
async function sendRequest(endpoint, payload) {

    const response = await fetch(endpoint, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(payload)
    });


    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error(
            "Server returned an invalid response."
        );
    }


    if (!response.ok) {
        throw new Error(
            data.detail ||
            data.message ||
            "Request failed."
        );
    }


    return data;
}


// Display normal text result
function displayTextResult(data) {

    if (!data.success) {
        resultContainer.innerHTML = `
            <div class="error">
                ${escapeHTML(
                    data.result || "Generation failed."
                )}
            </div>
        `;
        return;
    }


    resultContainer.innerHTML = `
        <div class="result-text">
            ${escapeHTML(data.result || "")}
        </div>
    `;
}


// Display quiz
function displayQuiz(data) {

    if (!data.success) {
        resultContainer.innerHTML = `
            <div class="error">
                Quiz generation failed.
            </div>
        `;
        return;
    }


    if (!data.questions || data.questions.length === 0) {
        resultContainer.innerHTML = `
            <div class="error">
                No quiz questions were generated.
            </div>
        `;
        return;
    }


    let html = "";


    data.questions.forEach((question, questionIndex) => {

        html += `
            <div class="quiz-question">

                <h3>
                    Question ${questionIndex + 1}
                </h3>

                <p>
                    ${escapeHTML(question.question)}
                </p>
        `;


        question.options.forEach((option, optionIndex) => {

            html += `
                <button
                    class="option"
                    data-question="${questionIndex}"
                    data-option="${optionIndex}"
                >
                    ${escapeHTML(option)}
                </button>
            `;

        });


        html += `
                <div
                    class="quiz-explanation"
                    id="explanation-${questionIndex}"
                    style="display:none;"
                >
                    ${escapeHTML(
                        question.explanation ||
                        "Correct answer."
                    )}
                </div>

            </div>
        `;

    });


    resultContainer.innerHTML = html;


    // Quiz option buttons
    const optionButtons =
        document.querySelectorAll(".option");


    optionButtons.forEach(button => {

        button.addEventListener("click", function () {

            const questionIndex =
                Number(this.dataset.question);

            const optionIndex =
                Number(this.dataset.option);


            const question =
                data.questions[questionIndex];


            const selectedAnswer =
                question.options[optionIndex];


            const buttons =
                document.querySelectorAll(
                    `[data-question="${questionIndex}"]`
                );


            buttons.forEach(item => {

                item.disabled = true;


                const itemIndex =
                    Number(item.dataset.option);


                if (
                    question.options[itemIndex] ===
                    question.correct_answer
                ) {
                    item.classList.add("correct");
                }

            });


            if (
                selectedAnswer !==
                question.correct_answer
            ) {
                this.classList.add("wrong");
            }


            const explanation =
                document.getElementById(
                    `explanation-${questionIndex}`
                );


            explanation.style.display = "block";

        });

    });
}


// Generate button
submitButton.addEventListener("click", async function () {

    const task = taskSelect.value;

    const text = userInput.value.trim();


    // Empty input check
    if (!text) {

        resultContainer.innerHTML = `
            <div class="error">
                Please enter a topic or question.
            </div>
        `;

        return;
    }


    setLoading(true);


    try {

        let data;


        // Question & Answer
        if (task === "qa") {

            data = await sendRequest(
                "/qa",
                {
                    question: text
                }
            );

            displayTextResult(data);
        }


        // Explain
        else if (task === "explain") {

            data = await sendRequest(
                "/explain",
                {
                    topic: text
                }
            );

            displayTextResult(data);
        }


        // Quiz
        else if (task === "quiz") {

            data = await sendRequest(
                "/quiz",
                {
                    text: text
                }
            );

            displayQuiz(data);
        }


        // Summarize
        else if (task === "summarize") {

            data = await sendRequest(
                "/summarize",
                {
                    text: text
                }
            );

            displayTextResult(data);
        }


        // Learning path
        else if (task === "learn") {

            data = await sendRequest(
                "/learn/recommendations",
                {
                    topic: text,
                    level: levelSelect.value
                }
            );

            displayTextResult(data);
        }

    }

    catch (error) {

        console.error("EduGenie Error:", error);


        resultContainer.innerHTML = `
            <div class="error">
                <strong>Error:</strong><br>
                ${escapeHTML(error.message)}
            </div>
        `;
    }

    finally {

        setLoading(false);

    }

});


// Update task when dropdown changes
taskSelect.addEventListener(
    "change",
    updateTaskUI
);


// Initial UI
updateTaskUI();