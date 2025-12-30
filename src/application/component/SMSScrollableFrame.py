# @see https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame

from tkinter import Frame, Scrollbar, Canvas


class SMSScrollableFrame(Frame):
    def __init__(self, container, bg: str):
        super().__init__(master=container, width=1200, height=750)
        self.bg = bg
        self.create_scrollable_frame()

    def get_interior(self):
        return self.interior

    def reload(self):
        self.children.clear()
        self.create_scrollable_frame()

    def create_scrollable_frame(self):
        vscrollbar = Scrollbar(self, orient="vertical")
        vscrollbar.grid(sticky='ns', row=0, column=1)

        canvas = Canvas(self, highlightthickness=0, width=1200, height=750, yscrollcommand=vscrollbar.set, bg=self.bg)
        canvas.grid(sticky='nsew', row=0, column=0)
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = Frame(canvas, width=1200, height=750, bg=self.bg)
        interior_id = canvas.create_window(0, 0, window=self.interior, anchor="nw")

        def __configure_interior(event):
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())

            canvas.config(scrollregion="0 0 %s %s" % size)

            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=self.interior.winfo_reqwidth())

        self.interior.bind('<Configure>', __configure_interior)

        def __configure_canvas(event):
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', __configure_canvas)
