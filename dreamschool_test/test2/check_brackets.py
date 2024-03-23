def check_brackets(input_str):
    stack = []  # 一个栈压入和弹出括号

    length = len(input_str)
    output = []
    for _ in range(length):
        output.append("0")

    for i, char in enumerate(input_str):
        if char == '(':
            stack.append(i)
            output[i] = ' '
        elif char == ')':
            if stack:
                stack.pop()
                output[i] = ' '
            else:
                output[i] = '?'
        else:
            output[i] = ' '

    for index in stack:
        output[index] = 'x'

    return output


input_str = input("Please input a string:")
print(input_str)
output_str = check_brackets(input_str)
for char in output_str:
    print(char, end='')
