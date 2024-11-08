import os
import mysql.connector
from mysql.connector import Error
import json

# Database connection details
db_config = {
    'user': 'Nuh',
    'password': 'Uhh',
    'host': 'localhost'
}


def create_schemas_and_tables(path):
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Traverse directories and process JSON files
        for root, dirs, files in os.walk(path):
            schema_name = os.path.basename(root)
            if schema_name.startswith('.'):
                continue  # Skip hidden directories

            # Create schema if it doesn't already exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{schema_name}`;")
            cursor.execute(f"USE `{schema_name}`;")
            print(f"Schema '{schema_name}' created or already exists.")

            for file_name in files:
                if file_name.endswith('.json'):
                    table_name = file_name.rsplit('.', 1)[0]

                    # Load JSON file
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as json_file:
                        json_data = json.load(json_file)

                        # If the JSON contains multiple objects, get the keys from the first object
                        if isinstance(json_data, list) and len(json_data) > 0:
                            columns = json_data[0].keys()

                            # Create table with columns matching the JSON keys
                            create_table_query = f"""
                                CREATE TABLE IF NOT EXISTS `{table_name}` (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    uuid CHAR(36) NOT NULL DEFAULT (UUID()),  -- UUID column with default value of a new UUID
                                    {', '.join([f'`{col}` TEXT' for col in columns])},
                                    UNIQUE KEY unique_uuid (uuid)  -- Ensure UUID is unique across all records
                                );
                            """

                            cursor.execute(create_table_query)
                            print(f"Table '{table_name}' created in schema '{schema_name}'.")

                            # Insert JSON data into the table
                            for record in json_data:
                                placeholders = ', '.join(['%s'] * len(columns))
                                insert_query = f"""
                                    INSERT IGNORE INTO `{table_name}` ({', '.join([f'`{col}`' for col in columns])}, `uuid`)
                                    VALUES ({placeholders}, UUID());
                                """
                                values = tuple(record.get(col, None) for col in columns)
                                cursor.execute(insert_query, values)
                                connection.commit()

        cursor.close()
        connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)


# Specify the directory path
directory_path = "./MTU Banweb Dump"
create_schemas_and_tables(directory_path)
