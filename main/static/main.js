const testTypeInput = document.getElementById("testType");
const skillTypeInput = document.getElementById("skillType");
const startBtn = document.getElementById("startBtn");
const form = document.getElementById("homeForm");

function toggleSelection(buttonGroup, selectedBtn) {
    buttonGroup.forEach(btn => {
        btn.classList.remove("active", "btn-primary", "btn-success", "btn-warning");
        // aria-pressed などアクセシビリティの属性も更新
        btn.setAttribute("aria-pressed", "false");
    });
    selectedBtn.classList.add("active");
    selectedBtn.setAttribute("aria-pressed", "true");

    // 色付け
    if (selectedBtn.id.includes("toeic") || selectedBtn.id.includes("toefl")) {
        selectedBtn.classList.add("btn-primary");
    } else if (selectedBtn.id.includes("writing")) {
        selectedBtn.classList.add("btn-success");
    } else {
        selectedBtn.classList.add("btn-warning");
    }
}

// ボタン配列（既存のIDを使用）
const testButtons = [document.getElementById("toeicBtn"), document.getElementById("toeflBtn")];
const skillButtons = [document.getElementById("writingBtn"), document.getElementById("speakingBtn")];

testButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        toggleSelection(testButtons, btn);
        // より確実にテキストを得るために data-value 属性を使うのがベター
        testTypeInput.value = (btn.dataset.value || btn.textContent).trim();
        updateStartButtonState();
    });
});

skillButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        toggleSelection(skillButtons, btn);
        skillTypeInput.value = (btn.dataset.value || btn.textContent).trim();
        updateStartButtonState();
    });
});

function updateStartButtonState() {
    startBtn.disabled = !(testTypeInput.value && skillTypeInput.value);
}

form.addEventListener("submit", (e) => {
    // skill_type と test_type を小文字に変換
    const skill = skillTypeInput.value.toLowerCase();
    const test = testTypeInput.value.toLowerCase();

    // フォーム action を動的に設定
    form.action = `/${skill}/${test}`;  // 例: /writing/toeic
});
