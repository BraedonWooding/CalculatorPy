import math as m
import random
from Logger import *
import time
from Constants import *

#Handles power calculations - Binary
def powerNS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))
    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("^")

    #Splits the binary format into an array of [a,b] then performs the appropriate calculation of a**b
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

#Handles divide calculations - Binary
def divideS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("/")

    #Splits the binary format into an array of [a,b] then performs the appropriate calculation of a/b
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

#Handles add calculations - Binary
def addS(inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("+")

    #Splits the binary format into an array of [a,b] then performs the appropriate calculation of a+b
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

#Handles sub calculations - Binary
#Different doesn't turn into array just converts the groups - Probably from when I used to not split them up.
#Not bothered to change
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

#The handler to do either sub or add
def addSubS(string) -> float:
    if "+" in string.group(0):
        return addS(string)
    elif "-" in string.group(0):
        return subS(string)
    else:
        logError("Input Error")
        return m.nan

#The handler to do either divide times or modulo
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

#Handles times calculations - Binary
def timesS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("*")

    #Splits the binary format into an array of [a,b] then performs the appropriate calculation of a*b
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

#Handles modulo calculations - Binary
def modS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(0))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    splitS = stringRep.split("%")

    #Splits the binary format into an array of [a,b] then performs the appropriate calculation of a%b
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

#Handles percentage calculations - Binary
def perS (inputString) -> float:
    time1 = time.clock()
    stringRep = "".join(inputString.group(1))

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    #Just divides by 100 to convert from percentage to decimal
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

#Handles factorial calculations - Binary
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

#Handler for ceiling, floor or rounding
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

#Handles round calculations where it rounds a to b decimal places - Binary but in function format
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

#Handles flooring calculations - Unary in function format
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

#Handles ceiling calculations - Unary in function format
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

#Handles root calculations - Binary in function format
def singleRootS (inputString) -> float:
    inputString += " "
    time1 = time.clock()
    search = re.search(rootFuncRegex, inputString)
    # A lot of searching and regex to make sure in right format.
    # Not very costly since just an overall of 1 due to complex regex.
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

#Handler for either square root, rt.x or cubt
def rootFuncS (inputString) -> float:
    #Not going to be grouped
    if "sqrt" in inputString or "√" in inputString:
        return sqrtS(inputString)
    elif "rt" in inputString:
        return rtNS(inputString)
    elif "cubt" in inputString:
        return cubtS(inputString)
    else:
        logError("Root Format Error")
        return m.nan

#Handles sqrt calculations - Unary in function or pre-operator format
def sqrtS (inputString) -> float:
    time1 = time.clock()
    stringRep = inputString

    stringRep = stringRep.replace("(", "", 1)
    stringRep = stringRep.replace(")", "", 1)

    #Boolean for if 'sqrt' in stringRep
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

#Handles sub calculations - Unary in function format
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

#Handles random 0-1 calculations - No parameters
def randomNonBracketFuncS() -> float:
    time1 = time.clock()
    rdm = random.random()
    logL(log = "     Working out: random between 0 and 1 is " + rdm, time=time.clock()-time1)
    return rdm

#Handles random 0-100 calculations - No Parameters
def random2NonBracketFuncS() -> float:
    time1 = time.clock()
    rdm = random.uniform(0, 100)
    logL(log="     Working out: random between 0 and 100 is " + rdm, time=time.clock()-time1)
    return rdm

#Handles random int 0-100 calculations - No Parameters
def randomIntNonBracketFuncS() -> float:
    rdm = random.randint(0, 100)
    logL(log="     Working out:  between 0 and 100 is " + rdm)
    return rdm

#Handles random int x-y calculations - Binary in function format
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

#Handles random x-y calculations - Binary in function format
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

#Handles rt.x calculations - Binary in rt.a(b) where it roots b by a
def rtNS (inputString) -> float:
    time1 = time.clock()
    stringRep = inputString
    stringRep = stringRep.replace(" ", "")

    #Similar to root funtion it just groups things
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
        logError("The number wasn't in the format for rooting.")

#Handles int calculations - Unary
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

#Handles atan calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles acos calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles asin calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles tan calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles cos calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles sin calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
def sinFuncS(inputString) -> str:
    time1 = time.clock()
    result = re.search(sinRegex, inputString)
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

#Handles acot calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles asec calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles acosec calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles cot calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles sec calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles cosec calculations - Unary
#If radians mode is enabled then converts the number to degrees else it is in radians
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

#Handles binary calculations - Unary
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

#Handles hexadecimal calculations - Unary
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

#Handles octal calculations - Unary
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

#Handles base of n (a) where a of base n is convert to base 10 calculations - Unary
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

#Handles modulo calculations - Binary in function format
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