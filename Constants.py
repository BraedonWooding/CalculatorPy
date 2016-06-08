import re

#Just all the regex constants below for easy changing and code maintenance

symbols = r'\*|\/|\(|\)|\-|\+|\^|\%|\π|\√\(*.\)|!'

wordedSymbols = r'Pi|euler|sqrt|cubt|rt|floor|ceil|round|sin|cos|tan|-sin|-cos|-tan|bin|base|log|per|rand|randInt|int|bin|hex|oct|base|mod|ans|M|pB|E|eB|P<'

numberRegex = r'(-?(\d*\.\d+|\d+))'

answerRegex = r'(ans\s*\((.*?)\))'

percentageRegex = r'\s*(\%)\s*\D'

factorialRegex = r'\s*(\!)\s*'

roundingIntRegex = r'(ceil|floor)\s*\((.*?)\)'

roundFuncRegex = r'\s*round\s*\((\d*\.\d+|\d+)\,\s*(\d*)\)\s*'

roundRegex = r'(round)\((.*?),\s*(.*?)\)\s'

multipleRootRegex = r'(sqrt|cubt|√|rt\.\d*)\s*\((.*?)\)'

singleRootRegex = r'(root)\s*\((.*?)\,\s*(.*?)\)'

rootFuncRegex = r'\s*root\s*\(' + numberRegex + r',\s*' + numberRegex + r'\)\s'

randomRegex = r'(rand)\s*\((.*?),\s*(.*?)\)|(randInt)\s*\((.*?),\s*(.*?)\)|(randInt)|(srand)|(rand)'

randomIntFuncRegex = r'(randInt)\s*\((.*?)\,\s*(.*?)\)'

randomFuncRegex = r'(rand)\s*\((.*?)\,\s*(.*?)\)'

timeRegex = r'T<s*(' + numberRegex + r')\s*,\s*(' + numberRegex + r')\s*>'

rtFuncRegex = r'rt\.(\d*?)\((.*?)\)'

intFuncRegex = r'(int)\((.*?)\)'

modRegex = r'(mod)\s*\((.*?)\,(.*?)\)'

xyTimes = numberRegex + r'\s*(x|y)\s*'

intRegex = r'(int)\((.*?)\)'

powerRegex = r'\s*(\^)\s*'

modDivideTimesRegex = r'\s*(/|\*|%)\s*'

addMinusRegex = r'\s*(\+|\-)\s*'

startStopStepRegex = r'\s*\[start:\s*' + numberRegex + r'\s*end:\s*' + numberRegex + r'\s*step:\s*' + numberRegex + r'\]'

colourSetterRegex = r'C<(.*?)>'

repeatRegexAll = r'R<(.*?)>'

repeatRegexIter = numberRegex + r',?'

pointAllRegex = r'P<(.*?)>'

pointRegexIter = r'(' + numberRegex + r'\s*,\s*' + numberRegex + r'\s*-\s*' + numberRegex + r'\s*,\s*' + numberRegex + r');?'

xEqualsRegex = r'x\s*='

yEqualsRegex = r'y\s*='

xyRegex = r'\{(.*?)\}'

xyRegexIter = r'\s*(x|y|-?(\d*\.\d+|\d+))\s*(<|>|<=|>=|==|!=)\s*(x|y|-?(\d*\.\d+|\d+)),?'

trigRegex = r'(sin|cos|tan|cosec|sec|cot|asin|asoc|atan|acosec|asec|acot)\s*\((.*?)\)\s'

prebaseRegex = r'\s*(bin|oct|hex)\s*\((.*?)\)\s'

baseRegex = r'(base)\s*\((.*?),\s*(.*?)\)\s'

binRegex = r'(bin)\s*\((.*?)\)\s'

hexRegex = r'(hex)\s*\((.*?)\)\s'

octRegex = r'(oct)\s*\((.*?)\)\s'

atanRegex = r'(atan)\((.*?)\)'

tanRegex = r'(tan)\((.*?)\)'

acosRegex = r'(acos)\((.*?)\)'

cosRegex = r'(cos)\((.*?)\)'

asinRegex = r'(asin)\((.*?)\)'

sinRegex = r'(sin)\((.*?)\)'

acotRegex = r'(acot)\((.*?)\)'

cotRegex = r'(cot)\((.*?)\)'

asecRegex = r'(asec)\((.*?)\)'

secRegex = r'(sec)\((.*?)\)'

acosecRegex = r'(acosec)\((.*?)\)'

cosecRegex = r'(cosec)\((.*?)\)'

"""
####Sub Check Expression (Expression) -> valid as Boolean
```
IF PATTERN symbols AND PATTERN '|' AND PATTERN wordedSymbols IN Expression:
	RETURN TRUE
ELSE:
	RETURN FALSE
ENDIF
```
"""
#Returns true if the expression has symbols
def hasSymbols (expression) -> bool:
    if re.search(symbols + r'|' + wordedSymbols, expression):
        return True
    else:
        return False