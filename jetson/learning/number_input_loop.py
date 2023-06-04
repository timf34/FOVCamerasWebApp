import sys

while True:
    user_input = sys.stdin.readline().strip()  # Read a line from stdin and remove the newline character at the end
    if user_input == 'q':
        break
    print("The number you entered is", user_input)
