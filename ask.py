from random import randint
import time, pprint, json

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
    
    print(eq_count) 
    return equations

def ask():
    global valid_equations
    pp = pprint.PrettyPrinter()
    #assumes length of 8
    operations = ['+','-','*','/']
    digits = []
    
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations

    guess = input("Enter the guess.\n")
    while (not equation_computes(guess)):
        print("Equation does not compute.")
        guess = input("Enter the guess.\n")
    result = input("Enter the result.\n")

    length = 8
    conditions=[]
    for i in range(0,length):
        if i==0 or i==length-1:
            conditions.append(digits.copy())
        else:
            conditions.append(symbols.copy())
    equals_conditions = [True]*(length-2)

    while (result!="exit"):
        for i in range(0, len(result)):
            if result[i].upper()=='B' and guess.index(guess[i])==i:
                for j in range(0, len(conditions)):
                    if guess[i] in conditions[j]:
                        conditions[j].remove(guess[i])
            elif result[i].upper()=='P':
                if guess[i]=='=':
                    equals_conditions[i-1]=False
                else:
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
        print("Probability: "+str(1/len(valid_equations)*100)+"%")
        #pp.pprint(conditions)
        result = input("Enter the result.\n")
        if (result=="exit"):
            break
    #"87-53=34"


def filter_equations(conditions, equals_conditions):
    global valid_equations
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

    while i<len(valid_equations):
        
        equation_symbols = []
        value = 0
        equation = valid_equations[i]

        equal_index = equation.index('=')
        if (not equals_conditions[equal_index-1]):
            valid_equations.pop(i)
            continue

        # checks if each character is allowed at the position
        pop = False
        for j in range(0,length):
            if equation[j]=='=':
                continue
            if not equation[j] in conditions[j]:
                valid_equations.pop(i)
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

def main():
    global valid_equations

    try:
        with open('valid_equations.json','r') as f:
            data = json.load(f)
            valid_equations = data["equations"]
            indices = data["indices"]
    except:
        pass

    ask()
    

if __name__ == "__main__":
    main()
