# credit: uses this as a guideline for structuring my tkinter:
# https://www.youtube.com/watch?v=73WpYMulq2k

# Flask code created using this guide:
# https://realpython.com/flask-by-example-part-1-project-setup/

from wikipedia import WikipediaPage
import requests
from flask import Flask, request


class Wiki:
    """Class for Wikipedia movie info. """

    def __init__(self, movie_title):
        self.title = movie_title

    def get_plot(self):
        """gets the plot"""
        # This is in case 'Plot' is not found
        plot_names = ['Plot', 'Summary', 'Premise', 'Synopsis']
        plot_section = None
        self.full_plot_section = None
        for i in plot_names:
            try:
                plot_section = WikipediaPage(self.title).section(i)

                # saves this to use in get_keywords
                self.full_plot_section = plot_section

                # this is a brief SUMMARY, not the whole movie
                plot_section = plot_section[:1000] + "..."
                if plot_section is not None:
                    plot_section = plot_section.replace('\n',
                                                        ' ')  # remove newlines
                    return plot_section
            except TypeError:
                continue
        if plot_section is None:
            plot_section = 'none'
            return plot_section

    def get_rt_score(self):
        """gets Rotten Tomatoes score"""
        full_page = WikipediaPage(self.title).content
        sentences = nltk.sent_tokenize(full_page)
        rt_score = [x for x in sentences if
                    "Rotten Tomatoes" in x and "%" in x]

        # for films without a Rotten Tomatoes score (ex. La Jetee)
        if rt_score:
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

    def call_keywords_microservice(self):
        """added this to shorten original get_keywords function"""
        try:
            plot = self.full_plot_section  # limited this to prevent problems
        except TypeError:
            plot = "None"

        # Michelle's microservice:
        req_url = 'https://the-text-analyzer.herokuapp.com/keyword-service'

        my_response = requests.post(req_url, data=plot.encode('utf-8'))
        my_response = my_response.json()
        orig_dict = my_response
        relevance_dict = {}
        for i in orig_dict:
            relevance_dict[i] = orig_dict[i][
                'relevance']  # make a new dict with JUST relevance
        return relevance_dict

    def get_keywords(self):
        """gets keywords from Michele's microservice"""
        relevance_dict = Wiki.call_keywords_microservice(self)

        # this part uses code from https://bit.ly/3ppwYLn
        sorted_relevance_dict = \
            sorted(relevance_dict, key=relevance_dict.get, reverse=True)

        # only show first 20 keywords
        sorted_keywords = [key for key in sorted_relevance_dict][:30]
        keywords_str = ''
        for i in sorted_keywords:
            keywords_str += i + '   '

        return keywords_str


class GUI:
    """class for everything in the GUI"""

    def __init__(self):
        """sets up the GUI"""
        self.window = tk.Tk()
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (width, height))
        self.window.attributes('-topmost',
                               True)  # ensure this window is on top

        # not totally sure what this does or if it's necessary
        self.window.grid_columnconfigure(0, weight=1)

    def get_movie_info(self):
        """gets the movie info"""
        if self.text_input.get():
            self.movie = self.text_input.get()

            # I did not auto-capitalize first letter of every word-
            # otherwise (it won't work for films like Titanic (1997 film))
            self.mov = Wiki(self.movie)
            plot = self.mov.get_plot()
            score = self.mov.get_rt_score()
            keywords = self.mov.get_keywords()
            txt = "Movie Summary:" + '\n' + plot + '\n\n' + \
                  'Rotten Tomatoes score:' + \
                  '\n' + score + '\n\n' + \
                  'Keywords (words to help the user gauge interest):' + \
                  '\n' + keywords
        else:
            txt = 'Please enter a movie!'

        txt_label = tk.Label(self.window, text=txt,
                             wraplength=self.window.winfo_screenwidth(),
                             justify="left", font='calibri 13')
        txt_label.grid(row=3, column=0)

    def get_movie_name(self):
        """gets movie names"""
        return self.movie

    def initiate_gui(self):
        """initiates the GUI"""
        self.window.title("Movie Summary")
        welcome_label = tk.Label(self.window, text='Enter a movie title!',
                                 font='calibri 20')
        welcome_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)
        self.text_input = tk.Entry()
        self.text_input.grid(row=1, column=0, sticky="WE", padx=10)
        dl_button = tk.Button(text='Go', font='calibri 13',
                              command=self.get_movie_info)
        dl_button.grid(row=2, column=0, sticky="WE", padx=5, pady=5)
        self.window.mainloop()


# To send info to another microservice:
app = Flask(__name__)


@app.route("/")  # this links index to app.route
def send_summary():  # for Nick's microservice
    """exports the full wikipedia page"""

    user_input = request.args.get("article")
    full_page_2 = WikipediaPage(user_input).summary
    return str(full_page_2)


if __name__ == '__main__':

    '''these two need to be imported here so Heroku doesn't try to import them
    (Heroku doesn't work well with them)'''
    import tkinter as tk
    import nltk

    start = GUI()
    start.initiate_gui()
