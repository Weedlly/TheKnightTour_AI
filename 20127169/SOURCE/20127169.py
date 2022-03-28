import time
import sys
n = 8

start_x = 0
start_y = 0

init_x = 0
init_y = 0

writed = False

InitTime = time.perf_counter()
EndTime = 0

step = 0

move_x = [2, 1, -1, -2, -2, -1, 1, 2]
move_y = [1, 2, 2, 1, -1, -2, -2, -1]



'''
    Backtracking
'''

def isSafe(x, y, board):
	if(x >= 0 and y >= 0 and x < n and y < n and board[x][y] == -1):
		return True
	return False

def printBacktracking(n, board, runningTime):
    with open("20127169_backtrack.txt", "w") as f:
        f.write(str(init_y + 1) + " " + str(init_x + 1) + " " + str(n) + "\n")
        f.write(str(step) + "\n")
        f.write(str(runningTime * 1000) + "\n")
        for i in range(n):
            for j in range(n):
                f.write(str(board[i][j]))
                if (j != n - 1):
                    f.write(" ")
            if (i != n - 1):
                f.write("\n")


def solveKT(n,init_x,init_y):
  global EndTime
  global InitTime
  board = [[-1 for i in range(n)]for i in range(n)]
  board[init_x][init_y] = 1
  pos = 2
  InitTime = time.perf_counter()
  if (solveKTUtil(n, board, init_x, init_y, pos) == False):
      return False
  else:
      EndTime = time.perf_counter()
      printBacktracking(n, board, EndTime - InitTime)

def solveKTUtil(n,board, curr_x, curr_y, pos):
    global writed
    if(writed == True):
       return False
    EndTime = time.perf_counter()
    if((EndTime - InitTime) * 1000 > 60 * 60 * 1000):
        writed = True
        printBacktracking(n, board, EndTime - InitTime)
        return False
    if(pos == n**2 + 1):
        return True
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if(isSafe(new_x, new_y, board)):
            global step
            step = step + 1
            board[new_x][new_y] = pos
            if(solveKTUtil(n, board, new_x, new_y, pos+1)):
                return True

            # Backtracking
            board[new_x][new_y] = -1
    return False


'''
    Warnsdoff Heuristic
'''
def limits(x,y):
    return (x >= 0 and y >= 0) and (x < n and y < n)
 
def isempty(a,x,y):
    return (limits(x, y) and (a[y*n+x] < 0))
 
def getDegree(a,x,y):
    count = 0
    for i in range(8):
        if(isempty(a,x+move_x[i],y+move_y[i])):
            count += 1
    return count

def nextMove(a, x, y):

    min_deg_idx = -1 
    min_deg = (n + 1)
    c = 0
    nx = 0
    ny = 0
    
    for i in range(8):
        nx = x + move_x[i]
        ny = y + move_y[i]
        if(isempty(a,nx,ny)):
            c = getDegree(a,nx,ny)
            if(c < min_deg):
                min_deg = c
                min_deg_idx = i
    
    if(min_deg_idx == -1):
        return False
    
    nx = x + move_x[min_deg_idx]
    ny = y + move_y[min_deg_idx] 
 
    a[ny*n+nx] = a[y*n+x] + 1
 
    global init_x
    global init_y
    init_x = nx
    init_y = ny

    global step
    step = step + 1
    return True

def printHeuristic(a,runningTime):

    with open("20127169_heuristic.txt", "w") as f:
        f.write(str(start_y + 1) + " " + str(start_x + 1) + " " + str(n) + "\n")
        f.write(str(step) + "\n")
        f.write(str(runningTime * 1000) + "\n")
        for i in range(n):
            for j in range(n):
                f.write(str(a[i*n+j]))
                if (j != n - 1):
                    f.write(" ")
            if(i != n-1):
                f.write("\n")
 
def findTour():
  
    a = [-1 for i in range(n*n)]

    global init_x
    global init_y
    global EndTime
    tmp = init_x
    init_x = init_y
    init_y = tmp

    a[init_y*n+init_x] = 1 # Mark first move.
    
    for i in range(n*n-1):
        if(nextMove(a, init_x, init_y) == False):
            EndTime = time.perf_counter()
            printHeuristic(a,EndTime - InitTime)
            return False

  
    EndTime = time.perf_counter()
    printHeuristic(a,EndTime - InitTime)
    return True


'''
    Main
'''

if (len(sys.argv) == 7):
    
    init_x = int(sys.argv[4]) - 1
    init_y = int(sys.argv[2]) - 1
    n = int(sys.argv[6])
    start_x = init_x
    start_y = init_y

    #Call Heuristic
    findTour()

    step = 1
    init_x = start_x
    init_y = start_y

    InitTime = time.perf_counter()
    EndTime = 0
    #Call Backtracking
    solveKT(n,init_x,init_y)
