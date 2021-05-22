# credit: uses this as a guideline for structuring my tkinter: https://www.youtube.com/watch?v=73WpYMulq2k
# GET AND POST using code from here: https://www.geeksforgeeks.org/get-post-requests-using-python/

import os
import nltk  # I may have to add in nltk.download('punkt')
from wikipedia import WikipediaPage
import tkinter as tk
import requests
from flask import Flask, request

app = Flask(__name__)
#env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
#app.config.from_object(env_config)

class Wiki:
    """Class for Wikipedia movie info. """

    def __init__(self, movie_title):
        self.title = movie_title

    def get_plot(self):
        # This is in case 'Plot' is not found
        # In the future have it search for the section names to speed this up
        plot_names = ['Plot', 'Summary', 'Premise', 'Synopsis']
        plot_section = None # not necessary?
        self.full_plot_section = None
        for i in plot_names:
            try:
                plot_section = WikipediaPage(self.title).section(i)
                self.full_plot_section = plot_section # saves this to use in get_keywords
                plot_section = plot_section[:1000] + '...'  # this is a brief SUMMARY, not the whole movie
                if plot_section is not None:
                    plot_section = plot_section.replace('\n',' ') # remove newlines
                    return plot_section
            except TypeError:
                continue
        if plot_section is None:
            plot_section = 'none'
            return plot_section


    def get_rt_score(self):
        full_page = WikipediaPage(self.title).content
        sentences = nltk.sent_tokenize(full_page)
        rt_score = [x for x in sentences if "Rotten Tomatoes" in x and "%" in x]

        # for films without a Rotten Tomatoes score (ex. La Jetee)
        if rt_score != []:
            rt_score = rt_score[0]
        else:
            rt_score = 'none'

        # To clean it up and remove everything before the last newline char:
        rt_score = rt_score.strip()  # remove trailing \n
        nl_indx = 0  # counter for the last newline character
        for i in range(len(rt_score)):
            if rt_score[i] == '\n':
                nl_indx = i
        if nl_indx == 0:
            nl_indx = -1  # exception
        rt_score = rt_score[nl_indx + 1:]
        return rt_score




    def get_keywords(self):
        # to be implemented with Michele's code

        """url_helper = self.title.replace(' ', '_')
        url = 'https://en.wikipedia.org/wiki/' + url_helper""" # use later for Nick?

        plot = self.full_plot_section[:300] # limited this to prevent problems

        req_url = 'https://the-text-analyzer.herokuapp.com/keyword-service'

        my_response = requests.post(req_url, data = plot)
        my_response = my_response.json()
        orig_dict = my_response
        new_dict = {}
        for i in orig_dict:
            new_dict[i] = orig_dict[i]['relevance'] # make a new dict with JUST relevance

        sorted_keywords = []
        # this part uses code from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        for this_key in sorted(new_dict, key=new_dict.get, reverse=True):
            sorted_keywords.append(this_key)

        sorted_keywords = sorted_keywords [:20]  # only show first 20 keywords

        keywords_str = ''
        for i in sorted_keywords:
            keywords_str += i + '   '

        return keywords_str

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (width, height))
        self.window.attributes('-topmost', True)  # ensure this window is on top
        self.window.grid_columnconfigure(0, weight = 1) # not totally sure what this does or if it's necessary

    def get_movie_info(self):
        if self.text_input.get():
            self.movie = self.text_input.get()

            # omit this- it messes up other things like Titanic (1997 film)
            #movie = movie.title() # capitalizes first letter of every word (for safety not guaranteed)
            self.mov = Wiki(self.movie)
            plot = self.mov.get_plot()
            score = self.mov.get_rt_score()
            keywords = self.mov.get_keywords()
            txt = "Movie Summary:" + '\n' + plot + '\n\n' + 'Rotten Tomatoes score:' + \
                  '\n' + score + '\n\n' + 'Keywords:' + '\n' + keywords
        else:
            txt = 'Please enter a movie!'

        txt_label = tk.Label(self.window, text=txt,
                              wraplength=self.window.winfo_screenwidth(),
                              justify="left", font='calibri 13')
        txt_label.grid(row=3, column=0)

    def get_movie_name(self):
        return self.movie

    def initiate_GUI(self):
        self.window.title("Movie Summary")
        welcome_label = tk.Label(self.window, text = 'Enter a movie title!',font='calibri 20')
        welcome_label.grid(row = 0, column = 0, sticky = "N", padx = 20, pady = 10)
        self.text_input = tk.Entry()
        self.text_input.grid(row = 1, column = 0, sticky = "WE", padx = 10)
        dl_button = tk.Button(text = 'Go', font = 'calibri 13', command = self.get_movie_info)
        dl_button.grid(row=2, column=0, sticky="WE", padx=5, pady=5)
        self.window.mainloop()

# To send info to another microservice:
@app.route("/")  # GV: this links index to app.route
def send_summary(): # for Nick's microservice
    '''exports the full wikipedia page'''


    '''user_input = request.args.get("article")
    full_page_2 = WikipediaPage(user_input).content
    return str(full_page_2)'''

    return "Hello this is the new version!"


if __name__ == '__main__':
    start = GUI()
    start.initiate_GUI()


#test_movies_list = ['Safety Not Guaranteed', 'Titanic (1997 film)', 'The Matrix', 'La Jetée', 'Hot Tub Time Machine', 'WandaVision', 'Lost (TV series)', 'Alias (TV series)', 'computer science', 'curry']
