#   Problem: Create Simple Calculator
#   Description: The program computes the simple arithmetic expressions and finds the 
#       value of mathematical functions or factorial entered by the user. After the
#       user enters the mathematical expression, the program validates and evaluates 
#       the user entry with the regular expressions set in the Calculator class. The  
#       program then computes and stores the result inside the Calculator class 
#       according to the mathematical expression. 
#       In addition, the Calculator class stores the value of the memory cell that is
#       accessed through the memory commands (M+, M-, MC, and MR).
#   
#   Name: Mykhaylo Ignatyev
#   ID : 20359765
#   Status: 100% Complete
import math
import re

def main() :    
    entry = ""

    calc = Calculator()
    
    #print("This program is a calculator which computes simple mathematical")
    #print("expressions and functions.") 
    #print()
    #print("* For the information about legal syntax and supported functions write")
    #print("* \"help\" in the command line.")
    #print()
    #print("* To exit from the calculator, write \"quit\" in the command line.")
    #print()

    #calc.help()

    while entry != "quit" :
        entry = input("[x = %s]: " % calc.getX())

        if len(entry) != 0 and entry != "quit" :
            if entry == "help" :
                calc.help()
            else :
                try : 
                    calc.compute(entry)
                except ZeroDivisionError as exception :
                    print()
                    print(str(exception))
                    print()
                except ValueError as exception :
                    print()
                    print(str(exception))
                    print()
                except OSError as exception : 
                    print()
                    print(str(exception))
                    print()

## A calculator which computes simple mathematical expressions and functions
#    
class Calculator :
    # Regular expression for matching arithmetic operations. First operand  
    # (\d+|[xXe]|[pP][iI]) (operand1) could be the number or x (previous result), or e,   
    # or Pi, second group ([-+/*^%]) (operator) is the operator, the third 
    # (\d+|[xXe]|[pP][iI]) (operand2) - the number, or x, or e, or Pi.
    REGULAR_MATH = r"(?P<operand1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))\s*" + \
                    r"(?P<operator>[-+/*^%])\s*" + \
                    r"(?P<operand2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))"   

    # Regular expression for matching functions. First group (func) is the function name  
    # (function name (\w+)), second group (\d+|[xXe]|[pP][iI]) (arg1) - the first  
    # argument, the third group (\d+|[xXe]|[pP][iI]) (arg2) – the second argument.
    REGULAR_FUNC = r"(?P<func>\w+)\s*\(\s*(?P<arg1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))" + \
                    r"\s*[,]?\s*(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\)"
    
    # Regular expression for matching factorials. (\d+) represents the number.
    REGULAR_FACT = r"(?P<factNum>\d+)!"

    # Regular expression for matching arithmetic operations whose operands can be
    # mathematical functions or factorials. First group of the expression is the 
    # first operand that is either a function (func1), a number (operand1, 
    # which could also be x (previous result), or e, or Pi), or a factorial (factNum1).
    # The second group ([-+/*^%]) (operator) is the operator whereas the third group  
    # (\d+|[xXe]|[pP][iI]) (operand2) is either a function (func2), a number (operand2
    # which could also be x, or e, or Pi), or a factorial (factNum2).
    REGULAR_ARITHM = r"(((?P<func1>\w+)\s*\(\s*(?P<arg1>[+-]?(\d+(\.\d+)?|" + \
            r"[xXe]|[pP][iI]))\s*[,]?\s*" + \
            r"(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum1>\d+)!)|" + \
            r"(?P<num1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI])))\s*" + \
            r"(?P<operator>[-+/*^%])?\s*" + \
            r"(((?P<func2>\w+)\s*\(\s*(?P<arg3>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))" + \
            r"\s*[,]?\s*(?P<arg4>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum2>\d+)!)|" + \
            r"(?P<num2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI])))?"
    
    # Regular expression for matching complex arithmetic operations whose operands can 
    # be mathematical functions or factorials and whose order is defined by the 
    # parentheses. First group of the expression (parLeft) is an optional opening  
    # parentheses which define the order of the mathematical operations. The second 
    # group ([-+/*^%]) (operator), optional, is the operator whereas the third – an 
    # operand that is either a function (func), a number (operand, which could also 
    # be x (previous result), or e, or Pi), a factorial (factNum), or a variable (var).
    # The fourth group (parRight) is an optional opening parentheses.
    REGULAR_COMPLX_MATH = r"(?P<memOper>M([+-RC]))|" + \
            r"((?P<parLeft>\()?\s*" + \
            r"(?P<operator>[-+/*^%])?\s*" + \
            r"(((?P<func>\w+)\s*\(\s*(?P<arg1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))" + \
            r"\s*[,]?\s*(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum>\d+)!)|" + \
            r"(?P<num>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))|" + \
            r"(?P<var>\w+))\s*" + \
            r"((?P<comma>,)|" + \
            r"(?P<parRight>\)))?)"

    # Regular expression for matching factorials. "M([+-RC])" - results in adding and
    # substracting the value to the memory cell, recalling and clearing the value
    # stored in the memory cell
    REGULAR_MEM = r"M([+-RC])"

    # A list of mathematical function which contains the mathematical function names as 
    # a key and executable functions with parameters as the values for those keys 
    FUNCTIONS = {
        "sin" : lambda arg1: math.sin(arg1),
        "csc" : lambda arg1: 1 / math.sin(arg1),
        "cos" : lambda arg1: math.cos(arg1),
        "sec" : lambda arg1: 1 / math.cos(arg1),
        "tan" : lambda arg1: math.tan(arg1),
        "cot" : lambda arg1: 1 / math.cot(arg1),
        "arcsin" : lambda arg1: math.asin(arg1),
        "arccos" : lambda arg1: math.acos(arg1),
        "arctan" : lambda arg1: math.atan(arg1),
        "sqrt" : lambda arg1: math.sqrt(arg1),
        "log" : lambda arg1, arg2: math.log(arg1, arg2),
        "ln" : lambda arg1: math.log(arg1),
        "round" : lambda arg1, arg2: round(arg1, arg2),
        "rad" : lambda arg1: math.radians(arg1),
        "deg" : lambda arg1: math.degrees(arg1),
        "bin" : lambda arg1: bin(arg1),
        "hex" : lambda arg1: hex(arg1),
        "neg" : lambda arg1: (-1) * arg1,
        "abrt" : lambda arg1, arg2: arg1 ** (1 / arg2),
        }

    # Precedence of operators in a mathematical expression
    OPERATOR_PREC = {"(": 1, "+": 2, "-" : 2, "*" : 3, "/": 3, "%" : 3, "^": 4, "!" : 5}

    ## Creates the stored result and memory cell
    #  @param self reference to the instance of a class
    #
    def __init__(self) :
        self._x = 0.0         # Stored result
        self._memory = 0.0    # Memory cell

        # Compiles the regex pattern for arithmetic expressions
        self._reArithm = re.compile(self.REGULAR_MATH)
        # Compiles the regex pattern for complex arithmetic expressions
        self._reComplx = re.compile(self.REGULAR_COMPLX_MATH)
        # Compiles the regex pattern for functions  
        self._reFunc = re.compile(self.REGULAR_FUNC)
        # Compiles the regex pattern for factorial
        self._reFact = re.compile(self.REGULAR_FACT)
        # Compiles the regex pattern for memory cell
        self._reMem = re.compile(self.REGULAR_MEM)

    ## Computes the mathematical expression 
    #  @param entry mathematical expression
    #  @return result of the mathematical expression
    #
    def compute(self, entry) :
        result = 0.0
        mathExp = []        # Dictionary of mathematical expression

        if self._reComplx.match(entry) :
            mathExp = self.retrieveExprList(entry)
        # Verify if entry matches the pattern REGULAR_MEM
        elif self._reMem.match(entry) :
            # Perform the memory operation with the given operation name        
            self.performMemOper(entry)
        else :
            print()
            print("Error: Unknown input: %s. Enter \"help\" for guidelines." % entry)
            print()

        return result

    ## Calculates the arithmetic expression
    #  @param num1 first operand
    #  @param operator function operator
    #  @param num2 second operand (None when factorial is computed)
    #  @return result of mathematical operation 
    #
    def calcArithmExpr(self, num1, operator, num2 = None) :
        result = self._x

        match operator : 
            case "+":  
                result = num1 + num2
            case "-":  
                result = num1 - num2
            case "*":  
                result = num1 * num2
            case "/":  
                if num2 == 0 :
                    raise ZeroDivisionError("Error: Second operand is zero.")
                
                result = num1 / num2
            case "^":  
                result = num1 ** num2
            case "%":  
                if num2 == 0 :
                    raise ZeroDivisionError("Error: Second operand is zero.")

                result = num1 % num2
            case "!" : 
                # Verify that the number is a whole number
                if not self.isIntegerNum(num1) :
                    raise ValueError("Error: the number for factorial must be a whole number.")
                
                result = self.calcFact(num1)
            case None : 
                result = num1
            case _:
                print() 
                print("Error: Invalid operator:", operator)
                print()
        
        return result
    
    ## Calculates factorial of a number
    #  @param self reference to the instance of a class
    #  @param num a whole number
    #
    def calcFact(self, num) :      
        return num * self.calcFact(abs(num) - 1) if abs(num) != 0 else 1 
    
    ## Evaluates and calculates the value of mathematical function with given parameters
    #  @param self reference to the instance of a class
    #  @param function mathermatical function
    #  @param num1 first argument of the function
    #  @param num2 second argument (used for log and arbitrary root functions)
    #  @return result of mathematical operation 
    #
    def calcFunc(self, function, num1, num2 = None) :
        result = self._x

        if function in self.FUNCTIONS :
            match function :
                case "csc" :
                    # Verify that the number does not equal to Pi * n
                    if (math.pi - num1) % math.pi <= 0.01 :
                        raise ZeroDivisionError("Error: cosecant is undefined at Pi * n.")

                    result = self.FUNCTIONS[function](num1)
                case "sec" :
                    # Verify that the number does not equal to Pi * ((1/2) + n)
                    if (math.pi * ((1 / 2) + round(num1 / math.pi)) - num1) <= 0.01 :
                        raise ZeroDivisionError("Error: secant is undefined at Pi * ((1/2) + n).")

                    result = self.FUNCTIONS[function](num1)
                case "cot" :
                    # Verify that the number does not equal to Pi * n
                    if (math.pi - num1) % math.pi <= 0.01 :
                        raise ZeroDivisionError("Error: cosecant is undefined at Pi * n.")

                    result = self.FUNCTIONS[function](num1)
                case "log":
                    if num2 is None :
                        num2 = 10

                    result = self.FUNCTIONS[function](num1, num2)
                case "ln": 
                    result = math.log(num1)
                case "round" :
                    if num2 is None :
                        num2 = 2

                    result = self.FUNCTIONS[function](num1, num2)
                case "abrt":
                    if num2 is None :
                        raise ValueError("Error: no second argument was passed to abrt() function.")
                    elif num2 == 0 :
                        raise ZeroDivisionError("Error: second argument of abrt() function is zero.")

                    result = self.FUNCTIONS[function](num1, num2)
                case _:
                    result = self.FUNCTIONS[function](num1)
        else : 
            print()
            print("Error: Invalid expression:", function)
            print()
            
        return result
    
    ## Performs operations with the memory cell:
    ##     - M+ adds the last result to the memory cell
    ##     - M- subtracts the last result from the memory cell
    ##     - MR reads the value from the memory cell
    ##     - MC clears the memory cell
    #  @param self reference to the instance of a class
    #  @param operation memory operation
    #
    def performMemOper(self, operation) : 
        match operation :
            case "M+" : 
                self._memory += self._x
            case "M-" :
                self._memory -= self._x
            case "MC" : 
                self._memory = 0
            case "MR" : 
                print()
                print("M:", self._memory)
                print()
            case _: 
                print()
                print("Error: wrong expression:", operation)
                print()

    ## Converts the value of a string to float
    #  @param self reference to the instance of a class
    #  @param val string to resolve
    #  @return float-point value of val
    #
    def convertToFloat(self, val) :
        num = 0.0 

        match val :
                case "x" | "+x" | "X" | "+X" : 
                    num = self._x
                case "-x" | "-X" : 
                    num = (-1) * self._x
                case "pi" | "+pi" | "pI" | "+pI" | "Pi" | "+Pi" | "PI" | "+PI" : 
                    num = math.pi
                case "-pi" | "-pI" | "-Pi" | "-PI" : 
                    num = (-1) * math.pi
                case "e" | "+e": 
                    num = math.e
                case "-e" : 
                    num = (-1) * math.e
                case None : 
                    num = None
                case _: 
                    num = float(val) 
        
        return num
        
    ## Converts the arithmetic expression to reverse Polish notation
    #  @param self reference to the instance of a class
    #  @param arithmExpr original arithmetic expression
    #  @return list of operands and operators in reverse Polish notation
    #
    def convertToPolish(self, arithmExpr) :
        mathExp = []
        operatorStack = []

        for elem in arithmExpr :        
            if self.isFloat(elem) :            
                mathExp.append(elem)
            elif elem == "(" :
                operatorStack.append(elem)
            elif elem == ")" :
                while len(operatorStack) > 0 and operatorStack[-1] != "(" :
                    mathExp.append(operatorStack.pop())

                if len(operatorStack) > 0 :
                    operatorStack.pop()
            elif elem in self.OPERATOR_PREC :
                while len(operatorStack) > 0 and self.OPERATOR_PREC[elem] <= self.OPERATOR_PREC[operatorStack[-1]] :
                    mathExp.append(operatorStack.pop())

                operatorStack.append(elem)
            else :  
                raise OSError("Error: Invalid expression:", elem)

        while len(operatorStack) > 0 :
            operator = operatorStack.pop()

            if operator != "(" :
                mathExp.append(operator)

        if len(mathExp) % 2 == 0 : 
            raise OSError("Error: Not enough operands.")
    
        return mathExp
    
    ## Parses through the mathematical expression and converts it to a list of 
    ## operands and operators
    #  @param self reference to the instance of a class
    #  @param entry mathematical expression
    #  @return list of operands and operators
    #
    def retrieveExprList(self, entry) :
        mathExp = []

        for item in self._reComplx.finditer(entry) :
                # Retrieve the dictionary with the named subgroups of the match
                token = item.groupdict()

                # Verify if the opening parentheses are present in the expression
                if token["parLeft"] is not None :
                    # Add the opening parentheses to the mathematical expression stack
                    mathExp.append(token["parLeft"])

                # Verify if the operator is present in the expression
                if token["operator"] : 
                    # Add the operator to the mathematical expression stack
                    mathExp.append(token["operator"])

                # Verify if a function with arguments is present in the expression
                if token["func"] is not None :
                    # Convert the values of keys arg1 and arg2 in dictionary to float
                    arg1 = self.convertToFloat(token["arg1"])
                    arg2 = self.convertToFloat(token["arg2"])

                    # Compute the mathematical function with given arguments
                    operand = self.calcFunc(token["func"], arg1, arg2)

                    # Add the calculated result to the mathematical expression stack
                    mathExp.append(operand)
                # Verify if a factorial is present in the expression
                elif token["factNum"] is not None :
                    # Convert the value of the key factNum1 in dictionary to float
                    num = self.convertToFloat(token["factNum"])

                    # Compute the factorial with the given number
                    operand = self.calcFact(num)
                    
                    # Add the calculated factorial to the mathematical expression stack
                    mathExp.append(operand)
                # Verify if a number are present in the expression
                elif token["num"] is not None :
                    # Convert the value of key num1 in dictionary to float
                    operand = self.convertToFloat(token["num"])

                    # Add the number to the mathematical expression stack
                    mathExp.append(operand)
                # Verify if unknown operand are present in the expression
                elif token["var"] is not None :
                    raise ValueError("Error: Invalid operand:", token["var"])

                if token["parRight"] is not None :
                    # Add the closing parentheses to the mathematical expression stack
                    mathExp.append(token["parRight"])

        return mathExp
    
    ## Validates that the string is a rational number
    #  @param self reference to the instance of a class
    #  @param entry a string
    #  @return True if the string is a rational number else False
    #
    def isFloat(self, entry) :
        isValidEntry = False
        startPos = 0

        # Verify that the string is not empty
        if len(entry) > 0 :
            # Verify that the string starts with +- and increment the starting pos by 1
            if entry.startswith("+-") :
                startPos = 1

            # Find the position of the first point
            pointPos = entry.find(".")

            # If the point is not found, verify that the string from start pos is 
            # an integer
            if pointPos == -1 and entry[startPos : ].isdigit() :
                isValidEntry = True
            # If the point was found, verify that the substrings divided by the point
            # are integers 
            elif pointPos >= 0 and entry[startPos : pointPos].isdigit() and entry[pointPos + 1 : ].isdigit() : 
                isValidEntry = True

        return isValidEntry
    
    ## Validates that the string is an integer
    #  @param self reference to the instance of a class
    #  @param entry a string
    #  @return True if the string is an integer else False
    #
    def isInteger(self, entry) :
        isValidEntry = False

        if len(entry) != 0 :
            # Verify that the string starts with +- and increment the starting pos by 1
            startPos = 1 if entry.startswith("+-") else 0
            
            # Verify that the string from start pos is an integer
            if entry[startPos : ].isdigit() :
                isValidEntry = True
        
        return isValidEntry
    
    ## Validates that the number is a whole number
    #  @param self reference to the instance of a class
    #  @param num a number
    #  @return True if the number is a whole number else False
    #
    def isIntegerNum(self, num) :    
        return num % 1 == 0
    
    ## Retrieves the value of variable x
    #  @return value of x
    #
    def getX(self) :
        return self._x
    
    ## Retrieves the value in the memory cell
    #  @return value in the memory cell
    #
    def getMemoryVal(self) :
        return self._memory

    ## Provides information about the functionality of the calculator class
    #  @param self reference to the instance of a class
    #
    def help(self) :
        print()
        print("Supported functions:")
        print("\t- Addition: Number + Number")
        print("\t- Subtraction: Number - Number")  
        print("\t- Multiplication: Number * Number") 
        print("\t- Division: Number / Number") 
        print("\t- Modulus: Number % Number") 
        print("\t- Exponents: Number ^ Number") 
        print("\t- Factorial: Number!") 
        print("\t\t* Note: \"Number\" must be a whole number.")
        print("\t- Trigonometric functions (sin, cos, tan, arctan, etc.): sin(Number)")
        print("\t\t* Note: Default units for the angle is in Radians (Rad).")
        print("\t\t* Note: \"Pi\" is the variable for Pi.")
        print("\t- Square root: sqrt(Number)") 
        print("\t- Arbitrary roots: abrt(Number, Number)") 
        print("\t- Logarithms: log(Number); ln(Number)")
        print("\t\t * Note: The default base for log() function is 10.")
        print("\t- Negation: neg(Number)") 
        print("\t- Rounding: round(Number)")
        print("\t\t * Note: Rounds the number to 2 decimal places by default.")
        print("\t- Angles in degrees or radians: deg(Number); rad(Number)") 
        print("\t- Conversion from base 10 to binary (for integers only): bin(Number)")
        print("\t- Previous result used as first operand: x + Number")
        print("\t- The ability to store and recall results: M+; M-; MR; MC") 
        print()
    
if __name__ == "__main__" :
    main()