import GraphicsFrame
import UIConstants

_logs = []
_lines = []
_errors = []
_times = []

#Func to clear
def clear():
    global _errors, _lines, _logs, _times
    _logs = []
    _lines = []
    _errors = []
    _times = []

#Func to queue an error
def logError(error):
    """
    ####Sub Log Error (error)
    BEGIN SUB
    add error to errors
    END SUB
    """
    global _errors
    _errors.append(error)

#'logs' a log and line and a time
def logL(log, line=-1, time=0.0):
    """
    ####Sub Log (log, line)
    BEGIN SUB
    add log to logs
    add line to lines
    END SUB
    """
    global _logs, _lines, _times
    _logs.append(log)
    _lines.append(line)
    _times.append(time)

#Formats then prints the logs/errors
def printLog():
    global _lines, _logs, _errors, _times
    #If no errors are logged
    if len(_errors) == 0 or True:
        #Loop through lines and remove any duplicates
        for i in range(len(_lines)):
            if i < len(_lines):
                line = _lines[i]
                if line in (_lines[:i] + _lines[i+1:]) and line > -1:
                    _lines = _lines[:i] + _lines[i + 1:]
                    _logs = _logs[:i] + _logs[i + 1:]
                    _times = _times[:i] + _times[i + 1:]
                    line-=1
        #Loop through and print logs
        for i in range(len(_logs)):
            if "Working out" in _logs[i] or "ANSWER" in _logs[i] or "Expression" in _logs[i] or "FINISHED" in _logs[i]:
                GraphicsFrame.selfV.logText(_logs[i] + ((" (in " + '{:0.4f}'.format(_times[i]*1000) + " milliseconds)") if (len(_times) > i and _times[i] != 0 and UIConstants.gTime) else ""))
            else:
                GraphicsFrame.selfV.logText("  Line " + str(round(_lines[i], 2)) + ": " + _logs[i] + ((" (in " + '{:0.4f}'.format(_times[i]*1000) + " milliseconds)") if (len(_times) > i and _times[i] != 0 and UIConstants.gTime) else ""))
    #Print errors
    else:
        for error in _errors:
            GraphicsFrame.selfV.logText("\n" + error)