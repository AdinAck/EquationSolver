# Load permutated equation list from "build.py" for evaluation.
# By Adin Ackerman and Garrett Kunkler

import sys
import numpy as np
from math import sqrt, cos, sin, pi

def replaceExclude(string, name, val, bad):
    # print("before:",string)
    out = string
    length = len(name)
    i = 0
    while i < len(string)-length+1:
        # print(string[i:i+length])
        if string[i:i+length] == name:
            isLeftGood = False
            isRightGood = False
            if i != 0:
                if string[i-1] in bad:
                    isLeftGood = True
            else: isLeftGood = True
            if i != len(string)-length:
                if string[i+length] in bad:
                    isRightGood = True
            else: isRightGood = True
            if isLeftGood and isRightGood:
                # print("Replacing",name,"with",val,"in",string)
                out = out[:i]+val+out[i+length:]
                string = out
                # print("out:",out)
                i += len(val)
            # print(string[i:i+length],isLeftGood,isRightGood)
        i += 1
    # print("after:",out)

    return out

def gigaMegaSolver(equations,formulas,available,bad,done=[]):
    i = -1
    while -i < len(equations)+1:
        if len(equations) == 0 or len(formulas) == 0:
            return
        # ====================
        # Test for any variables in right side of equation.
        n = 0
        # print(equations[i][1])
        # print(looking)
        for k in available:
            if k in equations[i][1]:
                n += 1
        # ====================
        # If none, solve variable equal to expression.
        if n == 0:
            val = str(eval(equations[i][1])) # Evaluate
            name = equations[i][0]
            if name in available: # If variable being solved for was not provided in beginning.
                # print("eq:",equations)
                # print("form:",formulas)
                print("\nUsing equation:",formulas[i][0],"=",formulas[i][1])
                print("Plugging in values:",equations[i][0],"=",equations[i][1])
                available.remove(name)
             # Change known variable to solved variable for next iteration.
                print(name,"=",val)
            done.append(name) # Add solved variable to list of solved variables.
            # ====================
            # Remove all occasions of "newly solved variable = something".
            for j in range(len(equations)-1,-1,-1):
                if equations[j][0] in done:
                    equations.pop(j)
                    formulas.pop(j)
                elif name in equations[j][1]:
                    # Replace all occasions of newly solved variable with value.
                    equations[j][1] = replaceExclude(equations[j][1],name,val,bad)

            # Recurse
            gigaMegaSolver(equations,formulas,available,bad,done)
        i -= 1


def run(directory):
    print("Loading...")
    bad = np.load(directory+"/cached/bad.npy").tolist()
    arr = np.load(directory+"/cached/arr.npy").tolist()
    available = np.load(directory+"/cached/available.npy").tolist()
    equations2 = np.load(directory+"/cached/permutated.npy").tolist()
    formulas2 = np.load(directory+"/cached/permutated.npy").tolist().copy()

    print("Substituting from given...")
    for e in equations2:
        for c in arr:
            e[1] = replaceExclude(e[1],c[0],c[1],bad)
            e[0] = replaceExclude(e[0],c[0],c[1],bad)

    print("Checking for already known values...")
    pre = False
    for i in equations2:
        try:
            eval(i[1])
            pre = True
        except:
            pass
    if pre:
        print("\n---")
        gigaMegaSolver(equations2,formulas2,available,bad)
        print("\n---\n")
    else:
        print("None found.")
    if len(available) >= 2:
        print("Available variables:",available)

        while True:
            stuff = input("var name? ")
            if stuff == "end":
                break
            if stuff not in available:
                print("Variable is not available for evaluation.")
                continue
            know = stuff
            val = input(know+" = ")
            arr.append([know,val])

        for e in equations2:
            for c in arr:
                e[1] = replaceExclude(e[1],c[0],c[1],bad)
                e[0] = replaceExclude(e[0],c[0],c[1],bad)

        print("\n---")
        gigaMegaSolver(equations2,formulas2,available,bad)
        print("\n---\n")
    else:
        print("No possible variable solutions remain. Exiting.")
        exit()

try:
    run(sys.argv[1])
except IndexError:
    print("Loading as module.")
