import os, struct, sys, random, string

# Settings
# The aspell dictionary to select from:
lang        = 'is'
# Take out any words from dictionary containing these characters:
word_filter = './-'
# Number of words in the password
nWords      = 2
# Probability for each character to be upper case:
probUpper   = 0.5
# Number of digits between each word:
nDigits   = 2
# Number of special characters after each number:
nSpecials = 1
# Only pick from words with at least this length:
wlen_min  = 5
# Only pick from words with at most this length:
wlen_max  = 8

# Minimum password length:
pwd_minlen = 10
# Maximum password length:
pwd_maxlen = 30
# End of settings

# ------

# First generate a full list of words from aspell-nb:
if not os.path.isfile('my.dict'):
    cmd = 'aspell -d {0} dump master | aspell -l {0} expand > my.dict'.format(lang)
    os.system(cmd)

# Remove words we don't want included..
if not os.path.isfile('my2.dict'):
    fo = open( 'my2.dict', 'w')
    for l in open('my.dict','r'):
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

with open('my2.dict') as f:
    lines = f.read().splitlines()

maxN = len(lines)

# Needed for selection of random digit:
digits = [str(i) for i in range(10)]
rnd = random.SystemRandom()

def gen_pwd():
    pwd = ''
    
    for n in range(nWords):
        ran = rnd.randint(0, maxN)
        word = list(lines[ran])
        for j in range(len(word)):
            if rnd.uniform(0.0, 1.0) < probUpper:
                word[j] = word[j].upper()
        pwd += ''.join(word)
        if n+1<nWords:
            for i in range(nDigits):
                pwd += str(rnd.randint(0,9))
            for i in range(nSpecials):
                pwd += rnd.choice( string.punctuation)
    return pwd

pwd = gen_pwd()
while len(pwd) < pwd_minlen or len(pwd) > pwd_maxlen:
    pwd = gen_pwd()
print(pwd)
