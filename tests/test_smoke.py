from pathlib import Path


def test_expected_structure():
    assert Path('services/chat-service/app/services/graph.py').exists()
    assert Path('frontend/src/App.jsx').exists()
