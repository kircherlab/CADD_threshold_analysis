import sys
import csv
import gzip


def specific_attributes(csv_input, csv_output, attributes=None):

    if attributes is None:
        return csv_input
    else:
        with gzip.open(csv_input, mode='rt', newline='') as originalfile:
            reader = csv.DictReader(originalfile)

            with open(csv_output, 'w', newline='') as newfile:
                fieldnames = attributes
                writer = csv.DictWriter(newfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    writer.writerow({attr: row[attr] for attr in attributes})


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter_variants.py <input_csv> <output_csv> <attributes_file>")
        sys.exit(1)

    csv_input = sys.argv[1]
    csv_output = sys.argv[2]
    attributes_file = sys.argv[3]

    with open(attributes_file, 'r') as f:
        attributes = [line.strip() for line in f]

    specific_attributes(csv_input, csv_output, attributes)
