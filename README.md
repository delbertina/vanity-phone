# vanity-phone
Generate possible vanity translations of a phone number.

## Included
- Python script for a lambda to convert a string into a vanity phone number
    - Handles any length and format of NA phone numbers & outputs back formatted
    - Method to automatically insert into DynamoDB using env var for table name

- React frontend for viewing the entries
    - Ran out of time to finish my idea for a quick and dirty method to query the database
    - For now, displays placeholder data on a minimally-styled page with MUI

## Stretch Goals

I only had a couple of hours to put towards this project, but with more time I would have worked on finishing up my Python CDK script for generating and setting up a working demo of connected services.

After that, I would focus my time on integrating the frontend with the system using API gateways etc. 

Possibly would have devoted more time to diving into Amazon Connect, but that service seems to have very limited free resources and quickly gets very expensive. Not looking to incure charges for this project just yet.

## Reflection

I spent the majority of the time I had to dedicate to this project on the python script. 

Initially, I tried to setup the weighting data in a more complicated way but ultimately settled on the current implementation. The script randomly selects an option from the list and some options appear more frequently than others.

I also persued structuring the data in a way that much more distinctly takes into account the scrabble scores for each letter and tries to generate vanity numbers that are the closest to 1.5x the count of translatable numbers (not including 1 and 0) to favor having a lot of common 1 point but also favor having 1 or 2 higher point value letters.

I decided that my definition of "best" was more about mimicking English word patterns such as avoiding double vowels. So I mixed the loose scrabble weighting with a backtracking algorithm and ended up really happy with the results I got from tests.

In an enterprise setting, it would probably be a better solution to generate all of the possible combinations and use machine learning trained on English words to assign a score to each possibility on how English-y the combination is and get the top results back.
