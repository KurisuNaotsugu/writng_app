document.addEventListener("DOMContentLoaded", function() {
    // DOM取得
    const userText = document.getElementById("userText");
    const wordCountDisplay = document.getElementById("wordCount");
    const timerDisplay = document.getElementById("timer");
    const recordBtn = document.getElementById("recordBtn");
    const stopBtn = document.getElementById("stopBtn");
    const transcribeBtn = document.getElementById("transcribeBtn");
    const taskSelect = document.querySelector("select[name='task_type']");
    const directionBox = document.getElementById("directionBox");

    // 初期値
    let timer = null;
    let timeLeft = 15 * 60;
    let mediaRecorder = null;
    let audioChunks = [];
    let audioBlob = null;

    // タイマー関連関数
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

    // ワードカウント
    function countWords(text) {
        let words = text.trim().split(/\s+/);
        return words[0] === "" ? 0 : words.length;
    }

    // イベント設定
    userText.addEventListener("input", () => {
        wordCountDisplay.textContent = countWords(userText.value);
    });

    // 初期表示
    wordCountDisplay.textContent = countWords(userText.value);
    updateTimerDisplay();

    // task変更時の処理
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

    // 録音開始
    recordBtn.addEventListener("click", async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.start();
        startTimer();
        console.log("Recording started...");
    });

    // 録音停止
    stopBtn.addEventListener("click", () => {
        if (!mediaRecorder) return;
        mediaRecorder.stop();
        pauseTimer();
        console.log("Recording stopped.");

        mediaRecorder.onstop = () => {
            audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            console.log("Audio ready for transcription.");
        };
    });

    // Transcribe（文字起こし）
    transcribeBtn.addEventListener("click", async () => {
    if (!audioBlob) {
        alert("録音データがありません。先にRecord → Stopしてください。");
        return;
    }

    // FormDataを構築
    const formData = new FormData();
    formData.append("audio_file", audioBlob, "recording.webm");
    formData.append("test_type", TestType);
    formData.append("skill_type", "Speaking");
    formData.append("task_type", taskSelect.value);

    try {
        const response = await fetch("/writing/transcript", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Server error ${response.status}: ${errText}`);
        }

        // HTMLを受け取りそのまま再描画
        const html = await response.text();
        document.open();
        document.write(html);
        document.close();
    } catch (err) {
        console.error("Transcription failed:", err);
        alert("Transcription failed. Check console for details.");
    }
}); 
});