import csv
import re
from datetime import datetime, timedelta

class ScheduleManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.rows = self.read_csv_file()
        self.desired_format = r"\d{1,2}/\d{1,2}/\d{4}"  # Pattern for date in format "month/day/year"
        self.dates_found = self.extract_dates_from_csv()
    
    def read_csv_file(self):
        rows = []
        try:
            with open(self.file_path, newline="") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
        return rows
    
    def extract_dates_from_csv(self):
        dates_found = []
        for row in self.rows:
            dates = re.findall(self.desired_format, ",".join(row))
            dates_found.extend(dates)
        return dates_found
    
    def generate_schedule(self):

        start_time = datetime.strptime("08:00", "%H:%M")
        block_length = 90
        breaks = [15, 30, 15, 10]

        schedule = []
        breakss = []

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

    def print_schedule_for_date(self, date):

        day = date.split("/")[1]  # Extract the day from the date
        start_index = (int(day) - 1) * 16 + 1  # Calculate the start index for the given day
        end_index = start_index + 16  # Calculate the end index

        # Print the schedule for the given date
        print("Schedule for date:", date)
        print("First Row:", self.rows[0][start_index:end_index])
        print("Second Row:", self.rows[1][start_index:end_index])
        print("Third Row:", self.rows[2][start_index:end_index])
        print("Fourth Row:", self.rows[3][start_index:end_index])
        print("Fifth Row:", self.rows[4][start_index:end_index])
        print()  # Extra line for readability

# Example usage
if __name__ == "__main__":
    file_path = "maj.csv"
    manager = ScheduleManager(file_path)
    
    if manager.dates_found:
        for date in manager.dates_found:
            manager.print_schedule_for_date(date)
    else:
        print("No dates found in the CSV.")
