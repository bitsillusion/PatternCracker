"""
     ___________________
    |                   |
    | 9      8        7 |
    |                   | 
    | 6      5        4 |
    |                   |
    | 3      2        1 |
    |___________________|

    THE TUPLES
    3-> (0,0)
    2-> (0,1)
    1-> (0,2)
    6-> (1,0)
    5-> (1,1)
    4-> (1,2)
    9-> (2,0)
    8-> (2,1)
    7-> (2,2)
"""


def generate_combinations(points):
    """
    Generate all possible combinations of the provided list of points.
    The list of points should be a list of lists.
    Each sublist should contain a list of numbers.
    """
    combinations = []
    
    #Remove redundant numbers in the list of points
    points_set = list(set(points))

    # Recursive helper function to generate combinations
    def generate_helper(current_combination, remaining_numbers):
        if not remaining_numbers:
            # If no more numbers are left, add the current combination to the list
            combinations.append(current_combination)
            return

        # Iterate through each number in the remaining numbers
        for i in range(len(remaining_numbers)):
            # Remove the current number from the remaining numbers
            next_number = remaining_numbers[i]
            remaining = remaining_numbers[:i] + remaining_numbers[i+1:]

            # Recursively call the helper function with the updated combination and remaining numbers
            generate_helper(current_combination + [next_number], remaining)

    # Start the generation process with an empty combination and all numbers
    generate_helper([], points_set)

    # Return the list of combinations
    return combinations

def tuple_to_number(tuples):
    """
    Converts a cells tuple id to a number 
    """
    conversion_table = {
        (0, 0): 7,
        (0, 1): 8,
        (0, 2): 9,
        (1, 0): 4,
        (1, 1): 5,
        (1, 2): 6,
        (2, 0): 1,
        (2, 1): 2,
        (2, 2): 3
    }
    return conversion_table[tuples]


def convert_to_tuple(numbers):
    """
    Converts a list of lists of numbers to tuple to be used to visualize the patterns
    """

    # Define the conversion table as a dictionary
    conversion_table = {
        7: (0, 0),
        8: (0, 1),
        9: (0, 2),
        4: (1, 0),
        5: (1, 1),
        6: (1, 2),
        1: (2, 0),
        2: (2, 1),
        3: (2, 2)
    }

    tuples = []

    for sublist in numbers:
        converted_sublist = []
        for number in sublist:
            if number in conversion_table:
                converted_sublist.append(conversion_table[number])
            else:
                raise ValueError(
                    f"Invalid number {number}. The number should be between 1 and 9.")
        tuples.append(converted_sublist)
    return tuples


def remove_invalid_combinations(combinations):
    """
    Removes invalid combinatons from the list of combinations
    This will ensure that generated patterns are valid
    A line shouuld not cross over a non selected point

    When two extreme points are selected, then a middle point must appear between them eg 7-4-1 not 7-1-2 or before them
    EXTREME POINTS 
    1---3--->2
    4---6--->5
    7---9--->8

    1---7--->4
    2---8--->5
    3---9--->6

    7---3--->5
    1---9--->5

    """
    valid_combinations = []
    valid = True

    def check_previous(n, x, comb):
        """Checks if the middle point exists before the current point 
            Args:
                n (int): the current index
                x (int): the middle point to check
                comb (int): the current combination to check against
        """
        for i in range(n, -1, -1):
            if comb[i] == x:
                return True
        return False

    for comb in combinations:
        #Checking if comb is valid
        for n in range(0,len(comb) -1):

            if comb[n] in (1,3) and comb[n+1] in (1,3):
                if check_previous(n,2,comb):
                    valid = True
                else:
                    valid = False
                    break
            elif comb[n] in (4,6) and comb[n+1] in (4,6):
                if check_previous(n,5,comb):
                    valid = True
                else:
                    valid = False
                    break
            elif comb[n] in (7,9) and comb[n+1] in (7,9):
                if check_previous(n,8,comb):
                    valid = True
                else:
                    valid = False
                    break
            elif comb[n] in (7,1) and comb[n+1] in (1,7):
                if check_previous(n,4,comb):
                    valid = True
                else:
                    valid = False
                    break
            elif comb[n] in (2,8) and comb[n+1] in (8,2):
                if check_previous(n,5,comb):
                    valid = True
                else:
                    valid = False
                    break
            elif comb[n] in (3,9) and comb[n+1] in (3,9):
                if check_previous(n,6,comb):
                    valid = True
                else:
                    valid = False
                    break
            elif (comb[n] in (7, 3) and comb[n+1] in (3, 7) or comb[n] in (1, 9) and comb[n+1] in (9, 1)):
                if check_previous(n,5,comb):
                    valid = True
                else:
                    valid = False
                    break
            valid = True        
        if valid:
            valid_combinations.append(comb)
    return valid_combinations

def visualizeHash(patternHash):
    """
        Create the corresponding pattern from a pattern hash
    """

def createPatternHash(pattern, hashingAlgorithm):
    """
        Create a hash representation of a function

    """
    