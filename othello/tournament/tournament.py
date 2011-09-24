import sys
import os
import time

sys.path.append('/u/epnichol/b351/othello/src/')

import driver

def run(white_engine_file_num):

    #for p in sys.path: print p

    # Load the list of the programs to play as white in this run.
    path = '/u/epnichol/b351/othello/src/driver/'
    log_file = path + "tournament.log." + str(white_engine_file_num)

    file = open(path + 'white_engines_' + str(white_engine_file_num) + '.txt', 'r')
    white_engines=[]
    for engine in file.readlines():
        white_engines.append(engine.rstrip())

    file.close()
    print white_engines

    # Load the list of all programs.
    file = open(path + 'engines.txt', 'r')

    engines=[]
    for engine in file.readlines():
        engines.append(engine.rstrip())
    file.close()

    print engines

    # Iterate over all possible games. Check the log: if this game was already played, skip it.
    # If the game was not played, play it!

    for white_engine in white_engines:
        for black_engine in engines:
            # skip self-games
            if white_engine == black_engine:
                continue

            # check the log; was this game recorded yet?
            # Make sure the log exists.
            try:
                log = open(log_file, 'r')
            except IOError:
                pass
            else:
                target_str = 'white=' + white_engine + ',black=' + black_engine
                found = False
                for line in log.readlines():
                    if line.startswith(target_str):
                        found = True
                        break
                log.close()
                if found:
                    continue


            # run a game and log the results.
            driver.run(white_engine, black_engine, log_file, False)


    print "\nDONE!!!!!!!\n"



if __name__ == '__main__':
    print "---------------------"
    print "\nOthello Tournament!\n-------------------"
    print time.strftime("%a, %d %b %Y %H:%M:%S")
    print "---------------------"
    # check syntax of command line
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " white_engine_file_number"
        print "\tex: " + sys.argv[0] + " 2"
        sys.exit()

    run(sys.argv[1])

