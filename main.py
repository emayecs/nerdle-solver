from random import randint
from tkinter import W
from tqdm import tqdm
import json, argparse, pprint, sys

SYMBOLS = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/']
DIGITS = ['0','1','2','3','4','5','6','7','8','9']

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

def is_valid_equation(eq):
    index = eq.index('=')
    ex1 = eq[0:index]
    ex2 = eq[index+1:]
    return is_valid_expression(ex1) and is_valid_expression(ex2)

'''
determines if the expression has any errors
'''
def is_valid_expression(ex):
    # negative numbers are ok
    if (is_operation(ex[0]) and ex[0]!='-' or is_operation(ex[-1])):
        return False
    # if an operation is next to another operation
    for i in range(len(ex)-1):
        if (is_operation(ex[i]) and is_operation(ex[i+1])):
            #allows operation before '-'
            if i==0 or ex[i+1]!='-':
                return False

    #prevent more than 3 operations from being in a row
    for i in range(len(ex)-2):
        if is_operation(ex[i]) and is_operation(ex[i+1]) and is_operation(ex[i+2]):
            return False

    '''
    #prevent negative 0's
    if len(ex)>=2:
        if ex[i]=='-' and ex[i+1]=='0':
            return False
    for i in range(len(ex)-2):
        if is_operation(ex[i]) and ex[i+1]=='-' and ex[i+2]=='0':
            return False
    '''

    #prevent dividing by 0
    ex_copy = ex
    while '/' in ex_copy:
        i = ex_copy.index('/')
        j = i+1
        number = ""
        is_negative = False
        while j<len(ex_copy):
            if is_operation(ex_copy[j]):
                # don't break loop if first char after operation is '-'; negative number
                if not (ex_copy[j]=='-' and j==i+1):
                    break
            number+=ex_copy[j]
            j+=1
        number = int(number)
        if number==0:
            return False
        ex_copy = ex_copy[i+1:]

    return True

'''
evalutes an expression's value
'''
def evaluate_expression(ex):
    if not is_valid_expression(ex):
        raise RuntimeError(f'{ex} is not a valid expression')

    ex_split = []
    number = ""

    #split expression into numbers and operations
    for i in range(len(ex)):
        #check negative numbers
        if ex[i]=='-':
            if i==0:
                number+=ex[i]
                continue
            elif is_operation(ex[i-1]):
                number+=ex[i]
                continue

        if is_operation(ex[i]):
            ex_split.append(int(number))
            ex_split.append(ex[i])
            number = ""
        else:
            number+=ex[i]

            # last element so add to array
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
returns true if it computes, otherwise false
'''
def equation_computes(eq):
    if (not is_valid_equation(eq)):
        return False
    equals_index = eq.index('=')
    left = evaluate_expression(eq[:equals_index])
    right = evaluate_expression(eq[equals_index+1:])
    return (left==right)

'''
determines if leading zeros are in equation/expression
'''
def contains_leading_zeroes(ex):
    for i in range(0,len(ex)-1):
        if (ex[i]=='0' and not is_operation(ex[i+1])):
            if i==0 or is_operation(ex[i-1]):
                return True
    return False

'''
randomly generate x equations (may/may not evaluate)
'''
def generate_random(x): 
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
        
        if (is_valid_equation(eq) and contains_symbol):
            counter+=1
            equations.append(eq)
    return equations

'''
generates a 2-d array of possible values for an expression of a given length
'''
def generate_values(length):
    operations = ['+','-','*','/']
    digits = ['0','1','2','3','4','5','6','7','8','9']
    symbols = digits + operations
    values = []
    for i in range(length):
        if i==length-1:
            values.append(digits)
        elif i==0:
            values.append(digits+['-'])
        else:
            values.append(symbols)
    return values

'''
generates an array of all 0's of a given length
'''
def generate_indices(length):
    indices = []
    for i in range(length):
        indices.append(0)
    return indices

'''
writes all data into json file
'''
def write_data(equations, left_ex_length, right_ex_length, left_ex_indices, right_ex_indices, generated_left_ex):
    with open('equations.json','w') as f:
        json.dump(
            {"equations": equations,
            "lengths":[left_ex_length, right_ex_length],
            "indices":[left_ex_indices, right_ex_indices],
            "generated":generated_left_ex,
            },
        f,indent = 2)

'''
verify all equations compute
'''
def verify_equations():
    print('\nverifying equations...')
    equations = []
    with open('equations.json','r') as f:
        data = json.load(f)
        equations = data["equations"]
    for eq in equations:
        if not is_valid_equation(eq):
            print(f'equation is invalid: {eq}')
            return
        if not equation_computes(eq):
            print(f'equation does not compute: {eq}')
            return
    print('all equations verified \n')

'''
generates possible equations (default length 8), takes ~30 seconds
- fractions not allowed (e.g. 5/4=10/8)
'''
def generate_equations(length=8):
    print("\n generating equations...\n")
    left_ex_length = 1
    right_ex_length = length-left_ex_length-1

    left_ex_values = []
    right_ex_values = []

    left_ex_indices = []
    right_ex_indices = []

    #array of all valid expressions on the LHS that are stored in the index they evaluate to
    generated_left_ex = []

    equations = []

    try:
        with open('equations.json','r') as f:
            data = json.load(f)
            equations = data["equations"]
            left_ex_length = data["lengths"][0]
            right_ex_length = data["lengths"][1]
            left_ex_indices = data["indices"][0]
            right_ex_indices = data["indices"][1]
            generated_left_ex = data["generated"]

        left_ex_values = generate_values(left_ex_length)
        right_ex_values = generate_values(right_ex_length)

    except:
        left_ex_values = generate_values(left_ex_length)
        right_ex_values = generate_values(right_ex_length)

        left_ex_indices = generate_indices(left_ex_length)
        right_ex_indices = generate_indices(right_ex_length)

        for i in range(int(pow(10,left_ex_length))):
            generated_left_ex.append([])
        for i in range(int(pow(10,left_ex_length-1))-1):
            generated_left_ex.append([])
            
        write_data(equations, left_ex_length, right_ex_length, left_ex_indices, right_ex_indices, generated_left_ex)

    while left_ex_length<=right_ex_length:

        left_permutations = 1
        for i in range(left_ex_length):
            left_permutations*=len(left_ex_values[i])
        
        for _ in tqdm(range(left_permutations)):
            if left_ex_indices[-1]>=len(left_ex_values[-1]):
                break
            left_ex = ""

            #generate expression
            for i in range(left_ex_length):
                index = left_ex_indices[i]
                left_ex+=left_ex_values[i][index]
            
            #add expression to array if valid
            if is_valid_expression(left_ex):# and not leading_zeroes(left_ex):
                value = evaluate_expression(left_ex)
                if value==int(value):
                    value = int(value)
                    if value>=0:
                        generated_left_ex[value].append(left_ex)
                    #negative numbers
                    else:
                        generated_left_ex[int(pow(10,left_ex_length))-value-1].append(left_ex)

            #update indices
            left_ex_indices[0]+=1

            for i in range(left_ex_length-1):
                if left_ex_indices[i]==len(left_ex_values[i]):
                    left_ex_indices[i]=0
                    left_ex_indices[i+1]+=1

        right_permutations = 1
        for i in range(right_ex_length):
            right_permutations*=len(right_ex_values[i])
        
        for _ in tqdm(range(right_permutations)):
            if right_ex_indices[-1]>=len(right_ex_values[-1]):
                break

            right_ex = ""

            #generate expression
            for i in range(right_ex_length):
                index = right_ex_indices[i]
                right_ex+=right_ex_values[i][index]
            
            #check if expression is valid
            if is_valid_expression(right_ex):# and not leading_zeroes(right_ex):
                value = evaluate_expression(right_ex)
                #check if value is within bounds of LHS
                if value==int(value) and value<int(pow(10,left_ex_length)) and value>-1*int(pow(10,left_ex_length-1)):
                    value = int(value)
                    #generate equations
                    if value>=0:
                        for exp in generated_left_ex[value]:
                            equations.append(exp+"="+right_ex)
                            equations.append(right_ex+"="+exp)
                    else:
                        for exp in generated_left_ex[int(pow(10,left_ex_length))-value-1]:
                            equations.append(exp+"="+right_ex)
                            equations.append(right_ex+"="+exp)
            
            #update indices
            right_ex_indices[0]+=1

            for i in range(right_ex_length-1):
                if right_ex_indices[i]==len(right_ex_values[i]):
                    right_ex_indices[i]=0
                    right_ex_indices[i+1]+=1

        write_data(equations, left_ex_length, right_ex_length, left_ex_indices, right_ex_indices, generated_left_ex)
        
        #reset variables
        left_ex_length+=1
        right_ex_length-=1

        left_ex_values = generate_values(left_ex_length)
        right_ex_values = generate_values(right_ex_length)

        left_ex_indices = generate_indices(left_ex_length)
        right_ex_indices = generate_indices(right_ex_length)

        generated_left_ex.clear()
        for i in range(int(pow(10,left_ex_length))):
            generated_left_ex.append([])
        for i in range(int(pow(10,left_ex_length-1))-1):
            generated_left_ex.append([])
    
    print("\ncompleted equation generation\n")

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
        
        if (is_valid_equation(eq) and contains_symbol):
            counter+=1
            equations.append(eq)
    return equations

def remove_negatives(equations):
    print("Removing equations with negative numbers...")
    new_equations = equations
    i = 0
    for _ in tqdm(range(len(new_equations))):
        equation = new_equations[i]
        if equation[0]=='-' and not is_operation(equation[1]):
            new_equations.pop(i)
            continue
        should_pop = False
        for j in range(len(equation)-2):
            if is_operation(equation[j]) and equation[j+1]=='-' and not is_operation(equation[j+2]):
                should_pop = True
                break
        if should_pop:
            new_equations.pop(i)
            continue     
        i+=1
    return new_equations

def remove_leading_zeroes(equations):
    print("Removing equations with leading zeros...")
    new_equations = equations
    i = 0
    for _ in tqdm(range(len(new_equations))):
        equation = new_equations[i]
        if contains_leading_zeroes(equation):
            new_equations.pop(i)
            continue
        i+=1
    return new_equations

def remove_equal_zero(equations):
    print("Removing equations that equal 0...")
    new_equations = equations
    i = 0
    for _ in tqdm(range(len(new_equations))):
        equation = new_equations[i]
        ex1 = equation[0:equation.index('=')]
        value = evaluate_expression(ex1)
        if value==0:
            new_equations.pop(i)
            continue
        i+=1
    return new_equations


'''
Given the initial guess and result, provides guesses to solve the nerdle based on each guess's result
'initial_guess': the user's initial guess
'result': the color-coded result of the intial guess
'''
def solve(eq, initial_guess, result):
    equations = eq.copy()

    # initialize conditions:
    # 2-d array of 8 arrays, with the array at the nth index containing all possible characters at the nth index of the equation
    length = 8
    conditions=[]
    for i in range(0,length):
        if i==0:
            conditions.append(DIGITS.copy()+['-'])
        elif i==length-1:
            conditions.append(DIGITS.copy())
        else:
            conditions.append(SYMBOLS.copy())
    
    #a boolean array of length 6; the value at the nth index denotes if it's possible for the equation to have a '=' at the (n+1)th index
    equals_conditions = [True]*(length-2)

    guess = initial_guess

    #modify conditions based on result
    while result!="q":
        frequency = [0]*len(SYMBOLS)
        for i in range(len(result)):
            guessed_char = guess[i] 

            if result[i].upper()=='B':
                #there is a 'guess_char' somewhere => can only eliminate 'guess_char' from this position
                if frequency[SYMBOLS.index(guessed_char)]>=1:
                    if guessed_char in conditions[i]:
                        conditions[i].remove(guessed_char)
                #there are no 'guess_char' in the equation besides the ones that have been already found
                else:
                    for j in range(len(conditions)):
                        #remove 'guess_char' from all conditions unless 'guess_char' is the right value there
                        if result[j].upper()=='G' and guessed_char==guess[j]:
                            continue
                        if guessed_char in conditions[j]:
                            conditions[j].remove(guessed_char)
            
            elif result[i].upper()=='P':
                # '=' in the wrong place
                if guessed_char=='=':
                    equals_conditions[i-1]=False
                else:
                    frequency[SYMBOLS.index(guess[i])]+=1
                    if guessed_char in conditions[i]:
                        conditions[i].remove(guessed_char)
            
            elif result[i].upper()=='G':
                if guessed_char=='=':
                    for j in range(len(equals_conditions)):
                        if j!=i-1:
                            equals_conditions[j] = False
                else:
                    conditions[i]=[guessed_char]

        guess, equations = filter_equations(equations, conditions, equals_conditions, frequency)
        
        print("Best guess: "+guess)

        try:
            if len(equations)==0:
                raise RuntimeError("result is impossible—no equations fit conditions")
            probability = round(1/len(equations)*100,3)
        except RuntimeError as e:
            print(e)
            sys.exit()
        
        print(f"{len(equations)} possible equation(s), {probability}% probability")

        if probability==100:
            return

        result = input("Enter the result:\n")
        if (result=="q"):
            return

'''
run a simulation of solving a nerdle
'''
def simulate(eq, target, first_guess):
    equations = eq.copy()
    guesses = [first_guess]
    pp = pprint.PrettyPrinter()
    #assumes length of 8
    operations = ['+','-','*','/']
    digits = []
    
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations

    guess = guesses[0]
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
        guess, equations = filter_equations(equations, conditions, equals_conditions)
        guesses.append(guess)
        result = equation_similarity(target, guess)
        color_guess(result, guess)
        if (guess==target):
            break

    if (len(equations)!=1 and guess!=target):
        print(f"{bcolors.WARNING}WARNING: failed to solve {target} within 6 turns{bcolors.ENDC}",end="")
    return guesses

'''
Given a target equation, return the result/similarity of the guess in terms of 'G', 'P', or 'B'
'''
def equation_similarity(target, guess):
    similarity = "."*len(guess)
    symbol_frequency = [0]*len(SYMBOLS)

    # check characters that are correct (green)
    for i in range(len(guess)):
        if guess[i]==target[i]:
            similarity=similarity[:i]+"G"+similarity[i+1:]
        else:
            symbol_frequency[SYMBOLS.index(target[i])]+=1
    
    for i in range(len(guess)):
        if similarity[i]=="G":
            continue
        index = SYMBOLS.index(guess[i])
        #purple
        if symbol_frequency[index]>=1:
            symbol_frequency[index]-=1
            similarity=similarity[:i]+"P"+similarity[i+1:]
        #black
        else:
            similarity=similarity[:i]+"B"+similarity[i+1:]
    return similarity

'''
return the best guess and a list of all possible equations given the conditions

'eq': array of all potential equations up to this point
'conditions': a 2-d array of 8 arrays; the array at the nth index contains all possible characters that can be found at the nth index of the equation
'equals_conditions': a boolean array of length 6; the value at the nth index denotes if it's possible for the equation to have a '=' at the (n+1)th index
'symbol_frequency': an frequency array for all symbols in the target. the number at the nth index of 'symbol_frequency' denotes the number of SYMBOLS[n] in the target.
'''
def filter_equations(eq, conditions, equals_conditions, symbol_frequency):
    equations = eq.copy()
    pp = pprint.PrettyPrinter()

    # frequency array of each character in conditions
    symbol_count = [0]*len(SYMBOLS)
    for c in conditions:
        for s in c:
            symbol_count[SYMBOLS.index(s)]+=1

    i=0
    highest_value = 0
    best_equation = ""

    print('Filtering equations...')

    for _ in tqdm(range(len(equations))):
        if i>=len(equations):
            break
    #while i<len(equations):
        checked_characters = []
        value = 0
        equation = equations[i]

        # remove the equation if the equal sign is not in the right place
        equal_index = equation.index('=')
        if not equals_conditions[equal_index-1]:
            equations.pop(i)
            continue

        # checks if each character is allowed at the position
        pop = False
        for j in range(len(equation)):
            char = equation[j]
            
            if char=='=':
                #only need to check if char is occupating a green spot
                if len(conditions[j])==1:
                    pop = True
                    break
                continue
            #check if character is not allowed in its current position
            if not char in conditions[j]:
                pop = True
                break
            
            # add the frequency of the char in conditions to 'value'
            if not char in checked_characters:
                checked_characters.append(char)
                value+=symbol_count[SYMBOLS.index(equation[j])]

        if pop:
            equations.pop(i)
            continue

        #remove equations that do not contain symbols that are purple
        purple_symbols = []
        for j, freq in enumerate(symbol_frequency):
            if freq>=1:
                purple_symbols.append(SYMBOLS[j])

        for symbol in purple_symbols:
            if symbol not in equation:
                pop = True
                break
        
        if pop:
            equations.pop(i)
            continue
        
        if value>highest_value or best_equation=='':
            best_equation = equation
            highest_value = value
        i+=1

    print('Finished filtering equations.')

    return best_equation, equations

'''
simulates solving n nerdles
'''
def run_simulation(equations, n, first_guess):
    print('Beginning simulation...\n')
    for i in range(n):
        target = equations[randint(0,len(equations)-1)]
        try:
            print("Equation: "+target)
            simulate(equations, target, first_guess)
        except Exception as e: 
            print("Error with solving: "+target)
            print(e)
            break
        print()

'''
returns the equations stored in the json file
'''
def read_equations():
    try:
        with open('equations.json','r') as f:
            data = json.load(f)
            equations = data["equations"]
            return equations
    except:
        print('equations could not be read from equations.json')
        sys.exit()


'''
starts a nerdle game with a random equation
'''
def play(eq, chances):
    print('starting game...')
    print('enter q to quit\n')

    # Choose random equation
    equations = eq.copy()
    target = equations[randint(0,len(equations)-1)]
    guesses = 0
    guesses=[]
    results=[]

    while (len(guesses)<chances):
        print()
        #prints the current status of the game
        for i in range(chances):
            if i<len(guesses):
                guess = guesses[i]
                result = results[i]
                color_guess(result, guess)
            else:
                print(u"\u2588"*8)
        print()
        guess = input('Guess:\n')
        #error checking
        if (guess == 'q'):
            return
        while (len(guess)!=len(target)):
            print("Guess must have a length of "+len(target))
            print()
            guess = input('Guess:\n')
        while (not equation_computes(guess)):
            print("Equation does not compute.")
            print()
            guess = input('Guess:\n')
        guesses.append(guess)

        #find similarity to target
        result = equation_similarity(target, guess)
        results.append(result)
        if (target==guess):
            return
    
    #print final status of the game
    for i in range(chances):
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

'''
returns a list of equations given the command line arguments
'''
def filter_initial_equations(include_negatives, include_leading_zeroes, allow_equal_zero):
    equations = read_equations()
    if not (include_negatives and include_leading_zeroes and allow_equal_zero):
        print('Filtering initial equations...')

    if not include_negatives:
        equations = remove_negatives(equations)
    
    if not include_leading_zeroes:
        equations = remove_leading_zeroes(equations)

    if not allow_equal_zero:
        equations = remove_equal_zero(equations)
    
    print('Finished filtering initial equations.')
    return equations

'''
parses the arguments for the play function
'''
def parse_play_args(parser, args):
    if (args.chances<=0):
        parser.error('\'chances\' must be greater than 0')

    equations = filter_initial_equations(args.include_negatives, args.include_leading_zeroes, args.allow_equal_zero)
    play(equations, args.chances)

'''
parses the arguments for the solve function
'''
def parse_solve_args(parser, args):
    if len(args.guess)!=8:
        parser.error('\'guess\' must be an equation of length 8')
    
    equations = filter_initial_equations(args.include_negatives, args.include_leading_zeroes, args.allow_equal_zero)
    solve(equations, args.guess, args.result)

'''
parses the arguments for the simulate function
'''
def parse_simulate_args(parser, args):
    if (args.iterations<=0):
        parser.error('\'iterations\' must be >= 1')
    if len(args.first_guess)!=8:
        parser.error('\'first_guess\' must be an equation of length 8')
    if not is_valid_equation(args.first_guess):
        parser.error('\'first_guess\' must be a valid equation')
    if not equation_computes(args.first_guess):
        parser.error('\'first_guess\' must compute')

    equations = filter_initial_equations(args.include_negatives, args.include_leading_zeroes, args.allow_equal_zero)
    run_simulation(equations, args.iterations, args.first_guess)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Nerdle Solver & Utility')
    
    subparser = parser.add_subparsers(dest='command')

    parser.add_argument('--no_negatives', action='store_const', dest = 'include_negatives', const = False,
     default = True, help = "equations with with negative numbers will not be included (e.g. -4*3=-12")
    parser.add_argument('--no_leading_zeroes', action='store_const', dest = 'include_leading_zeroes', const = False,
     default = True, help = "equations with leading zeroes will not be included (e.g. 004*3=12")
    parser.add_argument('--dne_zero', action='store_const', dest = 'allow_equal_zero', const = False,
     default = True, help = "equations that equal 0 will not be included (e.g. 0*9999=0")

    solve_parser = subparser.add_parser('solve')
    solve_parser.add_argument('guess', type = str, help = "guess for the equation")
    solve_parser.add_argument('result', type = str,  help = "string, each letter denoting the result of the guess")

    play_parser = subparser.add_parser('play')
    play_parser.add_argument('chances', type = int, help = "the number of chances that the user gets to guess the equation")

    simulate_parser = subparser.add_parser('simulate')
    simulate_parser.add_argument('iterations', type = int, help = "number of desired simulations")
    simulate_parser.add_argument('first_guess', type = str, help = "the first guess to be used for the simulations")


    args = parser.parse_args()
    

    if args.command == 'solve':
        parse_solve_args(parser, args)

    elif args.command == 'play':
        parse_play_args(parser, args)

    elif args.command == 'simulate':
        parse_simulate_args(parser, args)

def main():
    
    parse_arguments()
    
    

if __name__ == "__main__":
    main()
