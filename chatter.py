
# wayne warren 2017 - 19
import shelve
import random
from time import asctime
from nltk.tag import pos_tag
from nltk import word_tokenize

# for building a sentence
from nltk.parse.generate import generate # trying out grammar based on usr
from nltk import CFG

# for concordance test
from nltk.text import Text

# for syns and defs
from nltk.corpus import wordnet

# using tagset='universal' throughout when tagging grammar types, makes positions txt easier to read but also means
# punctuation is classified too (as a dot) instead of being recorded as it is.(read help(nltk.tag.mapping))
# Also think about tagging sentences as a whole for better accuracy.

# reduce as much use of random as pos. search 'todo' for places where this can be done or to add things.

# todo, function words mean combining a search,
# i.e 'when' > herbie_replies.append( self.find_natural(noun, num) ). if 'when' in usr, search num and noun (or what was after 'the') etc.
class Chatter(object):

    def __init__(self):

        # herbie's reply
        self.say = ""

        # commands are checked before conversing normally, add more later
        self.commands = ["/define", "/time", "/undo"]
        
        # a sample of the basic types, used for creating lists of these types from associated files
        self.types_universal = ['verb','noun','pron','adj','adv','adp','conj','det','num','prt','x','.'] #_UNIVERSAL_TAGS in nltk\\tag\\mapping.py
        self.types_file = ["noun","verb","adverb", "adjective"] # used once for files of that type.
        # try and get them all from wordnet by type.
        self.punctuation = [".",",","!","?","-",";"]
        self.conj = ["and", "but", "or","if","because","until", "while", "although"]
        self.part = ["at","on","out","that","up","with"]
        self.adpos = ["on","of","at","with","by","into","under"]
        self.pronouns = ["he","their","her","its","my","i","us"]
        self.det = ["the","a","an","another","no","some","any","my","our","their","her","his","its","each","every","this","that"]
        
        # lines in each testwords file
        self.adjective_len = 0
        self.adverb_len = 0
        self.noun_len = 0
        self.verb_len = 0

        # text files for randwords
        self.adjectives_file_words = []
        self.adverbs_file_words = []
        self.verbs_file_words = []
        self.nouns_file_words = []

        #
        self.recent_pos_store = ""
        # to use key words from recent user replies or check if herbie reply is the same
        self.session_said_natural = []
        self.count_session_said_natural = 0

    def get_dict(self, words_list):
        """Make a dictionary containing word types as keys that store the words in a list"""
        user_reply_dict = {}
        for w in words_list:
            word_type = self.find_type(w)
            try:
                user_reply_dict[word_type] += [w]
            except KeyError:
                #print ("chatter.py get_dict():no such key, creating one for the first time")
                user_reply_dict[word_type] = []
                user_reply_dict[word_type] += [w]
                
        return user_reply_dict

    def concordance_test(self, word):
        """Build or get text source and change to list"""
        sentence_string = "just a place holder for a book or something. worth doing"
        textList = sentence_string.split(".")
        text = Text(textList)
        text.concordance(word)

    def grammar_check(self, sentence):
        """so self.say is set, a sentence has been found or created,
        time to help it make sense"""  
        pass

    def get_testwords_file_lengths(self):
        """Record the length of the text files that contain lists of words of each type."""
        for t in self.types_file:
            file_choice = open("test_words/"+t+".txt")
            length = len(file_choice.readlines())
            if t == "noun":
                self.noun_len = length
            if t == "verb":
                self.verb_len = length
            if t == "adverb":
                self.adverb_len = length
            if t == "adjective":
                self.adjective_len = length

    def buld_wordTypes_rand(self):
        """Creates a list for each word type  from the files
        provided."""
        adj_file_words = open("test_words/adjective.txt")
        self.adjectives_file_words = adj_file_words.readlines()
        adj_file_words.close()
        
        adv_file_words = open("test_words/adverb.txt")
        self.adverbs_file_words = adv_file_words.readlines()
        adv_file_words.close()
        
        ver_file_words = open("test_words/verb.txt")
        self.verbs_file_words = ver_file_words.readlines()
        ver_file_words.close()
        
        nou_file_words = open("test_words/noun.txt")
        self.nouns_file_words = nou_file_words.readlines()
        nou_file_words.close()

    # todo build a similar method to this, that uses the concordance method to find a common word used in place or near it. 
    def get_rand_word(self, gtype):
        """If herbie decides to use a random word it can use this method
        to provide a random word of that type from the lists made in buld_wordTypes_rand."""
        randword = "temporary"
        
        if gtype == "noun":
            length = self.noun_len
            randword = self.nouns_file_words[random.randint(0,length)].strip("\n")
        if gtype == "verb":
            length = self.verb_len
            randword = self.verbs_file_words[random.randint(0,length)].strip("\n")
        if gtype == "adv":
            length = self.adverb_len
            randword = self.adverbs_file_words[random.randint(0,length)].strip("\n")
        if gtype == "adj":
            length = self.adjective_len
            randword = self.adjectives_file_words[random.randint(0,length)].strip("\n")
        if gtype == "conj":
            randword = random.choice(self.conj)
        if gtype == "det":
            randword = random.choice(self.det)
        if gtype == "adp":
            randword = random.choice(self.adpos)
        if gtype == "num":
            randword = str(random.randint(0,101))   
        if gtype == "prt":
            randword =  random.choice(self.part)
        if gtype == "pron":
            randword =  random.choice(self.pronouns)
        if gtype == ".":
            randword =  random.choice(self.punctuation)
                     
        return randword
    
    def query_input(self, user_say):
        """Ask the user what the word means. Doing this helps build the natural.db, (hopefully the reply is related
        to the word asked about)"""
        ask = "What is '" + user_say + "'?"
        # todo 1:1 QA what db [Q][ans] so next time it can be searched with the right words if "?" is supplied.
        return ask
        
    def get_random(self):
        print("chatter.py get_random() couldnt form anything related, so here we are. random sentence below;")
        rand_gram = self.get_rand_word( "det")
        rand_gram += " "
        rand_gram += self.get_rand_word( "adj")
        rand_gram += " "
        rand_gram +=  self.get_rand_word( "noun")
        return rand_gram
        
    def save_natural_db(self, user_say):
        """Store what the user replied with in
        the natural.db."""
        sentence = shelve.open("natural", writeback=True)
        user_say_string = " ".join(user_say)
        
        # each word is now a key pointing to a list of sentences that use
        # that word.
        if user_say[0] not in self.commands: #recent test. dont save commands to herbie, they are different. 
            for word in user_say:
                try:
                    sentence[word] += [user_say_string]
                    sentence[word] = list(set(sentence[word]))
                except KeyError:
                    print("chatter.py save_natural_db():no such key, creating one for the first time")
                    sentence[word] = []
                    sentence[word] += [user_say_string]
                    sentence[word] = list(set(sentence[word]))
                
        sentence.close()

    def find_natural(self, word, wordTwo=None):
        """Find a sentence in the natural.db with the word given to use as a reply,
        ( used by get_natural ) Optionally supply an added word to search with
        the original search word key"""
        match = "(0_0)"
        sentences = shelve.open("natural", writeback=True)

        # only check prev input if there's at least one entry
        session_stored = False
        if len(self.session_said_natural) > 0:
            session_stored = True
            
        # go through db
        key_exists = False
        try:
            sentences[word]
            key_exists = True    
        except KeyError:
            print("chatter.py find_natural(): expected key error, just want to know if i can access this key...")
            
        if key_exists:
            for sentn in sentences[word]:
                # if wordTwo has a len find it in sent n with original word as key
                if wordTwo:  
                    if wordTwo in sentn:
                        if session_stored and sentn != self.session_said_natural[-1]: # only look at latest reply
                            match = sentn
                            break
                        if not session_stored:
                            # no prev user replies to compare to
                            match = sentn
                            break
                else:
                    if session_stored and sentn != self.session_said_natural[-1]: # only look at latest reply
                        match = sentn
                        break
                    if not session_stored:
                        # no prev user replies to compare to
                        match = sentn
                        break
                
            # finally an expensive shuffle, todo or find a way to make sure sentn is the first element in sentences[word], a kind of
            # contextual ordering... either way, try and remove use of random later.
            tmp = sentences[word]
            random.shuffle(tmp)
            sentences[word] = tmp
            tmp = []
            sentences.close()

        # keep track of what was said, dont repeat too much
        if len(match) > 0 and match != "(0_0)":
            self.session_said_natural += [match] #; print("Match #########:" + match)
        return match

    def get_natural(self, words_list):
        """Uses the natural database to get user replies to reply with
        calling find_natural() to acess the db with a word""" 
        user_reply_dict = self.get_dict(words_list)        
        user_reply_keys = user_reply_dict.keys()
        print(user_reply_keys)
        herbie_replies = []
        
        # helper method to get sentences containing other word types incase sentences with focus noun not found
        def try_next_wordType(wtype):
            if wtype in user_reply_keys:
                for word in user_reply_dict[wtype]:
                    herbie_replies.append( self.find_natural(word) )
            return len(herbie_replies)
        
        # order of word types matters, preference is to reply with a focus on a noun over replying
        # with a focus on a conjunction...
        if "noun" in user_reply_keys:
            w_list = user_reply_dict["noun"] # for second arg in find_natural
            for word in user_reply_dict["noun"]:
                w_list.remove(word)
                if len(w_list) > 0:
                    herbie_replies.append( self.find_natural(word, w_list.pop() ))
                else:
                    herbie_replies.append( self.find_natural(word ))

        ### after that if herbie_replies is empty try these
        reply_len = len(herbie_replies)
        for tag in self.types_universal:
            reply_len = try_next_wordType(tag)
            if reply_len > 0:
                print("chatter.py get_natural alternate type used: " + tag)
                break
  
        # add preference here, random or specific kinds of sentences
        print("chatter.py get_natural(self, words_list); herbie_replies list below:")
        print (herbie_replies)
        return herbie_replies
        
    def find_type(self, word):
        """Classify a word by its grammar type."""
        # put single word in list form so the string isnt split into letters
        tagged_word = pos_tag([word], tagset='universal') 
        obj_type = tagged_word[0][1] # from L of tuples, 2nd is type
        
        if len(obj_type) < 1:
            return "err"
        else:
            return obj_type.lower() # tags are capitalized.

    def get_synonym(self, word):
        """Find a similar word to the one supplied."""
        syns = wordnet.synsets(word)
        if len(syns) > 0:
            alt_list = (syns[0].lemmas())
            lem = []
            if len(alt_list) > 1:
                lem = alt_list[1] # or select from if many
                synonym = lem.name()
                tp = type(synonym)
                if tp.__name__ == 'str':
                    #print ("syn: " + synonym + "\n")
                    return synonym
                else:
                    return "err"
        else:
            return "err"

    def get_synonym_group(self, word):
        """Find a similar set of words to the one supplied."""
        syns = wordnet.synsets(word, lang='eng')
        syn_list = []
        
        if len(syns) > 0:
            for i in range(len(syns)):
                syn = syns[i].name()
                syn = syn[0:syn.find(".")]
                if syn != word:
                    syn_list.append(  syn)
            
            return syn_list

    # pass only stronger words to this, like nouns and pronouns, not conj or numbers etc.
    def get_partial_rand(self, words_list):
        """This is where stored user patterns from positions.txt are used
           for a grammar that has word types similar to the grammar of the words supplied."""
        #(dont use last of session said, that's the word_list in str form use one just before
        # to mix things up. session_said_natural[-2]. this session stuff is optional, everything below it is what the prog did before.
        session_store = False
        session_prev_dict = {}
        if len(self.session_said_natural) > 1:
            session_store = True
        if session_store:
            session_prev_dict = self.get_dict(self.session_said_natural[-2].split(" "))

        # normal behaviour 
        user_reply_dict = self.get_dict(words_list)        
        user_reply_keys = user_reply_dict.keys()
        
        ## count word types
        user_type_count = {}
        total_words = len(words_list)
        for key in user_reply_keys:
            user_type_count[key] = len( user_reply_dict[key] )

        ## count types in each line of positions.txt, look for same count of focus types for each line then stop.
        # todo len(pos_lines[x]) look for greater than, but not by too much, then herbie shouldnt have to guess a whole lot.
        pos_file = open("positions.txt", "r")
        pos_lines = pos_file.readlines()
        random.shuffle(pos_lines) # todo less rand.
        pos_file.close()
        
        partial_match = ""
        match_found = False
        for x in range(len(pos_lines)):
            key_passed = 0
            for key in user_type_count:
                key_count = pos_lines[x].count(key.upper())
                if key_count == user_type_count[key]:
                    key_passed += 1

            if key_passed == len( user_type_count.keys() ) and pos_lines[x] != self.recent_pos_store+"\n":
                    #print(pos_lines[x] +"*******"+self.recent_pos_store)
                    partial_match = pos_lines[x] # todo store each match instead of break, then loop match_found case
                    match_found = True
                    break

        mock_sentence = ""        
        if match_found:
            
            print("chatter.py get_partial_rand() partial_match: " + partial_match)
            partial_match=partial_match.replace("\n", "")
            self.recent_pos_store = ""
            
            for typ in partial_match.split(":"):

                if typ.lower() in user_reply_dict.keys():
                    lst = user_reply_dict[ typ.lower() ]
                    mock_sentence += lst.pop()
                    user_reply_dict[ typ.lower() ] = lst
                    mock_sentence += " "
                    
                elif session_store == True and typ.lower() in session_prev_dict.keys():
                    lst = session_prev_dict[ typ.lower() ]
                    if len(lst) > 0:
                        mock_sentence += lst.pop()
                        session_prev_dict[ typ.lower() ] = lst
                        mock_sentence += " "
                    else:
                        # to prevent coming to this condition again.
                        #(session_store is likely true still anyway, but the list in session dict has been used up)
                        session_store = False
                        
                    
                else:
                    mock_sentence += self.get_rand_word( typ.lower() ) # todo less rand, conc.
                    mock_sentence += " "

            print("chatter.py get_partial_rand() mock sentence: " + mock_sentence)
        return mock_sentence
        
            
    def get_full_artificial(self, words_list):
        """A test method for creating a sentence based on user input..."""
        #(dont use last of session said, that's the word_list in str form, use the one just before
        # to mix things up. session_said_natural[-2]. this session stuff is optional, everything below it is what the prog did before.
        session_store = False
        session_prev_dict = {}
        if len(self.session_said_natural) > 1:
            session_store = True
        if session_store:
            session_prev_dict = self.get_dict(self.session_said_natural[-2].split(" "))

        # normal below, as before...
        herbie_reply = ""
        
        # try and fill the grammar structure in with related words
        meaning_pairs = []
        for word in words_list:
            pair_define = [self.find_type(word), word]
            meaning_pairs.append(pair_define)
            
        meaning_pairs_copy = meaning_pairs[:]
        
        # fill the test grammar with synonyms and related words from usr. Grammar can be doc str
        # or list of strings. fill in what we can in each list element (string of grammar type)
        # replacing hash with a relevant word. todo add pronouns and adverbs. todo make other basic grammar rules if this one cant be filled. 
        test_gram = ["S -> NP VP",
        "NP -> Det N",
        "PP -> P NP",
        "VP -> '#'",            # slept e.g - verb
        "VP -> '#' NP",         # saw e,g
        "VP -> '#' PP",         # walked e.g
        "Det -> '#'",           # the e.g  - article/determiner
        "Det -> '#'",           # a e.g
        "N -> '#'",             # man e.g - noun
        "N -> '#'",             # park e.g
        "N -> '#'",             # dog e.g
        "P -> '#'",             # in e.g - preposition
        "P -> '#'"]             # with e.g

        #print(test_gram[3:]) # ignore base structure rules, just filling in the rest, so from 3...
        # PASS ONE. fill as many as possible
        nouns_filled = 0; verbs_filled = 0
        part_copy = self.part[:]; det_copy = self.det[:]; det_copy.remove("an")
        #                                                                                          from *3* is to skip the first 3 elements in test_Gram (they dont need to be filled)****
        for i in range(3, len(test_gram) ):
            #print(test_gram[i])
            if "VP" in test_gram[i] and "#" in test_gram[i]:
                #print(test_gram[i])
                for j in range(len(meaning_pairs)):
                    if meaning_pairs[j][0] == "verb":
                        test_gram[i] = test_gram[i].replace("#", meaning_pairs[j][1])
                        del meaning_pairs[j]
                        verbs_filled += 1
                        break

            if test_gram[i] == "N -> '#'":
                for j in range(len(meaning_pairs)):
                    if meaning_pairs[j][0] == "noun" :
                        test_gram[i] = test_gram[i].replace("#", meaning_pairs[j][1])
                        del meaning_pairs[j]
                        nouns_filled += 1
                        break
                    
            if "Det" in test_gram[i] and "#" in test_gram[i]:
                for j in range(len(meaning_pairs)):
                    if meaning_pairs[j][0] == "det" :
                        test_gram[i] = test_gram[i].replace("#", meaning_pairs[j][1])
                        del meaning_pairs[j]
                        break
                    else:
                        detn = random.choice(det_copy)
                        det_copy.remove(detn)
                        test_gram[i] = test_gram[i].replace("#", detn)

        
            if test_gram[i] == "P -> '#'":
                part = random.choice(part_copy) # todo less rand. run concordance of verbs and nouns found and use prepositions most commonly associated with those words.
                part_copy.remove(part)
                test_gram[i] = test_gram[i].replace("#", part)

        # PASS TWO. fill gaps
        # filling nouns... check if synonyms are also nouns a bit later
        if nouns_filled > 0 and nouns_filled < 3:
            syns_num = 3 - nouns_filled
            nouns_extra = []
            for pair in meaning_pairs_copy:
                if pair[0] == "noun":
                    nouns = self.get_synonym_group( pair[1] )
                    if nouns:
                        nouns_extra += nouns

            nouns_extra = list(set(nouns_extra))
            
            if len(nouns_extra) >= syns_num:
                for i in range(3, len(test_gram) ):
                    if test_gram[i] == "N -> '#'":
                        test_gram[i] = test_gram[i].replace("#", nouns_extra.pop())
                        nouns_filled += 1
            else:
                if session_store == True and "noun" in session_prev_dict.keys(): # try other session if fail later
                    if nouns_filled < 3:
                        for i in range(3, len(test_gram) ):
                            if test_gram[i] == "N -> '#'":
                                lst = session_prev_dict["noun"]
                                if len(lst) > 0:
                                    noun = lst.pop()
                                    session_prev_dict["noun"] = lst
                                    test_gram[i] = test_gram[i].replace("#", noun)
                                    nouns_filled += 1
                        
        print("\n\n###################################################")
        # filling verbs... check if synonyms are also verbs a bit later
        if verbs_filled > 0 and verbs_filled < 3:
            syns_num = 3 - verbs_filled
            verbs_extra = []
            for pair in meaning_pairs_copy:
                if pair[0] == "verb":
                    verbs = self.get_synonym_group( pair[1] )
                    if verbs:
                        verbs_extra += verbs

            verbs_extra = list(set(verbs_extra))
            
            if len(verbs_extra) >= syns_num:
                for i in range(3, len(test_gram) ):
                    if "VP" in test_gram[i] and "#" in test_gram[i]:
                        test_gram[i] = test_gram[i].replace("#", verbs_extra.pop())
                        verbs_filled += 1

            else:
                if session_store == True and "verb" in session_prev_dict.keys(): # try other session if fail later
                    if verbs_filled < 3:
                        for i in range(3, len(test_gram) ):
                            if "VP" in test_gram[i] and "#" in test_gram[i]:
                                lst = session_prev_dict["verb"]
                                if len(lst) > 0:
                                    verb = lst.pop()
                                    session_prev_dict["verb"] = lst
                                    test_gram[i] = test_gram[i].replace("#", verb)
                                    verbs_filled += 1

        # apply the grammar
        if nouns_filled == 3 and verbs_filled == 3:
            grammar = CFG.fromstring(test_gram)
            replies = []
            for sentence in generate(grammar, depth=4):
                print ("artificial reply: " +  ' '.join(sentence))
                replies.append(' '.join(sentence))

            # temp. todo see if removing repeat words first and increasing depth before gets a better reply.
            herbie_reply = max(replies)
            #print ("TEST: " + herbie_reply)

        else:
            herbie_reply = "err"
            
        return herbie_reply

    def parse_command(self, command_string, word):
        """answer only to a command and skip all sentence creation"""
        # todo time
        herbie_reply = ""

        if command_string == "/define" and len(word) > 0:
            syns = wordnet.synsets(word)
            if len(syns) > 0:
                herbie_reply = syns[0].definition()
        if command_string == "/time": herbie_reply = asctime()
        if command_string == "/undo": pass # todo it would have to use session_said[-1] word keys and remove session_said[-1] sentences from those keys.
        #print("cmd reply: " + herbie_reply)
        return herbie_reply
    
    def get_pos_tags(self, words):
        """Make a list of grammar types in the order they are found in a sentence and return the result."""
        pos_tags = []
        text = word_tokenize(words)
        #tagged_text = pos_tag(text)
        pos_tags = [pos for (token,pos) in pos_tag(text, tagset='universal')]
        return pos_tags
    
    def store_word_position(self, words):
        """This method stores the grammar patterns of sentences input by the user for get_partial_rand(list_words)."""
        pos_tags_store = self.get_pos_tags(words)
        tags_save = ":".join(pos_tags_store)
        # get previous lines written so as not to repeat
        pos_file = open("positions.txt", "r")
        pos_lines = pos_file.readlines()
        pos_file.close()
        # time to write
        positions_file = open("positions.txt", "a")
        
        if len(pos_lines) == 0:
            positions_file.write(tags_save+"\n")
            
        else:
            already_stored = False
            
            for x in range(len(pos_lines)):
                if pos_lines[x] == tags_save+"\n":
                    already_stored = True
                    
            if already_stored == False:
                positions_file.write(tags_save+"\n")
                self.recent_pos_store = tags_save
                    

        positions_file.close()

    def format_reply(self, reply):
        """Format sentence for the final reply."""
        # todo needs to handle len of 0 etc later
        herbie_reply = reply
        herbie_reply = herbie_reply[0].upper() + herbie_reply[1:]
        if herbie_reply[-1] == " ":
            herbie_reply = herbie_reply[0:-1] + "."
        else:
            herbie_reply += "."

        # no underscore
        herbie_reply = herbie_reply.replace("_", " ")
        return herbie_reply

    def format_wordsIn(self, words_str):
        """Make changes to words so that they are classified correctly."""
        w_str = words_str
        if " i " in words_str: w_str = w_str.replace(" i ", " I ")
        # adding an extra space helps make sure they are list elements when split is called later and for nltk tagging.
        if w_str[-1] == "?": w_str = w_str[:-1] + " ?"
        if w_str[-1] == "!": w_str = w_str[:-1] + " !" 
        return w_str

    def lets_chat_gui(self, words_in):
        """This is where all the methods above are put in use and where decisions are made, all to form a reply. The only
        method used by main.py."""
        self.say = ""
        
        string_words = self.format_wordsIn(words_in)
        list_words = string_words.split() # make sure the changes are reflected in the new list

        # record grammar ordering of the sentence using pos tags / indicates a command
        if string_words[0] != "/": self.store_word_position(string_words)
            
        # update natural speech database for use later.
        self.save_natural_db(list_words)

        # call to get_artifical
        def artificial(list_words):
            reply = self.get_full_artificial(list_words)
                
            if reply == "err":
                # dont ask what an entire sentence means, just single words
                if len(list_words) == 1:
                    print("C4")
                    action_temp = ["ask", "rand"]
                    action = random.choice(action_temp) # todo less rand
                    if action == "ask":
                        self.say = self.query_input(string_words)
                    else:
                        self.say = self.get_partial_rand(list_words) # still valid with a list with 1 element
            else:
                print("D")
                print("used artifical: ")
                self.say = reply
                
            
        ####################################### decision branching starts here #####################################
        # commands for herbie, shouldnt be too many.
        if list_words[0] in self.commands:
            if len(list_words) == 2:
                self.say = self.parse_command(list_words[0], list_words[1])
                # if there is no definition...    
                if len(self.say) == 0:
                    self.say = self.query_input(list_words[1])
            elif len(list_words) == 1:
                self.say = self.parse_command(list_words[0], "nothing")

            
            
        else:
            
            # normal behaviours
            nat_list = self.get_natural(list_words)
            nat_list = list(set(nat_list))
            
            if len(nat_list) > 0:
                
                # pick from others if > 1
                if len(nat_list) == 1:
                    # get_natural returned usr string back, meaning it just made keys for it but found nothing in natural.db
                    if nat_list[0] == string_words: # string form of list_words
                        # dont ask what an entire sentence means, just what single words are
                        if len(list_words) == 1:
                            action_temp = ["ask", "rand"]
                            action = random.choice(action_temp) # todo if not in natural db, ask.
                            if action == "ask":
                                print("A1")
                                self.say = self.query_input(string_words)
                            else:
                                print("A2")
                                self.say = self.get_partial_rand(list_words) # still valid list with 1 entry
                                
                        else:
                            print("A3")
                            self.say = self.get_partial_rand(list_words)
                            if len(self.say) == 0 or self.say == "temporary":
                                artificial(list_words)
                                
                    else:
                       
                        print("B")
                        self.say = nat_list[0] 

                        
                if len(nat_list) > 1:
                    # if len > 1 usr strings that are the same can be removed or replaced by something
                    # that indicates it should be ignored.(0_0)... to stop repeating what was typed right back at usr
                    for i in range(len(nat_list)):
                        #print(nat_list[i])
                        if nat_list[i] == string_words:
                            nat_list[i] = "(0_0)"
                            
                    print(nat_list)
                    # choose from good answers. ignoring '(0_0)'
                    nat_choices = []
                    for nat in nat_list:
                        if nat != "(0_0)":
                            nat_choices += [nat]
                    
                    if len(nat_choices) > 0:
                        print("C1")
                        self.say = random.choice(nat_choices) # todo less rand... add scoring to value more relevant replies
                        
                    else:
                        print("C2")
                        artificial(list_words)
                    
            else:
                # len(nat_list) == 0. That means 'self.get_natural(list_words)' yielded no results, so try other stuff.
                # replying with a number to a number is temporary.
                if self.find_type(list_words[0]) == "num":
                    print("C2b")
                    self.say = self.get_rand_word("num")
                else:
                    print("C3")
                    artificial(list_words)
                
        ## no real answer found this is where to try the concordance method and fall back
        # to randomness
        if len(self.say) == 0 or self.say == "(0_0)":
            print("E")
            self.say = self.get_partial_rand(list_words)
            if len(self.say) == 0:
                print("F")
                self.say = self.get_random()
                    
        print("final say:(" + self.say +")")
        
        # neaten reply
        if len(self.say) > 0:
            self.say = self.format_reply(self.say)
        else:
            print("G")
            self.say = "Test message: could not form sentence."

        # after a while i can repeat myself
        if self.count_session_said_natural == 10:
            self.session_said_natural = []
            self.count_session_said_natural = 0

        self.count_session_said_natural += 1
        
        return self.say
