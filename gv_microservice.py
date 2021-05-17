# credit: uses this as a guideline for structuring my tkinter: https://www.youtube.com/watch?v=73WpYMulq2k

import nltk  # I may have to add in nltk.download('punkt')
from wikipedia import WikipediaPage
import tkinter as tk

class Wiki:
    """Class for Wikipedia movie info. """

    def __init__(self, movie_title):
        self.title = movie_title

    def get_plot(self):
        # This is in case 'Plot' is not found
        plot_names = ['Plot', 'Summary', 'Premise', 'Synopsis']
        plot_section = None # not necessary?
        for i in plot_names:
            try:
                plot_section = WikipediaPage(self.title).section(i)
                plot_section = plot_section[:1000] + '...'  # this is a brief SUMMARY, not the whole movie
                if plot_section is not None:
                    plot_section = plot_section.replace('\n',' ') # remove newlines
                    return plot_section
            except TypeError:
                continue
        if plot_section is None:
            plot_section = 'none'
            return plot_section

    # In future have it search for the section names to speed this up

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
        return ''


'''test_movies_list = ['Safety Not Guaranteed', 'Titanic (1997 film)', 'The Matrix',
               'La Jetée', 'Hot Tub Time Machine', 'WandaVision',
               'Lost (TV series)', 'Alias (TV shows)', 'computer science', 'curry']'''

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (width, height))
        self.window.title("Movie Summary")
        self.window.attributes('-topmost', True)  # ensure this window is on top
        self.window.grid_columnconfigure(0, weight = 1) # not totally sure what this does or if it's necessary

    def get_movie_info(self):
        if self.text_input.get():
            movie = self.text_input.get()
            mov = Wiki(movie)
            plot = mov.get_plot()
            score = mov.get_rt_score()
            keywords = mov.get_keywords()
            txt = "Movie Summary:" + '\n' + plot + '\n\n' + 'Rotten Tomatoes score:' + \
                  '\n' + score + '\n\n' + 'Keywords:' + '\n' + keywords
        else:
            txt = 'Please enter a movie!'

        self.label = tk.Label(self.window, text=txt,
                              wraplength=self.window.winfo_screenwidth(),
                              justify="left", font='calibri 13')
        self.label.grid(row=3, column=0)

    def initiate_GUI(self):
        welcome_label = tk.Label(self.window, text = 'Enter a movie title!',font='calibri 20')
        welcome_label.grid(row = 0, column = 0, sticky = "N", padx = 20, pady = 10)
        self.text_input = tk.Entry()
        self.text_input.grid(row = 1, column = 0, sticky = "WE", padx = 10)
        dl_button = tk.Button(text = 'Go', font = 'calibri 13', command = self.get_movie_info)
        dl_button.grid(row=2, column=0, sticky="WE", padx=5, pady=5)
        self.window.mainloop()

if __name__ == '__main__':
    GUI().initiate_GUI()
