import nltk  # I may have to add in nltk.download('punkt')
from wikipedia import WikipediaPage


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
                    return plot_section
            except TypeError:
                continue







    # In future have it search for the section names to speed this up
    # other tests: WandaVision,

    # make try except there ^
    def get_rt_score(self):
        full_page = WikipediaPage(self.title).content
        rt_score = 'Not Found'  # A safeguard in case there is no RT score
        sentences = nltk.sent_tokenize(full_page)
        rt_score = \
        [x for x in sentences if "Rotten Tomatoes" in x and "%" in x][0]

        # TODO: Make safeguard for if it's not found (try except?)
        # IMPORTANT! ex. La Jetee. Also see Black Beauty
        # also try random non-movies (biology, curry, buffalo, computer science

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


movies_list = ['Safety Not Guaranteed', 'Titanic (1997 film)', 'The Matrix',
               'La Jetée', 'Hot Tub Time Machine', 'WandaVision',
               'Lost (TV series)', 'Alias (TV shows)', 'computer science', 'curry']

# class GUI:
# def start_GUI(self):

if __name__ == '__main__':
    mov = Wiki(input('Enter a movie title:\n'))
    # mov = Wiki("The Matrix")

    import tkinter

    window = tkinter.Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))

    window.title("Movie Summary")

    txt = "Movie Summary:" + '\n' + mov.get_plot() + '\n\n\n' + 'Rotten Tomatoes score:' + \
          '\n' + mov.get_rt_score() + '\n\n\n' + 'Keywords:' + '\n' + mov.get_keywords()
    label = tkinter.Label(window, text=txt,
                          wraplength=window.winfo_screenwidth(),
                          justify="left", font='calibri 13').pack()
    window.mainloop()
