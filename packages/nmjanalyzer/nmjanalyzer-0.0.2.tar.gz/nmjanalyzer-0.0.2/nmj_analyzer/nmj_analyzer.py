import tkinter as  tk
from .Processing import process_subject
fields = ['X Resolution', 'Z Resolution', 'ID', 'threshold', 'Path to images', 'Path to saved output']
dict_fields = ['dx','dz','name', 'thresh','path_images','path_save']
def fetch_and_process(entries):
    dict_arg = {}
    for (entry,fie) in zip(entries,dict_fields):
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text))
        dict_arg[fie]=text
    thresh = float(dict_arg['thresh'])
    pixdim = [float(dict_arg['dx']), float(dict_arg['dx']), float(dict_arg['dz'])]
    process_subject(dict_arg['path_images'], dict_arg['path_save'] , dict_arg['name'], thresh=thresh, pixdim=pixdim)


def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')

        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        if field == 'threshold':
            ent.insert(tk.END, '64')
            ent_ttp = CreateToolTip(ent, 'Indicate the threshold at which to consider a pixel as positive')
        if field == 'X Resolution':
            ent.insert(tk.END,'0.48')
            ent_ttp = CreateToolTip(ent, 'Indicate the axial resolution')
        if field =='Z Resolution':
            ent.insert(tk.END, '1.750')
            ent_ttp = CreateToolTip(ent, 'Indicate the non-axial resolution / slice thickness')
        if field == 'ID':
            ent_ttp = CreateToolTip(ent, 'Indicate the ID of the given subject')
        entries.append((field, ent))
    return entries

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def main():
    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch_and_process(e)))
    b1 = tk.Button(root, text='Process',
                  command=(lambda e=ents: fetch_and_process(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()


if __name__ == '__main__':
    main()
