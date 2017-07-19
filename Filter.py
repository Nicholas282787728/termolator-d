import logging
import pickle
import re
from nltk.corpus import stopwords  # not encumbered by license, see stopwords.readme()
from nltk.stem import PorterStemmer as Stemmer  # NLTK's license, Apache

from DataDef import File
from typing import Dict, List, Any
import dictionary

#
#   #semanticbeeng @todo global state : consider moving to dictionary.py
#
abbreviations: Dict[str, str] = {}
stops: List[str] = []
stemdict: Dict[str, str] = {}  # stemming dictionary
unstemdict: Dict[str, List[str]] = {}  # reverse stemming dictionary

#
stemmer = Stemmer()
logger = logging.getLogger()


#
#
#
def _get_abbreviations(file: File) -> None:
    """Import abbreviations from jargon file"""
    global abbreviations

    f = file.openText()
    for line in f.readlines():
        temp = line.split('|||')
        fullword = temp[0]
        shortwords = temp[1].split('||')
        for w in shortwords:
            abbreviations[w] = fullword

    abbreviations = dictionary.freeze_dict(abbreviations)       # @semanticbeeng @todo global state initialization
    f.close()


#
#
#
def _get_stops() -> None:
    """Import stop words either from a text file or stopwords corpus"""
    global stops
    import Settings
    filename=Settings.dir_name + 'patentstops.txt'

    if filename:
        f = File(filename).openText()
        for line in f.readlines():
            stops += line.split()
        f.close()
    else:
        stops = stopwords.words('english')


#
#
#
def _get_stemdict(filename: str) -> None:
    logger.debug('Loading stemming dictionary...')
    f = File(filename).openBin(mode='r')
    global stemdict
    global unstemdict
    stemdict, unstemdict = pickle.load(f)
    f.close()

    # stemdict = dictionary.freeze_dict(stemdict)           # @semanticbeeng @todo global state initialization : this fails
    unstemdict = dictionary.freeze_dict(unstemdict)         # @semanticbeeng @todo global state initialization


#
#
#
def _save_stemdict(filename: str) -> None:
    logger.debug('Saving stemming dictionary...')
    f = File(filename).openBin(mode='w')
    global stemdict
    global unstemdict
    pickle.dump((stemdict, unstemdict), f)
    f.close()


#
#
#
def _reGlue(words: List[str]) -> str:
    """Helper function to turn a list of words into a string"""
    ret = ""
    for i in range(len(words)):
        ret += words[i] + " "
    ret = ret.strip()
    return ret


#
#
#
def expand(string: str) -> str:
    """Expand abbreviations within string"""
    global abbreviations
    if not abbreviations:
        _get_abbreviations(File('./jargon.out'))
    words = string.split()
    for i in range(len(words)):
        temp = abbreviations.get(words[i])
        if temp:
            words[i] = temp
    string = _reGlue(words)
    return string


#
#
#
def removeStops(string: str) -> str:  # NOT NEEDED AS NP EXTRACTING REMOVES THEM
    """Strip stop words off the beginning and ending of a phrase"""
    global stops
    if not stops:
        _get_stops()
    # entire phrase in stops
    if string in stops:
        return ""
    words = string.split()
    if not words:
        return ""
    # beginning stops (loses case of multiword stops)
    while words[0] in stops:
        words.pop(0)
        if not words:
            return ""
    # ending stops (loses case of multiword stops)
    while words[-1] in stops:
        words.pop(0)
        if not words:
            return ""
    string = _reGlue(words)
    return string


#
#
#
def bad_unicode(string: str) -> bool:
    for char in string:
        if ord(char) > 127:
            print(char)
            return (True)
    return (False)      # @semanticbeeng @todo static typing


#
#
#
def remove_non_unicode(string: str) -> str:
    output = ''
    for char in string:
        if ord(char) > 127:
            output = output + ' '
        else:
            output = output + char
    output = output.strip(' ')
    return (output)


#
#
#
def stem(string: str) -> str:
    """Stem a phrase"""
    # global stemmer            # @semanticbeeng not used
    # if not stemmer:
    #     stemmer = Stemmer()
    # words = string.split()
    # for i in range(len(words)):
    #    words[i] = self.stemmer.stem(words[i])
    # stemming last word only
    # string = self._reGlue(words)
    #
    # string2 = stemmer.stem(string)
    # if string2 not in stemdict:
    #    stemdict[string2] = string
    # FIX ME
    if string not in stemdict:
        if bad_unicode(string):
            ## added A. Meyers 8/28/15
            string = remove_non_unicode(string)
            if len(string) > 3:
                temp = stemmer.stem(string)
            else:
                temp = string
        elif len(string) > 3:
            ## print('***',string,'***')
            temp = stemmer.stem(string)
        else:
            temp = string
        if temp:
            stemdict[string] = temp
        if not temp:
            pass
        elif temp not in unstemdict:
            unstemdict[temp] = [string]
        elif string not in unstemdict[temp]:
            unstemdict[temp].append(string)
    else:
        temp = stemdict[string]
    return temp


#
#
#
def unstem(string: str) -> List[str]:
    """Undo stemming of a phrase"""
    global stemdict
    # if string in stemdict:
    #    return stemdict[string]
    # else:
    #    return string
    if string in unstemdict:
        return unstemdict[string]
    else:
        return [string]


#
#
#
def lowercase(string: str) -> str:
    """Return an all lowercase representation of a string"""
    return string.lower()


#
#
#
def isWord(string: str) -> str:
    """Test the legitimacy of the proposed phrase. Taken from Shasha's implementation"""
    # criteria:
    pattern = re.compile(r"""
(
&lt
|%
|/
|\\
|&\ lt
|\)
|\(
|\.
|\+
|and\
|\ and
|\ and\
)
""", re.I | re.VERBOSE | re.UNICODE)
    if len(string) < 2:
        return ''
    elif re.findall(pattern, string):
        return ''
    # must contain at least one letter
    for i in range(len(string)):
        if string[i].isalpha():
            return string
    return ''


# available filters:
# @semanticbeeng @todo static typing: how to define a function type? F=(string: str) -> str
criteria: Dict[str, Any] = {
            'abbreviation': expand,
            'stops': removeStops,
            'stem': stem,
            'case': lowercase,
            'isWord': isWord}
