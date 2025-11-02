document.addEventListener("DOMContentLoaded", function() {
    const userText = document.getElementById("userText");
    const wordCountDisplay = document.getElementById("wordCount");
    const timerDisplay = document.getElementById("timer");
    const startBtn = document.getElementById("startBtn");
    const pauseBtn = document.getElementById("pauseBtn");
    const taskSelect = document.querySelector("select[name='task_type']");
    const directionBox = document.getElementById("directionBox");

    let timer = null;
    let timeLeft = 15 * 60;

    function updateTimerDisplay() {
        let m = String(Math.floor(timeLeft / 60)).padStart(2, "0");
        let s = String(timeLeft % 60).padStart(2, "0");
        timerDisplay.textContent = `${m}:${s}`;
    }

    function startTimer() {
        if (timer) return;
        timer = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                updateTimerDisplay();
            } else {
                clearInterval(timer);
                timer = null;
            }
        }, 1000);
    }

    function pauseTimer() {
        clearInterval(timer);
        timer = null;
    }

    function countWords(text) {
        let words = text.trim().split(/\s+/);
        return words[0] === "" ? 0 : words.length;
    }

    // 初期表示
    wordCountDisplay.textContent = countWords(userText.value);
    updateTimerDisplay();

    // イベント
    userText.addEventListener("input", () => {
        wordCountDisplay.textContent = countWords(userText.value);
    });
    startBtn.addEventListener("click", startTimer);
    pauseBtn.addEventListener("click", pauseTimer);

    // タスク切り替え
    taskSelect.addEventListener("change", () => {
        const selectedTest = TestType;
        const selectedTask = taskSelect.value;
        if (selectedTest && selectedTask) {
            const taskObj = examData[selectedTest].Writing.find(
                t => t.task === selectedTask
            );
            if (taskObj) {
                directionBox.textContent = taskObj.direction;
                clearInterval(timer);
                timer = null;
                timeLeft = taskObj.time_per_question_seconds;
                updateTimerDisplay();
            }
        } else {
            directionBox.textContent = "Please select test and task";
        }
    });
});
