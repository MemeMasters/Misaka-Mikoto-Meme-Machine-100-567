import re

from . import dice, BadEquation


class Calculator:
    """
    This parses textual equations, and calculates the result.

    If you want to add your own functions, all you need to do is to set 
    its precidence in the precidence variable, set the number of operands
    needed if it has more or less than 2, and create the function as a lambda
    in the functions dict.

    """

    # Lower numbers mean a lower precidence (it is less important)
    precidence = {
        '+': 2, '-': 2,
        '*': 3, '/': 3,
        '^':4, '%':4,
        'd': 5, 'adv': 5, 'dis': 5, 'top': 5, 'bot': 5,
        'round': 6}
    
    # A function by default has 2 arguments, if it does not, list the number required here.
    function_length = {
        'round': 1,
        'top': 3,
        'bot': 3
    }

    # All the functions are defined here as lambdas.
    functions = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '^': lambda a, b: a ** b,
        '%': lambda a, b: a % b,
        'd': lambda a, b: dice.roll_sum(round(b), round(a))[0],
        'adv': lambda a, b: dice.roll_top(round(b), 1, round(a)),
        'dis': lambda a, b: dice.roll_top(round(b), 1, round(a), False),
        'top': lambda a, b, c: dice.roll_top(round(b), round(c), round(b)),
        'bot': lambda a, b, c: dice.roll_top(round(b), round(c), round(b)),
        'round': lambda a: round(a)
    }

    def _load_equation(self, data: list) -> list:
        """
        Parse an equation to be calculated easier by a computer using the
        Shunting Yard Algorithm.

        A SYA equation looks like this:

        ```
        5 + 4 * 3 => 5 4 3 * +
        ```
        """
        stack = list()
        num_parens = 0

        equation = list()

        for i in data:
            try:
                number = float(i)
                equation.append(number)
            except ValueError:  # If the item is not a number, it must be an operator
                # Check if the item is the end of a paranthesis
                if i == ')':
                    # If so, pop all the operands up to the acompanying paranthesis
                    num_parens -= 1
                    while len(stack) > 0:
                        pop = stack.pop()
                        if pop == '(':
                            break
                        equation.append(pop)
                else:
                    if i == '(':
                        num_parens += 1
                    else:
                        # If the precidence of the stack is greater than the current precidence, than pop until it's not
                        while len(stack) > 0 and self.__class__.precidence.get(i, 0) <= self.__class__.precidence.get(stack[-1], 0):
                            pop = stack.pop()
                            if pop == '(':
                                raise BadEquation("Mismatched parentheses")
                            equation.append(pop)
                    # Add the operator to the stack
                    stack.append(i)
        
        if num_parens is not 0:
            raise BadEquation("Mismatched parentheses")
        
        while len(stack) > 0:
            equation.append(stack.pop())
        
        return equation
    
    def _calculate_equation(self, equation: list) -> float:
        """
        calculate a Shunting Yard equation.
        """
        stack = list()

        for i in equation:
            if isinstance(i, float):
                stack.append(i)
            else:
                try:
                    try:
                        # Load the operands
                        operands = list()
                        for _ in range(self.__class__.function_length.get(i, 2)):
                            operands.insert(0, stack.pop())

                        # Process the function
                        stack.append(self.__class__.functions[i](*operands))
                    except IndexError:
                        raise BadEquation("Unbalanced number of operators or operands")
                except IndexError:
                    raise BadEquation("Invalid Operator '{}'".format(i))
        
        if len(stack) is not 1:
            raise BadEquation("Invalid number of operands")
        
        return stack.pop()

    def parse_equation(self, string: str) -> float:
        """
        Parse a human readable equation.

        This supports the following operators:

        ```
        + - * / ^ % d ( ) round(x)
        ```

        Note: d is used for rolling dice where the firstoperand is the number of dice
        to roll, and the second is the number of faces.
        
        an example of an equation:

        ```
        ((5 * 4 + 3 / 6) % 6)d6 = 2d6
        ```

        If there is a formatting problem with the given equation, a BadEquation error
        will be thrown.
        """
        # parse the string into a list of operators and operands.

        # (?|?|?) regex or
        # [^\w.,\s] matches any single character that is not a word, number, _, `,`, or whitespace
        # [\d.]+ matches any number
        # [a-z]+ matches any lower case word
        # goto https://regex101.com/ for help creating your own regexes.
        equation = re.findall(r"([^\w.,\s]|[\d.]+|[a-z]+)", string.lower())

        # Parse the equation using the Shunting Yard Algorithm
        equation = self._load_equation(equation)

        # Find the answer to the equation
        value = self._calculate_equation(equation)

        # Force the result into an int if it's an integer value
        return int(value) if value == int(value) else value
