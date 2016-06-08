from Functions import *
from math import *
from Constants import *
from fractions import Fraction
from UIConstants import  *
import wx
import GraphicsFrame
import Logger
import ValueRememberer
import time

# Function that takes in a stringed expression and returns the final string value of that expression
# Line is just a simple value that states what line the thing is at
# Extra before text is just what is before the statement (so it looks nice)
# And after is the same (just cosmetic)
# print text is just a bool for printing text or not

def repeatExpressionTillDone (expression, startLine = -1, extraBeforeText="", extraAfterText="", printText=True) -> str:
    inputtedExpression = expression
    #print(expression)
    line = startLine
    repeats = 0
    try:
        float(inputtedExpression)
    except (ArithmeticError, TypeError, NameError, ValueError):
        if hasSymbols(inputtedExpression):
            checkBool = True
        else:
            checkBool = False
    else:
        checkBool = False
    #Main Loop
    while checkBool is True:
        #Runs once
        inputtedExpression = runOnceExpression(inputtedExpression, line, extraBeforeText=extraBeforeText, extraAfterText=extraAfterText)
        #Adds to line
        if line != -1:
            line += 0.1
        repeats += 1
        #To prevent recursion loops
        if repeats >= 100 and UIConstants.gRecursionStopper:
            break
        try:
            float(inputtedExpression)
        except (ArithmeticError, TypeError, NameError, ValueError):
            if hasSymbols(inputtedExpression):
                checkBool = True
            else:
                checkBool = False
        else:
            checkBool = False

    if printText:
        return inputtedExpression
    else:
        try:
            fl = float(inputtedExpression)
            return fl
        except (ValueError, AssertionError, ArithmeticError, TypeError, NameError):
            return nan

#Runs once doing a single expressional value (and all placeholders)
def runOnceExpression(expression, line = -1, extraBeforeText = "", extraAfterText = "") -> str:
    timeLine = time.clock()
    inputtedExpression = expression + " "
    #Replace pi or π
    inputtedExpression = inputtedExpression.replace("Pi", str(pi))
    inputtedExpression = inputtedExpression.replace("π", str(pi))
    inputtedExpression = inputtedExpression.replace("pB", "(" + str(pi) + ")")

    #Replace euler (e)
    inputtedExpression = inputtedExpression.replace("euler", str(e))
    inputtedExpression = inputtedExpression.replace("E", str(e))
    inputtedExpression = inputtedExpression.replace("eB", "(" + str(e) + ")")

    inputtedExpression = inputtedExpression.replace("M", str(ValueRememberer.getMemory()))

    #answer/memory replacement
    numberChecker = re.search(answerRegex, inputtedExpression)
    if numberChecker is not None:
        try:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(ValueRememberer.getAnswerN(int(numberChecker.group(2)))) + inputtedExpression[numberChecker.end():]
        except (ValueError, TypeError, NameError):
            pass

    #Brackets with a * infront
    #this will make sure that if any number or brackets is before another one it will add a * sign
    for i in range(len(inputtedExpression)):
        # Double checker to see if i for some reason is too large
        if i < len(inputtedExpression):
            # If its opening then set the starting point
            if inputtedExpression[i] == "(":
                if i - 1 >= 0:
                    try:
                        float(inputtedExpression[i-1])
                        inputtedExpression = inputtedExpression[:i] + "*" + inputtedExpression[i:]
                    except ValueError:
                        if inputtedExpression[i-1] == ")":
                            inputtedExpression = inputtedExpression[:i] + "*" + inputtedExpression[i:]
            elif inputtedExpression[i] == "√":
                try:
                    float(inputtedExpression[i-1])
                    inputtedExpression = inputtedExpression[:i] + "*" + inputtedExpression[i:]
                except ValueError:
                    break
    #Same as brackets but for some other keywords
    if "sqrt" in inputtedExpression:
        try:
            index = inputtedExpression.index("sqrt")
            if index > 0:
                float(inputtedExpression[index - 1])
                inputtedExpression = inputtedExpression[:index] + "*" + inputtedExpression[index:]
        except ValueError:
            pass
    elif "cubt" in inputtedExpression:
        try:
            index = inputtedExpression.index("cubt")
            if index > 0:
                float(inputtedExpression[index - 1])
                inputtedExpression = inputtedExpression[:index] + "*" + inputtedExpression[index:]
        except ValueError:
            pass
    elif "rt" in inputtedExpression:
        try:
            index = inputtedExpression.index("rt")
            if index > 0:
                float(inputtedExpression[index - 1])
                inputtedExpression = inputtedExpression[:index] + "*" + inputtedExpression[index:]
        except ValueError:
            pass

    #Replace placeholders
    #Percentage checking - Search for all percentages with a variable amount of white spaces on either side
    numberChecker = re.search(numberRegex + percentageRegex, inputtedExpression)
    # If search had results
    if numberChecker is not None:
        # Set expression to equal to everything before then the value then everything after
        inputtedExpression = inputtedExpression[:numberChecker.start()] + str(perS(numberChecker)) + inputtedExpression[numberChecker.end():]
    else:
        #Factorial
        numberChecker = re.search(numberRegex + factorialRegex, inputtedExpression)
        # If search has results
        if numberChecker is not None:
            # Set expression to equal to everything before then the value then everything after
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(facS(numberChecker)) + inputtedExpression[numberChecker.end():]

    if numberChecker is not None:
        return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression,
                            extraAfterText=extraAfterText, timeV=timeLine)
    #Functions
    #Int functions
    numberChecker = re.search(roundingIntRegex, inputtedExpression)
    if numberChecker is not None:
        inputtedExpression = inputtedExpression[:numberChecker.start()] + str(intFuncS(numberChecker.group(1) + repeatExpressionTillDone(numberChecker.group(2), startLine=line+0.1))) + inputtedExpression[numberChecker.end():]
    else:
        #Rounding function
        numberChecker = re.search(roundRegex, inputtedExpression)
        if numberChecker is not None:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(roundS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line+0.1) + ", " + repeatExpressionTillDone(numberChecker.group(3),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
        else:
            #Root functions
            numberChecker = re.search(multipleRootRegex, inputtedExpression)
            if numberChecker is not None:
                inputtedExpression = inputtedExpression[:numberChecker.start()] + str(rootFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2), startLine=line) + ")")) + inputtedExpression[numberChecker.end():]
            else:
                #Single root function - root(81, 2) = 9
                numberChecker = re.search(singleRootRegex, inputtedExpression)
                if numberChecker is not None:
                    inputtedExpression = inputtedExpression[:numberChecker.start()] + str(singleRootS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line+0.1) + ", " + repeatExpressionTillDone(numberChecker.group(3),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
                if numberChecker is not None:
                    return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression,
                                        extraAfterText=extraAfterText, timeV=timeLine)

    #Random functions
    numberChecker = re.search(randomRegex, inputtedExpression)
    if numberChecker is not None:
        #Small rand (0-1)
        if numberChecker.group(8) is not None:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(randomNonBracketFuncS()) + inputtedExpression[numberChecker.end():]
        #Large rand (0-100)
        elif numberChecker.group(9) is not None:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(random2NonBracketFuncS()) + inputtedExpression[numberChecker.end():]
        #Random Int (0-100)
        elif numberChecker.group(7) is not None:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(randomIntNonBracketFuncS()) + inputtedExpression[numberChecker.end():]
        elif numberChecker.group(4) is not None:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(randomIntFuncS(numberChecker.group(4) + "(" + repeatExpressionTillDone(numberChecker.group(5),startLine=line+0.1) + ", " + repeatExpressionTillDone(numberChecker.group(6),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
        else:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(randomFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line+0.1) + ", " + repeatExpressionTillDone(numberChecker.group(3),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
            return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression, extraAfterText=extraAfterText, timeV=timeLine)

    if numberChecker is not None:
        return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression,
                                extraAfterText=extraAfterText, timeV=timeLine)
    #Trig Functions
    #Sin, Cos, Tan
    numberChecker = re.search(trigRegex, inputtedExpression)
    if numberChecker is not None:
        #Run function
        if numberChecker.group(1) == "sin":
            inputtedExpression = inputtedExpression[:numberChecker.start()] + sinFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2), startLine=line+0.1) + ")")+ inputtedExpression[numberChecker.end():]
            #Sine
        elif numberChecker.group(1) == "cos":
            inputtedExpression = inputtedExpression[:numberChecker.start()] + cosFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2), startLine=line+0.1) + ")")+ inputtedExpression[numberChecker.end():]
            #Cos
        elif numberChecker.group(1) == "tan":
            inputtedExpression = inputtedExpression[:numberChecker.start()] + tanFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2), startLine=line+0.1) + ")")+ inputtedExpression[numberChecker.end():]
            #Tan
        else:
            #Cosec, Sec, Cot
            # Run function
            if numberChecker.group(1) == "cosec":
                inputtedExpression = inputtedExpression[:numberChecker.start()] + cosecFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                # Cosec
            elif numberChecker.group(1) == "sec":
                inputtedExpression = inputtedExpression[:numberChecker.start()] + secFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                # Sec
            elif numberChecker.group(1) == "cot":
                inputtedExpression = inputtedExpression[:numberChecker.start()] + cotFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                # Cot
            else:
                #Inverse Sine, Cos, Tan
                # Run function
                if numberChecker.group(1) == "asin":
                    inputtedExpression = inputtedExpression[:numberChecker.start()] + asinFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                    # Asin
                elif numberChecker.group(1) == "acos":
                    inputtedExpression = inputtedExpression[:numberChecker.start()] + acosFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                    # Acos
                elif numberChecker.group(1) == "atan":
                    inputtedExpression = inputtedExpression[:numberChecker.start()] + atanFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                    # Atan
                else:
                    # Inverse Cosec, Sec, Cot
                    # Run function
                    if numberChecker.group(1) == "acosec":
                        inputtedExpression = inputtedExpression[:numberChecker.start()] + acosecFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                        # Acosec
                    elif numberChecker.group(1) == "asec":
                        inputtedExpression = inputtedExpression[:numberChecker.start()] + asecFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2), startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                        # Asec
                    elif numberChecker.group(1) == "acot":
                        inputtedExpression = inputtedExpression[:numberChecker.start()] + acotFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")") + inputtedExpression[numberChecker.end():]
                        # Acot
    if numberChecker is not None:
        return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression,
                                        extraAfterText=extraAfterText, timeV=timeLine)

    #Base Functions
    numberChecker = re.search(prebaseRegex, inputtedExpression)
    if numberChecker is not None:
        #Base Mode
        if numberChecker.group(1) == "bin":
            #Binary
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(binFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
        elif numberChecker.group(1) == "oct":
            #Octal
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(octFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
        elif numberChecker.group(1) == "hex":
            #Hexadecimal
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(hexFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
    else:
        numberChecker = re.search(baseRegex, inputtedExpression)
        if numberChecker is not None:
            #Base X
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(baseFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line+0.1) + "," + repeatExpressionTillDone(numberChecker.group(3),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]

    if numberChecker is not None:
        return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression,
                            extraAfterText=extraAfterText, timeV=timeLine)

    #Word format of shortcuts
    numberChecker = re.search(modRegex, inputtedExpression)
    if numberChecker is not None:
            #Mod mode
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(modFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line+0.1) + "," + repeatExpressionTillDone(numberChecker.group(3) ,startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]
    else :
        numberChecker = re.search(intRegex, inputtedExpression)
        if numberChecker is not None:
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(intFormatFuncS(numberChecker.group(1) + "(" + repeatExpressionTillDone(numberChecker.group(2),startLine=line + 0.1) + ")")) + inputtedExpression[numberChecker.end():]

    if numberChecker is not None:
        return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression,
                            extraAfterText=extraAfterText, timeV=timeLine)
    # Bracket loop
    #If brackets exist in expression
    if "(" in inputtedExpression or ")" in inputtedExpression:
        #If number + brackets exist then add a * next to number and bracket

        #Simple counters to represent location of brackets
        bracketStart = -1
        bracketEnd = -1
        #Goes through all the string (range of length of string)
        for i in range(len(inputtedExpression)):
            #Double checker to see if i for some reason is too large
            if i < len(inputtedExpression):
                #If its opening then set the starting point
                if inputtedExpression[i] == "(":
                    bracketStart = i
                #Else if its closing bracket set the ending point and then break after ending
                elif inputtedExpression[i] == ")":
                    bracketEnd = i
                    break
        """
                    MAIN BRACKET CODE
                    This is simple:
                    Sets new Expression to equal an 'runexpression' of everything in the bracket
                    First it sets it to everything before the start of the brackets then add the expression of everything in the brackets (from the start to the end non-inclusive) then the ending of the brackets
        """
        if bracketEnd > -1 and bracketStart > -1:
            newExpression = repeatExpressionTillDone(inputtedExpression[bracketStart+1:bracketEnd], startLine= line, extraAfterText= inputtedExpression[bracketEnd:], extraBeforeText=inputtedExpression[:bracketStart+1])
            #To not Logger.log twice
            line = -1
            inputtedExpression = inputtedExpression[:bracketStart] + newExpression + inputtedExpression[bracketEnd+1:]
        else:
            Logger.logError("SYNTAX ERROR: Brackets not in right format")
            return ""
    #If all brackets are taken care of then do rest of checking
    else:
        #Power checking - Search for all powers with a variable amount of white spaces on either side
        numberChecker = re.search(numberRegex + powerRegex + numberRegex, inputtedExpression)
        #If search had results
        if numberChecker is not None:
            # Set expression to equal to everything before then the value then everything after
            inputtedExpression = inputtedExpression[:numberChecker.start()] + str(powerNS(numberChecker)) + inputtedExpression[numberChecker.end():]
        #This format is to make sure it handles all powers before doing anything else
        else:
            #Divide/Sub/Mod checker - Search for all * or / or % with a variable amount of white spaces on either side
            numberChecker = re.search(numberRegex + modDivideTimesRegex + numberRegex, inputtedExpression)
            #If search had results
            if numberChecker is not None:
                # Set expression to equal to everything before then the value then everything after
                inputtedExpression = inputtedExpression[:numberChecker.start()] + str(divideTimesModS(numberChecker)) + inputtedExpression[numberChecker.end():]
            else:
                #Add/Sub checker - Search for all + or - with a variable amount of white spaces on either side
                #i.e. If its like -2 + 2 then it the addSubS will run plus else it will run minus if its -2 - 2
                numberChecker = re.search(numberRegex + addMinusRegex + numberRegex, inputtedExpression)
                if numberChecker is not None:
                    # Set expression to equal to everything before then the value then everything after
                    inputtedExpression = inputtedExpression[:numberChecker.start()] + str(addSubS(numberChecker)) + inputtedExpression[numberChecker.end():]
    return returnValues(line=line, extraBeforeText=extraBeforeText, expression=inputtedExpression, extraAfterText=extraAfterText, timeV=timeLine)

#Since it was being used in multiple places this makes it easier to make changes
def returnValues (line, extraBeforeText, expression, extraAfterText, timeV):
    if line > -1:
        Logger.logL(log=extraBeforeText + expression + extraAfterText, line=float(line), time=time.clock()-timeV)
    return expression

#Iterator for a start stop with a floating point step (decimal step)
def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

def processTAndR(text) ->str:
    # For x to y time variable
    if "T" in str(text):
        timeR = re.search(timeRegex, text)
        if timeR is not None:
            text = re.sub(timeRegex, "", text)
            originalT = text
            newText = ""
            for i in drange(float(timeR.group(1)), float(timeR.group(4)) + 0.1, 1):
                newText += (("& " if i != float(timeR.group(1)) else "") + originalT.replace("T", str(i)))
            text = newText

    # For x, y, z etc repeat variable
    if "R" in str(text):
        repeatR = re.search(repeatRegexAll, text)
        if repeatR is not None:
            text = re.sub(repeatRegexAll, "", text)
            originalT = text
            newText = ""
            repeatIter = re.finditer(repeatRegexIter, repeatR.group(1))
            first = True
            for repeatI in repeatIter:
                newText += (("& " if not first else "") + originalT.replace("R", str(repeatI.group(1))))
                first = False
            text = newText
    return text

#Process expression (main loop)
def processExpression(text):
    #For timelogging
    time1 = time.clock()
    Logger.clear()

    matcher = re.finditer(xyTimes, text)
    for match in matcher:
        text = text[:match.start()+(1 if match.start() > 0 else 0)] + " * " + text[match.end()-1:]

    expressions = str(text).replace("X", "x").replace("Y", "y").split("&")

    if "x" in text or "y" in text or "X" in text or "Y" in text:
        #Graphing mode ACTIVATED.  If x or y then graph
        #TypeOfF is for domain/range
        typeOfF = TypeOfF()
        lastExp = expressions[len(expressions)-1]
        # Default domain/range to make sure its not to big
        # Gets wiped if you set a domain/range
        typeOfF.addExpression(ExpressionF([-9999], ["<="], ["x"]))
        typeOfF.addExpression(ExpressionF([9999], [">="], ["x"]))
        typeOfF.addExpression(ExpressionF([-9999], ["<="], ["y"]))
        typeOfF.addExpression(ExpressionF([9999], [">="], ["y"]))

        #Checks if domain/range symbols exist
        if "[" in lastExp or "{" in lastExp :
            typeResult = re.search(startStopStepRegex, lastExp)
            #Domain
            if typeResult is not None:
                expressions[len(expressions)-1] = re.sub(startStopStepRegex, "", expressions[len(expressions)-1])
                try:
                    typeOfF = TypeOfF(start=float(typeResult.group(1)), end=float(typeResult.group(3)), step=float(typeResult.group(5)))
                except (ValueError, NameError, TypeError, ArithmeticError):
                    logError("ERROR: Couldn't convert the range ([ ]) variable.")
            #Range
            domainResultAll = re.finditer(xyRegex, lastExp)
            if domainResultAll is not None:
                typeOfF.expressions = []
                expressions[len(expressions) - 1] = re.sub(xyRegex, '', expressions[len(expressions) - 1])
                for domainResultIter in domainResultAll:
                    domainResult = re.finditer(xyRegexIter, domainResultIter.group(1))
                    expressionV = []
                    firstV = []
                    secondV = []
                    for result in domainResult:
                        expressionV.append(result.group(3))
                        firstV.append(result.group(1))
                        secondV.append(result.group(4))
                    typeOfF.addExpression(ExpressionF(firstV, expressionV, secondV))

        #Points and expressions
        data = []
        legends = []

        if "P<" in lastExp:
            pointResultAll = re.finditer(pointAllRegex, lastExp)
            if pointResultAll is not None:
                try:
                    expressions[len(expressions) - 1] = re.sub(pointAllRegex, '', expressions[len(expressions) - 1])
                    for pointResult in pointResultAll:
                        pointResultIter = re.finditer(pointRegexIter, pointResult.group(1))
                        for result in pointResultIter:
                            data.append([[(float(result.group(2)), float(result.group(4))), (float(result.group(6)), float(result.group(8)))]])
                            legends.append("".join(result.group(1)))
                except (ValueError, NameError, TypeError):
                    pass

        #For dynamic graph range
        minX = 0
        maxX = 0
        minY = 0
        maxY = 0
        #Loop through expressions
        coloursChosen = []
        repeatText = processTAndR("&".join(expressions))
        expressions = [x.lstrip(" ") for x in repeatText.split("&")]
        legends.extend(expressions)
        for q in range(len(expressions)):
            if "C<" in expressions[q]:
                colourResult = re.search(colourSetterRegex, expressions[q])
                if colourResult is not None:
                    expressions[q] = re.sub(colourSetterRegex, "", expressions[q])
                    if colourResult.group(1).upper() in GraphicsFrame.colours:
                        coloursChosen.append(colourResult.group(1))
            #Local data points
            dataQ = []
            #For index navigation
            currentIndex = 0
            inputtedExpression = expressions[q]
            #MAIN LOOP
            for i in drange(typeOfF.start, typeOfF.end, typeOfF.step):
                #X loop
                if re.search(xEqualsRegex, inputtedExpression):
                    newText = re.sub(xEqualsRegex, "", inputtedExpression).replace("y", str(round(i, 4)))
                    val = float(repeatExpressionTillDone(newText, printText=False))
                    #Nan means an error occured which means we most likely encountered an asymptote
                    if math.isnan(val) is False:
                        stop = False
                        val = round(val, 4)
                        for expressionTest in typeOfF.expressions:
                            if performCalculation(expressionTest, valueX=val, valueY=i) is False:
                                stop = True
                                if len(dataQ) > currentIndex:
                                    currentIndex += 1
                        if stop is False:
                            if maxX < val:
                                maxX = val
                            elif minX > val:
                                minX = val

                            if maxY < i:
                                maxY = i
                            elif minY > i:
                                minY = i

                            if len(dataQ) <= currentIndex:
                                dataQ.append([(val, (round(i, 4)))])
                            else:
                                dataQ[currentIndex].append((val, (round(i, 4))))
                    elif len(dataQ) > currentIndex:
                        currentIndex+=1
                #Y loop
                elif re.search(yEqualsRegex, inputtedExpression):
                    newText = re.sub(yEqualsRegex, "", inputtedExpression).replace("x", str(round(i, 4)))
                    val = float(repeatExpressionTillDone(newText, printText=False))
                    #Nan means an error occured which means we most likely encountered an asymptote
                    if math.isnan(val) is False:
                        stop = False
                        val = round(val, 4)
                        for expressionTest in typeOfF.expressions:
                            if performCalculation(expressionTest, valueX=i, valueY=val) is False:
                                stop = True
                                if len(dataQ) > currentIndex:
                                    currentIndex += 1
                        if stop is False:
                            if maxY < val:
                                maxY = val
                            elif minY > val:
                                minY = val

                            if maxX < i:
                                maxX = i
                            elif minX > i:
                                minX = i

                            if len(dataQ) <= currentIndex:
                                dataQ.append([(round(i, 4), val)])
                            else:
                                dataQ[currentIndex].append((round(i, 4), val))
                    elif len(dataQ) > currentIndex:
                        currentIndex += 1
                else:
                    #If here then graph not in right format
                    Logger.logError("ERROR: All expressions need to contain x = or X = and/or y = or Y =.")
                    Logger._logs = []
                    Logger._lines = []
                    Logger._times = []
                    Logger.logL("FINISHED GRAPH" + text, -1, time.clock()-time1)
                    Logger.printLog()
                    return
            data.append(dataQ)
        #Produce graph
        if len(coloursChosen) == 0:
            coloursChosen = None
        graphics = GraphicsFrame.GraphicsFrame(None, data=data, x=(minX*1.1, maxX*1.1), y=(minY*1.1, maxY*1.1), expression=text, start_colours=coloursChosen, legends=legends)
        graphics.Show()
        Logger.clear()
        Logger.logL("FINISHED GRAPH: " + text, -1, time.clock() - time1)
        Logger.printLog()
        #Exit
        return
    #Else if not in graph mode then just do normal
    repeatText = processTAndR("&".join(expressions))
    expressions = repeatText.split("&")
    for i in range(len(expressions)):
        #Local variables
        time2 = time.clock()
        inputtedExpression = expressions[i]
        original = inputtedExpression
        previous = ""
        line = -1
        #Log initial
        Logger.logL(log="\nExpression: " + inputtedExpression, line=-1, time=0)
        #MAIN LOOP
        while True:
            line += 1
            try:
                float(inputtedExpression)
                break
            except (ArithmeticError, TypeError, NameError, ValueError):
                if not hasSymbols(inputtedExpression):
                    break
            #Recursion stopper (Can't be disable)
            if previous == inputtedExpression:
                break
            else:
                previous = inputtedExpression
            inputtedExpression = runOnceExpression(inputtedExpression, line)
            #Recursion stopper (can be disabled)
            if line >= 100 and UIConstants.gRecursionStopper:
                break
        # Recursion stopper (can be disabled)
        if line < 100 or not UIConstants.gRecursionStopper:
            #Return answer
            if UIConstants.gFraction:
                try:
                    inputtedExpression = Fraction.from_float(float(inputtedExpression)).limit_denominator()
                except (ValueError, TypeError):
                    break
            elif inputtedExpression is Fraction:
                try:
                    inputtedExpression =  str(float(inputtedExpression))
                except ValueError:
                    inputtedExpression = repeatExpressionTillDone(inputtedExpression, printText=False)
            Logger.logL(log="ANSWER: " + original + " = " + str(inputtedExpression), line=float(-1), time=time.clock()-time2)
            ValueRememberer.addAnswer(inputtedExpression)
            ValueRememberer.setMemory(inputtedExpression)
        else:
            #Recurred to many times
            Logger.logError("Recurred to many times")
    #Print final
    Logger.logL(log="FINISHED: did all expressions", line=-1, time=time.clock()-time1)
    Logger.printLog()

#To prevent multiple instances
#Globals
_AppBuilt = None
_frame = None
_menu = None
#Starts the app the globals are to make sure multiple instances don't exist
def StartApp():
    global _AppBuilt, _frame, _menu
    if _frame is not None:
        _frame.onExit(None)
        _frame = None
    if _AppBuilt is not None:
        _AppBuilt.Destroy()
        _AppBuilt = None
    _AppBuilt = wx.App()
    _frame = GraphicsFrame.ProgramFrame(None, processExpression)
    _frame.Show()
    _menu = GraphicsFrame.CalculatorMenu(_frame)
    _AppBuilt.MainLoop()

#Only main command in whole thing.  This will start the program everything else is event based and function driven!!
StartApp()