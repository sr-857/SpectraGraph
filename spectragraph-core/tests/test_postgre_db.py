
import pytest
from unittest.mock import MagicMock, call, patch
from sqlalchemy.exc import OperationalError
from spectragraph_core.core.postgre_db import ensure_db_connection, DatabaseUnavailableError

@pytest.fixture
def mock_engine(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("spectragraph_core.core.postgre_db.engine", mock)
    return mock

@pytest.fixture
def mock_logger(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("spectragraph_core.core.postgre_db.logger", mock)
    return mock

def test_ensure_db_connection_success(mock_engine, mock_logger):
    """Test successful connection."""
    ensure_db_connection(max_retries=1)
    mock_engine.connect.assert_called_once()
    mock_logger.info.assert_called()

def test_ensure_db_connection_retry(mock_engine, mock_logger):
    """Test retry logic: fail once, then succeed."""
    # Simulate one failure then success
    mock_engine.connect.side_effect = [OperationalError("Select 1", None, Exception("Fail")), MagicMock()]
    
    # Needs at least 2 retries to succeed on second attempt
    ensure_db_connection(max_retries=3, base_delay=0.01)
    
    assert mock_engine.connect.call_count == 2
    mock_logger.warning.assert_called() # Should indicate retry
    mock_logger.info.assert_called() # Finally succeed

def test_ensure_db_connection_fail_retries(mock_engine, mock_logger):
    """Test failure after max retries."""
    mock_engine.connect.side_effect = OperationalError("Select 1", None, Exception("Fail"))
    
    with pytest.raises(DatabaseUnavailableError):
        ensure_db_connection(max_retries=2, base_delay=0.01)
        
    assert mock_engine.connect.call_count == 2
    mock_logger.error.assert_called()

def test_diagnostics_generic_failure(mock_engine, mock_logger):
    """Test actionable advice is logged on failure."""
    error = OperationalError("select 1", None, Exception("connection refused"))
    mock_engine.connect.side_effect = error
    
    with pytest.raises(DatabaseUnavailableError):
        ensure_db_connection(max_retries=1, base_delay=0.01)
        
    # Check if we logged the helpful message
    found = False
    for call_args in mock_logger.error.call_args_list:
        args, _ = call_args
        if args and "Possible causes and solutions" in args[0]:
            found = True
            break
    assert found, "Did not find expected diagnostic message block"

