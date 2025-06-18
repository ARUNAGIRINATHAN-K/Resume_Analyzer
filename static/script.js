document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('resume', document.getElementById('resume').files[0]);
    formData.append('job_desc', document.getElementById('job_desc').value);
    
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    
    if (result.error) {
        document.getElementById('results').innerHTML = `<p>Error: ${result.error}</p>`;
    } else {
        document.getElementById('results').innerHTML = `
            <p>Match Score: ${result.match_score}%</p>
            <p>Missing Skills: ${result.missing_skills.join(', ')}</p>
            <a href="/download_report/${result.analysis_id}">Download Report</a>
        `;
    }
});