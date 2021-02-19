# POSSIBLE FUNCTIONS IN THIS FILE ARE:
#
# QUERYDATABASE
#       INPUT: query,database from which it comes. Returns normal results as seen in esystant
#       OUTPUT: result from that query
# QUERY
#       INPUT: localhost,root,password,database,query
# GROUPBYUSER
#       INPUT: output from one of the afformentioned query functions
#       OUTPUT: dictionary with per user, all of the data in a 2-D array. (so per user)
# TESTBASE
#       INPUT: Output from groupybyuser() call
#       OUTPUT: the first TEST_PERCENTAGE Of the users and their respective information. (set to 0.9 normally)
# VERIFICATIONBASE
#       INPUT; Same as above
#       OUTPUT: the other TEST_PERCENTAGE of the users.
#
#

# First thing we're going to do is just writing a function to fetch data. We write two: One given just a query and a
# database,  one more detailed with host info

# Ook in deze file weer belangrijk dat we de naam van databases en passwoord matchen


# https://stackoverflow.com/questions/12988351/split-a-dictionary-in-half
# Easy function. Just takes the first 90% Of the users.
# For easy measure, change variable TEST_PERCENTAGE
def testBase(d):
    return dict(list(d.items())[:int(len(d) * TEST_PERCENTAGE)])


def verificationBase(d):
    return dict(list(d.items())[int(len(d) * TEST_PERCENTAGE):])


TEST_PERCENTAGE = 0.9
VERIFICATION_PERCENTAGE = 1 - TEST_PERCENTAGE

