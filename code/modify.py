import csv

# Specify the path to your CSV file
filename = '/home/kangyi/Lyrics-audio-Alignment/dataset/output-en/metadata.csv'

# This will hold all rows from the CSV, 
# each row is a list of values
data = []

with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    data.append(header)
    for row in reader:
        if row[1] == None or row[1] == '': 
            row[1] = ' ' 
        
        data.append(row)

# Specify the name of the new CSV file you want to create
new_filename = '/home/kangyi/Lyrics-audio-Alignment/dataset/output-en/metadata new.csv'

with open(new_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write each list in 'data' as a row in the new CSV
    for row in data:
        writer.writerow(row)

print(f"Data successfully written to {new_filename}")