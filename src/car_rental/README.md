# Car Rental Data

This is the generated Car Rental info.

## How it works

The logic to generate the data is located in `cars.py`.

Basically we read the `cars.csv` file that has name of many cars and their types. Running this file generates `cars.json` which separates the cars in three main types `Luxury`, `Premium` and `Basic`. Each car has a `price_multiplier` that dictates how expensive renting that car should be. We will also have a city multiplier and based on those two info we can find the price for rental. We may also make some consideration of time of week.

The images of the cars are in the `images` folder.
