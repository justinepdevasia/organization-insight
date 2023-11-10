import csv

# Read the objects.csv file and create a set of valid IDs
valid_ids = set()
with open('objects.csv', 'r') as objects_file:
    objects_reader = csv.DictReader(objects_file)
    for row in objects_reader:
        valid_ids.add(row['id'])

# Function to filter and write data to a new CSV file
def filter_and_write(input_file, output_file, id_column_names):
    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
        reader = csv.DictReader(in_file)
        writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            if all(row[id_column] in valid_ids for id_column in id_column_names):
                writer.writerow(row)

# Filter and write data for ipos.csv
filter_and_write('ipos.csv', 'filtered_ipos.csv', ['object_id'])

# Filter and write data for acquisitions.csv
filter_and_write('acquisitions.csv', 'filtered_acquisitions.csv', ['acquiring_object_id', 'acquired_object_id'])
