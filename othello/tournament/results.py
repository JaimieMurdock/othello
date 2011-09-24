import sys
import os
import time

#sys.path.append('/u/epnichol/b351/othello/src/')
path = '/Users/eric/workspace/othello/src/driver/results/'
sys.path.append(path)


# Load the list of all programs.
file = open(path + 'engines.txt', 'r')

engines=[]
for engine in file.readlines():
    engines.append(engine.rstrip())
file.close()

#print engines

# Iterate over all engines and count up wins/draws.
print "Engine\t\t\tSCORE\tWinWhite\tWinBlack\tDrawWhite\tDrawBlack\tLossWhite\tLossBlack"
print "--------------------------------------------------------"
for engine in engines:
    wins_white = 0
    wins_black = 0
    draws_white = 0
    draws_black = 0
    loss_white = 0
    loss_black = 0

    # Try all logs.
    for i in range(1,5):
        log_file = path + "tournament.log." + str(i)
        log = open(log_file)
        for line in log.readlines():
            if line.find('white=' + engine + ',') != -1:
                if line.find('winner=' + engine + ',') != -1:
                    wins_white += 1
                elif line.find('draw') != -1:
                    draws_white += 1
                else:
                    loss_white +=1
            elif line.find('black=' + engine + ',') != -1:
                if line.find('winner=' + engine + ',') != -1:
                    wins_black += 1
                elif line.find('draw') != -1:
                    draws_black += 1
                else:
                    loss_black += 1
        log.close()

    score = wins_white + wins_black + (draws_white+draws_black)/2
    print (engine + '\t\t\t' + str(score) + '\t' + str(wins_white) + '\t' + str(wins_black) + '\t' + str(draws_white) + '\t' + str(draws_black) + \
            '\t' + str(loss_white) + '\t' + str(loss_black))
