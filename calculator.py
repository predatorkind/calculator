import re

"""
Calculator lets you read a file containing simple equations (+, -, *, /) and provides solutions
in equations.txt file.

"""
def verify_input(options_list):
    """
    Asks for input and checks if matches any of the available options in list as regular expression
    :param options_list: list of available options
    :return: returns a valid selected option
    """
    while True:
        user_input = input("> ").strip().lower()
        for option in options_list:
            pattern = re.compile(option)

            if pattern.match(user_input):
                return user_input
        print("Invalid option. Try again.")


def read_equations(file_name):
    """
    read equations from a text tile and add them to a 2D list
    :param file_name: path to the text file
    :return: 2D list of equations or None on error
    """
    equations = []
    num_pattern = re.compile("^[0-9]+[.]?[0-9]*$")

    try:
        with open(file_name, "r") as f:
            for line in f.readlines():
                elements = line.split(" ")
                # each line has to consist of 3 elements: number, operation, number
                if len(elements) == 3:
                    # check if first element is a number
                    if num_pattern.match(elements[0].strip()):
                        # check if second element one of the 4 operations
                        if elements[1] == "+" or elements[1] == "-" or elements[1] == "*" or elements[1] == "/":
                            # check if third element is a number
                            if num_pattern.match(elements[2].strip()):
                                equations.append([elements[0].strip(), elements[1].strip(), elements[2].strip()])
        return equations
    except FileNotFoundError:
        print(f"{file_name} not found.")
        return None


def read_file():
    """
    reads a text file provided by user and displays its contents
    """
    # ask user for filename
    file = input("Enter a file to display.\n> ")

    # open file and print each line
    try:
        with open(file, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"{file} not found.")


def welcome_screen():
    """
    prints the welcome screen
    """
    print("""**************************
***   THE CALCULATOR   ***
**************************""")


def main_menu():
    """
    displays Main Menu
    """
    # The string content cannot be indented as it is a multiline string that preserves formatting.
    # If the line were indented they would appear shifted while displayed in the program.
    # Normally wrong indentation gets flagged by my IDE. In this case it is showing as correct.
    print("""
Choose an option:
1. (M)anual
2. (R)ead and Compute
3. (D)isplay File
4. (H)elp
5. (E)xit
    """)


def calculate(equation_list):
    """
    calculates an equation
    :param equation_list: list containing equation elements: number, operation, number
    :return: result of the operation
    """
    result = "ERROR"
    if equation_list[1] == "+":
        result = float(equation_list[0]) + float(equation_list[2])
    elif equation_list[1] == "-":
        result = float(equation_list[0]) - float(equation_list[2])
    elif equation_list[1] == "*":
        result = float(equation_list[0]) * float(equation_list[2])
    elif equation_list[1] == "/":
        if float(equation_list[2]) == 0:
            result = "ERROR"
        else:
            result = float(equation_list[0]) / float(equation_list[2])
    return result


def manual_calculator():
    """
    executes manual calculator procedure
    """
    # ask user for numbers and operation
    print("Enter number 1:")
    num1 = float(verify_input(["^[0-9]+[.]?[0-9]*$"]))
    print("Enter operation (+, -, *, /):")
    operation = verify_input(["^\\+$", "^\\-$", "^\\*$", "^\\/$"])
    print("Enter number 2:")
    num2 = float(verify_input(["^[0-9]+[.]?[0-9]*$"]))

    # calculate result
    result = calculate([num1, operation, num2])
    format_equation([num1, operation, num2, result])


def format_equation(equation_list):
    """
    formats equation and display it to the user
    :param equation_list: list of equation elements: number, operation, number, result
    :return:
    """
    num1 = equation_list[0]
    num2 = equation_list[2]
    operation = equation_list[1]
    result = equation_list[3]

    # do not strip zeros from "0" strings
    if num1 != "0":
        num1 = str(float(round(num1, 6))).rstrip('0').rstrip('.')

    if num2 != "0":
        num2 = str(float(round(num2, 6))).rstrip('0').rstrip('.')

    if result == "ERROR":
        result = "ERROR. Cannot divide by zero."
    elif result != "0":
        result = str(float(round(result, 6))).rstrip('0').rstrip('.')

    # display formatted result
    print(f"{num1} {operation} {num2} = {result}")
    save_to_file([num1, operation, num2, result])


def save_to_file(equation):
    """
    saves equations to equations.txt
    :param equation: equation as list
    """
    data = f"\n{equation[0]} {equation[1]} {equation[2]} = {equation[3]}"
    with open("equations.txt", "a") as f:
        f.write(data)


def automatic_calculator():
    """
    executes automatic calculator that reads equations from a text file
    :return:
    """
    # ask user for filename
    equations = read_equations(input("Enter a txt file name with equations adhering"
                                     " to the following format: number operation number.\n> "))
    if equations is None:
        print("File not found. Try again.")
    else:
        # print formatted equation with the result
        for equation in equations:
            result = calculate(equation)
            format_equation([float(equation[0]), equation[1], float(equation[2]), result])


def main_loop():
    welcome_screen()
    main_menu()
    while True:
        selection = verify_input(["^1$", "^2$", "^3$", "^4$", "^5&", "^m$", "^r$", "^d$", "^h$", "^e$"])
        if selection == "1" or selection == "m":
            manual_calculator()
            main_menu()
        elif selection == "2" or selection == "r":
            automatic_calculator()
            main_menu()
        elif selection == "3" or selection == "d":
            read_file()
            main_menu()
        elif selection == "4" or selection == "h":
            main_menu()
        elif selection == "5" or selection == "e":
            exit()


# start the main loop of the program
main_loop()
