#!/usr/bin/python
# docdist1.py - initial version of document distance
#
# Original version by Ronald L. Rivest on February 14, 2007
# Revision by Erik D. Demaine on September 12, 2011
#
# Usage:
#    docdist1.py filename1 filename2
#     
# This program computes the "distance" between two text files
# as the angle between their word frequency vectors (in radians).
#
# For each input file, a word-frequency vector is computed as follows:
#    (1) the specified file is read in
#    (2) it is converted into a list of alphanumeric "words"
#        Here a "word" is a sequence of consecutive alphanumeric
#        characters.  Non-alphanumeric characters are treated as blanks.
#        Case is not significant.
#    (3) for each word, its frequency of occurrence is determined
#    (4) the word/frequency lists are sorted into order alphabetically
#
# The "distance" between two vectors is the angle between them.
# # If x = (x1, x2, ..., xn) is the first vector (xi = freq of word i)
# # and y = (y1, y2, ..., yn) is the second vector,
# # then the angle between them is defined as:
# #    d(x,y) = arccos(inner_product(x,y) / (norm(x)*norm(y)))
# # where:
# #    inner_product(x,y) = x1*y1 + x2*y2 + ... xn*yn
# #    norm(x) = sqrt(inner_product(x,x))

import math
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.
#from collections import OrderedDict
from sortedcontainers import SortedDict
import sys
import string

##################################
# Operation 1: read a text file ##
##################################
def read_file(filename):
    """ 
    Read the text file with the given filename;
    return a list of the lines of text in the file.
    """
    try:
        f = open(filename, 'r')
        return f.read()
    except IOError:
        print ("Error opening or reading input file: ",filename)
        sys.exit()

#################################################
# Operation 2: split the text lines into words ##
#################################################
def get_words_from_line_list(L):
    """
    Parse the given list L of text lines into words.
    Return list of all words found.
    """
    word_list = []
    for line in L:
        words_in_line = get_words_from_string(line)
        word_list += words_in_line
    return word_list

translation_table = str.maketrans(string.punctuation + string.ascii_uppercase,
                                     " "*len(string.punctuation) + string.ascii_lowercase)

def get_words_from_string(line):
    """
    Return a list of the words in the given input string,
    converting each word to lower-case.

    Input:  line (a string)
    Output: a list of strings 
              (each string is a sequence of alphanumeric characters)
    """
    line = line.translate(translation_table)
    word_list = line.split()
    return word_list
##############################################
# Operation 3: count frequency of each word ##
##############################################
def count_frequency(word_list):
    """
    Return a list giving pairs of form: (word,frequency)
    """
    D = {}
    for new_word in word_list:
        if new_word in D:
            D[new_word] += 1
        else:
            D[new_word] = 1
    return D

###############################################################
# Operation 4: sort words into alphabetic order             ###
###############################################################

#########################################
## compute word frequencies for input file ##
#############################################
def word_frequencies_for_file(filename):
    """
    Return alphabetically sorted list of (word,frequency) pairs 
    for the given file.
    """
    line_list = read_file(filename)
    word_list = get_words_from_line_list(line_list)
    freq_mapping = count_frequency(word_list)
    freq_mapping = dict(SortedDict(freq_mapping).items())

    print("File",filename,":",)
    print(len(line_list),"lines,",)
    print(len(word_list),"words,",)
    print(len(freq_mapping),"distinct words")

    return freq_mapping

def inner_product(D1,D2):

    """
    Inner product between two vectors, where vectors
    are represented as lists of (word,freq) pairs.

    Example: inner_product([["and",3],["of",2],["the",5]],
                           [["and",4],["in",1],["of",1],["this",2]]) = 14.0 
    """
    sum = 0.0
    for key in D1:
        if key in D2:
            sum += D1[key] * D2[key]
    return sum

def vector_angle(D1,D2):
    """
    The input is a list of (word,freq) pairs, sorted alphabetically.

    Return the angle between these two vectors.
    """
    numerator = inner_product(D1,D2)
    denominator = math.sqrt(inner_product(D1,D1)*inner_product(D2,D2))
    return math.acos(numerator/denominator)

def main():
    if len(sys.argv) != 3:
        print ("Usage: docdist1.py filename_1 filename_2")
    else:
        filename_1 = sys.argv[1]
        filename_2 = sys.argv[2]
        sorted_word_list_1 = word_frequencies_for_file(filename_1)
        sorted_word_list_2 = word_frequencies_for_file(filename_2)
        distance = vector_angle(sorted_word_list_1,sorted_word_list_2)
        print ("The distance between the documents is: %0.6f (radians)"%distance)

if __name__ == "__main__":
    import profile
    profile.run("main()")

    
    



