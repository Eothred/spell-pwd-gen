import os, struct, sys, secrets, string, yaml
from types import SimpleNamespace

if len(sys.argv) > 1:
    conf_file = sys.argv[1]
else:
    conf_file = "config.yml"
with open(conf_file, "r") as fin:
    config = SimpleNamespace(**yaml.safe_load(fin))


if os.path.isfile('words.txt'):
    filename = 'words.txt'
else:
    filename = 'words-{}.txt'.format(config.lang)

if not os.path.isfile(filename):
    # First generate a full list of words from aspell-nb:
    if not os.path.isfile('unfiltered-{}.txt'.format(config.lang)):
        cmd = 'aspell -d {0} dump master | aspell -l {0} expand > unfiltered-{0}.txt'.format(config.lang)
        os.system(cmd)

    # Remove words we don't want included..
    fo = open( 'words-{}.txt'.format(config.lang), 'w')
    for l in open('unfiltered-{}.txt'.format(config.lang),'r'):
        for ls in l.split():
            # Remove all very short and very long words:
            if len(ls) < wlen_min or len(ls) > wlen_max:
                continue
            # Remove all words with upper case:
            if ls != ls.lower():
                continue
            # Remove all words with special characters:
            if any([i in ls.lower() for i in word_filter]):
                continue
            fo.write(ls+'\n')

with open(filename) as f:
    lines = f.read().splitlines()

print(f"Number of words to choose from is {len(lines)}")

rnd = secrets.SystemRandom()

def gen_pwd():
    pwd = ''

    for n in range(config.nWords):
        word = list( rnd.choice(lines))
        for j in range(len(word)):
            if rnd.uniform(0.0, 1.0) < config.probUpper:
                word[j] = word[j].upper()
        pwd += ''.join(word)
        if n+1<config.nWords:
            for i in range(config.nDigits):
                pwd += str(rnd.randint(0,9))
            for i in range(config.nSpecials):
                pwd += rnd.choice(config.specials)
    return pwd

pwd = gen_pwd()
print(f"Password length: {len(pwd)}")
while len(pwd) < config.pwd_minlen or len(pwd) > config.pwd_maxlen:
    pwd = gen_pwd()
print(pwd)
