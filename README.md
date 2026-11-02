![Introduction banner: the sleeping car corridor before any name is spoken](intro-banner.png)

# dat-pseudonymize-column

Title block: the name above is set in Bowlby One SC in lamp amber on a nightwatch indigo plate, with an ink rule beneath it and one small slipper at the left of the first heading only, in the manner of a log cover.

![Logo](logo.png)

![Wordmark banner](banner.png)

![Animated scene](scene.svg)

![Major separator](sep-heavy.svg)


# dat-Pseudonymize-Column
Replaces values in a specified column of a CSV file with pseudonyms drawn with the Faker library, routed by the shape of each value. Signed integers stay numeric, keeping the sign and the digit count. Decimals stay numeric, keeping the sign, the integer digit count, and the number of decimal places. Email shaped values are replaced with an email, dates in YYYY-MM-DD form or DD/MM/YYYY form are replaced with a date in the same form, one or two word strings are replaced with a name, and longer text is replaced with text. Empty cells stay empty. Each distinct original value gets one pseudonym: the first value drawn for it is reused for every later row with the same original, so repeated values still match each other in the output and the column can still be used as a key. A --seed makes the draws reproducible, and the mapping holds within a seeded run as well. Other shapes are not preserved as their own kind: a value that matches none of the classes above is replaced with a name.


![Major separator](sep-heavy.svg)

> Log note: repeats share one pseudonym. Each distinct original value draws one pseudonym, and that same pseudonym serves every later row holding the same original, so repeats still match each other in the output and the column can still serve as a join key.

## Install
`git clone https://github.com/ShadowStrikeHQ/dat-pseudonymize-column`


![Minor separator](sep-light.svg)

> Log note: seed zero counts as a seed. The code tests for None, so --seed 0 works, and a seed makes the draws repeatable.

## Usage
`./dat-pseudonymize-column [params]`


![Minor separator](sep-light.svg)

> Log note: leading zeros are lost. A three digit value written with leading zeros draws a plain three digit number, and a code can come back looking like a quantity.

## Parameters
- `-h`: Show help message and exit
- `--locale`: Locale for Faker (default: en_US).
- `--seed`: Seed for Faker's random number generator for reproducibility. Repeated original values receive the same pseudonym within a run, with or without a seed.


![Minor separator](sep-light.svg)

> Log note: a slash date always returns day first. A month first value in that layout comes back day first, and nothing in the output marks the swap.

## License
Copyright (c) ShadowStrikeHQ

![Minor separator](sep-light.svg)

![Major separator](sep-heavy.svg)

## Night log notes, gathered at the last door

The buttons of this re-skin read Swap the Column, Set the Seed, and Read the Night Log. Its headings read One Column Only, Shape Chooses the Swap, Repeats Still Match, Zero Is a Real Seed, and Zeros Are Not Kept. The working form is python3 main.py, then the input CSV path, then the output CSV path, then the column name, with --locale (default en_US) and --seed (an integer, no default) after them. Python 3 and Faker at 20.1.0 or later are required, and the Faker import sits at the top of main.py, so without Faker even a request for help stops at that import. A missing column, an empty input, and a missing input file each end the run at exit 1, a short row is written without a swap for that cell, and a clean run exits 0. Seed zero is a real seed. Leading zeros are not kept. The repository LICENSE file carries the MIT License; its holder line pairs a pen name with one initial for the rest of the name, and that initial is left unexpanded here.
