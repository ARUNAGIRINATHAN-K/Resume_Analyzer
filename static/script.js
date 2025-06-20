document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const resultsDiv = document.getElementById('results');
    const submitBtn = document.querySelector('.btn');
    
    // Reset UI
    errorDiv.style.display = 'none';
    resultsDiv.style.display = 'none';
    loadingDiv.style.display = 'block';
    submitBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('resume', document.getElementById('resume').files[0]);
    formData.append('job_desc', document.getElementById('job_desc').value);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (result.error) {
            errorDiv.textContent = result.error;
            errorDiv.style.display = 'block';
        } else {
            let tableRows = result.evaluation_table.map(row => `
                <tr>
                    <td>${row.criteria}<br><small>${row.description}</small></td>
                    <td>${row.expected}</td>
                    <td>${row.resume}</td>
                    <td>${row.score}%</td>
                </tr>
            `).join('');
            
            resultsDiv.innerHTML = `
                <p>Composite Match Score: ${result.match_score}%</p>
                <p>Missing Skills: ${result.missing_skills.join(', ') || 'None'}</p>
                <table class="evaluation-table">
                    <thead>
                        <tr>
                            <th>Criteria</th>
                            <th>Expected</th>
                            <th>Your Resume</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tableRows}
                    </tbody>
                </table>
                <a href="/download_report/${result.analysis_id}">Download Report</a>
            `;
            resultsDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'Network error occurred. Please try again.';
        errorDiv.style.display = 'block';
    } finally {
        loadingDiv.style.display = 'none';
        submitBtn.disabled = false;
    }
});

// Update file name display
document.getElementById('resume').addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || 'No file chosen';
    document.querySelector('.file-name').textContent = fileName;
});