![Banner](banner.png)

# dat-Pseudonymize-Column
Replaces values in a specified column of a CSV file with pseudonyms drawn with the Faker library, routed by the shape of each value. Signed integers stay numeric, keeping the sign and the digit count. Decimals stay numeric, keeping the sign, the integer digit count, and the number of decimal places. Email shaped values are replaced with an email, dates in YYYY-MM-DD form or DD/MM/YYYY form are replaced with a date in the same form, one or two word strings are replaced with a name, and longer text is replaced with text. Empty cells stay empty. Each distinct original value gets one pseudonym: the first value drawn for it is reused for every later row with the same original, so repeated values still match each other in the output and the column can still be used as a key. A --seed makes the draws reproducible, and the mapping holds within a seeded run as well. Other shapes are not preserved as their own kind: a value that matches none of the classes above is replaced with a name.

## Install
`git clone https://github.com/ShadowStrikeHQ/dat-pseudonymize-column`

## Usage
`./dat-pseudonymize-column [params]`

## Parameters
- `-h`: Show help message and exit
- `--locale`: Locale for Faker (default: en_US).
- `--seed`: Seed for Faker's random number generator for reproducibility. Repeated original values receive the same pseudonym within a run, with or without a seed.

## License
Copyright (c) ShadowStrikeHQ
