"""
'pi-to-the-nth.py by Curtis Wilson (@tightpin, Github)

A program that utilizes Nilakantha Somayaji's infinite series of calculating pi 
to return a result with n decimal places, as provided by the user.

The range is capped at 20 as Nilakantha's series provides around 18 decimal
places of accuracy with 1,000,000 iterations, which on standard machines takes
several seconds to compute. The number of iterations (and the range) can be
increase within the code's global variables.
"""
from decimal import Decimal, getcontext
from sre_constants import RANGE
import urllib.request
import urllib.parse
import json


ITERATIONS = 1000000    # One million iterations provides 18 decimal-points of accuracy
RANGE_MAX = 20          # TODO: Find if range can be scaled to ITERATIONS

"""
Main function to handle user input and print results.
"""
def main():
    while True:
        try:
            places = int(input("Enter a digit, n, between 1 and 20 to have pi returned to the nth degree: "))
            if places in range (1, RANGE_MAX):
                # Specify the precision of the Decimal object's results
                getcontext().prec = places + 1
                result = nilakantha(ITERATIONS) 
                print(result)
                checkResult(result, places)
                break
        # Handle ValueError and pass to error message
        except ValueError:
            pass
        print("Incorrect input, try again.")

"""
An implementation of Nilakantha's series of calculating pi, as found on
https://www.wikihow.com/Write-a-Python-Program-to-Calculate-Pi.
"""
def nilakantha(iterations) -> Decimal:
    result = Decimal(3.0)
    op = 1
    n = 2
    for n in range(2, 2 * iterations + 1, 2):
        result += 4 / Decimal(n * (n + 1) * (n + 2) * op)
        op *= -1
    return result

"""
It's good to check our math against an objective truth. Luckily, Google has accurately calculated pi to a trillion digits
AND they deliver!
https://pi.delivery/#apipi_get
"""
def checkResult(result, places):
    truepi = fetchPi(places)
    print('Compare to: ',truepi)
    checkpi = str(result).replace('.', '')
    if truepi == checkpi:
        print ("✅ It appears the math is correct.")
    else:
        print ("❌ The two versions of pi do not align - somebodies math is wrong.")


def fetchPi(end):
    #API Counts 3 as a digit place, so we add one to compensate
    url = 'https://api.pi.delivery/v1/pi?start=0&numberOfDigits='+str(end+1) 
    call = urllib.request.urlopen(url)
    #After making the call, we use the json library to change it into a python compatible object
    clean = json.loads(call.read().decode('utf-8'))
    return clean['content']

if __name__ == "__main__":
    main()