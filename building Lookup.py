import json
import os
from sortedcontainers import SortedDict

# Create a SortedDict (TreeMap equivalent in Python)
buildings = SortedDict({
    1: "Administration Building",
    4: "ROTC Building",
    5: "Academic Office Building, College of Business, Social Sciences",
    7: "Electrical Energy Resources Centre",
    8: "Dow Environmental Sciences & Engineering Building",
    9: "Alumni House, Advancement & Alumni Engagement",
    10: "Rozsa Center for the Performing Arts",
    11: "Walker Hall",
    12: "Minerals & Materials Engineering Building",
    13: "Center for Diversity & Inclusion",
    14: "Grover C. Dillman Hall",
    15: "Fisher",
    16: "Public Safety & Police Services",
    17: "J. R. Van Pelt & John & Ruanne Opie Library",
    18: "U. J. Noblet Forestry Building",
    19: "Chemical Sciences & Engineering Building",
    20: "R. L. Smith MEEM",
    24: "Student Development Complex",
    25: "Kearly Stadium Press Box",
    28: "Kanwal & Ann Rekhi Hall",
    30: "Little Huskies Child Development Center",
    31: "Douglass Houghton Hall",
    32: "Daniell Heights Apartments",
    34: "Memorial Union Building",
    37: "Wadsworth Hall",
    38: "West McNair Hall",
    40: "East McNair Hall",
    44: "Facilities Management, Husky Motors",
    45: "Sustainability Demonstration House",
    48: "Hillside Place",
    50: "Gates Tennis Center",
    51: "Grad Commons",
    82: "Transfer House",
    84: "Harold Meese Center, Psychology & Human Factors",
    95: "Advanced Technology Development Complex",
    100: "Great Lakes Research Center",
    103: "A. E. Seaman Mineral Museum",
    107: "Peace Corps Master's International House",
    114: "H-STEM Building",
    119: "East Hall—Opening Fall 2025"
})


def edit_location_in_json(directory):
    for root, dirs, files in os.walk(directory):
        # Skip directories starting with '.'
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)

                try:
                    # Load JSON data
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Modify the "Location" field in each entry
                    for entry in data:
                        location = entry.get("Location", "")
                        if location[:2].isdigit():
                            # Extract the building number and convert to int
                            building_number = int(location[:2])
                            # Replace the first two digits with the building name
                            entry["Location"] = buildings.get(building_number, "Unknown Building") + location[2:]

                    # Save the updated JSON data back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)

                    print(f"Updated 'Location' for file: {file_path}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error processing file {file_path}: {e}")


# Run the function, specifying the new location
edit_location_in_json("./")
