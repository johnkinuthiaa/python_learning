# a while loop performs a condition multiple times provided a condition is true
# i =0
# j=10
# while i<10:
#     print("*"*i)
#     i +=1
# Guessing game

secret_number =8
answer_found =False
tries =3
while answer_found==False and tries >0:
    my_answer =int(input("Enter your guess: "))
    if my_answer ==secret_number:
        answer_found=True
        print(f"You found the answer")
    else:
        tries -=1
        print(f"you are wrong!! you have {tries} remaining ")
if tries ==0 and answer_found==False:
    print("Game over!!You lose")


