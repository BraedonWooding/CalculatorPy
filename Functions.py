import math as m
import random
from Logger import *
import time
from Constants import *

def powerNS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))
    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("^")

    if len(splitS) >= 2:
        try:
            fl = pow(float(splitS[0]), float(splitS[1]))
            logL(log="     Working out: " + "^".join([inputString.group(1), inputString.group(5)]) + " = " + str(fl), time=time.clock()-time1)
            if fl % 1 == 0:
                return int(fl)
            else:
                return fl
        except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
            logError("Power Error")
            return m.nan
    else:
        logError("Power Error")
        return m.nan

def divideS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("/")

    if len(splitS) >= 2:
        try:
            fl = float(splitS[0]) / float(splitS[1])
            logL(log="     Working out: " + "/".join([inputString.group(1), inputString.group(5)]) + " = " + str(fl), time=time.clock()-time1)
            if fl % 1 == 0:
                return int(fl)
            else:
                return fl
        except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
            logError("Divide Error")
            return m.nan
    else:
        logError("Divide Error")
        return m.nan

def addS(inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("+")

    if len(splitS) >= 2:
        try:
            fl = float(splitS[0]) + float(splitS[1])
            logL(log="     Working out: " + "+".join([inputString.group(1), inputString.group(5)]) + " = " + str(fl), time=time.clock()-time1)
            if fl % 1 == 0:
                return int(fl)
            else:
                return fl
        except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
            logError("Add Error")
            return m.nan
    else:
        logError("Add Error")
        return m.nan

def subS(inputString) -> float:
    time1 = time.clock()
    try:
        fl = float(inputString.group(1)) - float(inputString.group(5))
        logL(log="     Working out: " + "-".join([inputString.group(1), inputString.group(5)]) + " = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Sub Error")
        return m.nan

def addSubS(string) -> float:
    if "+" in string.group(0):
        return addS(string)
    elif "-" in string.group(0):
        return subS(string)
    else:
        logError("Input Error")
        return m.nan

def divideTimesModS (string) -> float:
    if "*" in string.group(0):
        return timesS(string)
    elif "/" in string.group(0):
        return divideS(string)
    elif "%" in string.group(0):
        return modS(string)
    else:
        logError("Input Error")
        return m.nan

def timesS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("*")

    if len(splitS) >= 2:
        try:
            fl = float(splitS[0]) * float(splitS[1])
            logL(log="     Working out: " + "*".join([inputString.group(1), inputString.group(5)]) + " = " + str(fl), time=time.clock()-time1)
            if fl % 1 == 0:
                return int(fl)
            else:
                return fl
        except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
            logError("Times Error")
            return m.nan
    else:
        logError("Times Error")
        return m.nan

def modS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("%")

    if len(splitS) >= 2:
        try:
            fl = float(splitS[0]) % float(splitS[1])
            logL(log="     Working out: " + "%".join([inputString.group(1), inputString.group(5)]) + " = " + str(fl), time=time.clock()-time1)
            if fl % 1 == 0:
                return int(fl)
            else:
                return fl
        except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
            logError("Modulo Error")
            return m.nan
    else:
        logError("Modulo Error")
        return m.nan

def perS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(1))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    try:
        fl = float(stringRep) / 100
        logL(log="     Working out: " + inputString.group(1) + "% = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Percentage Error")
        return m.nan

def facS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(1))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    try:
        fl = float(m.factorial(float(stringRep)))
        logL(log="     Working out: " + inputString.group(1) + "! = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        if float(inputString.group(1)) % 1 != 0:
            logError("Tried to factorial a decimal number")
        else:
            logError("Factorial Error")
        return m.nan

def intFuncS (inputString) -> float:
    if "ceil" in inputString:
        return ceilS(inputString)
    elif "floor" in inputString:
        return floorS(inputString)
    elif "round" in inputString:
        return roundS(inputString)
    else:
        logError("Input Error")
        return m.nan

def roundS (inputString) -> float:
    time1 = time.clock()
    search = re.search(roundFuncRegex, inputString)
    if search is None:
        logError("Rounding not in right format, format is: round(numberToRound, nDecimalPlaces)")
        return 0
    try:
        fl = round(float(search.group(1)), int(search.group(2)))
        logL(log="     Working out: rounding " + search.group(1) + " to "  + search.group(2) + " d.p. = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except AssertionError:# (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Rounding not in right format, format is: round(numberToRound, nDecimalPlaces)")
        return m.nan

def floorS (inputString) -> float:
    time1 = time.clock()
    stringRep = inputString

    stringRep = stringRep.replace("(", "")
    stringRep = stringRep.replace(")", "")
    stringRep = stringRep.replace(",", "")
    stringRep = stringRep.replace("floor", "")

    try:
        fl = m.floor(float(stringRep))
        logL(log="     Working out: floor(" + stringRep + ") = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except(TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Floor Error")
        return m.nan

def ceilS (inputString) -> float:
    time1 = time.clock()
    stringRep = inputString

    stringRep = stringRep.replace("(", "")
    stringRep = stringRep.replace(")", "")
    stringRep = stringRep.replace(",", "")
    stringRep = stringRep.replace("ceil", "")

    try:
        fl = m.ceil(float(stringRep))
        logL(log="     Working out: ceil(" + stringRep + ") = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        return m.nan

def singleRootS (inputString) -> float:
    inputString += " "
    time1 = time.clock()
    search = re.search(rootFuncRegex, inputString)
    if search is None:
        logError("Root not in right format: Format is root(numberToRoot, nthRoot)")
        print(inputString)
        return m.nan
    try:
        power = 1.0/float(search.group(3))
        fl = pow(float(search.group(1)), power)
        logL(log="     Working out: rooting " + search.group(1) + " by " + search.group(3) + " = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        return m.nan

def rootFuncS (inputString) -> float:
    #Not going to be grouped
    if "sqrt" in inputString or "√" in inputString:
        return sqrtS(inputString)
    elif "rt" in inputString:
        return rtNS(inputString)
    elif "cubt" in inputString:
        return cubtS(inputString)

def sqrtS (inputString) -> float:
    time1 = time.clock()
    stringRep = inputString

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    sqrtB = ("sqrt" in stringRep)
    stringRep = stringRep.replace("sqrt", "")
    stringRep = stringRep.replace("√", "")

    try:
        if float(stringRep) >= 0:
            fl = m.sqrt(float(stringRep))
            if sqrtB:
                logL(log="     Working out: sqrt(" + stringRep + ") = " + str(fl), time=time.clock()-time1)
            else:
                logL(log="     Working out: √(" + stringRep + ") = " + str(fl), time=time.clock()-time1)
            if fl % 1 == 0:
                return int(fl)
            else:
                return fl
        else:
            logError("Root negative")
            return m.nan
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Square Root Format Error")
        return m.nan

def cubtS (inputString) -> float:
    time1 = time.clock()
    stringRep = inputString

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    stringRep = stringRep.replace("cubt", "")

    try:
        fl = pow(float(stringRep), 1/3)
        logL(log="     Working out: cubt(" + stringRep + ") = " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Cubt Format Error")
        return m.nan

def randomNonBracketFuncS() -> float:
    time1 = time.clock()
    rdm = random.random()
    logL(log = "     Working out: random between 0 and 1 is " + rdm, time=time.clock()-time1)
    return rdm

def random2NonBracketFuncS() -> float:
    time1 = time.clock()
    rdm = random.uniform(0, 100)
    logL(log="     Working out: random between 0 and 100 is " + rdm, time=time.clock()-time1)
    return rdm

def randomIntNonBracketFuncS() -> float:
    rdm = random.randint(0, 100)
    logL(log="     Working out:  between 0 and 100 is " + rdm)
    return rdm

def randomIntFuncS(inputString) -> float:
    time1 = time.clock()
    randomFunctions = re.search(randomIntFuncRegex, inputString)

    try:
        fl = random.randint(int(randomFunctions.group(2)), int(randomFunctions.group(3)))
        logL(log="     Working out: random between " + randomFunctions.group(2) + " and " + randomFunctions.group(
            3) + " is " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Random Format Error")
        return m.nan

def randomFuncS(inputString) -> float:
    time1 = time.clock()
    randomFunctions = re.search(randomFuncRegex, inputString)

    try:
        fl = random.uniform(float(randomFunctions.group(2)), float(randomFunctions.group(3)))
        logL(log="     Working out: random between " + randomFunctions.group(2) + " and " + randomFunctions.group(3) + " is " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Random Format Error")
        return m.nan

def rtNS (inputString) -> float:
    time1 = time.clock()
    stringRep = inputString
    stringRep = stringRep.replace(" ", "")

    numberSearch = re.search(rtFuncRegex, stringRep)
    if numberSearch is not None:
        power = 1/float(numberSearch.group(1))
        try:
            fl = pow(float(numberSearch.group(2)), power)
            logL(log="     Working out: " + numberSearch.group(1) + "th root" + "(" + numberSearch.group(2) + ") = " + str(fl), time=time.clock()-time1)
            if fl % 1 == 0:
                return int(fl)
            else:
                return fl
        except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
            logError("Your number wasn't in the format for rootin")
            return m.nan
    else:
        logError("Your number wasn't in the format for rooting.")

def intFormatFuncS(inputString) -> float:
    time1 = time.clock()
    intFunctions = re.search(intFuncRegex, inputString)
    try:
        fl = int(float(intFunctions.group(2)))
        logL(log="     Working out: integer format of " + intFunctions.group(2) + " equals " + str(fl), time=time.clock()-time1)
        return fl
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("int Format Error")
        return m.nan

def atanFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(atanRegex, inputString)
    try:
        fl = m.atan(float(result.group(2)))
        fl = m.degrees(fl) if not UIConstants.gRadians else fl
        logL(log="     Working out: atan(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("atan Format Error")
        return str(m.nan)

def acosFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(acosRegex, inputString)
    try:
        fl = m.acos(float(result.group(2)))
        fl = m.degrees(fl) if not UIConstants.gRadians else fl
        logL(log="     Working out: acos(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("acos Format Error")
        return str(m.nan)

def asinFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(asinRegex, inputString)
    try:
        fl = m.asin(float(result.group(2)))
        fl = m.degrees(fl) if not UIConstants.gRadians else fl
        logL(log="     Working out: asin(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("asin Format Error")
        return str(m.nan)

def tanFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(tanRegex, inputString)
    try:
        if UIConstants.gRadians is False:
            fl = m.tan(m.radians(float((result.group(2)))))
        else:
            fl = m.tan(float(result.group(2)))
        logL(log="     Working out: tan(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("tan Format Error")
        return str(m.nan)

def cosFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(cosRegex, inputString)
    try:
        if UIConstants.gRadians is False:
            fl = m.cos(m.radians(float(result.group(2))))
        else:
            fl = m.cos(float(result.group(2)))
        logL(log="     Working out: cos(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("cos Format Error")
        return str(m.nan)

def sinFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(sinRegex, inputString)
    #print(inputString)
    #print(result.groups())
    try:
        if UIConstants.gRadians is False:
            fl = m.sin(m.radians(float(result.group(2))))
        else:
            fl = m.sin(float(result.group(2)))
        logL(log="     Working out: sin(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("sin Format Error")
        return str(m.nan)

def acotFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(acotRegex, inputString)
    try:
        fl = 1/m.atan(float(result.group(2)))
        fl = m.degrees(fl) if not UIConstants.gRadians else fl
        logL(log="     Working out: acot(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("acot Format Error")
        return str(m.nan)

def asecFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(asecRegex, inputString)
    try:
        fl = 1/m.acos(float(result.group(2)))
        fl = m.degrees(fl) if not UIConstants.gRadians else fl
        logL(log="     Working out: asec(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("asec Format Error")
        return str(m.nan)

def acosecFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(acosecRegex, inputString)
    try:
        fl = 1/m.asin(float(result.group(2)))
        fl = m.degrees(fl) if not UIConstants.gRadians else fl
        logL(log="     Working out: acosec(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("acosec Format Error")
        return str(m.nan)

def cotFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(cotRegex, inputString)
    try:
        if UIConstants.gRadians is False:
            fl = 1.0/(m.tan(m.radians(float(result.group(2)))))
        else:
            fl = 1.0/(m.tan(float(result.group(2))))
        logL(log="     Working out: cot(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("cot Format Error")
        return str(m.nan)

def secFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(secRegex, inputString)
    try:
        if UIConstants.gRadians is False:
            fl = 1/m.cos(m.radians(float(result.group(2))))
        else:
            fl = 1/m.cos(float(result.group(2)))
        logL(log="     Working out: sec(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("sec Format Error")
        return str(m.nan)

def cosecFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(cosecRegex, inputString)
    try:
        if UIConstants.gRadians is False:
            fl = 1/m.sin(m.radians(float(result.group(2))))
        else:
            fl = 1/m.sin(float(result.group(2)))
        logL(log="     Working out: cosec(" + result.group(2) + ") = " + str(fl), time=time.clock()-time1)
        return str(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("cosec Format Error")
        return str(m.nan)

def binFuncS(inputString) -> float:
    time1 = time.clock()
    result = re.search(binRegex, inputString)
    try:
        fl = int(result.group(2), 2)
        logL(log="     Working out: binary of " + result.group(2) + " is " + str(fl), time=time.clock()-time1)
        return float(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Binary Format Error")
        return m.nan

def hexFuncS(inputString) -> float:
    time1 = time.clock()
    result = re.search(hexRegex, inputString)
    try:
        fl = int(result.group(2), 16)
        logL(log="     Working out: hexadecimal of " + result.group(2) + " is " + str(fl), time=time.clock()-time1)
        return float(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Hexadecimal Format Error")
        return m.nan

def octFuncS(inputString) -> float:
    time1 = time.clock()
    result = re.search(octRegex, inputString)
    try:
        fl = int(result.group(2), 8)
        logL(log="     Working out: octal of " + result.group(2) + " is " + str(fl), time=time.clock()-time1)
        return float(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Octal Format Error")
        return m.nan

def baseFuncS(inputString) -> float:
    time1 = time.clock()
    result = re.search(baseRegex, inputString)
    try:
        fl = int(result.group(2), int(result.group(3)))
        logL(log="     Working out: base " + result.group(3) + " of " + result.group(2) + " is " + str(fl), time=time.clock()-time1)
        return float(fl)
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Base formatting not right should be base(x, n) with x being a value of base n")
        return m.nan

def modFuncS(inputString) -> float:
    time1 = time.clock()
    modFunctions = re.search(modRegex, inputString)

    try:
        fl = float(modFunctions.group(2))%float(modFunctions.group(3))
        logL(log="     Working out: modulo (remainder) of " + modFunctions.group(2) + " and " + modFunctions.group(3) + " is " + str(fl), time=time.clock()-time1)
        if fl % 1 == 0:
            return int(fl)
        else:
            return fl
    except (TypeError, ArithmeticError, AssertionError, NameError, ValueError):
        logError("Modulo Error")
        return m.nan