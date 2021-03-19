import sys, json
from random import shuffle

# Edge-match puzzle solver v1

def openFile():
    if len(sys.argv) < 2:
        print("File must be specified, quitting")
        return
    else:
        try:
            file = open(sys.argv[1])
            array = file.read().replace("\n", " ")
            file.close()

            data  = json.loads(array)
            cards = []
            for n in range(len(data)):
                cards.append(data[str(n)])
            return cards

        except NameError:
            print("File could not be found")
            return


    
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
        try:
            if (solution[posn][0] + solution[5][2]) == 0 and (solution[posn][1] + solution[7][3]) == 0:
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

    if len(findMatches(card, posn)) == 0:
        if checkValidSolution(grid, 8):
            return True
        else:
            removeCard(card)
            return False
    else:
        children = findMatches(card, posn)
        posn += 1
        for c in list(children):
            if backtrack(c, posn):
                return True
        removeCard(card)
        return False


results_table = []

def printResults(count):
    print("Count of tries/attempts to solve " + count)


def gameStart():
    for n in range(0, 9):
        for z in range(0, 4):
            cards[n] = rightRotate(cards[n], 1)
            if checkValidSolution(grid, 8):
                print("Solution is: " + str(grid))
                results_table.append(grid)
                printResults(str(trackCount()))
                return
            else:
                backtrack(cards[n], 1)

cards = openFile()
shuffle(cards)
gameStart()
            
# data to be written row-wise in csv file

# opening the csv file in 'a+' mode
#file = open('results_table.csv', 'a+', newline ='')  
# writing the data into the file
#with file:
#    write = csv.writer(file)
#    write.writerows(results_table)


