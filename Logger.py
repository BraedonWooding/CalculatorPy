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
    _errors.append(error)

#'logs' a log and line and a time
def logL(log, line=-1, time=0.0):
    _logs.append(log)
    _lines.append(line)
    _times.append(time)

#Formats then prints the logs/errors
def printLog():
    global _lines, _logs, _times
    #If no errors are logged
    if len(_errors) == 0 or True:
        #Loop through lines and remove any duplicates
        for i, line in enumerate(_lines):
            if i < len(_lines):
                if line in (_lines[:i] + _lines[i+1:]) and line > -1:
                    _lines = _lines[:i] + _lines[i + 1:]
                    _logs = _logs[:i] + _logs[i + 1:]
                    _times = _times[:i] + _times[i + 1:]
                    line-=1
        #Loop through and print logs
        for i, log in enumerate(_logs):
            if "Working out" in log or "ANSWER" in log or "Expression" in log or "FINISHED" in log:
                GraphicsFrame.selfV.logText(log + ((" (in " + '{:0.4f}'.format(_times[i]*1000) + " milliseconds)") if (len(_times) > i and _times[i] != 0 and UIConstants.gTime) else ""))
            else:
                GraphicsFrame.selfV.logText("  Line " + str(round(_lines[i], 2)) + ": " + log + ((" (in " + '{:0.4f}'.format(_times[i]*1000) + " milliseconds)") if (len(_times) > i and _times[i] != 0 and UIConstants.gTime) else ""))
    #Print errors
    else:
        for error in _errors:
            GraphicsFrame.selfV.logText("\n" + error)