import Logger

_answers = []
_memory = 0

"""
####Sub Add Memory (number)
BEGIN Sub
memory = number
END SUB
"""
#Sets memory
def setMemory (number):
    global _memory
    _memory = number
"""
####Sub Add Answer (answer)
BEGIN SUB
add answer to answers
END SUB
"""
#Adds answer
def addAnswer (answer):
    global  _answers
    _answers.append(answer)
"""
####Sub Clear()
BEGIN SUB
empty answers
memory = 0
END SUB
"""
#Clear all
def clear():
    global _answers, _memory
    _answers = []
    _memory = 0
"""
####Sub Get Memory() -> memory as Int
BEGIN SUB
return memory
END SUB
"""
#Returns memory
def getMemory() -> float:
    global _memory
    return _memory
"""
####Sub Get AnswerN(n) -> answer as Int
BEGIN SUB
tempIndex = length of answers minus n
IF tempIndex >= 0
	return answers[tempIndex]
ELSE
	return 0
ENDIF
END SUB
"""
#Gets answer of n
def getAnswerN(n) -> float:
    global _answers
    tempIndex = len(_answers)-n
    if tempIndex >= 0:
        return _answers[tempIndex]
    else:
        Logger.logError("Accessed Answer that doesn't exist")
        return 0