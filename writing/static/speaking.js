document.addEventListener("DOMContentLoaded", function() {
    // DOM取得
    const userText = document.getElementById("userText");
    const wordCountDisplay = document.getElementById("wordCount");
    const timerDisplay = document.getElementById("timer");
    const startBtn = document.getElementById("startBtn");
    const pauseBtn = document.getElementById("pauseBtn");
    const transcribeBtn = document.getElementById("transcripeBtn");
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
    startBtn.addEventListener("click", async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.start();
        startTimer();
        console.log("Recording started...");
    });

    // 録音停止
    pauseBtn.addEventListener("click", () => {
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
    transcribeBtn.addEventListener("click", () => {
        if (!audioBlob) {
            alert("録音データがありません。先にRecord → Stopしてください。");
            return;
        }

        const form = document.getElementById("writingForm");
        const formData = new FormData(form);
        formData.append("audio_file", audioBlob, "recording.webm");

        form.action = "/writing/transcript"; // Flaskのルートに送信
        form.method = "POST";

        // 通常のフォーム送信（再レンダリング）
        const tempForm = document.createElement("form");
        tempForm.method = "POST";
        tempForm.action = "/writing/transcript";
        const blobInput = document.createElement("input");
        blobInput.type = "hidden";
        blobInput.name = "audio_file";
        blobInput.value = audioBlob;
        tempForm.appendChild(blobInput);
        document.body.appendChild(tempForm);
        form.submit();
    });
});
