def test_review_basic(client):
    response = client.post("/api/v1/review", json={
        "language": "python",
        "code": "print('Hello')",
        "review_type": "basic"
    })
    assert response.status_code == 200

    data = response.json()
    assert "remark" in data
    assert "score" in data
    assert isinstance(data["remark"], str)
    assert isinstance(data["score"], int)
