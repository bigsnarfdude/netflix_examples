alist = range(1,101)

def fizz(number):
    if number%3 == 0:
        return "Fizz"

def buzz(number):
    if number%5 == 0:
        return "Buzz"

def fizzbuzz(number):
    if fizz(number) and buzz(number):
        return "FizzBuzz"

def number(number):
    return number

[ fizzbuzz(item) or fizz(item) or buzz(item) or number(item) for item in alist ]



