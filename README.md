# Space Invaders! 

To play the game: 
1. Download this repository.
2. Open and run SpaceInvaders.py. 

This program emulates and runs the arcade game Space Invaders. 
It reads in data from an external file, included as "StartingInformation.txt", 
and relies on several image files, all included.
It will output a text file with the results of the game.

A note on effciency:
The program will run, but very slowly, since there are lots of intervals set, 
between the animation and the score & lives upkeep. 
However, if you comment out the two interval timers for the lives and score 
upkeeps, the animation will run well. Those two lines are labeled in the comments, 
and close to the end of the SpaceInvaders function. 
