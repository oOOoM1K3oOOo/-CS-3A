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
    
    print("This program is a calculator which computes simple mathematical")
    print("expressions and functions.") 
    print()
    print("* For the information about legal syntax and supported functions write")
    print("* \"help\" in the command line.")
    print()
    print("* To exit from the calculator, write \"quit\" in the command line.")
    print()

    calc.help()

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
    # Regular expression for matching numeric operations. First operand (\d+|[xXpe]) 
    # (group 1) could be the number or x (previous result), second operand ([-+/*^%]) 
    # (group 2) is the operator, the third (\d+) (group 3) - number.
    REGULAR_MATH = r"(?P<operand1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))\s*" + \
                    r"(?P<operator>[-+/*^%])\s*" + \
                    r"(?P<operand2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))$"   

    # Regular expression for matching functions. First operand is the word (function name 
    # (\w+) ), second (\d+) - the regular number.
    REGULAR_FUNC = r"(?P<func>\w+)\s*\(\s*(?P<arg1>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))" + \
                    r"\s*[,]?\s*(?P<arg2>[+-]?(\d+(\.\d+)?|[xXe]|[pP][iI]))?\s*\)$"
    
    # Regular expression for matching factorials. (\d+) represents the number.
    REGULAR_FACT = r"(?P<factNum>\d+)!"

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

        # Compiles the regex pattern for arithetic expressions
        self._reArithm = re.compile(self.REGULAR_MATH)
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
        num1 = 0.0
        num2 = 0.0
        mathExp = {}        # Dictionary of mathematical expression

        # Verify if entry matches the pattern REGULAR_MATH
        if self._reArithm.match(entry) :
            # Retrieve the dictionary of matched groups that follow REGULAR_MATH pattern          
            mathExp = self._reArithm.match(entry).groupdict()

            # Convert the values of keys in dictionary to float 
            num1 = self.convertToFloat(mathExp["operand1"])            
            num2 = self.convertToFloat(mathExp["operand2"])       

            # Compute the arithmetic expression 
            result = self.calcArithmExpr(num1, mathExp["operator"], num2)
            # Save the computed result in the class variable x
            self._x = result
        # Verify if entry matches the pattern REGULAR_FUNC
        elif self._reFunc.match(entry) : 
            # Retrieve the dictionary of matched groups that follow REGULAR_MATH pattern     
            mathExp = self._reFunc.match(entry).groupdict()

            # Convert the values of keys in dictionary to float
            num1 = self.convertToFloat(mathExp["arg1"])            
            num2 = self.convertToFloat(mathExp["arg2"])            

            # Get the value of the mathematical function with entered parameters
            result = self.calcFunc(mathExp["func"], num1, num2)
            # Save the computed result in the class variable x
            self._x = result
        # Verify if entry matches the pattern REGULAR_FACT
        elif self._reFact.match(entry) :       
            mathExp = self._reFact.match(entry).groupdict()

            # Convert the value of the key in dictionary to float
            num1 = self.convertToFloat(mathExp["factNum"])

            # Compute the factorial with the given number
            result = self.calcFact(num1)
            # Save the computed result in the class variable x
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
                if (math.pi - num1) % math.pi <= 0.01 :
                    raise ZeroDivisionError("Error: cosecant is undefined at Pi * n.")
                
                result = 1 / math.sin(num1)
            case "cos": 
                result = math.cos(num1)
            case "sec" :
                if ((math.pi / 2) - num1) % (math.pi / 2) <= 0.01 :
                    raise ZeroDivisionError("Error: secant is undefined at (1/2) * Pi * n.")
                
                result = 1 / math.cos(num1)
            case "tan": 
                result = math.tan(num1)
            case "cot" :
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