import math

gRadians = False
gTime = True
gRecursionStopper = True
gCentre = False
gGrid = True
gHiRes = False
gLegend = True
gFraction = False

#A [] or {} expressional. Aka a range or domain
class TypeOfF:
    def __init__(self, start = -100, end = 100, step = 0.25):
        self.start = start
        self.end = end
        self.step = step
        self.expressions = []

    def addExpression(self, expression):
        self.expressions.append(expression)

#Returns if the value is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Expressional aka y < 3.  For domain/range
class ExpressionF:
    def __init__(self, firstVs, expressionals, secondVs):
        self.firstVs = []
        self.secondVs = []
        self.expressionals = []
        for i in range(min(len(firstVs), len(expressionals), len(secondVs))):
            firstV = firstVs[i]
            secondV = secondVs[i]
            expressional = expressionals[i]

            if type(firstV) is str:
                if "x" in firstV or "X" in firstV:
                    self.firstVs.append(math.inf)
                elif "y" in firstV or "Y" in firstV:
                    self.firstVs.append(math.nan)
                elif is_number(firstV):
                    self.firstVs.append(float(firstV))
                else:
                    self.firstVs.append(0)
            else:
                self.firstVs.append(firstV)

            if type(secondV) is str:
                if "x" in secondV or "X" in secondV:
                    self.secondVs.append(math.inf)
                elif "y" in secondV or "Y" in secondV:
                    self.secondVs.append(math.nan)
                elif is_number(secondV):
                    self.secondVs.append(float(secondV))
                else:
                    self.secondVs.append(0)
            else:
                self.secondVs.append(secondV)

            self.expressionals.append(expressional)

    def __repr__(self):
        return " or ".join([str(self.firstVs[x]) + self.expressionals[x] + str(self.secondVs[x]) for x in range(min(len(self.firstVs), len(self.expressionals), len(self.secondVs)))])

#Performs the calculation to see if the values are fitting into the domain
def performCalculation(testing, valueX, valueY) -> bool:
    expression = ExpressionF(firstVs=testing.firstVs, secondVs=testing.secondVs, expressionals=testing.expressionals)
    returnValue = False
    for i in range(min(len(expression.firstVs), len(expression.expressionals), len(expression.secondVs))):
        expressional = expression.expressionals[i]
        firstV = expression.firstVs[i]
        secondV = expression.secondVs[i]

        try:
            #Asserts then if value is infinity/nan it will make it x or y respectively
            assert isinstance(expression, ExpressionF)
            if type(firstV) is float:
                if math.isinf(firstV):
                    firstV = valueX
                if math.isnan(firstV):
                    firstV = valueY
            if type(secondV) is float:
                if math.isinf(secondV):
                    secondV = valueX
                if math.isnan(secondV):
                    secondV = valueY

            #Actual checking of values
            #A bunch of if statements since python doesn't have switch for some reason
            if expressional == "<=":
                returnValue =firstV <= secondV
            elif expressional == ">=":
                returnValue =firstV >= secondV
            elif expressional == "==":
                returnValue =firstV == secondV
            elif expressional == "!=":
                returnValue =firstV != secondV
            elif expressional == "<":
                returnValue =firstV < secondV
            elif expressional == ">":
                returnValue =firstV > secondV
            else:
                returnValue =False

            if returnValue:
                return returnValue
        except (AssertionError, ValueError, TypeError):
            returnValue =False
    return returnValue