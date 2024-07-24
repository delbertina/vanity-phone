from random import randrange, shuffle
import time
import boto3
import os

# More of a specific letter makes it more likely to be picked at random
# Weighting is inversely related to scrabble score
t9_mapping = {
    '0': '0',
    '1': '1',
    '2': 'AABCC',
    '3': 'DDDEEF',
    '4': 'GGHHHIII',
    '5': 'JKKKLLLLLLL',
    '6': 'MNNNNOOOOOO',
    '7': 'PPPPPQRRRRRSSSSSSSS',
    '8': 'TTTTTTTUUV',
    '9': 'WWWWXYYYYYYYZ'
}

vowels = "AEIOU"
vowelDigits = "23468"
tableNameEnvVar = "vanityPhoneTableName"

def formatCountryCode(digits: str) -> str:
    return "+" + digits + " "

def formatAreaCode(digits: str) -> str:
    return "(" + digits + ") "

def formatPhoneNumber(digits: str) -> str:
    return digits[:3] + "-" + digits[3:]

def formatEightNine(digits: str) -> str:
    return formatCountryCode(digits[:-7]) + formatPhoneNumber(digits[-7:])

def formatTen(digits: str) -> str:
    return formatAreaCode(digits[:-7]) + formatPhoneNumber(digits[-7:])

def formatElevenPlus(digits: str) -> str:
    return formatCountryCode(digits[:-10]) + formatAreaCode(digits[-10:-7]) + formatPhoneNumber(digits[-7:])

def get_any(digit: str) -> str:
    randomInt = randrange(0, len(t9_mapping[digit]))
    return t9_mapping[digit][randomInt]

def get_vowel(digit: str) -> str:
    if digit not in vowelDigits:
        return get_any(digit)
    selectedVowel = [char for char in t9_mapping[digit] if char in vowels]
    return selectedVowel[0]

def get_consonant(digit: str) -> str:
    if digit in vowelDigits:
        return get_any(digit)
    filteredLetters = [char for char in t9_mapping[digit] if char not in vowels]
    randomInt = randrange(0, len(filteredLetters))
    return filteredLetters[randomInt]

def translate_raw(input: str) -> list[str]:
    # something
    returnVal = []
    inputLen = len(input)
    def translate_sub(current: str) -> None:
        if len(current) == inputLen:
            returnVal.append(current)
            return
        if not current:
            translate_sub(current + get_consonant(input[len(current)]))
            translate_sub(current + get_consonant(input[len(current)]))
        # Double vowels are pretty uncommon in English
        # So if the last letter is a vowel, specifically get a consonant
        elif current[-1] in vowels:
            translate_sub(current + get_consonant(input[len(current)]))
        translate_sub(current + get_any(input[len(current)]))            
    translate_sub("")
    return returnVal

def upload_results(inputNum: str, results: list[str]) -> None:
    print(results)
    
    # Upload to DynamoDB
    dynamodb = boto3.client('dynamodb')
    # Get table name from env var setup with CF, etc
    dynamodb.put_item(TableName=os.environ[tableNameEnvVar],
                      Item={
                          'inputNum':{'S': inputNum},
                          'timestamp':{'N': str(int(time.time())) },
                          "vanityNums": {"L": [{'S': item} for item in results]}
                          })

# Optional return length to directly call 
def translate_number(input: str, returnLen: int = 5) -> list[str]:
    # Filter out anything that isnt a digit
    rawNum = "".join([char for char in input if char.isdigit()])
    inputNum = rawNum
    # debug
    print(inputNum)
    
    # If the user entered anything less than 7 characters, pad with 0's
    if len(inputNum) < 7:
        inputNum = (inputNum + "0000000")[:7]
    
    inputLen = len(inputNum)
    results = translate_raw(inputNum[-7:])
    remainder = inputNum[:-7]
    shuffle(results)
    
    # This mainly supports US phone numbers
    if inputLen <= 7:
        results = [formatPhoneNumber(item) for item in results]
    elif inputLen <= 9:
        results = [formatEightNine(remainder + item) for item in results]
    elif inputLen == 10:
        results = [formatTen(remainder + item) for item in results]
    else:
        results = [formatElevenPlus(remainder + item) for item in results]
    
    # debug
    print(results)
    
    # Return only the top 5 results after the shuffle
    return results[:returnLen]
    
def translate_and_upload(input: str) -> None:
    results = translate_number(input)
    
    if results:
        upload_results(results)
    
# Test out locally
# print(translate_number("8004688646"))