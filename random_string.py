import random
import string
import argparse

def random_string(length):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for i in range(length))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random string.")
    parser.add_argument("length", type=int, help="The length of the random string to generate.")
    args = parser.parse_args()
    
    print(random_string(args.length))