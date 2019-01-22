import os, struct, sys, secrets, string

# Settings
# The aspell dictionary to select from:
lang        = 'is'
# Number of words in the password
nWords      = 3
# Probability for each character to be upper case:
probUpper   = 0.5
# Number of digits between each word:
nDigits     = 2
# Number of special characters after each number:
nSpecials   = 1
# The list of special characters to select from:
# (depending on keyboard layout these may be hard to find)
specials    = string.punctuation
# Minimum password length:
pwd_minlen  = 10
# Maximum password length:
pwd_maxlen  = 30

# The following settings defines the unfiltered - filtered list
# Take out any words from dictionary containing these characters:
word_filter = './-"'
# Only pick from words with at least this length:
wlen_min    = 4
# Only pick from words with at most this length:
wlen_max    = 10

# End of settings

# ------

if not os.path.isfile('filtered.txt'):
    # First generate a full list of words from aspell-nb:
    if not os.path.isfile('unfiltered.txt'):
        cmd = 'aspell -d {0} dump master | aspell -l {0} expand > unfiltered.txt'.format(lang)
        os.system(cmd)

    # Remove words we don't want included..
    fo = open( 'filtered.txt', 'w')
    for l in open('unfiltered.txt','r'):
        ls = l.strip()
        # Remove all very short and very long words:
        if len(ls) < wlen_min or len(ls) > wlen_max:
            continue
        # Remove all words with upper case:
        if l != l.lower():
            continue
        # Remove all words with special characters:
        if any([i in l.lower() for i in word_filter]):
            continue
        fo.write(l)

with open('filtered.txt') as f:
    lines = f.read().splitlines()

maxN = len(lines)

rnd = secrets.SystemRandom()

def gen_pwd():
    pwd = ''

    for n in range(nWords):
        word = list( rnd.choice(lines))
        for j in range(len(word)):
            if rnd.uniform(0.0, 1.0) < probUpper:
                word[j] = word[j].upper()
        pwd += ''.join(word)
        if n+1<nWords:
            for i in range(nDigits):
                pwd += str(rnd.randint(0,9))
            for i in range(nSpecials):
                pwd += rnd.choice( specials)
    return pwd

pwd = gen_pwd()
while len(pwd) < pwd_minlen or len(pwd) > pwd_maxlen:
    pwd = gen_pwd()
print(pwd)
