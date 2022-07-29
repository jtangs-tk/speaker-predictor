import sys
import math
import Hash_Table

HASH_CELLS = 57

def find_uniques(s):
        '''
        Given a string 's', finds the number of types of
        of characters used
        '''
        uniques = set()
        for letter in s:
            uniques.add(letter)
        
        return len(uniques)

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        self.k = k
        self.s = s
        self.hash_table = Hash_Table.Hash_Table(HASH_CELLS, 0)
        self.fill(self.s)

    def fill(self, s):
        '''
        Fills hash table with k-length sections of string s
        and k+1 length strings mapping to the number of times they appear
        '''
        new_string = s + s[0:self.k] # to make wrap-around easier
        for i in range(len(s)):
            sub1 = new_string[i:i+self.k]
            sub2 = new_string[i:i+self.k+1]

            M = self.hash_table.lookup(sub1)
            N = self.hash_table.lookup(sub2)

            self.hash_table.update(sub1, M + 1)
            self.hash_table.update(sub2, N + 1)


    def log_probability(self,s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences

        '''
        probabilities = []
        log_prob = 0
        S = find_uniques(self.s)

        new_string = s + s[0:self.k]
        for i in range(len(s)):
            sub1 = new_string[i:i+self.k]
            sub2 = new_string[i:i+self.k+1]
            M = self.hash_table.lookup(sub1)
            N = self.hash_table.lookup(sub2)
            prob = (M + 1) / (N + S)
            probabilities.append(prob)
                   
        return sum([math.log(prob) for prob in probabilities])


def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), 
    returns a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under an "order" 
    (character-based Markov model),
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    speaker_a = Markov(order, speech1)
    speaker_b = Markov(order, speech2)
    speech_length = len(speech3)

    likelihood1 = speaker_a.log_probability(speech3) / speech_length
    likelihood2 = speaker_b.log_probability(speech3) / speech_length

    if likelihood1 > likelihood2:
        return (likelihood1, likelihood2, 'Speaker A')
    else:
        return (likelihood1, likelihood2, 'Speaker B')


def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))
    print("Conclusion: Speaker " + conclusion + " is most likely")


if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "r") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "r") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "r") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)