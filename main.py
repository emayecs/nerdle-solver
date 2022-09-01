from random import randint
import time, pprint, json, argparse, sys

EQUATIONS = [] 
SYMBOLS = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def is_operation(c):
    operations = ['+','-','*','/','=']
    return c in operations

'''
determines if the equation has any errors (may or may not compute)
'''
def valid_equation(eq):
    if (is_operation(eq[0]) or is_operation(eq[-1])):
        return False
    if (eq.count('=')!=1):
        return False
    for i in range(0,len(eq)):
        # if an operation is next to another operation
        if (not is_operation(eq[i])):
            continue
        if (i+1<len(eq) and is_operation(eq[i+1])):
            return False
    if '/' in eq:
        # divide by 0
        for i in range(0, len(eq)-1):
            if eq[i]=='/' and eq[i+1]=='0':
                return False
    return True

def evaluate_expression(ex):
    ex_split = []
    number = ""
    for i in range(0, len(ex)):
        if is_operation(ex[i]):
            ex_split.append(int(number))
            ex_split.append(ex[i])
            number = ""
        else:
            number+=ex[i]
            if (i==len(ex)-1):
                ex_split.append(int(number))
    while (len(ex_split)>1):
        i = 0
        while '*' in ex_split or '/' in ex_split:
            if (ex_split[i]=='*'):
                ex_split[i-1]=ex_split[i-1]*ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i-=1
            elif ex_split[i]=='/':
                ex_split[i-1]=ex_split[i-1]/ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i-=1
            i+=1
        if (len(ex_split)==1):
            break
        i = 0
        while '+' in ex_split or '-' in ex_split:
            if (ex_split[i]=='+'):
                ex_split[i-1]=ex_split[i-1]+ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i-=1
            elif ex_split[i]=='-':
                ex_split[i-1]=ex_split[i-1]-ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i-=1
            i+=1
    return ex_split[0]

'''
determines if both sides of an equation equals each other
returns value if it computes and >=0, otherwise false
'''
def equation_computes(eq):
    if (not valid_equation(eq)):
        return False
    equals_index = eq.index('=')
    left = evaluate_expression(eq[:equals_index])
    right = evaluate_expression(eq[equals_index+1:])
    if left==right:
        return left
    return False

'''
determines if leading zeros are in equation
'''
def leading_zeroes(ex):
    for i in range(0,len(ex)-1):
        if (ex[i]=='0' and not is_operation(ex[i+1])):
            if i==0 or is_operation(ex[i-1]):
                return True
    return False

'''
randomly generate x equations (may/may not evaluate)
'''
def generate_equations(x): 
    operations = ['+','-','*','/']
    digits = []
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations
    counter = 0
    equations = []
    while (counter<x):
        eq = ""
        after_zero = False
        contains_symbol = False
        for i in range(0,7):
            if (after_zero): #prevents leading zeroes
                r = randint(10,12)
            else:
                r = randint(0,len(symbols)-1)
            if (r>9 and r<14):
                contains_symbol = True
            if (r==0 and (i==0 or is_operation(eq[-1]))):
                after_zero = True
            else:
                after_zero = False
            eq+=symbols[r]
        eq_pos = randint(1,6)
        eq = eq[:eq_pos]+'='+eq[eq_pos:]
        
        if (valid_equation(eq) and contains_symbol):
            counter+=1
            equations.append(eq)
    return equations

'''
generates all possible equations that compute
additional restraints:
- no leading zeroes
- equation != 0
- consequently, must have >=1 operation
'''
def bf_equations(conditions, equals_conditions): 
    global EQUATIONS
    
    operations = ['+','-','*','/']
    digits = []
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations
    
    length = 8
    indices = [0] * length

    eq_count = 0
    equations = EQUATIONS

    try:
        with open('valid_equations.json','r') as f:
            data = json.load(f)
            EQUATIONS = data["equations"]
            equations = EQUATIONS
            indices = data["indices"]
    except:
        pass

    t0 = time.perf_counter()
    while (indices[length-1]<len(conditions[length-1])):
        eq = ""
        for i in range(0,len(indices)):
            eq+=conditions[i][indices[i]]
        indices[0]+=1

        for i in range(0,length-1):
            if (indices[i]==len(conditions[i])):
                indices[i]=0
                indices[i+1]+=1
            if (indices[i]>9 and indices[i+1]>9):
                #skips index if index next to it is an operation
                indices[i]=0
                indices[i+1]+=1

        for i in range(0,len(equals_conditions)):
            if (not equals_conditions[i]):
                continue
            temp_eq = eq[:i+1]+'='+eq[i+2:]
            if (equation_computes(temp_eq) and not leading_zeroes(temp_eq) and eq[i+1]=='0'): 
                # last condition prevents repeated equations
                eq_count+=1
                equations.append(temp_eq) 
            if time.perf_counter()-t0>60:
                with open('valid_equations.json','w') as f:
                        json.dump({"indices":indices,"equations":equations}, f ,indent = 2)
                t0 = time.perf_counter()
    
    print(eq_count) 
    return equations

'''
Asks the user for their initial guess and result, and from there, provides guesses to solve the nerdle
'''
def ask(guess, result):
    global EQUATIONS
    reset_valid_equations()
    pp = pprint.PrettyPrinter()
    #assumes length of 8
    operations = ['+','-','*','/']
    digits = []
    
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations

    #conditions start with allowing all symbols in all places
    length = 8
    conditions=[]
    for i in range(0,length):
        if i==0 or i==length-1:
            conditions.append(digits.copy())
        else:
            conditions.append(symbols.copy())
    equals_conditions = [True]*(length-2)

    while (result!="exit"):
        frequency = [0]*len(symbols)
        for i in range(0, len(result)):                
            if result[i].upper()=='B':
                if guess.index(guess[i])==i:
                    #if the guess x is the first x in the guess, then no x's are in the equation
                    for j in range(0, len(conditions)):
                        if guess[i] in conditions[j]:
                            conditions[j].remove(guess[i])
                else:
                    if (frequency[symbols.index(guess[i])]>=1):
                        #the guess is in the equation, but not here
                        conditions[i].remove(guess[i])
                    else:
                        #there are no more guesses in the equation
                        for j in range(0, len(conditions)):
                            #x is green here
                            if len(conditions[j])==1 and conditions[j][0]==guess[i]:
                                continue
                            if guess[i] in conditions[j]:
                                conditions[j].remove(guess[i])
            elif result[i].upper()=='P':
                if guess[i]=='=':
                    equals_conditions[i-1]=False
                else:
                    frequency[symbols.index(guess[i])]+=1
                    if guess[i] in conditions[i]:
                        conditions[i].remove(guess[i])
            elif result[i].upper()=='G':
                if guess[i].upper()=='=':
                    for j in range(0, len(equals_conditions)):
                        if (j!=i-1):
                            equals_conditions[j] = False
                else:
                    conditions[i]=[guess[i]]

        guess = filter_equations(conditions, equals_conditions)
        
        print("Best Guess: "+guess)

        probability = 1/len(EQUATIONS)*100
        print("Probability: "+str(probability)+"%")

        if probability==100:
            return

        result = input("Enter the result:\n")
        if (result=="exit"):
            return

'''
run a simulation of solving a nerdle
'''
def simulate(target):
    global EQUATIONS
    guesses = ["35+46=81"]
    pp = pprint.PrettyPrinter()
    #assumes length of 8
    operations = ['+','-','*','/']
    digits = []
    
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations

    guess = "35+46=81"
    result = equation_similarity(target, guess)
    color_guess(result, guess)

    turns = 0

    #conditions start with allowing all symbols in all places
    length = 8
    conditions=[]
    for i in range(0,length):
        if i==0 or i==length-1:
            conditions.append(digits.copy())
        else:
            conditions.append(symbols.copy())
    equals_conditions = [True]*(length-2)

    while (turns<6):
        turns+=1
        frequency = [0]*len(symbols)
        for i in range(0, len(result)):                
            if result[i].upper()=='B':
                if guess.index(guess[i])==i:
                    #if the guess x is the first x in the guess, then no x's are in the equation
                    for j in range(0, len(conditions)):
                        if guess[i] in conditions[j]:
                            conditions[j].remove(guess[i])
                else:
                    if (frequency[symbols.index(guess[i])]>=1):
                        #the guess is in the equation, but not here
                        conditions[i].remove(guess[i])
                    else:
                        #there are no more guesses in the equation
                        for j in range(0, len(conditions)):
                            #x is green here
                            if len(conditions[j])==1 and conditions[j][0]==guess[i]:
                                continue
                            if guess[i] in conditions[j]:
                                conditions[j].remove(guess[i])
            elif result[i].upper()=='P':
                if guess[i]=='=':
                    equals_conditions[i-1]=False
                else:
                    frequency[symbols.index(guess[i])]+=1
                    if guess[i] in conditions[i]:
                        conditions[i].remove(guess[i])
            elif result[i].upper()=='G':
                if guess[i].upper()=='=':
                    for j in range(0, len(equals_conditions)):
                        if (j!=i-1):
                            equals_conditions[j] = False
                else:
                    conditions[i]=[guess[i]]
        #pp.pprint(conditions)
        guess = filter_equations(conditions, equals_conditions)
        guesses.append(guess)
        result = equation_similarity(target, guess)
        color_guess(result, guess)
        if (guess==target):
            break

    if (len(EQUATIONS)!=1 and guess!=target):
        print(f"{bcolors.WARNING}WARNING: failed to solve {target} within 6 turns{bcolors.ENDC}",end="")
    return guesses

'''
Given a target equation, return the result/similarity of the guess in terms of green, purple, and black
'''
def equation_similarity(target, guess):
    similarity = "."*len(guess)
    operations = ['+','-','*','/','=']
    digits = []
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations
    frequency = [0]*len(symbols)
    for i in range(0, len(guess)):
        if guess[i]==target[i]:
            similarity=similarity[:i]+"G"+similarity[i+1:]
        else:
            frequency[symbols.index(target[i])]+=1
    for i in range(0, len(guess)):
        if similarity[i]=="G":
            continue
        index = symbols.index(guess[i])
        if frequency[index]>=1:
            frequency[index]-=1
            similarity=similarity[:i]+"P"+similarity[i+1:]
        else:
            similarity=similarity[:i]+"B"+similarity[i+1:]
    return similarity

'''
filter equations that don't match the current conditions
'''
def filter_equations(conditions, equals_conditions):
    global EQUATIONS
    length = 8
    operations = ['+','-','*','/']
    digits = []
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations

    symbol_count = [0]*len(symbols)
    for c in conditions:
        for s in c:
            symbol_count[symbols.index(s)]+=1

    i=0
    highest_value = 0
    best_equation = ""
    done = False

    while i<len(EQUATIONS):
        
        equation_symbols = []
        value = 0
        equation = EQUATIONS[i]

        equal_index = equation.index('=')
        if (not equals_conditions[equal_index-1]):
            EQUATIONS.pop(i)
            continue

        # checks if each character is allowed at the position
        pop = False
        for j in range(0,length):
            if equation[j]=='=':
                continue
            if not equation[j] in conditions[j]:
                EQUATIONS.pop(i)
                pop = True
                break
            if not equation[j] in equation_symbols:
                equation_symbols.append(equation[j])
                value+=symbol_count[symbols.index(equation[j])]
        if (pop):
            continue

        if value>highest_value or best_equation=='':
            best_equation = equation
            highest_value = value
        i+=1
    return best_equation

'''
simulates solving n nerdles
'''
def run_simulation(n):
    global EQUATIONS
    for i in range(n):
        reset_valid_equations()
        target = EQUATIONS[randint(0,len(EQUATIONS)-1)]
        try:
            print("Equation: "+target)
            simulate(target)
        except Exception as e: 
            print("error with: "+target)
            print(e)
            break
        print()

'''
resets valid_equations to the equations stored in the json file
'''
def reset_valid_equations():
    global EQUATIONS
    try:
        with open('valid_equations.json','r') as f:
            data = json.load(f)
            EQUATIONS = data["equations"]
            indices = data["indices"]
    except:
        pass

'''
starts a nerdle game with a random equation
'''
def play():
    global EQUATIONS
    reset_valid_equations()
    target = EQUATIONS[randint(0,len(EQUATIONS)-1)]
    guesses = 0
    guesses=[]
    results=[]
    while (len(guesses)<6):
        print()
        for i in range(6):
            if i<len(guesses):
                guess = guesses[i]
                result = results[i]
                color_guess(result, guess)
            else:
                print(u"\u2588"*8)
        print()
        guess = input()
        if (guess == 'q'):
            return
        while (len(guess)!=len(target)):
            print("Guess must have a length of "+len(target))
            print()
            guess = input()
        while (not equation_computes(guess)):
            print("Equation does not compute.")
            print()
            guess = input()
        guesses.append(guess)
        result = equation_similarity(target, guess)
        results.append(result)
        if (target==guess):
            return
            
    for i in range(6):
        if i<len(guesses):
            guess = guesses[i]
            result = results[i]
            color_guess(result, guess)
        else:
            print(u"\u2588"*8)

    print('The answer was: '+target)

'''
Given a guess and its result, print the color-coded version
'''
def color_guess(result, guess):
    for j in range(len(guess)):
        if result[j]=="G":
            print(f"{bcolors.OKGREEN}{guess[j]}{bcolors.ENDC}",end="")
        if result[j]=="P":
            print(f"{bcolors.HEADER}{guess[j]}{bcolors.ENDC}",end="")
        if result[j]=="B":
            print(guess[j],end="")
    print()

def main():
    parser = argparse.ArgumentParser(description='Nerdle Solver & Utility')
    
    subparser = parser.add_subparsers(dest='command')
    solve_parser= subparser.add_parser('solve')
    play_parser = subparser.add_parser('play')
    simulate_parser = subparser.add_parser('simulate')
    
    solve_parser.add_argument('guess', type = str, help = "guess for the equation")
    solve_parser.add_argument('result', type = str,  help = "string, each letter denoting the result of the guess")

    simulate_parser.add_argument('iterations', type = int, help = "number of desired simulations")

    args = parser.parse_args()
    

    if args.command == 'solve':
        ask(args.guess, args.result)
    elif args.command == 'play':
        play()
    elif args.command == 'simulate':
        if (args.iterations<=0):
            parser.error('iterations must be >= 1')
        run_simulation(args.iterations)
    

if __name__ == "__main__":
    main()
