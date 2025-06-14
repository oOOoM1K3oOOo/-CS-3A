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
    REGULAR_COMPLX_MATH = r"(((?P<func1>\w+)\s*\(\s*(?P<arg1>[+-]?(\d+(\.\d+)?|" + \
            r"[xXe]|[pP][iI]))\s*[,]?\s*" + \
            r"(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum1>\d+)!)|" + \
            r"(?P<num1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI])))\s*" + \
            r"(?P<operator>[-+/*^%])?\s*" + \
            r"(((?P<func2>\w+)\s*\(\s*(?P<arg3>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))" + \
            r"\s*[,]?\s*(?P<arg4>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum2>\d+)!)|" + \
            r"(?P<num2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI])))?"
    
    REGULAR_ARITHM = r"(?P<operator>[-+/*^%])?\s*(((?P<func>\w+)\s*\(\s*" + \
            r"(?P<arg1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))\s*[,]?\s*" + \
            r"(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\))|" + \
            r"((?P<factNum>\d+)!)|" + \
            r"(?P<num>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI])))"

    # Regular expression for matching factorials. "M([+-RC])" - results in adding and
    # substracting the value to the memory cell, recalling and clearing the value
    # stored in the memory cell
    REGULAR_MEM = r"M([+-RC])"  

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
        operand1 = 0.0
        operand2 = 0.0
        mathExp = {}        # Dictionary of mathematical expression

        ## Verify if entry matches the pattern REGULAR_MATH
        #if self._reArithm.match(entry) :
        #    # Retrieve the dictionary of matched groups that follow REGULAR_MATH pattern          
        #    mathExp = self._reArithm.match(entry).groupdict()
        #
        #    # Convert the values of keys in dictionary to float 
        #    num1 = self.convertToFloat(mathExp["operand1"])            
        #    num2 = self.convertToFloat(mathExp["operand2"])       
        #
        #    # Compute the arithmetic expression 
        #    result = self.calcArithmExpr(num1, mathExp["operator"], num2)
        #    # Save the computed result in the class variable x
        #    self._x = result
        ## Verify if entry matches the pattern REGULAR_FUNC
        #elif self._reFunc.match(entry) : 
        #    # Retrieve the dictionary of matched groups that follow REGULAR_MATH pattern     
        #    mathExp = self._reFunc.match(entry).groupdict()
        #
        #    # Convert the values of keys in dictionary to float
        #    num1 = self.convertToFloat(mathExp["arg1"])            
        #    num2 = self.convertToFloat(mathExp["arg2"])            
        #
        #    # Get the value of the mathematical function with entered parameters
        #    result = self.calcFunc(mathExp["func"], num1, num2)
        #    # Save the computed result in the class variable x
        #    self._x = result
        ## Verify if entry matches the pattern REGULAR_FACT
        #elif self._reFact.match(entry) :       
        #    mathExp = self._reFact.match(entry).groupdict()
        #
        #    # Convert the value of the key in dictionary to float
        #    num1 = self.convertToFloat(mathExp["factNum"])
        #
        #    # Compute the factorial with the given number
        #    result = self.calcFact(num1)
        #    # Save the computed result in the class variable x
        #    self._x = result
        # Verify if entry matches the pattern REGULAR_COMPLX_MATH
        if self._reComplx.fullmatch(entry) :
            # Retrieve the dictionary of matched groups that follow REGULAR_COMPLX_MATH
            # pattern          
            mathExp = self._reComplx.fullmatch(entry).groupdict()

            if mathExp["func1"] is not None :
                # Convert the values of keys arg1 and arg2 in dictionary to float
                arg1 = self.convertToFloat(mathExp["arg1"])
                arg2 = self.convertToFloat(mathExp["arg2"])

                # Compute the arithmetic expression
                operand1 = self.calcFunc(mathExp["func1"], arg1, arg2)
            elif mathExp["factNum1"] is not None :
                # Convert the value of the key factNum1 in dictionary to float
                num = self.convertToFloat(mathExp["factNum1"])

                # Compute the factorial with the given number
                operand1 = self.calcFact(num)
            elif mathExp["num1"] is not None :
                # Convert the value of key num1 in dictionary to float
                operand1 = self.convertToFloat(mathExp["num1"])

            if mathExp["func2"] is not None :
                # Convert the values of keys arg3 and arg4 in dictionary to float
                arg3 = self.convertToFloat(mathExp["arg3"])
                arg4 = self.convertToFloat(mathExp["arg4"])

                # Compute the arithmetic expression
                operand2 = self.calcFunc(mathExp["func2"], arg3, arg4)
            elif mathExp["factNum2"] is not None :
                # Convert the value of the key factNum2 in dictionary to float
                num = self.convertToFloat(mathExp["factNum2"])

                # Compute the factorial with the given number
                operand2 = self.calcFact(num)
            elif mathExp["num2"] is not None :
                # Convert the value of key num2 in dictionary to float
                operand2 = self.convertToFloat(mathExp["num2"])

            result = self.calcArithmExpr(operand1, mathExp["operator"], operand2)
            self._x = result
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
    #  @param num2 second operand
    #  @return result of mathematical operation 
    #
    def calcArithmExpr(self, num1, operator, num2) :
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
            case None : 
                result = num1
            case _: 
                print("Error: Invalid operator:", operator)
        
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

        match function : 
            case "sin": 
                result = math.sin(num1)
            case "csc" :
                # Verify that the number does not equal to Pi * n
                if (math.pi - num1) % math.pi <= 0.01 :
                    raise ZeroDivisionError("Error: cosecant is undefined at Pi * n.")
                
                result = 1 / math.sin(num1)
            case "cos": 
                result = math.cos(num1)
            case "sec" :
                # Verify that the number does not equal to Pi * ((1/2) + n)
                if (math.pi * ((1 / 2) + round(num1 / math.pi)) - num1) <= 0.01 :
                    raise ZeroDivisionError("Error: secant is undefined at Pi * ((1/2) + n).")
                
                result = 1 / math.cos(num1)
            case "tan": 
                result = math.tan(num1)
            case "cot" :
                # Verify that the number does not equal to Pi * n
                if (math.pi - num1) % math.pi <= 0.01 :
                    raise ZeroDivisionError("Error: cosecant is undefined at Pi * n.")

                result = 1 / math.tan(num1)
            case "arcsin" :
                result = math.asin(num1)
            case "arccos" :
                result = math.acos(num1)
            case "arctan" :
                result = math.atan(num1)
            case "sqrt":
                result = math.sqrt(num1)
            case "log":
                if num2 is None :
                    num2 = 10
                 
                result = math.log(num1, num2)
            case "ln": 
                result = math.log(num1)
            case "round" :
                if num2 is None :
                    num2 = 2

                result = round(num1, int(num2))
            case "rad": 
                result = math.radians(num1)
            case "deg": 
                result = math.degrees(num1)
            case "bin":
                result = bin(int(num1))
            case "hex":
                result = hex(int(num1)) 
            case "neg": 
                result = (-1) * num1
            case "abrt":
                if num2 is None :
                    raise ValueError("Error: no second argument was passed to abrt() function.")
                elif num2 == 0 :
                    raise ZeroDivisionError("Error: second argument of abrt() function is zero.")
                
                result = num1 ** (1 / num2)
            case _:
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
        OPERATOR_PRIORITY = {"(": 1, "+": 2, "-" : 2, "*" : 3, "/": 3, "%" : 3, "^": 4}
        OPERATORS = "()+-*/%^"

        mathExp = []
        operatorStack = []


        for elem in arithmExpr :        
            if self.isFloat(elem) :            
                    mathExp.append(elem)
            elif elem in OPERATORS :
                if elem == "(" :
                    operatorStack.append(elem)
                elif elem == ")" :
                    while len(operatorStack) > 0 and operatorStack[-1] != "(" :
                        mathExp.append(operatorStack.pop())

                    operatorStack.pop()
                else :
                    while len(operatorStack) > 0 and OPERATOR_PRIORITY[elem] < OPERATOR_PRIORITY[operatorStack[-1]] :
                            mathExp.append(operatorStack.pop())

                    operatorStack.append(elem)
            else :  
                raise OSError("Error: Invalid expression:", elem)

        while len(operatorStack) > 0 :
            if operatorStack[-1] == "(" :
                operatorStack.pop()
            else :
                mathExp.append(operatorStack.pop())

        if len(mathExp) < 3 : 
            raise OSError("Error: Not enough operators.")
    
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
        if len(entry) != 0 :
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