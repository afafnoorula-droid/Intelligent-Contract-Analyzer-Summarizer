from app.services.chains import run_all_chains
from app.services.comparison import compare_contracts

def test_chains():
    text = "This is a sample contract for testing."
    result = run_all_chains(text)
    assert "summary" in result
    assert "clauses" in result
    assert "risk" in result

def test_comparison():
    result = compare_contracts("test1", "test2")
    assert "key_differences" in result