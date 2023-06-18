import re

def add_car(model, skin, data_file):
    # Read the data file
    with open(data_file, 'r') as file:
        lines = file.readlines()

    # Find the index of the last AI=none car and AI=fixed
    none_index = -1
    fixed_index = -1
    for i, line in enumerate(lines):
        if line.strip() == 'AI=none':
            none_index = i
        elif line.strip() == 'AI=fixed':
            fixed_index = i

    if none_index == -1 or fixed_index == -1:
        print("Error: Could not find the required lines in the file.")
        return

    # Find the car ID
    car_id = 0
    pattern = r"\[CAR_(\d+)]"
    for line in reversed(lines[:none_index]):
        match = re.search(pattern, line)
        if match:
            car_id = int(match.group(1))
            break

    # Find the position to insert the new car entry
    insert_index = none_index
    while insert_index < fixed_index and lines[insert_index].strip() != '':
        insert_index += 1

    # Create the new car entry
    new_car_entry = f"\n[CAR_{car_id+1}]\n"
    new_car_entry += f"MODEL={model}\n"
    new_car_entry += f"SKIN={skin}\n"
    new_car_entry += "SPECTATOR_MODE=0\n"
    new_car_entry += "DRIVERNAME=\n"
    new_car_entry += "TEAM=\n"
    new_car_entry += "GUID=\n"
    new_car_entry += "BALLAST=0\n"
    new_car_entry += "RESTRICTOR=0\n"
    new_car_entry += "AI=none\n"

    # Insert the new car entry into the lines list
    lines.insert(insert_index, new_car_entry)

    # Increment the car IDs of the existing cars after the insertion point
    for i in range(insert_index + 1, fixed_index):
        match = re.search(pattern, lines[i])
        if match:
            old_car_id = int(match.group(1))
            new_line = re.sub(pattern, f"[CAR_{old_car_id+1}]", lines[i])
            lines[i] = new_line

    # Write the updated lines back to the file
    with open(data_file, 'w') as file:
        file.writelines(lines)



def add_car_to_cfg(model, file_path):
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the CARS line and the first traffic car
    cars_index = -1
    traffic_index = -1
    for i, line in enumerate(lines):
        if line.startswith("CARS="):
            cars_index = i
            break

    if cars_index == -1:
        print("Error: Could not find the CARS line in the file.")
        return

    cars_line = lines[cars_index].strip()
    cars = cars_line.split("=")[1].split(";")

    # Check if the new car model is already present
    if model in cars:
        print("Car model already exists. No changes made.")
        return

    for i, car in enumerate(cars):
        if car.startswith("traffic_"):
            traffic_index = i
            break

    if traffic_index == -1:
        print("Error: Could not find the first traffic car in the file.")
        return

    # Update the CARS line
    cars.insert(traffic_index, model)
    updated_cars_line = "CARS=" + ";".join(cars) + "\n"
    lines[cars_index] = updated_cars_line

    # Find the MAX_CLIENTS line and increment the value
    max_clients_index = -1
    for i, line in enumerate(lines):
        if line.startswith("MAX_CLIENTS="):
            max_clients_index = i
            break

    if max_clients_index == -1:
        print("Error: Could not find the MAX_CLIENTS line in the file.")
        return

    max_clients_line = lines[max_clients_index].strip()
    max_clients_value = int(max_clients_line.split("=")[1])
    updated_max_clients_line = f"MAX_CLIENTS={max_clients_value + 1}\n"
    lines[max_clients_index] = updated_max_clients_line

    # Write the updated lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Usage example
# file_path = 'entry_list.ini'
# cfg_file_path = 'server_cfg.ini'
# model = 'new_car_model'
# skin = 'new_car_skin'

# add_car(model, skin, file_path)
# add_car_to_cfg(model, cfg_file_path)
