from random import randint
from tqdm import tqdm
import json, argparse, pprint, sys

SYMBOLS = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/']
DIGITS = ['0','1','2','3','4','5','6','7','8','9']

class bcolors:
    '''
    Class to color terminal output.
    '''
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
    '''
    Returns whether 'c' is a math operation.
    '''
    operations = ['+','-','*','/','=']
    return c in operations

def is_valid_equation(eq):
    '''
    Returns True or False, whether ``eq`` is a valid equation. 

    See Also
    --------
    is_valid_expression: Returns whether ``ex`` is a valid expression.
    '''
    index = eq.index('=')
    ex1 = eq[0:index]
    ex2 = eq[index+1:]
    return is_valid_expression(ex1) and is_valid_expression(ex2)

def is_valid_expression(ex):
    '''
    Returns whether ``ex`` is a valid expression.

    Parameters
    ----------
    ex : str
        Input expression.
    
    Returns
    -------
    bool
        True if ``ex`` meets all the following criteria, False otherwise:
        - The first or last characters in ``ex`` are not operations, except if the first character is a ``-``
        - ``ex`` does not contain 2 operations next to each other or the 2nd operation is a ``-``.
            (e.g. ``+/`` is not allowed, but ``+-`` is)
        - ``ex`` doesn't divide by 0, i.e. ``/0`` and ``/-0`` aren't present in the ``ex``
    '''
    # negative numbers are ok
    if is_operation(ex[0] and ex[0]!='-' or is_operation(ex[-1])):
        return False
    # if an operation is next to another operation
    for i in range(len(ex)-1):
        if is_operation(ex[i] and is_operation(ex[i+1])):
            #allows operation before '-'
            if i == 0 or ex[i+1] != '-':
                return False

    #prevent more than 3 operations from being in a row
    for i in range(len(ex)-2):
        if is_operation(ex[i]) and is_operation(ex[i+1]) and is_operation(ex[i+2]):
            return False
    
    # #prevent negative 0's
    # if len(ex)>=2:
    #     if ex[i]=='-' and ex[i+1]=='0':
    #         return False
    # for i in range(len(ex)-2):
    #     if is_operation(ex[i]) and ex[i+1]=='-' and ex[i+2]=='0':
    #         return False

    #prevent dividing by 0
    ex_copy = ex
    while '/' in ex_copy:
        i = ex_copy.index('/')
        j = i+1
        number = ""
        while j<len(ex_copy):
            if is_operation(ex_copy[j]):
                # don't break loop if first char after operation is '-'; negative number
                if not (ex_copy[j]=='-' and j==i+1):
                    break
            number += ex_copy[j]
            j += 1
        number = int(number)
        if number==0:
            return False
        ex_copy = ex_copy[i+1:]

    return True

def evaluate_expression(ex):
    '''
    Evaluates and returns the value of an expression.

    Parameters
    ----------
    ex : str
        Input expression.

    Returns
    -------
    int
        The value of ``ex``.
    
    Raises
    ------
        ValueError: If ``ex`` is not a valid expression.
    '''
    if not is_valid_expression(ex):
        raise ValueError(f'{ex} is not a valid expression')

    ex_split = []
    number = ""

    #split expression into numbers and operations
    for i in range(len(ex)):
        #check negative numbers
        if ex[i]=='-':
            if i==0:
                number += ex[i]
                continue
            elif is_operation(ex[i-1]):
                number += ex[i]
                continue

        if is_operation(ex[i]):
            ex_split.append(int(number))
            ex_split.append(ex[i])
            number = ""
        else:
            number+=ex[i]

            # last element so add to array
            if i==len(ex)-1:
                ex_split.append(int(number))
    
    while len(ex_split)>1:
        i = 0
        while '*' in ex_split or '/' in ex_split:
            if (ex_split[i]=='*'):
                ex_split[i-1] = ex_split[i-1] * ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i -= 1
            elif ex_split[i]=='/':
                ex_split[i-1]=ex_split[i-1] / ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i -= 1
            i += 1
        if len(ex_split)==1:
            break
        i = 0
        while '+' in ex_split or '-' in ex_split:
            if (ex_split[i]=='+'):
                ex_split[i-1] = ex_split[i-1] + ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i -= 1
            elif ex_split[i]=='-':
                ex_split[i-1] = ex_split[i-1] - ex_split[i+1]
                ex_split.pop(i)
                ex_split.pop(i)
                i -= 1
            i += 1
    return ex_split[0]

def equation_computes(eq):
    '''
    Returns whether both sides of an equation are equal.

    Parameters
    ----------
    eq : str
        Input equation.
    
    Returns
    -------
    bool
        True if both sides of ``eq`` are equal, False otherwise
    '''
    if (not is_valid_equation(eq)):
        return False
    equals_index = eq.index('=')
    left = evaluate_expression(eq[:equals_index])
    right = evaluate_expression(eq[equals_index+1:])
    return left == right

def contains_leading_zeros(ex):
    '''
    Returns whether the input contains leading zeros.

    Parameters
    ----------
    ex : str
        Input equation or expression.

    Returns
    -------
    bool
        True if the ``ex`` contains leading zeros, False otherwise.
        Leading zeros are numbers that are preceded by at least one 0 (e.g. ``007``).
    '''
    for i in range(0,len(ex)-1):
        if (ex[i]=='0' and not is_operation(ex[i+1])):
            if i==0 or is_operation(ex[i-1]):
                return True
    return False

def generate_random(x): 
    '''
    Returns an array of randomly generated equations that may or may not compute.
    '''
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
            eq += symbols[r]
        eq_pos = randint(1,6)
        eq = eq[:eq_pos]+'='+eq[eq_pos:]
        
        if (is_valid_equation(eq) and contains_symbol):
            counter += 1
            equations.append(eq)
    return equations

def generate_conditions(length):
    '''
    Generates a 2-d array of possible values for an expression of a given length.
    '''
    operations = ['+','-','*','/']
    digits = ['0','1','2','3','4','5','6','7','8','9']
    symbols = digits + operations
    values = []
    for i in range(length):
        if i==length-1:
            values.append(digits.copy())
        elif i==0:
            values.append(digits.copy()+['-'])
        else:
            values.append(symbols.copy())
    return values

def generate_indices(length):
    '''
    Generates an array of all 0's of a given length.
    '''
    indices = []
    for _ in range(length):
        indices.append(0)
    return indices

def write_data(equations, left_ex_length, right_ex_length, left_ex_indices, right_ex_indices, generated_left_ex):
    '''
    Writes all data into json file.
    '''
    with open('equations.json','w') as f:
        json.dump(
            {"equations": equations,
            "lengths":[left_ex_length, right_ex_length],
            "indices":[left_ex_indices, right_ex_indices],
            "generated":generated_left_ex,
            },
        f,indent = 2)

def verify_equations():
    '''
    Verify that all equations compute.
    '''
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


def generate_equations(length = 8):
    '''
    Generates possible equations that compute and writes them into ``equations.json``.

    Parameters
    ----------
    length : int, optional
        The length of the equations to be generated. If length is None, it is set to 8.
    
    Output
    ------
    dict
        A dictionary containing the generated equations and other generation data.

        equations : array
            An array of generated equations that compute.
            Equations that evaluate to a fraction are not included in ``equations.`` (e.g. 8/12=2/3)
    '''
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

        left_ex_values = generate_conditions(left_ex_length)
        right_ex_values = generate_conditions(right_ex_length)

    except:
        left_ex_values = generate_conditions(left_ex_length)
        right_ex_values = generate_conditions(right_ex_length)

        left_ex_indices = generate_indices(left_ex_length)
        right_ex_indices = generate_indices(right_ex_length)

        for i in range(int(pow(10,left_ex_length))):
            generated_left_ex.append([])
        for i in range(int(pow(10,left_ex_length-1))-1):
            generated_left_ex.append([])
            
        write_data(equations, left_ex_length, right_ex_length, left_ex_indices, right_ex_indices, generated_left_ex)

    while left_ex_length <= right_ex_length:

        left_permutations = 1
        for i in range(left_ex_length):
            left_permutations *= len(left_ex_values[i])
        
        for _ in tqdm(range(left_permutations)):
            if left_ex_indices[-1] >= len(left_ex_values[-1]):
                break
            left_ex = ""

            #generate expression
            for i in range(left_ex_length):
                index = left_ex_indices[i]
                left_ex += left_ex_values[i][index]
            
            #add expression to array if valid
            if is_valid_expression(left_ex):# and not leading_zeroes(left_ex):
                value = evaluate_expression(left_ex)
                if value == int(value):
                    value = int(value)
                    if value >= 0:
                        generated_left_ex[value].append(left_ex)
                    #negative numbers
                    else:
                        generated_left_ex[int(pow(10,left_ex_length))-value-1].append(left_ex)

            #update indices
            left_ex_indices[0] += 1

            for i in range(left_ex_length-1):
                if left_ex_indices[i] == len(left_ex_values[i]):
                    left_ex_indices[i] = 0
                    left_ex_indices[i+1] += 1

        right_permutations = 1
        for i in range(right_ex_length):
            right_permutations *= len(right_ex_values[i])
        
        for _ in tqdm(range(right_permutations)):
            if right_ex_indices[-1] >= len(right_ex_values[-1]):
                break

            right_ex = ""

            #generate expression
            for i in range(right_ex_length):
                index = right_ex_indices[i]
                right_ex += right_ex_values[i][index]
            
            #check if expression is valid
            if is_valid_expression(right_ex):# and not leading_zeroes(right_ex):
                value = evaluate_expression(right_ex)
                #check if value is within bounds of LHS
                if value==int(value) and value<int(pow(10,left_ex_length)) and value > -1 * int(pow(10,left_ex_length-1)):
                    value = int(value)
                    #generate equations
                    if value >= 0:
                        for exp in generated_left_ex[value]:
                            equations.append(exp+"="+right_ex)
                            equations.append(right_ex+"="+exp)
                    else:
                        for exp in generated_left_ex[int(pow(10,left_ex_length)) - value - 1]:
                            equations.append(exp+"="+right_ex)
                            equations.append(right_ex+"="+exp)
            
            #update indices
            right_ex_indices[0] += 1

            for i in range(right_ex_length - 1):
                if right_ex_indices[i] == len(right_ex_values[i]):
                    right_ex_indices[i] = 0
                    right_ex_indices[i+1] += 1

        write_data(equations, left_ex_length, right_ex_length, left_ex_indices, right_ex_indices, generated_left_ex)
        
        #reset variables
        left_ex_length += 1
        right_ex_length -= 1

        left_ex_values = generate_conditions(left_ex_length)
        right_ex_values = generate_conditions(right_ex_length)

        left_ex_indices = generate_indices(left_ex_length)
        right_ex_indices = generate_indices(right_ex_length)

        generated_left_ex.clear()
        for i in range(int(pow(10,left_ex_length))):
            generated_left_ex.append([])
        for i in range(int(pow(10,left_ex_length-1))-1):
            generated_left_ex.append([])
    
    print("\ncompleted equation generation\n")

def remove_negatives(equations):
    '''
    Returns a copy of ``equations`` without equations containing negative numbers.
    '''
    print("Removing equations with negative numbers...")
    new_equations = equations.copy()
    i = 0
    for _ in tqdm(range(len(new_equations))):
        equation = new_equations[i]
        if equation[0] == '-' and not is_operation(equation[1]):
            new_equations.pop(i)
            continue
        should_pop = False
        for j in range(len(equation) - 2):
            if is_operation(equation[j]) and equation[j+1] == '-' and not is_operation(equation[j+2]):
                should_pop = True
                break
        if should_pop:
            new_equations.pop(i)
            continue     
        i+=1
    return new_equations

def remove_leading_zeroes(equations):
    '''
    Returns a copy of ``equations`` without any equations with leading zeros.

    See Also
    --------
    contains_leading_zeros: Returns whether the input contains leading zeros.
    '''
    print("Removing equations with leading zeros...")
    new_equations = equations.copy()
    i = 0
    for _ in tqdm(range(len(new_equations))):
        equation = new_equations[i]
        if contains_leading_zeros(equation):
            new_equations.pop(i)
            continue
        i+=1
    return new_equations

def remove_equal_zero(equations):
    '''
    Returns a copy of ``equations`` without any equations that evaluate to 0.
    '''
    print("Removing equations that equal 0...")
    new_equations = equations.copy()
    i = 0
    for _ in tqdm(range(len(new_equations))):
        equation = new_equations[i]
        ex1 = equation[0:equation.index('=')]
        value = evaluate_expression(ex1)
        if value == 0:
            new_equations.pop(i)
            continue
        i += 1
    return new_equations

def update_conditions(guess, result, old_conditions, old_equals_conditions):
    '''
    Updates and returns the conditions of the target equation, i.e. the possible characters at each index of the target equation.

    Arguments
    ---------
    guess : str
        Equation that the user guessed.
    result : str
        Result of the intial guess, with 'g', 'p', and 'b', marking green, purple, and black characters respectively.
    old_conditions : 2-d array
        A 2-d array with currently known conditions of the target equation. The nth index of ``old_conditions``
        is an array containing the known characters that can be found at the nth index of the 
        target equation.
    old_equals_conditions : array of bools
        An array with currently known conditions of where ``=`` can be in the target equation. The nth index
        of ``old_equals_conditions`` is set to False if an ``=`` sign cannot be present at the 
        (n+1)th index ofthe target equation.

    Returns
    -------
    conditions : 2-d array
        The updated conditions of the target equation based on ``guess`` and ``result``.
    equals_conditions : array of bools
        The updated conditions of where ``=`` can be in the target equation. 
    frequency : array of ints
        A frequency array denoting how frequently each character appeared as a purple guess. The nth
        index of ``frequency`` is how many times the nth index of ``SYMBOLS`` appeared as purple in
        ``result.``
    '''
    pp = pprint.PrettyPrinter()
    frequency = [0]*len(SYMBOLS)
    conditions = old_conditions.copy()
    equals_conditions = old_equals_conditions

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
            if guessed_char=='=' and i >= 1:
                equals_conditions[i-1] = False
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
                conditions[i] = [guessed_char]
    
    return conditions, frequency, equals_conditions

def solve(eq, initial_guess, result):
    '''
    Prints recommended guesses to the terminal to solve the classic nerdle.

    Parameters
    ----------
    eq : array of strings
        List of possible equations that the target equation can be.
    initial_guess : str
        The user's initial guess.
    result : str
        Result of the intial guess, with 'g', 'p', and 'b', marking green, purple, and black characters respectively.
    
    Output
    ------
    guess
        The recommended guess.
    probability
        Prints the probability of guessing the target equation correct using the recommended guess.

    Input
    -----
    result
        Result of the recommended guess, with 'g', 'p', and 'b', marking green, purple, and black characters respectively.
        Must be the same length as ``initial_guess`` and only contain 'g','p','b','G','P', or 'B'.

    Raises
    ------
        RuntimeError: If 0 equations match the result entered by the user.
        ValueError: If ``result`` does not have the same length as ``initial_guess.``
        ValueError: If ``result`` contains other characters besides 'g','p','b','G','P', or 'B'.
    '''
    equations = eq.copy()

    # initialize conditions:
    length = len(initial_guess)
    conditions = generate_conditions(length)
    
    #a boolean array of length 6; the value at the nth index denotes if it's possible for the equation to have a '=' at the (n+1)th index
    equals_conditions = [True] * (length-2)

    guess = initial_guess

    #modify conditions based on result
    while result!="q":
        conditions, frequency, equals_conditions = update_conditions(guess, result, conditions, equals_conditions)
        #pp.pprint(conditions)
        guess, equations = filter_equations(equations, conditions, equals_conditions, frequency)
        
        print("Best guess: "+guess)

        if len(equations) == 0:
            raise RuntimeError("Result is impossible; no equations match conditions.")

        probability = round(1/len(equations)*100,3)
        
        print(f"{len(equations)} possible equation(s), {probability}% probability")

        if probability == 100:
            return

        result = input("Enter the result:\n")
        if result == "q":
            return
        elif len(result) != length:
            raise ValueError("\'result\' must be the same length as \'initial_guess\'.")
        else:
            valid_chars = ['g','p','b','G','P','B']
            for c in result:
                if c not in valid_chars:
                    raise ValueError("'result' must only contains characters from 'g','p','b','G','P', or 'B'.")

def simulate(eq, target, first_guess, chances):
    '''
    Runs a simulation of solving a classic Nerdle.

    Parameters
    ----------
    eq : array of strings
        An array containing all possible equations the target equation can be.
    target : str
        The target equation for the user to guess.
    first_guess : str
        The first guess that the user enters.
    chances : int
        The number of chances the computer gets to guess the Nerdle correctly.
    
    Returns
    -------
    guesses : array of strings
        An array containing all the guesses the computer made.
    '''
    equations = eq.copy()
    guesses = [first_guess]
    pp = pprint.PrettyPrinter()

    guess = guesses[0]
    result = equation_similarity(target, guess)
    color_guess(result, guess)

    turns = 0

    #conditions start with allowing all symbols in all places
    length = len(first_guess)
    conditions = generate_conditions(length)
    equals_conditions = [True] * (length - 2)

    while turns < chances:
        turns+=1
        conditions, frequency, equals_conditions = update_conditions(guess, result, conditions, equals_conditions)
        guess, equations = filter_equations(equations, conditions, equals_conditions, frequency, False)
        guesses.append(guess)
        result = equation_similarity(target, guess)
        color_guess(result, guess)
        if guess == target:
            break

    if len(equations) != 1 and guess != target :
        print(f"{bcolors.WARNING}WARNING: failed to solve {target} within {chances} turns{bcolors.ENDC}",end="")

    return guesses

def equation_similarity(target, guess):
    '''
    Return the result of the guess in terms of 'G', 'P', or 'B', given a target equation.

    Parameters
    ----------
    target : str
        The target equation.
    guess : str
        The guessed equation.
    
    Returns
    -------
    similarity : str
        The result of the guess.
    '''
    similarity = "."*len(guess)
    symbols = SYMBOLS+['=']
    symbol_frequency = [0]*len(symbols)

    # check characters that are correct (green)
    for i in range(len(guess)):
        if guess[i]==target[i]:
            similarity=similarity[:i]+"G"+similarity[i+1:]
        else:
            symbol_frequency[symbols.index(target[i])]+=1
    
    for i in range(len(guess)):
        if similarity[i]=="G":
            continue
        index = symbols.index(guess[i])
        #purple
        if symbol_frequency[index]>=1:
            symbol_frequency[index]-=1
            similarity=similarity[:i]+"P"+similarity[i+1:]
        #black
        else:
            similarity=similarity[:i]+"B"+similarity[i+1:]
    return similarity

def filter_equations(eq, conditions, equals_conditions, symbol_frequency, verbose=True):
    '''
    Return the best guess and a list of all possible equations the target equation can be.

    Parameters
    ----------
    eq : array of strings
        Array of all potential equations the target equation can be.
    conditions : 2-d array
        A 2-d array with currently known conditions of the target equation. The nth index of ``conditions``
        is an array containing the known characters that can be found at the nth index of the 
        target equation.
    equals_conditions : array of bools
        An array with currently known conditions of where ``=`` can be in the target equation. The nth index
        of ``equals_conditions`` is set to False if an ``=`` sign cannot be present at the 
        (n+1)th index ofthe target equation.
    symbol_frequency : array of ints
        A frequency array denoting how frequently each character appeared as a purple guess. The nth
        index of ``symbol_frequency`` is how many times the nth index of ``SYMBOLS`` appeared as purple in
        the recently guessed equation.
    verbose : bool
        If the status of filtering equations should be printed, including loading bars and terminal messages.
        If ``verbose`` is None, it is set to True.

    Returns
    -------
    best_equation : str
        The recommended equation to guess on the next round.
    equations : array of strings
        Updated array of all potential equations the target equation can be.
    '''
    equations = eq.copy()
    pp = pprint.PrettyPrinter()

    # frequency array of each character in conditions
    symbol_count = [0] * len(SYMBOLS)
    for c in conditions:
        for s in c:
            symbol_count[SYMBOLS.index(s)] += 1

    i = 0
    highest_value = 0
    best_equation = ""
    
    if verbose:
        print('Filtering equations...')

    iterator = tqdm(range(len(equations))) if verbose else range(len(equations))

    for _ in iterator:
        if i >= len(equations):
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
            
            if char == '=':
                #only need to check if char is occupating a green spot
                if len(conditions[j]) == 1:
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
            if freq >= 1:
                purple_symbols.append(SYMBOLS[j])

        for symbol in purple_symbols:
            if symbol not in equation:
                pop = True
                break
        
        if pop:
            equations.pop(i)
            continue
        
        if value > highest_value or best_equation == '':
            best_equation = equation
            highest_value = value
        i += 1

    if verbose:
        print('Finished filtering equations.')

    return best_equation, equations

def run_simulation(equations, n, first_guess, chances):
    '''
    Simulates solving ``n`` Nerdle games.
    '''
    print('Beginning simulation...\n')
    for _ in range(n):
        target = equations[randint(0,len(equations)-1)]
        try:
            print("Equation: "+target)
            simulate(equations, target, first_guess, chances)
        except Exception as e: 
            print("Error with solving: "+target)
            print(e)
            break
        print()

def read_equations():
    '''
    Returns the equations stored in the json file.
    '''
    try:
        with open('equations.json','r') as f:
            data = json.load(f)
            equations = data["equations"]
            return equations
    except:
        print('equations could not be read from equations.json')
        sys.exit()

def play(eq, chances):
    '''
    Starts a nerdle game on the command line.
    '''
    print('Starting game...')
    print('Enter q to quit\n')

    # Choose random equation
    equations = eq.copy()
    target = equations[randint(0,len(equations)-1)]
    guesses = 0
    guesses = []
    results = []

    while (len(guesses) < chances):
        print()
        #prints the current status of the game
        for i in range(chances):
            if i < len(guesses):
                guess = guesses[i]
                result = results[i]
                color_guess(result, guess)
            else:
                print(u"\u2588" * 8)
        print()
        guess = input('Guess:\n')
        #error checking
        if (guess == 'q'):
            return
        while (len(guess) != len(target)):
            print("Guess must have a length of " + len(target))
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
        if target == guess:
            return
    
    #print final status of the game
    for i in range(chances):
        if i < len(guesses):
            guess = guesses[i]
            result = results[i]
            color_guess(result, guess)
        else:
            print(u"\u2588" * 8)

    print('The answer was: '+target)

def color_guess(result, guess):
    '''
    Given a guess and its result, prints the color-coded version.
    '''
    for j in range(len(guess)):
        if result[j]=="G":
            print(f"{bcolors.OKGREEN}{guess[j]}{bcolors.ENDC}",end="")
        if result[j]=="P":
            print(f"{bcolors.HEADER}{guess[j]}{bcolors.ENDC}",end="")
        if result[j]=="B":
            print(guess[j],end="")
    print()

def filter_initial_equations(include_negatives, include_leading_zeroes, allow_equal_zero):
    '''
    Returns a list of equations given the command line arguments.
    '''
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

def parse_play_args(parser, args):
    '''
    Parses the arguments for the play function.
    '''
    if (args.chances<=0):
        parser.error('\'chances\' must be greater than 0')

    equations = filter_initial_equations(args.include_negatives, args.include_leading_zeroes, args.allow_equal_zero)
    play(equations, args.chances)

def parse_solve_args(parser, args):
    '''
    Parses the arguments for the solve function.
    '''
    if len(args.guess)!=8:
        parser.error('\'guess\' must be of length 8')
    
    equations = filter_initial_equations(args.include_negatives, args.include_leading_zeroes, args.allow_equal_zero)
    solve(equations, args.guess, args.result)

def parse_simulate_args(parser, args):
    '''
    Parses the arguments for the simulate function.
    '''
    if args.iterations <= 0:
        parser.error('\'iterations\' must be >= 1')
    if args.chances <= 0:
        parser.error('\'chances\' must be greater than 0')
    if len(args.first_guess) != 8:
        parser.error('\'first_guess\' must be of length 8')

    equations = filter_initial_equations(args.include_negatives, args.include_leading_zeroes, args.allow_equal_zero)
    run_simulation(equations, args.iterations, args.first_guess, args.chances)

def parse_arguments():
    '''
    Sets up the argument parser for the program.
    '''
    parser = argparse.ArgumentParser(description='Nerdle Solver & Utility')
    
    subparser = parser.add_subparsers(dest='command')

    parser.add_argument('--no_negatives', action='store_const', dest = 'include_negatives', const = False,
     default = True, help = "equations with with negative numbers will not be included (e.g. -4*3=-12)")
    parser.add_argument('--no_leading_zeroes', action='store_const', dest = 'include_leading_zeroes', const = False,
     default = True, help = "equations with leading zeroes will not be included (e.g. 004*3=12)")
    parser.add_argument('--dne_zero', action='store_const', dest = 'allow_equal_zero', const = False,
     default = True, help = "equations that equal 0 will not be included (e.g. 0*9999=0)")

    solve_parser = subparser.add_parser('solve')
    solve_parser.add_argument('guess', type = str, help = "guess for the equation")
    solve_parser.add_argument('result', type = str,  help = "a string with each letter denoting the result of the guess")

    play_parser = subparser.add_parser('play')
    play_parser.add_argument('chances', type = int, help = "the number of chances that the user gets to guess the equation")

    simulate_parser = subparser.add_parser('simulate')
    simulate_parser.add_argument('iterations', type = int, help = "number of simulations to run")
    simulate_parser.add_argument('first_guess', type = str, help = "the first guess to be used for the simulations")
    simulate_parser.add_argument('chances', type = int, help = "the number of chances that the simulator gets to guess the equation")

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