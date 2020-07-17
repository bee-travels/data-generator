
# buisness:
# --> will choose recommendation based on what most business people choose. Based on income >200000, will choose the fastest option for
# for inbetween, randomly select OR choose middle priced options
# flights and most expensive option for time/luxury.. For budget (<100000), choose least expensive recommendations

# business tags for hotel/car:

# more likely to be buisness if traveling with (1. leaving within 3-30 days in advance (2. also, 1 person
# if traveling 1-19 days in advanced, 85% chance business.
#           unless income > 200,000, 90% chance of being time (time is a rich business man); select highest price
# if traveling 20-30 days in advanced 60% chance business and 1 person
#           income > 200,000, 60% chance of being time (time is a rich business man)
# elif traveling 20-30 days in advanced 40% chance business and 2-3 people
#           income > 200,000, still 40% chance of being time (time is a rich business man)
# elif traveling 20-30 days in advanced 10% chance business and 4 or more people
#           income > 200,000, still 40% chance of being time (time is a rich business man)
# if traveling 30-60 days in advanced, 15% chance of leisure

# leisuire:
# --> will choose recommendation based on what most leisure people choose. Based on income >200000, will choose the luxury option
# for inbetween, randomly select OR choose middle priced options
# For budget (<100000), choose least expensive recommendations

# more likely to be leisure if (1. leaving 20-60 days in advanced (2. also 2 people or more
# if traveling 1-19 days in advance, 15% chance of being leisure. if also income > 200,000 then only 10% chance of leisure
# if traveling 20-30 days in advance and 1 person, only 40% chance of being leisure
# if traveling 20-30 days in advance and 2-3 people, 60% chance of being leisure
# if traveling 20-30 days in advance and 4 or more people, 90% chance of being leisure
# if traveling 30-60 days in advanced, 85% chance of leisure

# time
# leave also 7-14 days in advanced with high income > 200000: will select highest priced hotel within a 2 week timeline.
#    Will select the shortest duration flight, then most expensive
# luxury
# leave 30-60 days in
# budget
# will select cheapest
