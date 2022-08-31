from random import randint
from tqdm import tqdm
import time, json

valid_equations = [] #all possible equations that compute

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

'''
determines if the expression has any errors
'''
def valid_expression(ex):
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

    # divide by 0
    ex_copy = ex
    while '/' in ex_copy:
        index = ex_copy.index('/')
        if index<len(ex_copy)-1 and ex_copy[index+1]=='0':
            return False
        ex_copy = ex_copy[index+1:]

    return True

def evaluate_expression(ex):
    if not valid_expression(ex):
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
        
        if (valid_equation(eq) and contains_symbol):
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
generates possible equations (default length 8)
- no leading zeroes (e.g. 004*3=12)
- negatives allowed, no negative 0 (e.g. -0+6-5=1)
- fractions not allowed (e.g. 5/4=10/8)
'''
def complete_generate(length=8, save_time=60):
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
        with open('total_equations.json','r') as f:
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
            
        with open('total_equations.json','w') as f:
            json.dump(
                {"equations": equations,
                "lengths":[left_ex_length, right_ex_length],
                "indices":[left_ex_indices, right_ex_indices],
                "generated":generated_left_ex,
                },
                f,indent = 2)

    while left_ex_length<=right_ex_length:
        t0 = time.perf_counter()

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
            if valid_expression(left_ex) and not leading_zeroes(left_ex):
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

            #save data every save_time seconds
            t1 = time.perf_counter()
            if t1-t0>=save_time:
                t0 = t1
                with open('total_equations.json','w') as f:
                    json.dump(
                        {"equations": equations,
                        "lengths":[left_ex_length, right_ex_length],
                        "indices":[left_ex_indices, right_ex_indices],
                        "generated":generated_left_ex,
                        },
                        f,indent = 2)

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
            if valid_expression(right_ex) and not leading_zeroes(right_ex):
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
            
            #save data every save_time seconds
            t1 = time.perf_counter()
            if t1-t0>=save_time:
                t0 = t1
                with open('total_equations.json','w') as f:
                    json.dump(
                        {"equations": equations,
                        "lengths":[left_ex_length, right_ex_length],
                        "indices":[left_ex_indices, right_ex_indices],
                        "generated":generated_left_ex,
                        },
                        f,indent = 2)

        with open('total_equations.json','w') as f:
            json.dump(
                {"equations": equations,
                "lengths":[left_ex_length, right_ex_length],
                "indices":[left_ex_indices, right_ex_indices],
                "generated":generated_left_ex,
                },
                f,indent = 2)
        
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
generates all possible equations that compute
additional restraints:
- no leading zeroes
- equation != 0
- consequently, must have >=1 operation
'''
def generate_equations(conditions, equals_conditions): 
    global valid_equations
    
    operations = ['+','-','*','/']
    digits = []
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations
    
    length = 8
    indices = [0] * length

    eq_count = 0
    equations = valid_equations

    try:
        with open('valid_equations.json','r') as f:
            data = json.load(f)
            valid_equations = data["equations"]
            equations = valid_equations
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
    with open('valid_equations.json','w') as f:
        json.dump({"indices":indices,"equations":equations}, f ,indent = 2)
    print(eq_count) 
    return equations

def main():
    complete_generate()
    '''
    global valid_equations
    operations = ['+','-','*','/']
    digits = []
    
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations

    length = 8
    conditions=[]
    for i in range(0,length):
        if i==0 or i==length-1:
            conditions.append(digits.copy())
        else:
            conditions.append(symbols.copy())

    equals_conditions = [True]*(length-2)
    generate_equations(conditions, equals_conditions)
    '''


if __name__ == "__main__":
    main()
