import wolframalpha
import wikipedia
import requests
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[33].id)

appId = '7PRYW6-WTETRTVY6E'
client = wolframalpha.Client(appId)

# method that search wikipedia... 
def search_wiki(keyword=''):
    # running the query
    searchResults = wikipedia.search(keyword)
    # If there is no result, print no result
    if not searchResults:
        print("No result from Wikipedia")
        engine.say("No result from Wikipedia")
        engine.runAndWait()
        return
    # Search for page... try block 
    try:
        page = wikipedia.page(searchResults[0])
    except Exception as err:
        page = wikipedia.page(err.options[0])

    
    wikiTitle = str(page.title.encode('utf-8'))
    wikiSummary = str(page.summary.encode('utf-8'))
    print(wikiSummary)

    # If the result is longer than 150 words, speak the first 400 letters and ask if the user wants more
    if len(wikiSummary) > 150:
        engine.say(wikiSummary[:400])
        engine.runAndWait()
        engine.say("Would you like me to continue?")
        engine.runAndWait()
        proceed = input("Would you like me to continue: ")
        engine.runAndWait()

        # y or yes if you would like to hear the whole result
        if proceed == 'y' or proceed == 'yes':
            engine.say(wikiSummary[400:])
            engine.runAndWait()
        else:
            pass
    else:
        engine.say(wikiSummary)
        engine.runAndWait()

    

def search(text=''):
    res = client.query(text)
    # Wolfram cannot resolve the question
    if res['@success'] == 'false':
        print('Question cannot be resolved')
        engine.say("Question could not be resolved")
        engine.runAndWait()
    # Wolfram was able to resolve question
    else:
        result = ''
        # pod[0] is the question
        pod0 = res['pod'][0]
        # pod[1] may contains the answer
        pod1 = res['pod'][1]
        # checking if pod1 has primary=true or title=result|definition
        if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
            # extracting result from pod1
            result = resolveListOrDict(pod1['subpod'])
            print(result)

            # If the result is longer than 150 words, speak the first 400 letters and ask if the user wants more
            if len(result) > 150:
                engine.say(result[:400])
                engine.runAndWait()
                engine.say("Would you like me to continue sir?")
                engine.runAndWait()
                proceed = input("Would you like me to continue: ")
                engine.runAndWait()

                # y or yes if you would like to hear the whole result
                if proceed == 'y' or proceed == 'yes':
                    engine.say(result[400:])
                    engine.runAndWait()
                else:
                    pass

            else:
                engine.say(result)
                engine.runAndWait()
            
            question = resolveListOrDict(pod0['subpod'])
            question = removeBrackets(question)
            primaryImage(question)
        else:
            # extracting wolfram question interpretation from pod0
            question = resolveListOrDict(pod0['subpod'])
            # removing unnecessary parenthesis
            question = removeBrackets(question)
            # searching for response from wikipedia
            search_wiki(question)
            primaryImage(question)


def removeBrackets(variable):
    return variable.split('(')[0]

def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']

def primaryImage(title=''):
    url = 'http://en.wikipedia.org/w/api.php'
    data = {'action':'query', 'prop':'pageimages','format':'json','piprop':'original','titles':title}
    try:
        res = requests.get(url, params=data)
        key = res.json()['query']['pages'].keys()[0]
        imageUrl = res.json()['query']['pages'][key]['original']['source']
        print(imageUrl)
    except Exception as err:
        print('Exception while finding image:= '+str(err))
 
 
while True:
    q = input('Question: ')
    search(q)