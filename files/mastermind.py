##################################################################################
#### This plays the game mastermind ###########################################



import random
import os 
import copy





# CONSTANTS
NCodes=4






#Initialize game.  Just run once
def init_game(choice):
  
    global COLORS
    
    if (choice=='1'):
        
        print " GOOD : You chose letters.  To make a guess just type 4 letters drawn from abcdefg"
        print "    For example:  ddeg"
        # This is just a global list of available colors to choose from
        
        COLORS=['a','b','c','d','e','f','g']
    else:
        print " Most Excellent : You chose numbers.  To make a guess just type 4 letters drawn from 1234567"
        print "    For example  3243"
        COLORS=['1','2','3','4','5','6','7']

    #The answer code.  Preset it with "blanks".
    global key_code
    key_code=['','','','']
    
    #The guess code.  Preset it with "blanks"
    global guess_code
    guess_code=['','','','']



    #Python library structure (key=individual code, value=number of times key appears)
    global key_count
    global guess_count
    key_count={}
    guess_count={}
    for i in COLORS:
        key_count[i]=0
        guess_count[i]=0
  

    # History - save what the user guesses.  It is in count guess correct correct-placement
    global  history 
    history = []
    
    #GLOBAL FLAGS
    global f_CHEAT  #show the correct key 
    global f_TRACE  #trace for debug 
    
    f_CHEAT=False #SHOW the key 
    f_TRACE=False #TRACE the Program
  
  
#Make the answer  
def make_key_code():

    global COLORS
    
    # This contains the answer
    for i in range(NCodes):
        key_code[i]=random.choice(COLORS)

    #Zero out the tally of the answers
    for i in COLORS:
        key_count[i]=0
        
    #Tally the characters and sorts them in a dictionary
    for i in range(len(key_code)):
        key_count[key_code[i]]+=1
 
  

# This function checks how many colors are correct and how many are in the correct n_place
# It returns two values.  How many are in place correct, how many are out of place correct.

def check_answer():
    n_correct=0
    n_place=0
  
    #Zero out the guess tally
    for i in COLORS:
        guess_count[i]=0

    #Tally the characters and sorts them in a dictionary
    for i in range(len(guess_code)):
        guess_count[guess_code[i]]+=1

    if (f_TRACE):
        print
        print "[DEBUG-TRACE] : check_answer()"
        print key_count
        print guess_count
        print
        
        
        
    #Find out how many are correct
    for i in COLORS:
        n_correct+=min (guess_count[i],key_count[i] )
       
    # Find out how many are correctly placed    
    n_place=0
    #Fuond out how many are correctly placed
    for i in range(len(key_code)):
        if (key_code[i]==guess_code[i]):
            n_place+=1
    
    # return number of correct and number correctly placed in a tuple
    return (n_correct,n_place)
  
  

# List the history   
def do_list():

    print ("counter\tcode\tcorrect\t in position")
    for i in range(len(history)):
        (lc, lcode, lcorrect, lpos)=history[i]
        print (str(lc) +"\t"+ str(lcode) +"\t"+ str(lcorrect) +"\t"+ str(lpos) )
      


    
    
    

##########################################################################################
##########################################################################################
# MAIN ROUTINE
# TO Play, type mmind()
#########################################################################################

def mmind():
    
    
    print " Would you like to play with letters :abcdefg"
    print "                          or numbers :1234567"
    print "    Letters: press 1"
    print "    Numbers: press any other key"

    pick=raw_input("    Press 1 for letters")  
    
    init_game( pick )
    make_key_code()



    global f_CHEAT
    global f_TRACE
    
    f_play=True
    f_valid_input=False


    
    counter=0
    
    # The player is playing the game 
    while f_play:
        
        
        
        # Wait for the player to press a key.  Assume it is not valid at first
        f_valid_input=False
        
            
        while (f_valid_input==False):	
           # print("\n" * 5)


            print 
            print 
            print
            print "###########################################################################"
            print "PLAYING"
            print
            


            print "MENU"
            
            
            if (f_CHEAT):
                print ("[CHEAT] KEY=: "+str(key_code))
                
            print "[c]heat - show the correct key"
            print '[t]race - follow the code (DEBUG)'
            print "[l]ist your guesses so far"
            print ("Just type in "+str(len(key_code))+" from "+str(COLORS))
            
            
            #Let's get an input  
            input=raw_input("Type : ")
            
            
            # Now validate the input and decode command
            if (len(input)==1): # We typed in a single key
            
                if (input=='c'):  # Player wants to cheat and see the answer 
                    f_valid_input=True
                    f_CHEAT=True
                    
                elif (input=='t'):# Player  wants to follow the progressionn of the code 
                    f_valid_input=True
                    if (f_TRACE):
                        f_TRACE=False 
                    else:
                        f_TRACE=True
                        
                elif (input=='l'):  # Player wants to see all the guesses so far 
                    f_valid_input=True
                    do_list()
                    
                else:               # That's it.  The player pressed an invalid key 
                    f_valid_input=False 
                    
            elif (len(input)==len(key_code)): # Player pressed a 4 digit key 



                # Make sure the sequence is from a valid sequence 
                f_valid_input=True
                for i in range(len(input)):
                    if (input[i] in COLORS):
                        guess_code[i]=input[i]
                    else:
                        f_valid_input=False
                        
                # All good.  Now Calculate        
                if (f_valid_input==True):

                     # Check with the key (answer) to calculate number correct 
                    (n_correct,n_inplace)=check_answer()
                    
                    
                    # This is here to count the history.  
                    counter+=1   # Number of attempts
                    
                    # Save it to history.  We use the input because it is easier to read.  Also
                    # we need to do a deep copy of the guesses or it will just copy a pointer and counter
                    # the stored values keep changing.
                    
                    tmp_code=copy.deepcopy(input)  
                    history.append((counter,tmp_code, n_correct, n_inplace) )
        
                    # Tell the user what his/her guesses were
                    print ("Number of correct colors:"+str(n_correct))
                    print ("Number of correct colors in correct place:"+str(n_inplace))
                    
                    
                    # Victory condition
                    if (n_inplace==len(key_code)):
                        f_play=False
                        print
                        print 
                        print
                        print "*********"
                        print "You win!"
                        do_list()
            
        
            if f_valid_input == False:
                print "I don't understand that command"
                


  


  

  