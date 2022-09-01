from random import randint
from tqdm import tqdm
import json

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

    #prevent negative 0's
    if len(ex)>=2:
        if ex[i]=='-' and ex[i+1]=='0':
            return False
    for i in range(len(ex)-2):
        if is_operation(ex[i]) and ex[i+1]=='-' and ex[i+2]=='0':
            return False

    #prevent dividing by 0
    ex_copy = ex
    while '/' in ex_copy:
        index = ex_copy.index('/')
        if index<len(ex_copy)-1 and ex_copy[index+1]=='0':
            return False
        ex_copy = ex_copy[index+1:]

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
returns value if it computes, otherwise false
'''
def equation_computes(eq):
    if (not is_valid_equation(eq)):
        return False
    equals_index = eq.index('=')
    left = evaluate_expression(eq[:equals_index])
    right = evaluate_expression(eq[equals_index+1:])
    if left==right:
        return left
    return False

'''
determines if leading zeros are in equation/expression
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
generates possible equations (default length 8)
- no leading zeroes (e.g. 004*3=12)
- negatives allowed except for -0 (e.g. -0+6-5=1)
- fractions not allowed (e.g. 5/4=10/8)

takes ~35 seconds
'''
def generate_equations(length=8):
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
        
        for tqdm_counter in tqdm(range(left_permutations)):
            if left_ex_indices[-1]>=len(left_ex_values[-1]):
                break
            left_ex = ""

            #generate expression
            for i in range(left_ex_length):
                index = left_ex_indices[i]
                left_ex+=left_ex_values[i][index]
            
            #add expression to array if valid
            if is_valid_expression(left_ex) and not leading_zeroes(left_ex):
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
        
        for tqdm_counter in tqdm(range(right_permutations)):
            if right_ex_indices[-1]>=len(right_ex_values[-1]):
                break

            right_ex = ""

            #generate expression
            for i in range(right_ex_length):
                index = right_ex_indices[i]
                right_ex+=right_ex_values[i][index]
            
            #check if expression is valid
            if is_valid_expression(right_ex) and not leading_zeroes(right_ex):
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

def main():
    generate_equations()

if __name__ == "__main__":
    main()
