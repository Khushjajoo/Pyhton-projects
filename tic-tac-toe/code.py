"""tictactoe game for 2 players"""

choices=[]
for x in range (1, 10) :
    choices.append(x)

playerOneTurn = True
winner = False


def printBoard() :
    print( '\n -----')
    print( '|' + str(choices[0]) + '|' + str(choices[1]) + '|' + str(choices[2]) + '|')
    print( ' -----')
    print( '|' + str(choices[3]) + '|' + str(choices[4]) + '|' + str(choices[5]) + '|')
    print( ' -----')
    print( '|' + str(choices[6]) + '|' + str(choices[7]) + '|' + str(choices[8]) + '|')
    print( ' -----\n')


while winner==False:
    printBoard()

    if playerOneTurn :
        print( "Player 1:")
    else :
        print( "Player 2:")

    try:
        choice = int(input(">> "))
    except:
        print("please enter a valid field")
        continue

    if (choices[choice - 1] == 'X' or choices [choice-1] == 'O'):
        print("illegal move, please try again")
        continue

    if playerOneTurn :
        choices[choice - 1] = 'X'
    else :
        choices[choice - 1] = 'O'

    playerOneTurn = not playerOneTurn

    for x in range (0, 3) :
        y = x * 3
        if (choices[y-1] == choices[(y)] and choices[y-1] == choices[(y + 1)]) :
            winner = True
            printBoard()
            break
        if (choices[x-1] == choices[(x + 2)] and choices[x-1] == choices[(x + 5)]) :
            winner = True
            printBoard()
            break

    if((choices[0] == choices[4] and choices[0] == choices[8]) or
       (choices[2] == choices[4] and choices[4] == choices[6])) :
        winner = True
        printBoard()
        break
if (winner ==  False):
    print("Game is a draw")
if(__name__=="__main__")    
   print ("Player " + str(int(playerOneTurn + 1)) + " wins!\n")
