import argparse
import csv
import logging
import re
import sys
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description='Pseudonymize a column in a CSV file using Faker.')
    parser.add_argument('input_file', help='Path to the input CSV file.')
    parser.add_argument('output_file', help='Path to the output CSV file.')
    parser.add_argument('column_name', help='Name of the column to pseudonymize.')
    parser.add_argument('--locale', default='en_US', help='Locale for Faker (default: en_US).')
    parser.add_argument('--seed', type=int, help='Seed for Faker\'s random number generator for reproducibility.')
    return parser

_INT_RE = re.compile(r'^[+-]?\d+$')
_FLOAT_RE = re.compile(r'^[+-]?(?:\d+\.\d*|\.\d+)$')
_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
_DATE_ISO_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_DATE_SLASH_RE = re.compile(r'^\d{2}/\d{2}/\d{4}$')

def _int_of_length(fake, digits):
    if digits <= 1:
        return fake.random_int(min=0, max=9)
    return fake.random_int(min=10 ** (digits - 1), max=(10 ** digits) - 1)

def draw_pseudonym(fake, value):
    """Draw one pseudonym whose shape follows the original value.

    Signed integers stay numeric and keep their sign and digit count.
    Decimals stay numeric and keep their sign, integer digit count, and
    decimal places. Email shaped values get an email, ISO and day first
    slash dates get a date in the same format, empty cells stay empty,
    one or two word strings get a name, and longer text gets text.
    """
    if value == "" or value.strip() == "":
        return value
    text = value.strip()
    if _INT_RE.match(text):
        sign = ""
        digits_text = text
        if text[0] in "+-":
            sign, digits_text = text[0], text[1:]
        return f"{sign}{_int_of_length(fake, len(digits_text))}"
    if _FLOAT_RE.match(text):
        sign = ""
        body = text
        if text[0] in "+-":
            sign, body = text[0], text[1:]
        int_part, _, frac_part = body.partition(".")
        int_digits = len(int_part) if int_part else 1
        places = len(frac_part)
        drawn_int = _int_of_length(fake, int_digits)
        if places:
            drawn_frac = fake.random_int(min=0, max=(10 ** places) - 1)
            return f"{sign}{drawn_int}.{drawn_frac:0{places}d}"
        return f"{sign}{drawn_int}."
    if _EMAIL_RE.match(text):
        return fake.email()
    if _DATE_ISO_RE.match(text):
        try:
            return fake.date(pattern="%Y-%m-%d")
        except TypeError:
            return fake.date()
    if _DATE_SLASH_RE.match(text):
        return fake.date_object().strftime("%d/%m/%Y")
    if len(text.split()) >= 3:
        try:
            return fake.text(max_nb_chars=max(10, len(text)))
        except Exception:
            return fake.name()
    return fake.name()

def pseudonymize_column(input_file, output_file, column_name, locale='en_US', seed=None):
    """
    Replaces values in a specified column of a CSV file with pseudonyms.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        column_name (str): Name of the column to pseudonymize.
        locale (str, optional): Locale for Faker. Defaults to 'en_US'.
        seed (int, optional): Seed for Faker's random number generator. Defaults to None.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the specified column name is not found in the CSV file.
        Exception: For other unhandled errors during file processing or pseudonym generation.
    """
    try:
        # Initialize Faker with locale and seed
        fake = Faker(locale)
        # seed 0 is a real seed a caller may pass for a reproducible run, so
        # test for None here rather than truthiness.
        if seed is not None:
            Faker.seed(seed)

        # The header is read and the column is checked before the output
        # file is opened. Opening the output first left a header-only file
        # behind on a bad column name, which looks like a successful run
        # with one row instead of the failure it was.
        with open(input_file, 'r', newline='') as infile:
            reader = csv.reader(infile)
            header = next(reader, None)
            if header is None:
                raise ValueError("Input CSV file is empty, no header row found.")
            try:
                column_index = header.index(column_name)
            except ValueError:
                raise ValueError(f"Column '{column_name}' not found in the CSV file.")
            rows = list(reader)

        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)

            # One pseudonym per distinct original value. Keeping the mapping
            # means repeated values that named the same thing in the input
            # still name the same pseudonym in the output, seeded runs
            # included, so the column can still be used as a key.
            mapping = {}
            # Process each row
            for row in rows:
                # Pseudonymize the specified column
                try:
                    original_value = row[column_index]
                    if original_value not in mapping:
                        mapping[original_value] = draw_pseudonym(fake, original_value)
                    row[column_index] = mapping[original_value]
                except IndexError:
                     logging.warning(f"Row is shorter than expected. Skipping pseudonymization for this row.")
                
                writer.writerow(row)
        logging.info(f"Successfully pseudonymized column '{column_name}' in '{input_file}' and saved to '{output_file}'.")


    except FileNotFoundError:
        logging.error(f"Input file '{input_file}' not found.")
        raise
    except ValueError as e:
        logging.error(str(e))
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

def main():
    """
    Main function to execute the pseudonymization process.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        pseudonymize_column(args.input_file, args.output_file, args.column_name, args.locale, args.seed)
    except (FileNotFoundError, ValueError) as e:
        logging.error(str(e))
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    
    print("Data pseudonymization completed successfully.")

if __name__ == "__main__":
    main()