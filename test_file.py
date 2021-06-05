import requests

######################################################pasted from my main code:
'''Sample of how to use my Wikipedia summary exporter:

import requests
wiki_article = "hat"
payload = {"article": wiki_article}
web_page = 'https://hidden-basin-72940.herokuapp.com/'
output = requests.get(web_page, params=payload)
print(output.text)'''

###############################################################################








'''wiki_article = "hat"

payload = {"article": wiki_article}
output = requests.get('https://hidden-basin-72940.herokuapp.com/', params=payload)
print(output.text)'''


# This is if you wanted to test it with multiple articles at once:
test_movies_list = ['Safety Not Guaranteed', 'Titanic (1997 film)', 'The Matrix', 'La Jetée', 'Hot Tub Time Machine', 'WandaVision', 'Lost (TV series)', 'Alias (TV series)', 'computer science', 'curry', 'cat', 'dog', 'ogre', "The Office (American TV series)"]

for i in test_movies_list:


    payload = {"article": i}

    #output = requests.get('http://127.0.0.1:5000/', params=payload)

    output = requests.get('https://hidden-basin-72940.herokuapp.com/', params=payload)



    print(output.text)
    print('############################################################################################################')
    print('############################################################################################################')
    print('############################################################################################################')
    print('############################################################################################################')