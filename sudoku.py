#            Ali Meddeb  -  medde001@umn.edu - Exam1: Sudoku Puzzle - CSCI1133




#---------------------------------------------------------------------------
#---------------------- Importing Modules

import turtle as t
from random import *

#configuring turtle
t.tracer()
t.title('SUDOKU')
t.speed(0)
t.hideturtle()
t.showturtle()

#---------------------------------------------------------------------------
#---------------------- Initialising the Grid

def Draw_grid(): #This function will draw the empty 8x8 grid at the start
    t.width(2) # this part draws the outer thick lines
    t.speed(0)
    t.goto(0, 200)
    t.goto(-200, 200)
    t.goto(-200, -200)
    t.goto(200, -200)
    t.goto(200, 200)
    t.goto(0, 200)
    t.goto(0, -200)
    t.up()
    t.goto(-200, 0)
    t.down()
    t.goto(200, 0)
    t.width(1) # reducing width for thin lines
    for i in range(3): # this For loop draws the 2 thin vertical inner lines
        t.up()
        t.goto(-100+i*100,200)
        t.down()
        t.goto(-100+i*100,-200)
    for i in range(3): # this For loop draws the 2 thin horizontal inner lines
        t.up()
        t.goto(-200,100-i*100)
        t.down()
        t.goto(200,100-i*100)


def label(): #this function will label the grid from A to C and 0 to 3
    t.up()
    t.speed(0)
    for i in range(4): # repeating 4 times because 4 letters
        t.goto(-163+i*100,200) # write on top of the box
        t.write(str(i), font=("Arial", 30, "normal"))#writing the letter in function of its ASCII value
    for i in range(4):
        t.goto(-240,130-i*100) # write on top of the box
        t.write(chr(65+i), font=("Arial", 30, "normal"))

def grid_preset():
    grid_type=randint(1,5) #choosing randomly between 4 preset grids
    if grid_type==1:
        grid_content=[1,0,4,0,0,0,0,3,2,0,0,0,0,1,0,4]#the list is filled with numbers from right to left, top to bottom A0-A1...-D3
    if grid_type==2:
        grid_content=[0,3,1,0,4,0,0,0,0,0,0,1,0,4,2,0]
    if grid_type==3:
        grid_content=[0,0,4,0,4,0,0,1,3,0,0,2,0,2,0,0]
    if grid_type==4:
        grid_content=[2,0,3,0,0,0,0,1,4,0,0,0,0,2,0,3]
    if grid_type==5:
        grid_content=[0,4,1,0,1,0,0,0,0,0,0,2,0,2,3,0]
    return(grid_content)



def draw_number(List,element): #this function draws the initial numbers inside the grid from the grid_preset function
    i=0
    for element in List:
            if element!=0: #0 means empty space
                x=-150+100*(i%4) #choosing column number 
                y=125-100*(i//4) #choosing row number
                t.up()
                t.goto(x,y)
                t.down()
                t.write(element, font=("Arial" , 30, "normal"),align="center")
            i=i+1 #Going to the next element

        

#---------------------------------------------------------------------------
#---------------------- case selection and number insertion / deletion


def input_name(): #Player name input 
    while True:
        name=t.textinput('Name', 'Welcome to sudoku, please input your name (Min 3 chars, Max 10 chars) :')
        if len(name)in range(3,11): #name has more than 3 char and less than 10
            t.textinput('Rules', 'Fill in the grid so that every row, every column'\
                        ' and every 2x2 box contains the digits 1 through 4.'\
                        ' !Attention! There is only 1 solution for each puzzle.')
            return(name)
        
    

def case_selection(L,name): #user selects the case they want to edit
    while True:
        current_case_index=0
        current_case=t.textinput('Select a case', 'choose a case by typing the capital letter followed by the number. Ex: C3. or type "check" ')
        if len(current_case)==2 and current_case[0] in 'ABCD' and current_case[1] in '0123': # restrictng input to A-D followed by 0-3
            for i in range(65,69): #65-69 are ASCII for A-D (for the rows)
                for j in range(4): #going through the 4 columns
                    if  current_case== chr(i)+str(j):
                        return(current_case_index)
                    current_case_index=current_case_index+1

        if current_case.upper()=='CHECK': #user chooses to check the answer for the full grid:
            check_full_grid(L,name)




def input_answer(current_case_index,option,correction_type,List):
    while True:
        if option=='I':
            number_input=int((t.numinput('Number input','input a number between 1 and 4',minval=0, maxval=4))) #number input in 0-4 range
            if number_input in range(5): #checking that the input number is 0-4:
                t.up()
                t.goto(-150+(current_case_index%4)*100,125-(current_case_index//4)*100)#pointer goes to the specified case
                t.down()
                t.color('white')
                t.write('█',font=("Arial", 30, "normal"),align="center") #delete the previously drawn number
                t.color('grey')
                if correction_type:
                    if not(instant_correction(number_input,current_case_index,List)):
                        t.textinput('Error', 'Wrong answer, try again :')
                        return
                    else:
                        t.color('green')#red color means wrong
                        List[current_case_index]=number_input #changing the value in the list
                        t.write(str(number_input),font=("Arial", 30, "normal"),align="center") #drawing the new number
                        return
        if option=='D':
            t.up()
            t.goto(-150+(current_case_index%4)*100,125-(current_case_index//4)*100) #pointer goes to the specified case
            t.down()
            t.color('white')
            List[current_case_index]=0 #emptying the value from the list
            t.write('█',font=("Arial", 30, "normal"),align="center") #delete the previously drawn number
            break


        
#---------------------------------------------------------------------------
#----------------------       Checking solutions


def instant_correction(current_value,current_case_index,List):
    current_row=current_case_index//4
    current_column=current_case_index%4
    #Row verification
    for i in range(4):
        if current_value==List[i+4*current_row]:
            return(False)#value is refused because it already exists in the row
    #Column verification
    for i in range(4):
        if current_value==List[current_column+4*i]:
            return(False)#value is refused because it already exists in the column
    #Box Verification
    if current_case_index in [0,1,4,5]: #checking if value is in the 1st box
        if current_value in [List[0],List[1],List[4],List[5]]:
            return(False)#value is refused because it already exists in the box
    if current_case_index in [2,3,6,7]: #checking if value is in the 2nd box
        if current_value in [List[2],List[3],List[6],List[7]]:
            return(False)
    if current_case_index in [8,9,12,13]: #checking if value is in the 3rd box
        if current_value in [List[8],List[9],List[12],List[13]]:
            return(False)
    if current_case_index in [10,11,14,15]: #checking if value is in the 4th box
        if current_value in [List[10],List[11],List[14],List[15]]:
            return(False)
    return(True) #the value checks all conditions and is accepted



    
def check_full_grid(List,name): #This functions checks if the grid is fully complete and correct
    for el in List:
        if el==0 : #checking if any of the cases are empty
            t.textinput('Error', "It looks like the puzzle isn't fully completed")
            return
    index=0 #initializing index to start from 0
    correct_number =0
    backup_list=List.copy()#creates a copy of the list to iterate over
    for el in backup_list: 
        backup_list[index]=0#extracts the number (it's in the 'el' variable now) leaving 0 instead
        if instant_correction(el,index,backup_list)==True: #checking if 'el' breaks any of the rules
            correct_number +=1 #if 'el' is valid we increment
        index =index+1
    if correct_number == 16: #if all 'el' are valid, the sum (correct number) is equal to 16, thus the sudoku is correct.
        t.color('green')
        t.up()
        t.goto(-160,250)
        Congratulation_message="Congratulations " + name +"!" #Writing congratulations message
        t.write(Congratulation_message, font=("Arial", 30, "normal"))
        t.up()
        t.goto(-100,-250)
        t.write('You Win!', font=("Arial", 30, "normal"))
        t.textinput('Congratulations', "Thank you for playing the game. Restart the program if you want to play again.")
        t.bye() #game ends.
    else:
        t.textinput('Error', "It looks like your answer was incorrect. Try again")#error: answer incorrect
    

#---------------------------------------------------------------------------
#-----------------------      Game Options


def choose_option(name): #user selects input mode or delete mode
    while True:
        option=t.textinput('Mode',"Type: 'i' for input    'd' for deletion (i/d) ") 
        if option.upper()=='I': #user chooses to input a number in the selected case:
            option=option.upper()
            return(option)
            break

        if option.upper()=='D': #user chooses to delete number in the selected case:
            option=option.upper()
            return(option)
            break
  



def choose_correction(): #user selects whether to activate real time correction or not.
    while True:
        correction_type=t.textinput('Verification','Do you want to activate real time correction? Red = Wrong  Green = Correct (y/n): ')
        if correction_type=='y':
            return(True)
            break
        if correction_type=='n':
            return(False)
            break

    

#---------------------------------------------------------------------------
#-----------------------        Execution of the program  


def main(): #body of the program
        #getting the grid set up
        t.speed(0)
        t.ht()
        grid_content=[]
        Draw_grid()
        label()
        L=grid_preset()
        draw_number(L,1)
        #setup fnished
        player_name=input_name()
        correction_type=choose_correction()
        #Game starts:
        while True: #loop finishes when the user correctly finished the sudoku.
            current_case_index=case_selection(L,player_name)
            option=input_option=choose_option(player_name)
            input_answer(current_case_index,option,correction_type,L)
        
main() #executing the man program
