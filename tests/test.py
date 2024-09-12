from main import generate_schedule, print_schedule_for_date


def test_generate_schedule():
    schedule, breaks = generate_schedule()
    assert len(schedule) == 16
    assert "08:00-09:30" in schedule

def test_print_schedule_for_date():
    rows = [
        [""] * 100,
        [""] * 100,
        [""] * 100,
        [""] * 100,
        [""] * 100,
    ]
    rows[0][1:17] = [f"Class {i}" for i in range(1, 17)]
    result = print_schedule_for_date("01/01/2023", rows)
    assert result["First Row"] == [f"Class {i}" for i in range(1, 17)]
