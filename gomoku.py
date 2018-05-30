import pygame, random, sys


bSize = 7
depth = 3
res = 666
heur = True


if len(sys.argv) == 2:
    arg = sys.argv[1]
elif len(sys.argv) >= 4:
    arg = sys.argv[1]
    bSize = int(sys.argv[2])
    depth = int(sys.argv[3])
    if len(sys.argv) == 5:
        if sys.argv[4] == "noh":
            heur = False
else:
    arg = "hvc"


pygame.init()
screen = pygame.display.set_mode((res,res))
screen.fill([255,255,255])

for n in range(bSize):
    pygame.draw.line(screen, (0,0,0), (n*res/bSize,res), (n*res/bSize,0))
    pygame.draw.line(screen, (0,0,0), (0,n*res/bSize), (res,n*res/bSize))

board = [[0 for x in range(bSize)] for y in range(bSize)]

allMoves = []
heuristics = [0]


# ----------------------------------------------------------------------------


iteration = 0

def ai(side):
    global depth
    global iteration

    if side == 1:
        iteration = 0
        bestScore = -float("inf")
        bestMoves = [[0,0]]
        for move in legalMoves():
            tmpMove(side, move)
            score = minValue(side, -float("inf"), float("inf"))
            tmpRemove(move)
            iteration -= 1
            sys.stdout.write("\r" + str(move) +" "+ str(score) + "    ")
            sys.stdout.flush()
            #print move, score
            if score >= bestScore:
                if score == bestScore:
                    bestMoves.append(move)
                else:
                    bestScore = score
                    bestMoves = [move]
        if bestScore == -float("inf"):
            return 0
        heuristics[0] = bestScore
        chosenMove = bestMoves[random.randint(0,len(bestMoves)-1)]
        allMoves.append(chosenMove)
        sys.stdout.write("\r%d" % bestScore)
        print " ---------", side, chosenMove #                                          disp
        if bestScore == -10000:
            print " -->  damn!"
        elif bestScore == 10000:
            print " --> victory is mine!"
        makeMove(side, chosenMove)
        
    elif side == 2:
        iteration = 0
        bestScore = float("inf")
        bestMoves = [[0,0]]
        for move in legalMoves():
            tmpMove(side, move)
            score = maxValue(side, -float("inf"), float("inf"))
            tmpRemove(move)
            iteration -= 1
            sys.stdout.write("\r" + str(move) +" "+ str(score) + "    ")
            sys.stdout.flush()
            #print move, score
            if score <= bestScore:
                if score == bestScore:
                    bestMoves.append(move)
                else:
                    bestScore = score
                    bestMoves = [move]
        if bestScore == float("inf"):
            return 0
        heuristics[0] = bestScore
        chosenMove = bestMoves[random.randint(0,len(bestMoves)-1)]
        allMoves.append(chosenMove)
        sys.stdout.write("\r%d" % bestScore)
        print " ---------", side, chosenMove #                                          disp
        if bestScore == 10000:
            print " -->  damn!"
        elif bestScore == -10000:
            print " --> victory is mine!"
        makeMove(side, chosenMove)


def minValue(side, alpha, beta):
    global depth
    global iteration
    iteration += 1
    ev = terminal(side, 1)
    if ev[0]: return ev[1]    # terminal state
    else:
        if side == 1: side2 = 2
        else: side2 = 1
        if iteration > depth:
            return heuristic(side, 1)
        bestScoreMin = float("inf")
        bestMoves = []
        #print board_ #                                                                disp
        for move in legalMoves():
            tmpMove(side2, move)
            score = maxValue(side2, alpha, beta)
            iteration -= 1
            tmpRemove(move)
            bestScoreMin = min(score, bestScoreMin)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return bestScoreMin


def maxValue(side, alpha, beta):
    global depth
    global iteration
    iteration += 1
    ev = terminal(side, -1)
    if ev[0]: return ev[1]    # terminal state
    else:
        if side == 1: side2 = 2
        else: side2 = 1
        if iteration > depth:
            return heuristic(side, -1)
        bestScoreMax = -float("inf")
        bestMoves = []
        #print board_ #                                                                disp
        for move in legalMoves():
            tmpMove(side2, move)
            score = minValue(side2, alpha, beta)
            iteration -= 1
            tmpRemove(move)
            bestScoreMax = max(score, bestScoreMax)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return bestScoreMax


def legalMoves():
    moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                moves.append([i,j])
    return moves


def tmpMove(side, pos):
    board[pos[0]][pos[1]] = side
    allMoves.append(pos)
    heuristics.append(heuristics[-1])

def tmpRemove(pos):
    board[pos[0]][pos[1]] = 0
    del allMoves[-1]
    del heuristics[-1]


def terminal(side, minmax):
    win = checkwin(side)
    if win:
        return [True, minmax*10000]

    if len(allMoves) == bSize*bSize:
        fullBoard = True
    else:
        fullBoard = False
    if fullBoard:
        return [True, 0]
    else:
        return [False, 0]


def checkwin(side):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == side:
                if j < bSize-4:
                    if board[i][j:j+5] == [side, side, side, side, side]:
                        return side
                if i < bSize-4:
                    if [x[j] for x in board[i:i+5]] == [side, side, side, side, side]:
                        return side
                if j < bSize-4 and i < bSize-4:
                    if [board[i+x][j+x] for x in range(5)] == [side, side, side, side, side]:
                        return side
                if j > 3 and i < bSize-4:
                    if [board[i+x][j-x] for x in range(5)] == [side, side, side, side, side]:
                        return side
    return 0
"""
def checkwin(side):
    if allMoves == []:
        return 0
    x = allMoves[-1][0]
    y = allMoves[-1][1]
    _x = max(0, x-5)
    _y = max(0, y-5)
    x_ = min(bSize, x+5)
    y_ = min(bSize, y+5)
    lines = [
        board[x][_y:y_],
        [p[y] for p in board[_x:x_]],
        [board[x+p][y+p] for p in range(-min(x-_x,y-_y), min(x_-x,y_-y))],
        [board[x+p][y-p] for p in range(-min(x-_x,y_-y-1), min(x_-x,y-_y))]
    ]
    print "lines:", lines
    for line in lines:
        for i in range(len(line) - 5+1):
            print [line[i+j] for j in range(5)]
            if all(side == line[i+j] for j in range(5)):
                return side
    print "-----"
"""

def heuristic(side, minmax):
    if not heur:
        return 0
    if side == 1:
        side2 = 2
    else:
        side2 = 1
    ev = 0
    x = allMoves[-1][0]
    y = allMoves[-1][1]
    _x = max(0, x-5)
    _y = max(0, y-5)
    x_ = min(bSize, x+5)
    y_ = min(bSize, y+5)

    line = board[x][_y:y_]
    if side2 not in line:
        ev += line.count(side)**2
    elif line.count(side) <= 2:
        ev += line.count(side2)**2+1
    line = [p[y] for p in board[_x:x_]]
    if side2 not in line:
        ev += line.count(side)**2
    elif line.count(side) <= 2:
        ev += line.count(side2)**2+1
    line = [board[x+p][y+p] for p in range(-min(x-_x,y-_y), min(x_-x,y_-y))]
    if side2 not in line:
        ev += line.count(side)**2
    elif line.count(side) <= 2:
        ev += line.count(side2)**2+1
    line = [board[x+p][y-p] for p in range(-min(x-_x,y_-y-1), min(x_-x,y-_y))]
    if side2 not in line:
        ev += line.count(side)**2
    elif line.count(side) <= 2:
        ev += line.count(side2)**2+1

    return heuristics[-1] + ev*minmax


def makeMove(side, pos):
    board[pos[0]][pos[1]] = side
    if side == 1: color = (200,0,0)
    else: color = (0,0,200)
    pygame.draw.circle(screen, color, (pos[0]*res/bSize+res/bSize/2+1, pos[1]*res/bSize+res/bSize/2+1), res/bSize/2-1, 0)


# ----------------------------------------------------------------------------


pygame.display.flip()
pygame.time.delay(500)
endofgame = False

if arg == "hvc":
    while True:
        for event in pygame.event.get():
            if not endofgame and event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if board[int(mousepos[0]/float(res)*bSize)][int(mousepos[1]/float(res)*bSize)] == 0:
                    makeMove(1, [int(mousepos[0]/float(res)*bSize), int(mousepos[1]/float(res)*bSize)])
                    pygame.display.flip()
                    if checkwin(1):
                        print "\n\n  red won!  \n\n"
                        endofgame = True
                        continue
                    ai(2)
                    pygame.display.flip()
                    if checkwin(2):
                        print "\n\n  blue won!  \n\n"
                        endofgame = True
                        continue
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()
elif arg == "cvh":
    turn = 0
    while True:
        for event in pygame.event.get():
            if not endofgame and turn%2==0:
                turn += 1
                ai(1)
                pygame.display.flip()
                if checkwin(1):
                    print "\n\n  red won!  \n\n"
                    print allMoves
                    endofgame = True
                    continue
            if not endofgame and event.type == pygame.MOUSEBUTTONDOWN:
                turn += 1
                mousepos = pygame.mouse.get_pos()
                if board[int(mousepos[0]/float(res)*bSize)][int(mousepos[1]/float(res)*bSize)] == 0:
                    makeMove(2, [int(mousepos[0]/float(res)*bSize), int(mousepos[1]/float(res)*bSize)])
                    pygame.display.flip()
                    if checkwin(2):
                        print "\n\n  blue won!  \n\n"
                        print allMoves
                        endofgame = True
                        continue
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()
elif arg == "cvc":
    while True:
        if not endofgame:
            ai(1)
            pygame.display.flip()
            if checkwin(1):
                print "\n\n  red won!  \n\n"
                print allMoves
                endofgame = True
                continue
            ai(2)
            pygame.display.flip()
            if checkwin(2):
                print "\n\n  blue won!  \n\n"
                print allMoves
                endofgame = True
                continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()
