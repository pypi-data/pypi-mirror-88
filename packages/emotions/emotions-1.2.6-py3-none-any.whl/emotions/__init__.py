inp = 0
feel = 'good'
stob = [0, 1, 2, 3, 4]
stog = [6, 7, 8, 9]
ovimo = 'happy'
emotion_inp=2

def emotion(ask, url):
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)

    inp = 100
    feel = 'good'

    ovalue = firebase.get('/oi', None)
    ovalue = str(ovalue).replace('None, ', '')
    ovalue = str(ovalue).replace('[', '')
    ovalue = str(ovalue).replace(']', '')
    ovalue = str(ovalue).replace(' ', '')
    ovalue = ovalue.split(',')

    b = firebase.get('/feeling', None)
    c = str(b).replace('{', '')
    c2 = str(c).replace('}', '')
    c3 = str(c2).replace("'", '')
    c5 = str(c3).replace(' ', '')
    c4 = str(c5).split(',')

    for y in c4:
        compare = y.split(':')
        if ask == compare[0]:
            inp = int(float(compare[1]))

    knowb = bad = sum(stob) / len(stob)
    knowg = good = 7

    moodG = ovalue.count('10')
    moodB = ovalue.count('0')

    if moodG < moodB:
        ovimo = 'Frustrated'

    if moodG > moodB:
        ovimo = 'Happy'

    if moodG == len(ovalue):
        ovimo = 'Very-Happy'

    if moodB == len(ovalue):
        ovimo = 'Depressed'

    if moodB == moodG:
        ovimo = 'Moderate'

    # Bad
    if inp > bad and inp < 5:
        feel = 'angry'

    if inp == bad and inp < 5:
        feel = 'sad'

    if inp <=1 and inp < 5:
        feel = 'scared'

    # Good
    if inp > good and inp < 10 and inp > 5:
        feel = 'excited'

    if inp < good and inp < 10 and inp > 5:
        feel = 'happy'

    if inp == good and inp < 10 and inp > 5:
        feel = 'h-cited'

    if inp == 5:
        feel = 'nothing'

    emotion.feelings = 'I am feeling ' + feel + ' about ' + ask
    emotion.mood = 'mood:' + ovimo

    if inp == 100:

        print("Sorry I don't know about " + ask + ",")
        print("But I am Curious about it Can you please tell me,")
        print(
            "How you feel about it? (give the answer in 'angry','sad','scared','excited','happy','h-cited','nothing' : ")

        l = input()
        if l == 'angry':
            kit = 4
        if l == 'sad':
            kit = 2
        if l == 'scared':
            kit = 0
        if l == 'excited':
            kit = 8
        if l == 'happy':
            kit = 6
        if l == 'h-cited':
            kit = 7
        if l == 'nothing':
            kit = 5

        word = ask
        feeling = kit
        url = url

        learn(word, feeling, url)
        emotion.feelings = ''


def learn(word, feeling, url):
    l = word
    kit = l

    knoutings = kit
    emI = feeling
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)
    firebase.put('/feeling', knoutings, emI)

    count = firebase.get('/count', None)
    count = str(count).replace('None, ', '')
    count = str(count).replace('[', '')
    count = str(count).replace(']', '')
    count = str(count).replace(' ', '')

    count2 = int(count) + 1

    firebase.put('/count', '1', count2)

    print('Got it!')

    if emI in (0, 1, 2, 3, 4):
        firebase.put('/oi', count2, 0)

    if emI in (6, 7, 7.5, 8, 9):
        firebase.put('/oi', count2, 10)


def learn_info(word, url):
    # importing stuff
    import webbrowser
    import wikipedia
    import json
    from firebase import firebase
    from googlesearch import search

    # Declaring variables, etc.
    inp = word
    inp_name = word.replace('.', '')
    ans = 'nothing'
    wikipedia.set_lang("en")

    firebase = firebase.FirebaseApplication(url, None)
    words_db = firebase.get('/info', None)

    words_db_1 = []
    words_db_2 = []

    word_for_if = inp_name.lower()

    words_db_1 = []
    words_db_2 = []

    # Checking if information about a word is already in its database
    for x in words_db:
        words_db_1.append(x)
        words_db_2.append(words_db[x])
    if word_for_if in words_db_1:
        learn_info.ans = (words_db_2[words_db_1.index(word_for_if)])

    else:
        # Declaring variables, etc.
        query = inp
        query = query.replace(' ', '')

        urls = []
        urls2 = []
        ids = 32
        learn_info.feedback = 'nothing'

        # Searching in Google
        for x in search('What is ' + query, tld="co.in", num=10, stop=10, pause=2):
            # Filtering links to get wikipedia links
            if 'https://en.wikipedia.org/wiki' in x:
                x = x.replace('https://en.wikipedia.org/wiki', '')
                urls.append(x)

            if 'https://en.wikipedia.org/wiki' not in x:
                # importing stuff
                import requests
                import re
                import webbrowser

                inp = inp.lower()
                inp = inp.replace(' ', '+')

                # Searching in youtube (If wikipedia links not found)
                x = requests.get("https://www.youtube.com/results?search_query=what+is+" + inp)
                videoids = re.findall("watch\?v=(\S{11})", x.content.decode())
                learn_info.videoids = videoids
                ids = videoids[0]

        try:
            # Printing results for feedback
            learn_info.ans2 = wikipedia.summary(urls[0]) + ' (Did you get you answer?)'
            learn_info.ans = wikipedia.summary(urls[0])
            print(learn_info.ans2)
            feedback = input()

            # Processing feedback
            if feedback in ['Yes', 'yes']:
                firebase.put('/info', inp_name, learn_info.ans)
                txt = learn_info.ans

            elif feedback in ['No', 'no']:
                youtube_transcript(ids)
                youtubeans = youtube_transcript.ans
                firebase.put('/info', inp_name, '(From Youtube) ' + youtubeans)
                txt = youtube_transcript.ans

        except:
            youtube_transcript(ids)
            youtubeans = youtube_transcript.ans
            firebase.put('/info', inp_name, '(From Youtube) ' + youtubeans)
            txt = youtube_transcript.ans

        simplifier(txt,url,word)

        # Updating data in firebase
        count = firebase.get('/count', None)
        count = str(count).replace('None, ', '')
        count = str(count).replace('[', '')
        count = str(count).replace(']', '')
        count = str(count).replace(' ', '')

        count2 = int(count) + 1

        firebase.put('/count', '1', count2)

        if emotion_inp in (0, 1, 2, 3, 4):
            firebase.put('/oi', count2, 0)

        if emotion_inp in (6, 7, 7.5, 8, 9):
            firebase.put('/oi', count2, 10)


def op(inp):
    # Fliping emotions, asper the number-sequence
    if '7' in inp:
        op.out = inp.replace('7', '0')

    elif '6' in inp:
        op.out = inp.replace('6', '2')

    elif '8' in inp:
        op.out = inp.replace('8', '4')

    elif '2' in inp:
        op.out = inp.replace('2', '6')

    elif '0' in inp:
        op.out = inp.replace('0', '7')

    elif '4' in inp:
        op.out = inp.replace('4', '8')


def simplifier(txt,url,word):
    import re
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)

    # Processing txt
    txt = txt.lower()
    txt = txt.replace(',', '')
    txt = txt.replace('-', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')

    # Fetching initial values from firebase
    words_withvalue = firebase.get('/feeling', None)
    words_withvalue = str(words_withvalue).replace(',', '+')
    words_withvalue = str(words_withvalue).replace(':', ',')
    words_withvalue = str(words_withvalue).replace('{', '')
    words_withvalue = str(words_withvalue).replace('}', '')
    words_withvalue = str(words_withvalue).replace("'", '')
    words_withvalue = str(words_withvalue).replace(" ", '')
    words_withvalue = str(words_withvalue).split('+')
    wordjust = []
    wordve = []
    wordne = []

    # Removing unnessesary stuff
    txt = ''.join([i for i in txt if not i.isdigit()])
    txt = re.sub('( a | in | an )', ' ', txt)

    # Creating a Json for replacing words with numbers
    for x in words_withvalue:
        inp = x
        op(inp)
        x = x.split(',')
        wordjust.append(x)

    # Replacing words with nums
    for k, v in wordjust:
        txt = txt.lower()
        txt = txt.replace(k, v)

    try:
        try:
            # finding all and replacing negetive words
            findneg = re.findall(r"n't ((([\w ]+)|\d*\.?\d+) but|([\w ]+)|\d*\.?\d+)", txt)
            findneg = findneg[0][0]
            nums = re.findall(r"\d*\.?\d+", findneg)
            num = []
            for x in nums:
                inp = x
                op(inp)
                num.append(op.out)
            num = str(num).replace("'", '')
            num = str(num).replace("[", '')
            num = str(num).replace("]", '')
            txt = txt.replace(findneg, num)
            txt = txt.replace(',', '')

            # Removing everything but nums
            res = [int(i) for i in txt.split() if i.isdigit()]

            # Finding average to produce emotion
            emotion_inp = round(sum(res) / len(res))
            firebase.put('/feeling', word, emotion_inp)

        except:
            # Removing everything but nums
            res = [int(i) for i in txt.split() if i.isdigit()]

            # Finding average to produce emotion
            emotion_inp = round(sum(res) / len(res))
            firebase.put('/feeling', word, emotion_inp)

    except:
        print("I am afraid I don't know any of the words in the data about " + word)


def youtube_transcript(ids):
    # Extracting Subtitle
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        import re
        remov = []
        subtitles = YouTubeTranscriptApi.get_transcript(ids)
        remov = re.sub(r", 'start': [0-9]+(\.[0-9][0-9]?)?", '', str(subtitles))
        remov = re.sub(r", 'duration': [0-9]+(\.[0-9][0-9]?)?", '', remov)
        remov = re.sub(r"'text': ", '', remov)
        remov = re.sub(r"{", '', remov)
        remov = re.sub(r"}", '', remov)
        remov = remov.replace("\\n", " ")
        remov = remov.replace("'", '')
        finalsub = remov.replace('"', '')
        finalsub = finalsub.replace('[Music], ', '')
        finalsub = finalsub.replace('[', '')
        finalsub = finalsub.replace(']', '')
        finalsub = re.sub(r'(?<=[a-z])\d+\b', '', finalsub)
        finalsub = re.sub('♪INTRO', '', finalsub)

        youtube_transcript.ans = str(finalsub)

    except:
        webbrowser.open("https://www.youtube.com/watch?v=" + ids)
        print('I am afraid I cant read this video, can you please help me with that:')
        feedback = input('Please Give a summery of the topic')
        print('Thanks')inp = 0
feel = 'good'
stob = [0, 1, 2, 3, 4]
stog = [6, 7, 8, 9]
ovimo = 'happy'
emotion_inp=2

def emotion(ask, url):
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)

    inp = 100
    feel = 'good'

    ovalue = firebase.get('/oi', None)
    ovalue = str(ovalue).replace('None, ', '')
    ovalue = str(ovalue).replace('[', '')
    ovalue = str(ovalue).replace(']', '')
    ovalue = str(ovalue).replace(' ', '')
    ovalue = ovalue.split(',')

    b = firebase.get('/feeling', None)
    c = str(b).replace('{', '')
    c2 = str(c).replace('}', '')
    c3 = str(c2).replace("'", '')
    c5 = str(c3).replace(' ', '')
    c4 = str(c5).split(',')

    for y in c4:
        compare = y.split(':')
        if ask == compare[0]:
            inp = int(float(compare[1]))

    knowb = bad = sum(stob) / len(stob)
    knowg = good = 7

    moodG = ovalue.count('10')
    moodB = ovalue.count('0')

    if moodG < moodB:
        ovimo = 'Frustrated'

    if moodG > moodB:
        ovimo = 'Happy'

    if moodG == len(ovalue):
        ovimo = 'Very-Happy'

    if moodB == len(ovalue):
        ovimo = 'Depressed'

    if moodB == moodG:
        ovimo = 'Moderate'

    # Bad
    if inp > bad and inp < 5:
        feel = 'angry'

    if inp == bad and inp < 5:
        feel = 'sad'

    if inp <=1 and inp < 5:
        feel = 'scared'

    # Good
    if inp > good and inp < 10 and inp > 5:
        feel = 'excited'

    if inp < good and inp < 10 and inp > 5:
        feel = 'happy'

    if inp == good and inp < 10 and inp > 5:
        feel = 'h-cited'

    if inp == 5:
        feel = 'nothing'

    emotion.feelings = 'I am feeling ' + feel + ' about ' + ask
    emotion.mood = 'mood:' + ovimo

    if inp == 100:

        print("Sorry I don't know about " + ask + ",")
        print("But I am Curious about it Can you please tell me,")
        print(
            "How you feel about it? (give the answer in 'angry','sad','scared','excited','happy','h-cited','nothing' : ")

        l = input()
        if l == 'angry':
            kit = 4
        if l == 'sad':
            kit = 2
        if l == 'scared':
            kit = 0
        if l == 'excited':
            kit = 8
        if l == 'happy':
            kit = 6
        if l == 'h-cited':
            kit = 7
        if l == 'nothing':
            kit = 5

        word = ask
        feeling = kit
        url = url

        learn(word, feeling, url)
        emotion.feelings = ''


def learn(word, feeling, url):
    l = word
    kit = l

    knoutings = kit
    emI = feeling
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)
    firebase.put('/feeling', knoutings, emI)

    count = firebase.get('/count', None)
    count = str(count).replace('None, ', '')
    count = str(count).replace('[', '')
    count = str(count).replace(']', '')
    count = str(count).replace(' ', '')

    count2 = int(count) + 1

    firebase.put('/count', '1', count2)

    print('Got it!')

    if emI in (0, 1, 2, 3, 4):
        firebase.put('/oi', count2, 0)

    if emI in (6, 7, 7.5, 8, 9):
        firebase.put('/oi', count2, 10)


def learn_info(word, url):
    # importing stuff
    import webbrowser
    import wikipedia
    import json
    from firebase import firebase
    from googlesearch import search

    # Declaring variables, etc.
    inp = word
    inp_name = word.replace('.', '')
    ans = 'nothing'
    wikipedia.set_lang("en")

    firebase = firebase.FirebaseApplication(url, None)
    words_db = firebase.get('/info', None)

    words_db_1 = []
    words_db_2 = []

    word_for_if = inp_name.lower()

    words_db_1 = []
    words_db_2 = []

    # Checking if information about a word is already in its database
    for x in words_db:
        words_db_1.append(x)
        words_db_2.append(words_db[x])
    if word_for_if in words_db_1:
        learn_info.ans = (words_db_2[words_db_1.index(word_for_if)])

    else:
        # Declaring variables, etc.
        query = inp
        query = query.replace(' ', '')

        urls = []
        urls2 = []
        ids = 32
        learn_info.feedback = 'nothing'

        # Searching in Google
        for x in search('What is ' + query, tld="co.in", num=10, stop=10, pause=2):
            # Filtering links to get wikipedia links
            if 'https://en.wikipedia.org/wiki' in x:
                x = x.replace('https://en.wikipedia.org/wiki', '')
                urls.append(x)

            if 'https://en.wikipedia.org/wiki' not in x:
                # importing stuff
                import requests
                import re
                import webbrowser

                inp = inp.lower()
                inp = inp.replace(' ', '+')

                # Searching in youtube (If wikipedia links not found)
                x = requests.get("https://www.youtube.com/results?search_query=what+is+" + inp)
                videoids = re.findall("watch\?v=(\S{11})", x.content.decode())
                learn_info.videoids = videoids
                ids = videoids[0]

        try:
            # Printing results for feedback
            learn_info.ans2 = wikipedia.summary(urls[0]) + ' (Did you get you answer?)'
            learn_info.ans = wikipedia.summary(urls[0])
            print(learn_info.ans2)
            feedback = input()

            # Processing feedback
            if feedback in ['Yes', 'yes']:
                firebase.put('/info', inp_name, learn_info.ans)
                txt = learn_info.ans

            elif feedback in ['No', 'no']:
                youtube_transcript(ids)
                youtubeans = youtube_transcript.ans
                firebase.put('/info', inp_name, '(From Youtube) ' + youtubeans)
                txt = youtube_transcript.ans

        except:
            youtube_transcript(ids)
            youtubeans = youtube_transcript.ans
            firebase.put('/info', inp_name, '(From Youtube) ' + youtubeans)
            txt = youtube_transcript.ans

        simplifier(txt,url,word)

        # Updating data in firebase
        count = firebase.get('/count', None)
        count = str(count).replace('None, ', '')
        count = str(count).replace('[', '')
        count = str(count).replace(']', '')
        count = str(count).replace(' ', '')

        count2 = int(count) + 1

        firebase.put('/count', '1', count2)

        if emotion_inp in (0, 1, 2, 3, 4):
            firebase.put('/oi', count2, 0)

        if emotion_inp in (6, 7, 7.5, 8, 9):
            firebase.put('/oi', count2, 10)


def op(inp):
    # Fliping emotions, asper the number-sequence
    if '7' in inp:
        op.out = inp.replace('7', '0')

    elif '6' in inp:
        op.out = inp.replace('6', '2')

    elif '8' in inp:
        op.out = inp.replace('8', '4')

    elif '2' in inp:
        op.out = inp.replace('2', '6')

    elif '0' in inp:
        op.out = inp.replace('0', '7')

    elif '4' in inp:
        op.out = inp.replace('4', '8')


def simplifier(txt,url,word):
    import re
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)

    # Processing txt
    txt = txt.lower()
    txt = txt.replace(',', '')
    txt = txt.replace('-', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')

    # Fetching initial values from firebase
    words_withvalue = firebase.get('/feeling', None)
    words_withvalue = str(words_withvalue).replace(',', '+')
    words_withvalue = str(words_withvalue).replace(':', ',')
    words_withvalue = str(words_withvalue).replace('{', '')
    words_withvalue = str(words_withvalue).replace('}', '')
    words_withvalue = str(words_withvalue).replace("'", '')
    words_withvalue = str(words_withvalue).replace(" ", '')
    words_withvalue = str(words_withvalue).split('+')
    wordjust = []
    wordve = []
    wordne = []

    # Removing unnessesary stuff
    txt = ''.join([i for i in txt if not i.isdigit()])
    txt = re.sub('( a | in | an )', ' ', txt)

    # Creating a Json for replacing words with numbers
    for x in words_withvalue:
        inp = x
        op(inp)
        x = x.split(',')
        wordjust.append(x)

    # Replacing words with nums
    for k, v in wordjust:
        txt = txt.lower()
        txt = txt.replace(k, v)

    try:
        try:
            # finding all and replacing negetive words
            findneg = re.findall(r"n't ((([\w ]+)|\d*\.?\d+) but|([\w ]+)|\d*\.?\d+)", txt)
            findneg = findneg[0][0]
            nums = re.findall(r"\d*\.?\d+", findneg)
            num = []
            for x in nums:
                inp = x
                op(inp)
                num.append(op.out)
            num = str(num).replace("'", '')
            num = str(num).replace("[", '')
            num = str(num).replace("]", '')
            txt = txt.replace(findneg, num)
            txt = txt.replace(',', '')

            # Removing everything but nums
            res = [int(i) for i in txt.split() if i.isdigit()]

            # Finding average to produce emotion
            emotion_inp = round(sum(res) / len(res))
            firebase.put('/feeling', word, emotion_inp)

        except:
            # Removing everything but nums
            res = [int(i) for i in txt.split() if i.isdigit()]

            # Finding average to produce emotion
            emotion_inp = round(sum(res) / len(res))
            firebase.put('/feeling', word, emotion_inp)

    except:
        print("I am afraid I don't know any of the words in the data about " + word)


def youtube_transcript(ids):
    # Extracting Subtitle
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        import re
        remov = []
        subtitles = YouTubeTranscriptApi.get_transcript(ids)
        remov = re.sub(r", 'start': [0-9]+(\.[0-9][0-9]?)?", '', str(subtitles))
        remov = re.sub(r", 'duration': [0-9]+(\.[0-9][0-9]?)?", '', remov)
        remov = re.sub(r"'text': ", '', remov)
        remov = re.sub(r"{", '', remov)
        remov = re.sub(r"}", '', remov)
        remov = remov.replace("\\n", " ")
        remov = remov.replace("'", '')
        finalsub = remov.replace('"', '')
        finalsub = finalsub.replace('[Music], ', '')
        finalsub = finalsub.replace('[', '')
        finalsub = finalsub.replace(']', '')
        finalsub = re.sub(r'(?<=[a-z])\d+\b', '', finalsub)
        finalsub = re.sub('♪INTRO', '', finalsub)

        youtube_transcript.ans = str(finalsub)

    except:
        webbrowser.open("https://www.youtube.com/watch?v=" + ids)
        print('I am afraid I cant read this video, can you please help me with that:')
        feedback = input('Please Give a summery of the topic')
        print('Thanks')