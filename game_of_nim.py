import random
from operator import length_hint



no_of_piles = random.randint(2,5) # genrate random number of piles from 2 to 5
no_of_stones_list = [] # this list store all the number of stones per pile


def set_board(): # adding stones in list
    for pile in range(no_of_piles):
        no_of_stones_list.append(random.randint(1,8))
    if(sum(no_of_stones_list) < 2*len(no_of_stones_list)+1 ): # check 2N+1 requirement
        no_of_stones_list.clear()
    while(sum(no_of_stones_list) < 2*len(no_of_stones_list)+1): # call set board untill it no of stones is greater than 2n+1
        set_board()
set_board()
  
print("length of list is number of pile")
print(no_of_stones_list)
print("the number itself is the the number of stones")


def int_input(text): # this is to get valid integer data from the user
    while True:
        try:
            number = int(input(text))
            break
        except:
            print('Please enter a number')
            continue
    return number

# this function makes sure that the move user wants to make is possible
# for example we want dont want user to take 5 stone when there are only 2 available

def validate_move(pile, stones):
    if(pile > no_of_piles):
        print("Invalid pile input: Not enough piles")
        return False
    if(pile<= 0):
        print("Invalid pile input: Negative or zero piles not possible")
        return False
    if(no_of_stones_list[pile-1] < stones):
        print("Invalids stone input: Not enough stones")
        return False
    if(stones < 0):
        print("Invalid stones input : Negative stones not possible")
        return False
    if(stones == 0):
        print("Invalid stone input : cannot have 0 as stone input")
        return False
    return True

# getting user input for as which pile and how many stones to remove
def get_user_move():
    return int_input("enter pile number "), int_input("enter stones ")

# changing the data in the list containg stone data, after validating it
def make_move(pile, stones):
    if(validate_move(pile, stones) == True):
        no_of_stones_list[pile-1] = no_of_stones_list[pile-1] - stones
        print(stones," removed from pile number ", pile)
    else:
        print("Need to enter move again")
        pile, stones = get_user_move()
        make_move(pile,stones)
        
# this function is used to calculate all the possible move according to data in the list of stone
# every combination of [pile number , from 1 to maximum number of stones in the pile] is valid discarding piles with 0 stones 
def calculate_possible_moves():
    possible_moves = []
    for i in range(no_of_piles): # iterate over every pile
        for j in range(no_of_stones_list[i]):  # iterating over every stone
            possible_moves.append([i+1,j+1])
    return possible_moves


# this function makes a move by calculating which move leads to nim-sum of zero if possible
def nim_sum_way():
    possible_moves = calculate_possible_moves()           # calculating possible moves
    #uncomment to print all possible moves
    #print(possible_moves)
    def convert_to_bin(list):                             # converting into binary
        return ['{0:04b}'.format(i) for i in list]
    stones_list_bin = convert_to_bin(no_of_stones_list)   # stone_list_bin stores the pile and stone data in binary
    
    def calculate_nim_sum(bin_list):                      # function to calculate nim-sum
        nim_sum = []
        for i in range(4):
            temp = 0
            for j in bin_list:
                temp += int(j[i])
            if temp%2 == 0:
                nim_sum.append(0)
            else:
                nim_sum.append(1)
        return nim_sum
    nim_sum = calculate_nim_sum(stones_list_bin)         # nim-sum of current position
    temp_stones_list = no_of_stones_list.copy()          # copy of no_of_stones_list for calculations
    
    if(nim_sum == [0,0,0,0]):                                    # if numsum is already 0, computer makes a random move
        print("Nim-sum is zero. Computer makes a random move")
        pc_make_move()
        return 
    
    for move in possible_moves:                                 # for every move in list of possible move check                                  
        temp_stones_list[move[0]-1] -= move[1]                  # make that move in temprary list
        temp_stones_list_bin = convert_to_bin(temp_stones_list) 
        temp_nim_sum = calculate_nim_sum(temp_stones_list_bin)
        
        #Uncomment next line to print data of steps
        print("Move ",move," Temp-List ",temp_stones_list ," Nim-sum ", temp_nim_sum)
        
        
        if(sum(temp_nim_sum)==0):                                # check if the nim-sum becomes zero
            print("Computer makes following move")
            make_move(move[0],move[1])                           # if yes than make that move
            
            return
        else:
            temp_stones_list = no_of_stones_list.copy()          #else reset the temp list
    
    
    
def pc_make_move(): # whenever this function is called, it results in computer making a random move
    possible_moves = calculate_possible_moves()
    list_len = length_hint(possible_moves)
    move = possible_moves[random.randint(0,list_len-1)]
    print("Computer makes following move")
    make_move(move[0],move[1])
    

def check_game_over():                  #checks if the list of stone data is empty(has no stones left)
    if (sum(no_of_stones_list) == 0):
        return True
    else: 
        return False

def ask_game_type():                                            # asks for uses to enter option for which game to play
    print("Welcome to game of nim, How would you like to play")
    print("1. You vs computer, you move first")
    print("2. You vs computer, computer move first")
    print("3. Computer vs Computer")
    print("4. Testing case, play against random moves")
    number = 0
    while(number>4 or number<1):
        number = int_input("Enter number 1 to 4: ")
    return number
    
def user_vs_computer():                                       # user vs computer, user makes first move
    while(True):
        print()
        print()
        pile , stone = get_user_move()
        make_move(int(pile), int(stone))
        print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for computer to make, you win")
            return
        nim_sum_way()
        #print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for you to make, computer win")
            return    
def computer_vs_user():                                       # computer vs user, computer makes first move
    while(True):
        print()
        print()
        nim_sum_way()
        #print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for you to make, computer win")
            return
        pile , stone = get_user_move()
        make_move(int(pile), int(stone))
        #print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for computer to make, you win")
            return
        
def computer_vs_computer():                                   #computer plays against computer
    while(True):
        print()
        print()
        print("First player move")
        nim_sum_way()

        print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for you to make, player 1 win")
            return
        
        print("Second player move")
        nim_sum_way()
        print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for you to make, player 2 win")
            return
        
def user_vs_random():                                           #user plays against computet which makes random moves
    while(True):
        print()
        print()
        pile , stone = get_user_move()
        make_move(int(pile), int(stone))
        #print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for computer to make, you win")
            return
        pc_make_move()
        #print(no_of_stones_list)
        if(check_game_over() == True):
            print("no move left for you to make, computer win")
            return
        
        
# main function it calls the game function according to the users choice   
def main():                                         
    game_type = ask_game_type()
    print(no_of_stones_list)
    if(game_type ==1):       
        user_vs_computer()
    if(game_type == 2):
        computer_vs_user()
    if(game_type == 3):
        computer_vs_computer()
    if(game_type == 4):
        user_vs_random()
        
main()
