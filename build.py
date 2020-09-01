# Generate cached equation permutation list for use with "run.py"
# By Adin Ackerman and Garrett Kunkler

import sys
import os
import time
import numpy as np
from sympy import nonlinsolve
from sympy.parsing.sympy_parser import parse_expr

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

def permutate(arr,available):
    out = []
    solveFor = []
    bad = [" ", "*", "/", "+", "-", "(", ")"]
    for char in available:
        if findVar(arr[0],char,bad) or findVar(arr[1],char,bad):
            solveFor.append(char)
    for char in solveFor:
        try:
            print("Solving",arr,"for",char)
            yeeet = list(iter(nonlinsolve([parse_expr("-".join([arr[1],arr[0]]))],(parse_expr(char)))))
            try:
                while len(yeeet) == 1:
                    yeeet = list(iter(yeeet[0]))
                raise
            except:
                try:
                    while len(yeeet) > 1:
                        yeeet = yeeet[0]
                except:
                    pass

            for i in yeeet:
                temp = str(i)
                temp = temp.replace(",","")
                out.append([char,temp])
                print([char,temp])
        except SyntaxError:
            print(f"Failed to solve {arr} for {char}.")
        # final = [char,list(nonlinsolve([parse_expr("-".join([arr[1],arr[0]]))],(parse_expr(char))))[0][0]]

        # print(final)
        # out.append(final)

    return out

def generator(equations,available):
    output = []
    temp = []
    # print("before:",equations)
    for arr in equations:
        temp.extend(permutate(arr,available))
        for d in range(len(temp)-1,-1,-1):
            for eq in range(len(equations)-1,-1,-1):
                # print(equations[eq], temp[d])
                if equations[eq][0] == temp[d][0] and equations[eq][1] == temp[d][1]:
                    temp.pop(d)
                    d-=1
    equations.extend(temp)
    # print("after:",equations)

    for p in equations:
        loc = []
        for l in range(len(equations)):
            if equations[l][0] == p[0] and [equations[l][1],p[1]] not in output:
                if equations[l][0] in available and p[0] in available:
                    loc.append(l)
        for m in range(len(loc)-1):
            if [equations[loc[m]][1],equations[loc[m+1]][1]] not in output:
                numVars = 0
                for k in available:
                    if k in equations[loc[m]][1]+equations[loc[m+1]][1]:
                        solveFor = k
                        numVars+=1
                if numVars == 1:
                    garit = [k,str(list(nonlinsolve([" - ".join([equations[loc[m]][1],equations[loc[m+1]][1]])],(parse_expr(solveFor))))[0][0])]
                    if "complexes" in garit[1].lower() or "emptyset" in garit[1].lower() or "conditionset" in garit[1].lower():
                        break
                else:
                    garit = [equations[loc[m]][1],equations[loc[m+1]][1]]
                output.append(garit)
                # print(equations)

    temp = []
    # print("before:",equations)
    for arr in output:
        temp.extend(permutate(arr,available))
        # print("temp:",temp)
        for d in range(len(temp)-1,-1,-1):
            for eq in range(len(output)-1,-1,-1):
                # print(d)
                if len(output) > 0 and len(temp) > 0:
                    pass
                    # print(output[eq],temp[d])
                    # if output[eq][0] == temp[d][0] and output[eq][1] == temp[d][1]:
                    #     # print("pop!")
                    #     print("popping",temp[d])
                    #     temp.pop(d)
                    #     # print(temp)
                    #     d-=1
    equations.extend(temp)
    # print("after:",equations)
    equations.reverse()
    # print(equations)
    for i in range(len(equations)-1,-1,-1):
        # print("testing 0:",equations[i])
        if equations[i][1] == "0":
            # print("0:",equations[i])
            equations.pop(i)
    return equations

def findVar(string, name, bad):

    # print("before:",string)
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
                return True
            # print(string[i:i+length],isLeftGood,isRightGood)
        i += 1
    # print("after:",out)

    return False

def build(directory):
    print("Loading equations...")
    f = open(directory+"/equations.txt", "r")
    temp = f.readlines()
    equations = [i[:-1].split(" = ") for i in temp]
    for i in equations:
        print(i)

    f.close()
    temp = " ".join(np.asarray(equations).flatten())

    bad = [" ", "*", "/", "+", "-", "(", ")"]
    remove = ["sin", "cos", "sqrt"]
    available = []
    i = 0
    while i < len(temp):
        for j in range(i+1,len(temp)+1):
            try:
                if temp[i] not in bad and temp[j] in bad:
                    available.append(temp[i:j])
                    i += len(temp[i:j])
                    break
                elif temp[j] in bad:
                    break
            except IndexError:
                if temp[i] not in bad:
                    available.append(temp[i:j])
                    i += len(temp[i:j])
                    break
        i += 1

    available = list(dict.fromkeys(available))
    thing = list(available)
    thing.reverse()
    for char in thing:
        try:
            float(char)
            available.remove(char)
        except:
            for removeChar in remove:
                if removeChar in char:
                    available.remove(char)

    print("Loading given values...")
    f = open(directory+"/given.txt", "r")
    arr = [i[:-1].split(" = ") for i in f.readlines()]
    f.close()

    for c in arr:
        print(c)
        if c[0] in available:
            available.remove(c[0])

    print("Permutating...")
    yes = generator(equations,available)

    print("Checking for complex numbers...")
    for e in yes:
        if "complexes" in e[1].lower() or "emptyset" in e[1].lower() or "conditionset" in e[1].lower():
            print("Detected, removing.")
            yes.remove(e)

    try:
        os.mkdir(directory)
    except FileExistsError:
        print("Build directory already exists.")
    try:
        os.mkdir(directory+"/cached")
    except FileExistsError:
        print("Cache directory already exists.")
    print("Saving bad.")
    np.save(directory+"/cached/bad",bad)
    print("Saving arr.")
    np.save(directory+"/cached/arr",arr)
    print("Saving permutated.")
    np.save(directory+"/cached/permutated",yes)
    print("Saving available.")
    np.save(directory+"/cached/available",available)
    print("Done.")

build(sys.argv[1])
