"""
##################################
###        monkey vision       ###
##################################

Usage:
------
 $ monkey_vision [options] [id] [id ...]

 Help:
 ------
 $ monkey_vision -h
 $ monkey_vision --help


 Get image event point:
 Will return the list of possible interaction coordinates (event points) 
 visible in the provided screenshot. 
 ------
 $ monkey_vision -r imagePath
 $ monkey_vision --run imagePath


 Percentage compare between two images:
 Will return the calculated percentage of the match between two provided images.
 ------
 $ monkey_vision -m imagePath1 imagePath2
 $ monkey_vision --match imagePath1 imagePath2

"""

import sys
from monkey_vision.vision import get_event_points, percengate_compare

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return

    run_monkey_vision = "-r" in opts or "--run" in opts
    run_monkey_compare = "-m" in opts or "--match" in opts

    if run_monkey_vision:
        if not args:
            print("Error: An image path is required to analyze event points")
            return
        image_path = args[0]
        event_points = get_event_points(args[0])
        print(event_points)
        return event_points
    
    if run_monkey_compare:
        if not args or len(args) < 2:
            print("Error: Two image paths are required to run comparison.")
            return
        percentage_match = percengate_compare(args[0],  args[1])
        print(percentage_match)
        return percentage_match
    
    print("NO operation! Please refer to `monkey_vision --help` for more information.")

if __name__ == "__main__":
    main()