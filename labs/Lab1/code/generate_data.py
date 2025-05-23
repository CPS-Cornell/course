import random
import string

def generate_positive_integers(n, mean=10, std=4):
    nums = []
    while len(nums) < n:
        val = int(round(random.gauss(mean, std)))
        if val > 0:
            nums.append(val)
    return nums

def generate_alphabet_characters(n):
    return [random.choice(string.ascii_uppercase) for _ in range(n)]

def create_string(int_list, char_list):
    result = []
    for num, char in zip(int_list, char_list):
        result.append(char * num)
    return "".join(result)

def main():
    number_of_elements = 1000
    int_list = generate_positive_integers(number_of_elements, std=10, mean=4)
    char_list = generate_alphabet_characters(number_of_elements)
    final_string = create_string(int_list, char_list)
    with open("data.txt", "w") as f:
        f.write(final_string)
    print(final_string)


main()
