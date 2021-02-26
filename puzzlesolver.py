# Edge-match puzzle solver v1
# TODO: feature to read file containing card structure in similar
# format and output results to stdout or a file
# Figure out better approach to initialization loop 
# how is first card placed being rotated?

# Define card deck as a list of lists; order is t,l,b,r
cards = [[-2, -3, 4, 2],     #0
         [2, 3, 4, 1],       #1
         [2, -3, 4, -1],     #2
         [1, 3, 4, -1],      #3
         [-2, -3, 4, -1],    #4
         [-1, 2, 4, -3],     #5
         [-4, 1, -2, -3],    #6
         [-4, 3, 1, 2],      #7
         [-4, 1, -3, 2]]     #8


# Create an empty list (grid) to place cards; order is
#  0  1  2
#  3  4  5
#  6  7  8
grid = []


# Returns the rotated list (card)
def rightRotate(lists, num):
    output_list = []

    for item in range(len(lists) - num, len(lists)):
        output_list.append(lists[item])

    for item in range(0, len(lists) - num):
        output_list.append(lists[item])

    return output_list


# Place a card on the grid
def placeCard(card):
    try:
        grid.append(card)
    except IndexError as error:
        print("error " + error)


# Remove a card from the grid
def removeCard(card):
    try:
        grid.remove(card)
    except IndexError as error:
        print("error " + error)


# Check if tile is correctly placed at each position;
# if a tile is placed in the last (8th position)
# the game must be over
def checkValidSolution(solution, posn):

    if posn == 0:  #this position is always valid
        return True
    if posn == 1:
        if (solution[posn][1] + solution[0][3]) == 0:
            return True
    if posn == 2:
        if (solution[posn][1] + solution[1][3]) == 0:
            return True
    if posn == 3:
        if (solution[posn][0] + solution[0][2]) == 0:
            return True
    if posn == 4:
        if (solution[posn][0] + solution[1][2]) == 0 and (solution[posn][1] + solution[3][3]) == 0:           
            return True
    if posn == 5:
        if (solution[posn][0] + solution[2][2]) == 0 and (solution[posn][1] + solution[4][3]) == 0:
            return True
    if posn == 6:
        if (solution[posn][0] + solution[3][2]) == 0:
            return True
    if posn == 7:
        if (solution[posn][0] + solution[4][2]) == 0 and (solution[posn][1] + solution[6][3]) == 0:
            return True
    if posn == 8:
        try: # This needs to have exception covered since we know we will be checking this as gameover condition
            if (solution[posn][0] + solution[5][2]) == 0 and (solution[posn][1] + solution[7][3]) == 0:
                #print("Valid at posn 8")
                return True
            else:
                return False
        except Exception:
            pass
    if posn > 8 or posn < 0:
        print("Invalid card position to be checked for validity: " + str(posn))
        return False


# Simply returns the cards which are available to play (not placed on grid)    
def getRemainingCards():
    remainingcards = cards.copy()
    for c in list(grid):
        try:
            remainingcards.remove(c)  ## rotated in cards, not rotated on grid?
        except Exception:
            try:
                for x in range(1, 4):
                    rc = rightRotate(c, x)
                    remainingcards.remove(rc)
            except Exception:
                pass
    return remainingcards


# Return the matches (children) of card at depth (posn) of tree
def findMatches(card, posn):
    matches = []
    remainingcards = getRemainingCards()
    #print("remainingcards are " + str(remainingcards))
    for card in list(remainingcards):
        placeCard(card)
        if checkValidSolution(grid,posn): #if the card matches in next posn, add to match list and remove from grid
            matches.append(card)
            removeCard(card)
        else: # try rotating to see if each card would otherwise fit
            removeCard(card) # remove the card that was placed as is (0 rotated)
            for r in range(1, 4): # try 3 rotation positions
                rcard = (rightRotate(card,r)) # rotate
                placeCard(rcard) # try the rotated card
                if checkValidSolution(grid,posn):            
                    matches.append(rcard)
                    for index, item in enumerate(cards):
                        if card == item:
                            cards[index] = rcard
                    removeCard(rcard)

                else: # rotation doesn't work, so just remove
                    removeCard(rcard)
    return matches

# simply track the count to see how many executions of backtrack function
def trackCount(i=[0]):
    i[0]+=1 # mutable variable get evaluated ONCE
    return i[0]

# Worker function to recurse through tree of card placement combinations
def backtrack(card, posn):
    trackCount()
    #print("cards are " + str(cards))
    remainingcards = getRemainingCards()
    if card in remainingcards:
        placeCard(card)
    else:
        try:
            for r in range(1, 4):
                rot = rightRotate(card, r)

                for index, item in enumerate(cards):
                    if rot == item:
                        cards[index] = card
            placeCard(card)

        except Exception:
            print("Error placing " + str(card))

    #print("grid is " + str(grid) + " posn is " + str(posn))
    if len(findMatches(card, posn)) == 0:
        if checkValidSolution(grid, 8):
            print("Game is over")
            return True
        else:
            #print("Leaf (no further matches) but not game over")
            removeCard(card)
            return False
    else:
        children = findMatches(card, posn)
        #print("children (matches) are " + str(children) + " for posn " + str(posn))
        posn = posn + 1
        for c in list(children):
            if backtrack(c, posn):
                return True
        removeCard(card)
        return False


# Try each card in start position; there are better ways to write this
for n in range(0, 9):
    if checkValidSolution(grid, 8): # there are better ways to check this
        print("Solution is: " + str(grid))
        print("Attempt count is: " + str(trackCount()))
        break
    else:
        backtrack(cards[n], 1)