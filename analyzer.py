"""
This code analyzes all the combinations generated and fine tunes the output to generate fewer patterns

"""

def removePointsNotTouchingCross(combinations):
    """
    Removes combinations that cross the "grid-cross" without touching it
    This combination include
    1--->6
    1--->8
    2--->7
    2--->9
    3--->4
    3--->8
    4--->3
    4--->9
    6--->1
    6--->7
    7--->2
    7--->6
    8--->1
    8--->3
    8--->4
    9--->2
    9--->4
    """
    
    newCombination = []
    valid = False
    for comb in combinations:
        for n in range (0,len(comb)-1,1):
            if comb[n] == 1 and comb[n+1] in (6,8):
                valid = False
                break
            elif comb[n] == 2 and comb[n+1] in (7,9):
                valid = False
                break
            elif comb[n] == 3 and comb[n+1] in (4,8):
                valid = False
                break
            elif comb[n] == 4 and comb[n+1] in (3,9):
                valid = False
                break
            elif comb[n] == 6 and comb[n+1] in (1,7):
                valid = False
                break
            elif comb[n] == 7 and comb[n+1] in (2,6):
                valid = False
                break
            elif comb[n] == 8 and comb[n+1] in (1,3):
                valid = False
                break
            elif comb[n] == 9 and comb[n+1] in (4,2):
                valid = False
                break
            else:
                valid = True
        
        if valid == True:
            newCombination.append(comb)
    return newCombination

        
def analyzeWithAI(combinations):
    """
    This function will analyze the combinations using an AI and will return the most likely pattern
    """
    return combinations 
