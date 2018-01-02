# Cell-Simulation

A repository for a very basic cell replication simulation. 
Requires python 3.

Upon loading the program all the cells are randomized with one cell being set as the bacteria cell. Each time the incrementation button is hit the screen will desplay the next generation.

Whenever the reset button is hit all of the cells are randomized again, including the bacteria's initial position and attributes.

If detailed is set to True in the source code each cell displays in the order of Food, Water, Temp for the land cells or Food Requirement, Water Requirement, a range of Min Temperature - Max Temperature and the days left to live.

The increment button becomes disabled whenever either the bacteria has been eliminated or whenever the bacteria hits 80% concentration, as that is a stable amount.
