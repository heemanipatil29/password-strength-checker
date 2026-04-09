import re
password = input("Enter your password: ")
strength = 0
if len(password) >= 8:
    strength += 1
if re.search("[A-Z]",password):
    strength += 1
if re.search("[0-9]",password):
    strength += 1
if re.search("[a-z]",password):
    strength += 1
if re.search("[!@#$%&*+]",password):
    strength += 1
if strength <= 2:
    print("weak password")
elif strength == 4 or strength == 3:
    print("middle password")
else:
    print("Strong password")
    

