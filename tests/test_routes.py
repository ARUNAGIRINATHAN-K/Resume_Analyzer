import json

def test_index_route(client):
    """Test that the index route returns the upload page successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload Resume" in response.data or b"Resume Analyzer" in response.data

def test_api_analyze_text_success(client):
    """Test that the text re-analysis API endpoint processes valid inputs correctly."""
    payload = {
        "resume_text": "I am a skilled developer with experience in Python and Flask.",
        "job_description": "We seek a Python backend engineer with Flask experience."
    }
    response = client.post(
        '/api/analyze-text',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'overall_score' in data
    assert 'matched_keywords' in data
    assert 'python' in data['matched_keywords']

def test_api_analyze_text_missing_params(client):
    """Test validation errors for the text re-analysis endpoint."""
    # Missing job description
    payload_missing_jd = {
        "resume_text": "Only resume text"
    }
    response = client.post(
        '/api/analyze-text',
        data=json.dumps(payload_missing_jd),
        content_type='application/json'
    )
    assert response.status_code == 400
    
    # Missing resume text
    payload_missing_resume = {
        "job_description": "Only job description"
    }
    response = client.post(
        '/api/analyze-text',
        data=json.dumps(payload_missing_resume),
        content_type='application/json'
    )
    assert response.status_code == 400
