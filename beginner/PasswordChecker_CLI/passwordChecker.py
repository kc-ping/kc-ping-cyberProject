import re,json,math,argparse
# import dictionary check from wordfreq
import wordfreq
from colorama import Fore, Style, init

init(autoreset=True) # Reset color after each print

class PasswordStrengthTester: 
    def __init__(self, password):
        self.password = password
        self.score = 0
        self.entropyBits = 0
        self.rating= None

    def calculateStrength(self):
        self.score = 0
        pwd = self.password

        # Length tests
        if len(pwd) >= 8:
            self.score += 1
        if len(pwd) >= 12:
            self.score += 1

        # Character variety tests
        if re.search(r'[a-z]', pwd): #lowercase
            self.score += 1
        if re.search(r'[A-Z]', pwd): #uppercase
            self.score += 1
        if re.search(r'\d', pwd):    #digits
            self.score += 1
        if re.search(r'[^A-Za-z0-9]', pwd): #special chars
            self.score += 1

        commonPasswords =  wordfreq.top_n_list('en', 1000) # Top 1000 common passwords
        if pwd.lower() in commonPasswords:
            print(Fore.RED + "This password is on a common blacklist! Very Weak.")
            return  # We skip further checks since it's very weak
        
        commonWords = wordfreq.top_n_list('en', 10000) # Top 10,000 common words
        for word in commonWords:
            if word in pwd.lower():
                self.score -= 1
                print(Fore.YELLOW + f"Contains common word '{word}'. Consider avoiding dictionary words.")
                break

        # Entropy calculation
        def calculateEntropy(pwd): 
            # estimate character set size based on categories used
            charsetSize = 0
            if re.search(r'[a-z]', pwd):
                charsetSize += 26
            if re.search(r'[A-Z]', pwd):
                charsetSize += 26
            if re.search(r'\d', pwd):
                charsetSize += 10
            if re.search(r'[^A-Za-z0-9]', pwd):
                charsetSize += 32 # Approximation for special chars
            
            entropy = len(pwd) * math.log2(charsetSize) if charsetSize > 0 else 0
            return entropy
        
        entropyBits = calculateEntropy(pwd)
        self.entropyBits = entropyBits
        print(f'Estimated Entropy: {entropyBits:.2f} bits')
        ## real-world cracks often find patterns, so entropy is theoretical.
        
        rating = ""
        if self.score <= 1:
            rating = Fore.RED + "Very Weak"
        elif self.score == 2:
            rating = Fore.YELLOW + "Weak"
        elif self.score == 3:
            rating = Fore.CYAN + "Moderate"
        elif self.score == 4:
            rating = Fore.GREEN + "Strong"
        else:
            rating = Fore.GREEN + Style.BRIGHT + "Very Strong"

        # store rating (colored and plain)
        plainRating = re.sub(r'\x1b\[[0-9;]*m', '', rating)
        self.rating_colored = rating
        self.rating = plainRating


        # Build ASCII bar (one '#' per point, '-' for missing, total length = 6)
        bar = '[' + '#' * self.score + '-' * (6 - self.score) + ']'

        print(f"Strength: {bar}  {rating}{Style.RESET_ALL}  (Score: {self.score}/6)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Strength Checker CLI") # Argument parser
    parser.add_argument("password", help="Password to check strength for") # Required password argument
    parser.add_argument('--json', action='store_true', help="Output result in JSON format") # Optional JSON output
    args = parser.parse_args()

    tester = PasswordStrengthTester(args.password)
    tester.calculateStrength()
    if args.json:
        output = {
            "password": args.password,
            "score": tester.score,
            "rating": tester.rating,
            'entropy bits': tester.entropyBits
        }
        print(json.dumps(output, indent=4))