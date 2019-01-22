Dictionary Password generator
=============================



This is a simple Python script, that takes in your favourite aspell dictionary and generates a random password from it.

You could also easily use any list of words to randomly pick from if you prefer. Depending on my requirements for my dictionary, I typically get around 50k words to pick from.
Adding a couple of random digits and special characters, and adding randomized upper characters, I think the entropy quickly becomes large enough for most normal use cases with 2-3 words

You should select the dictionary from a language you are not easily associated with (and avoid English which I think is the most commonly used)

You could increase entropy by adding numbers and/or special characters in random places of the password rather than between each word.

Please report any issues if you deem this to be in any way an unsafe way to generate a password.

## Requirements

- This has only been tested on Linux but should work well on OSX. 
- Python 3 syntax (should work with Python 2 as well I think, replace the secrets module with random)
- aspell and the dictionary of choice (e.g. aspell-is) must be installed
