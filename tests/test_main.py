import pytest
from unittest.mock import mock_open, patch
from main import ScheduleManager  # Absolute import from the src directory

# Mock data
mock_csv_content = """header1,header2
1/12/2023,2/12/2023
3/12/2023,4/12/2023
"""
mock_dates = ["1/12/2023", "2/12/2023", "3/12/2023", "4/12/2023"]

@pytest.fixture
def mock_schedule_manager():
    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        manager = ScheduleManager("dummy_path.csv")
    return manager

def test_read_csv_file(mock_schedule_manager):
    manager = mock_schedule_manager
    rows = manager.read_csv_file()
    assert len(rows) == 3
    assert rows[1] == ["1/12/2023", "2/12/2023"]

def test_extract_dates_from_csv(mock_schedule_manager):
    manager = mock_schedule_manager
    dates = manager.extract_dates_from_csv()
    assert dates == mock_dates

def test_generate_schedule(mock_schedule_manager):
    manager = mock_schedule_manager
    schedule, breaks = manager.generate_schedule()
    
    assert len(schedule) == 16
    assert len(breaks) == 16
    assert schedule[0] == "08:00-09:30"  # Example check for the first schedule block
    assert breaks[0] == "Przerwa: 15 minut"  # Example check for the first break

def test_print_schedule_for_date(mock_schedule_manager, capsys):
    manager = mock_schedule_manager
    date = "1/12/2023"
    
    manager.print_schedule_for_date(date)
    captured = capsys.readouterr()
    
    assert "Schedule for date:" in captured.out
    assert "First Row:" in captured.out
    assert "Second Row:" in captured.out
    assert "Third Row:" in captured.out
    assert "Fourth Row:" in captured.out
    assert "Fifth Row:" in captured.out
