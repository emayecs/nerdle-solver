from random import randint

def valid_equation(eq): # if the equation doesn't have any errors (may or may not be true)
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
    if '/' in eq and eq[eq.index('/')+1]=='0':
        # divide by 0
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
        while i<len(ex_split):
            if ex_split[i]=='*' or ex_split[i]=='/':
                if (ex_split[i]=='*'):
                    ex_split[i-1]=ex_split[i-1]*ex_split[i+1]
                    ex_split.pop(i)
                    ex_split.pop(i)
                    i-=1
                else:
                    ex_split[i-1]=ex_split[i-1]/ex_split[i+1]
                    ex_split.pop(i)
                    ex_split.pop(i)
                    i-=1
            i+=1
        if (len(ex_split)==1):
            break
        i = 0
        while i<len(ex_split):
            if ex_split[i]=='+' or ex_split[i]=='-':
                if (ex_split[i]=='+'):
                    ex_split[i-1]=ex_split[i-1]+ex_split[i+1]
                    ex_split.pop(i)
                    ex_split.pop(i)
                    i-=1
                else:
                    ex_split[i-1]=ex_split[i-1]-ex_split[i+1]
                    ex_split.pop(i)
                    ex_split.pop(i)
                    i-=1
            i+=1
    return ex_split[0]

def equation_computes(eq):
    if (not valid_equation(eq)):
        return False
    equals_index = eq.index('=')
    left = evaluate_expression(eq[:equals_index])
    right = evaluate_expression(eq[equals_index+1:])
    return (left==right)

def is_operation(c):
    operations = ['+','-','*','/','=']
    return c in operations

def main():
    generate_equations(5)

def generate_equations(x): # randomly generate x equation
    operations = ['+','-','*','/','=']
    digits = []
    for i in range(0,10):
        digits.append(str(i))
    symbols = digits + operations
    counter = 0
    while (counter<x):
        eq = ""
        after_zero = False
        contains_symbol = False
        for i in range(0,7):
            if (after_zero): #prevents numbers besides 0 from starting with 0
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
        if (valid_equation(eq) and contains_symbol):
            counter+=1

if __name__ == "__main__":
    main()
