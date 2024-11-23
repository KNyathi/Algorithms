from datetime import datetime, timedelta
from collections import defaultdict

# Constants
SHIFT_8_HOURS = 8
SHIFT_12_HOURS = 12
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WEEKENDS = ["Saturday", "Sunday"]

# Helper Functions
def create_time_blocks(start_time, hours):
    """Creates start and end time blocks."""
    start = datetime.strptime(start_time, "%H:%M")
    end = start + timedelta(hours=hours)
    return start, end

def assign_breaks(driver, start, end, break_type):
    """Assign breaks to the driver during their shift."""
    breaks = []
    if break_type == "10-min":
        # Stagger 10-min breaks every 2 hours
        current = start + timedelta(hours=2)
        while current + timedelta(minutes=10) < end:
            breaks.append((current.strftime("%H:%M"), (current + timedelta(minutes=10)).strftime("%H:%M")))
            current += timedelta(hours=2)
    elif break_type == "1-hour":
        # 1-hour break during a lunch window
        lunch_start = datetime.strptime("13:00", "%H:%M")
        lunch_end = datetime.strptime("15:00", "%H:%M")
        if start <= lunch_start < end:
            breaks.append((lunch_start.strftime("%H:%M"), (lunch_start + timedelta(hours=1)).strftime("%H:%M")))
        elif lunch_start <= start < lunch_end:
            breaks.append((start.strftime("%H:%M"), (start + timedelta(hours=1)).strftime("%H:%M")))
    return breaks

# Classes
class Driver:
    def __init__(self, driver_id, shift_type):
        self.driver_id = driver_id
        self.shift_type = shift_type
        self.schedule = {day: [] for day in WEEKDAYS + WEEKENDS}
        self.breaks = {day: [] for day in WEEKDAYS + WEEKENDS}

class Bus:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.schedule = {day: [] for day in WEEKDAYS + WEEKENDS}

# Initialize buses and drivers
buses = [Bus(f"Bus_{i+1}") for i in range(8)]
drivers = []
driver_count = 0

# Rest day counter for 12-hour drivers
rest_day_counter = {}

# Reset schedules and rest-day counter
for bus in buses:
    bus.schedule = {day: [] for day in WEEKDAYS + WEEKENDS}

for driver in drivers:
    driver.schedule = {day: [] for day in WEEKDAYS + WEEKENDS}
    driver.breaks = {day: [] for day in WEEKDAYS + WEEKENDS}

# Adjusted allocation logic for 12-hour drivers
def allocate_continuous_12hr_drivers():
    global driver_count

    # Assign 8-hour drivers for weekdays
    for bus_index, bus in enumerate(buses):
        driver_count += 1
        driver = Driver(f"Driver_{driver_count}", "8-hour")
        drivers.append(driver)
        for day in WEEKDAYS:  # 8-hour drivers only work on weekdays
            start_time = (datetime.strptime("06:00", "%H:%M") + timedelta(minutes=bus_index * 10)).strftime("%H:%M")
            start, end = create_time_blocks(start_time, SHIFT_8_HOURS)
            breaks = assign_breaks(driver, start, end, "10-min")
            driver.breaks[day] = breaks
            driver.schedule[day].append((start, end, bus.bus_id))
            bus.schedule[day].append((start, end, driver.driver_id))

    # Assign continuous 12-hour drivers for all days
    for bus_index, bus in enumerate(buses):
        for day in WEEKDAYS + WEEKENDS:  # Cover all days of the week
            available_driver = None
            # Find a rested driver or assign a new one
            for driver_id, rest in rest_day_counter.items():
                if rest == 0:  # Driver available
                    available_driver = driver_id
                    rest_day_counter[driver_id] = 2  # Set 2-day rest after this shift
                    break
            if not available_driver:  # If no rested driver, assign a new one
                driver_count += 1
                available_driver = driver_count
                rest_day_counter[available_driver] = 2

            driver = next(
                (d for d in drivers if d.driver_id == f"Driver_{available_driver}"),
                Driver(f"Driver_{available_driver}", "12-hour"),
            )
            if driver.driver_id not in [d.driver_id for d in drivers]:
                drivers.append(driver)

            start_time = (datetime.strptime("14:15", "%H:%M") + timedelta(minutes=bus_index * 10)).strftime("%H:%M")
            start, end = create_time_blocks(start_time, SHIFT_12_HOURS)
            breaks = assign_breaks(driver, start, end, "1-hour")
            driver.breaks[day] = breaks
            driver.schedule[day].append((start, end, bus.bus_id))
            bus.schedule[day].append((start, end, driver.driver_id))

            # Decrement rest days for all other drivers
            for driver_id in rest_day_counter.keys():
                if driver_id != available_driver and rest_day_counter[driver_id] > 0:
                    rest_day_counter[driver_id] -= 1

# Allocate shifts for the week with continuous operation
allocate_continuous_12hr_drivers()

# Output the schedule in the requested format
print("Final Bus Schedule:")
for bus in buses:
    print(f"\n{bus.bus_id} Weekly Schedule:")
    for day in WEEKDAYS + WEEKENDS:
        if bus.schedule[day]:
            print(f"  {day}:")
            for shift in bus.schedule[day]:
                start_time = shift[0].strftime("%H:%M")
                end_time = shift[1].strftime("%H:%M")
                driver_id = shift[2]
                print(f"    Time: {start_time} - {end_time}, Driver: {driver_id}")

print("\nFinal Driver Schedule:")
for driver in drivers:
    print(f"\n{driver.driver_id} ({driver.shift_type}) Weekly Schedule:")
    for day in WEEKDAYS + WEEKENDS:
        if driver.schedule[day]:
            print(f"  {day}:")
            for shift in driver.schedule[day]:
                start_time = shift[0].strftime("%H:%M")
                end_time = shift[1].strftime("%H:%M")
                bus_id = shift[2]
                print(f"    Time: {start_time} - {end_time}, Bus: {bus_id}")
            if driver.breaks[day]:
                print("    Breaks:")
                for b in driver.breaks[day]:
                    print(f"      {b[0]} - {b[1]}")

print(f"\nTotal Drivers Used: {driver_count}")
