document.addEventListener('DOMContentLoaded', function () {
    const timerDisplay = document.getElementById('timer-display');
    const timeTakenInput = document.getElementById('time-taken-input');
    const testForm = document.getElementById('test-form');

    if (!timerDisplay || !testForm) return;

    let durationMinutes = parseInt(timerDisplay.dataset.duration || '30', 10);
    let totalSeconds = durationMinutes * 60;
    let secondsElapsed = 0;

    function updateTimer() {
        if (totalSeconds <= 0) {
            clearInterval(timerInterval);
            timeTakenInput.value = secondsElapsed;
            alert('Time is up! Your assessment will now be submitted automatically.');
            testForm.submit();
            return;
        }

        totalSeconds--;
        secondsElapsed++;
        timeTakenInput.value = secondsElapsed;

        const mins = Math.floor(totalSeconds / 60);
        const secs = totalSeconds % 60;
        timerDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

        if (totalSeconds < 300) {
            timerDisplay.classList.add('text-danger', 'fw-bold');
        }
    }

    const timerInterval = setInterval(updateTimer, 1000);

    // Question navigation & palette sync
    const radioInputs = document.querySelectorAll('.question-option-input');
    radioInputs.forEach(input => {
        input.addEventListener('change', function () {
            const qId = this.dataset.questionId;
            const paletteBtn = document.getElementById(`palette-btn-${qId}`);
            if (paletteBtn) {
                paletteBtn.classList.remove('btn-outline-secondary');
                paletteBtn.classList.add('btn-primary');
            }
        });
    });

    testForm.addEventListener('submit', function () {
        clearInterval(timerInterval);
        timeTakenInput.value = secondsElapsed;
    });
});
