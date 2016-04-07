import random

def getWordList(filePath):
        """Reads file from filePath and returns the list of words. Returns 0 if there IO error"""
        wordlist = 0
        try:
                infile=open(filePath,'r')
                wordlist=infile.readlines()
                infile.close()
        except:
                print("Something went wrong, can not process file at path {}".format(filePath))
        return wordlist

def processFile(wordList):
        """ Create dicitonary with length as key and list of words with that specific length as values """
        lenToWord = {}
        for item in wordList:
                item = item.strip().lower()
                if len(item) in lenToWord:
                        lenToWord[len(item)].append(item)
                else:
                        lenToWord[len(item)] = [item]
        return lenToWord

def displayWelcomeMessage():
        """ Displays the welcome message for the game """
        welcomeMessage = 'Hello...Welcome to Evil Hangman Game...\n'
        rules = "some rules"
        print(welcomeMessage)
        print(rules)

def checkLetterInput(letter,alreadyGuessed):
        toReturn = True
        """ Checks the letter entered by the user for its validity """
        if len(letter) > 2:
                print("Enter Single Engligh Alphabet Only")
                toReturn = False
        elif letter.lower() not in 'abcdefghijklmnopqrstuvwxyz':
                print("Enter Single Engligh Alphabet Only")
                toReturn = False
        elif letter in alreadyGuessed:
                print("Letter already guessed")
                toReturn = False
        return toReturn

def getPosition(word,letter):
        """ Returns the tuple of indices where the letter is found in the word """
        return tuple(i for i, ch in enumerate(word) if letter == ch)

def updatePattern(maxKey,letter,patternTillNow,secretWordLength):

        """ Updates the pattern till now """
        
        dashes = "_" * secretWordLength
        dashList = list(dashes)
        for i in maxKey:
                dashList[i] = letter
        dashes = ""
        dashes=dashes.join(dashList)
        newPattern = ""
        for i in range(len(patternTillNow)):
                if dashes[i] == "_" and patternTillNow[i] == "_":
                        newPattern += "_"
                elif dashes[i] != "_":
                        newPattern += letter
                else:
                        newPattern += patternTillNow[i]
        return newPattern

def incorrectLetterChoice(incorrectGuessesCount,looseCount,maxIncorrectGuesses,secretWordList):
        lost = False
        print("Incorrect Guess")
        incorrectGuessesCount+=1
        print("You have made {} incorrect guesses".format(incorrectGuessesCount))
        if incorrectGuessesCount > 8:
                print("You were not able to guess the correct answer")
                print("Correct Word is {}".format(secretWordList[0]))
                looseCount += 1
                lost = True
        if not lost:
                print("You can make {} more incorrect guesses".format(maxIncorrectGuesses - incorrectGuessesCount))
        return(incorrectGuessesCount,looseCount,lost)

def displayStatistics(winCount,looseCount):

        """ Displays statistics of the game """
        
        print("Statistics: Total Game: {} Wins: {} Loose: {}".format(winCount + looseCount,winCount,looseCount))

def TwistedHangman():
        """ This function Starts and Controls the Game """
        wordList = getWordList('dictionary.txt') #Reading File
        if wordList == 0:
                return
        lenToWord  = processFile(wordList) #Processing File
        displayWelcomeMessage() # Display welcome message
        dictionaryKeys = [i for i in lenToWord.keys()]
        noOfKeys = len(dictionaryKeys)
        winCount = 0
        looseCount = 0
        
        while True:
                # Setting up to play the game
                wordLengthIndex = random.randint(0,noOfKeys-1)
                secretWordLength = dictionaryKeys[wordLengthIndex]
                secretWordList = lenToWord[secretWordLength]
                patternTillNow = "_" * secretWordLength

                maxIncorrectGuesses = 8
                incorrectGuessesCount = 0
                
                alreadyGuessed = []
                lettersToBeGuessed = None

                while True:
                        # Playing the game
                        letter = input("Guess A letter: ")
                        letter = letter.strip().lower()  # Sanitizing for extra white spaces
                        letterCheckPassed = checkLetterInput(letter,alreadyGuessed)
                        if not letterCheckPassed:
                                continue
                        alreadyGuessed.append(letter)
                        
                        if len(secretWordList) != 1: # Still Playing Twisted Hangman
                                pattern = {}
                                # Generating Pattern Groups Here
                                for word in secretWordList:
                                        positionalPattern = getPosition(word,letter)
                                        if positionalPattern in pattern:
                                                pattern[positionalPattern].append(word)
                                        else:
                                                pattern[positionalPattern] = [word]
                                # Finding the maximum length list and updating secret word list
                                maxKey = None
                                maxLen = 0
                                for key in pattern:
                                        if len(pattern[key]) == maxLen:
                                                if key == tuple():
                                                        maxKey = key
                                                        maxLen = len(pattern[key])
                                                elif maxKey == tuple():
                                                        pass
                                        elif len(pattern[key]) > maxLen:
                                                maxKey = key
                                                maxLen = len(pattern[key])
                                                
                                secretWordList = pattern[maxKey]
                                patternTillNow = updatePattern(maxKey,letter,patternTillNow,secretWordLength)
                                
                                if maxKey == ():
                                        incorrectGuessesCount,looseCount,lost = incorrectLetterChoice(incorrectGuessesCount,looseCount,maxIncorrectGuesses,secretWordList)
                                        if lost:
                                                break
                                else:
                                        print("Correct Guess")
                                if "_" not in patternTillNow:
                                        print("You have successfully guessed the correct word")
                                        winCount += 1
                                        print("You guessed the word {} correctly".format(secretWordList[0]))
                                        break
                        else:
                                if lettersToBeGuessed == None:
                                        lettersToBeGuessed = []
                                        for char in secretWordList[0]:
                                                if char not in patternTillNow:
                                                        lettersToBeGuessed.append(char)
                                if letter in lettersToBeGuessed:
                                        print("Correct Guess")
                                        lettersToBeGuessed.remove(letter)
                                        alreadyGuessed.append(letter)
                                        if len(lettersToBeGuessed) == 0:
                                                print("You have successfully guessed the correct word")
                                                winCount += 1
                                                print("You guessed the word {} correctly".format(secretWordList[0]))
                                                break
                                else:
                                        incorrectGuessesCount,looseCount,lost = incorrectLetterChoice(incorrectGuessesCount,looseCount,maxIncorrectGuesses,secretWordList)
                                        if lost:
                                                break
                #Option to continue game
                option = input("Do you want to play again YES/NO")
                if option.lower() == "no":
                        displayStatistics(winCount,looseCount)
                        break
   	
   	




























































