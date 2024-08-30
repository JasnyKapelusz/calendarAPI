import csv
import re
from datetime import datetime, timedelta

desired_format = r"\d{1,2}/\d{1,2}/\d{4}"  # Pattern for date in format "month/day/year"
dates_found = []

# Read the CSV file and store the rows
rows = []
with open("maj.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        rows.append(row)

# Extract dates from the CSV
for row in rows:
    dates = re.findall(desired_format, ",".join(row))
    dates_found.extend(dates)


def generate_schedule():
    # Początkowa godzina zajęć
    start_time = datetime.strptime("08:00", "%H:%M")

    # Długość jednego bloku zajęć (w minutach)
    block_length = 90

    # Długości przerw między blokami zajęć (w minutach)
    breaks = [15, 30, 15, 10]

    schedule = []
    breakss = []

    # Generate time intervals
    block_counter = 0
    while start_time.hour < 21:
        if block_counter % 2 == 0:  # If it's a class block
            end_time = start_time + timedelta(minutes=block_length)
            schedule.append(
                start_time.strftime("%H:%M") + "-" + end_time.strftime("%H:%M")
            )
            start_time = end_time
        else:  # If it's a break
            przerwa = breaks[block_counter // 2]
            end_time = start_time + timedelta(minutes=przerwa)
            breakss.append("Przerwa: " + str(przerwa) + " minut")
            start_time = end_time
        block_counter += 1

    return schedule[:16], breakss[:16]  # Return only the first 16 blocks


def print_schedule_for_date(date):
    day = date.split("/")[1]  # Extract the day from the date
    start_index = (int(day) - 1) * 16 + 1  # Calculate the start index for the given day
    end_index = start_index + 16  # Calculate the end index

    # Print the schedule for the given date
    print("Schedule for date:", date)
    print("First Row:", rows[0][start_index:end_index])
    print("Second Row:", rows[1][start_index:end_index])
    print("Third Row:", rows[2][start_index:end_index])
    print("Fourth Row:", rows[3][start_index:end_index])
    print("Fifth Row:", rows[4][start_index:end_index])
    print()  # Extra line for readability


# Example usage: Print the schedule for a specific date found in the CSV
if dates_found:
    for date in dates_found:
        print_schedule_for_date(date)
else:
    print("No dates found in the CSV.")
