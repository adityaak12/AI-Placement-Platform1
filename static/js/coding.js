document.addEventListener('DOMContentLoaded', function () {
    const runBtn = document.getElementById('run-code-btn');
    const editorArea = document.getElementById('code-editor');
    const outputContainer = document.getElementById('code-output-container');
    const outputStatus = document.getElementById('output-status');
    const outputDetails = document.getElementById('output-details');
    const problemSlug = document.getElementById('problem-meta')?.dataset.slug;

    if (!runBtn || !editorArea || !problemSlug) return;

    runBtn.addEventListener('click', async function () {
        const code = editorArea.value;
        if (!code.trim()) {
            alert('Please write code before running.');
            return;
        }

        runBtn.disabled = true;
        runBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Running...';
        outputContainer.classList.remove('d-none');
        outputStatus.className = 'badge bg-secondary';
        outputStatus.textContent = 'Executing...';
        outputDetails.innerHTML = '<p class="text-muted">Evaluating code against sample test cases...</p>';

        try {
            const resp = await fetch(`/coding/run/${problemSlug}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            });

            const data = await resp.json();

            if (data.status === 'Accepted') {
                outputStatus.className = 'badge bg-success';
                outputStatus.textContent = `Accepted (${data.passed}/${data.total} Passed in ${data.execution_time_ms}ms)`;
            } else if (data.status === 'Wrong Answer') {
                outputStatus.className = 'badge bg-danger';
                outputStatus.textContent = `Wrong Answer (${data.passed}/${data.total} Passed)`;
            } else {
                outputStatus.className = 'badge bg-warning text-dark';
                outputStatus.textContent = `${data.status}`;
            }

            let html = '';
            if (data.error) {
                html += `<div class="alert alert-danger py-2 mb-3"><pre class="mb-0 text-danger" style="white-space:pre-wrap;">${data.error}</pre></div>`;
            }

            if (data.details && data.details.length > 0) {
                html += '<div class="table-responsive"><table class="table table-sm table-bordered"><thead><tr><th>Test Case</th><th>Status</th><th>Input</th><th>Expected</th><th>Actual</th></tr></thead><tbody>';
                data.details.forEach(tc => {
                    const statusBadge = tc.passed ? '<span class="badge bg-success">Passed</span>' : '<span class="badge bg-danger">Failed</span>';
                    html += `<tr><td>Case #${tc.test_case}</td><td>${statusBadge}</td><td><code>${tc.input || ''}</code></td><td><code>${tc.expected || ''}</code></td><td><code>${tc.actual || tc.error || ''}</code></td></tr>`;
                });
                html += '</tbody></table></div>';
            }

            outputDetails.innerHTML = html;
        } catch (err) {
            outputStatus.className = 'badge bg-danger';
            outputStatus.textContent = 'Execution Error';
            outputDetails.innerHTML = `<div class="alert alert-danger py-2">${err.message}</div>`;
        } finally {
            runBtn.disabled = false;
            runBtn.innerHTML = '<i class="bi bi-play-fill me-1"></i> Run Code';
        }
    });
});
