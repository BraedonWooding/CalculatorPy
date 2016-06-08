import Logger

_answers = []
_memory = 0

#Sets memory
def setMemory (number):
    global _memory
    _memory = number

#Adds answer
def addAnswer (answer):
    _answers.append(answer)

#Clear all
def clear():
    global _answers, _memory
    _answers = []
    _memory = 0

#Returns memory
def getMemory() -> float:
    return _memory

#Gets answer of n
def getAnswerN(n) -> float:
    tempIndex = len(_answers)-n
    if tempIndex >= 0:
        return _answers[tempIndex]
    else:
        Logger.logError("Accessed Answer that doesn't exist")
        return 0