# Multi-frame tkinter application v2.3
import tkinter as tk
import requests

#BACmE-38f66llPT9BDJAKPb_O_vkQ2COXxlA1Yt

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Graphical WebQuery 1.0")
        self.teamspeak_logo = tk.PhotoImage(file='C:/Users/qqWha/Desktop/python/Teamspeak/logo.png')
        self.iconphoto(False, self.teamspeak_logo)
        self._frame = None
        self.switch_frame(StartPage)
        self.api_key = ""
        self.server_id = ""

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def login(self, api_key, server_id):
        self.api_key = api_key
        self.server_id = server_id
        new_frame = QueryPage(self, api_key, server_id)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# pass the api key and id to the query page
class QueryPage(tk.Frame):
    def __init__(self, master, api_key, server_id):
        tk.Frame.__init__(self)
        self.api_key = "BACmE-38f66llPT9BDJAKPb_O_vkQ2COXxlA1Yt"
        self.server_id = server_id
        self.teamspeak_logo = tk.PhotoImage(file='C:/Users/qqWha/Desktop/python/Teamspeak/logo.png')
        tk.Label(self, text="Type your command below").grid(row=0, column=0)
        query_field = tk.Entry(self, width=35)
        query_field.grid(row=1, column=0, pady=10 )
        self.server_reply = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, height=10, cursor="arrow")
        self.server_reply.grid(row=2, column=0)
        self.scrollbar = tk.Scrollbar(self, command=self.server_reply.yview)
        self.scrollbar.grid(row=2, column=1, sticky="nsew")
        self.server_reply["yscrollcommand"] = self.scrollbar.set
        self.scrollbar = tk.Scrollbar(self, command=self.server_reply.yview())
        tk.Button(self, text="Submit Query", command=lambda: self.send_query(query_field.get())).grid(row=3, column=0)
        tk.Button(self, text="Back to Home", command=lambda: master.switch_frame(StartPage)).grid(row=4, column=0)
        tk.Button(self, text="Help?", command=lambda: master.switch_frame(HelpPage)).grid(row=5, column=0)
        tk.Label(self, image=self.teamspeak_logo).grid(row=6, column=0)

    def help_query(self, query):
        url = f"http://localhost:10080/{query}?api-key={self.api_key}"
        print(url)
        try:
            data = requests.post(url)
            reply = data.json()["body"]
            self.server_reply.insert(0, reply)
        except:
            self.server_reply.insert(0, "Did not work")
            print("Did not work")

    def send_query(self, query):
        queries = query.split()
        url = f"http://localhost:10080/{self.server_id}/{queries[0]}?api-key={self.api_key}"
        print(url)
        try:
            if len(queries)==1:
                data = requests.post(url) # with params
            elif len(queries)==3:
                data = requests.post(url, params={queries[1]: queries[2]})  # with params
            else:
                data = requests.post(url, params={queries[1]: queries[2], queries[3]: queries[4]})
            reply = data.json()["body"]
            self.server_reply.config(state=tk.NORMAL)
            self.server_reply.delete('1.0', tk.END)
            self.server_reply.insert('1.0', reply)
            self.server_reply.config(state=tk.DISABLED)
            print(reply)
        except Exception as e:
            print(e)
            self.server_reply.config(state=tk.NORMAL)
            self.server_reply.delete('1.0', tk.END)
            self.server_reply.insert("1.0", f"Did not work. {query} is not a valid command")
            self.server_reply.config(state=tk.DISABLED)
            print("Did not work")


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.teamspeak_logo = tk.PhotoImage(file='C:/Users/qqWha/Desktop/python/Teamspeak/logo.png')
        tk.Label(self, text="Welcome!").grid(row=0, column=0)
        tk.Label(self, text="Please enter your details below").grid(row=1, column=0)

        self.frame1 = tk.Frame(self)
        self.frame1.grid(row=2, column=0)
        tk.Label(self.frame1, text="Api-Key:              ").pack(side="left")
        self.api_key = tk.Entry(self.frame1)
        self.api_key.pack()
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=3, column=0)
        tk.Label(self.frame2, text="Virtual Server ID:").pack(side="left")
        self.virtual_server_id = tk.Entry(self.frame2, fg="grey")
        self.virtual_server_id.insert(0, "Default value: 1")
        self.virtual_server_id.pack()
        self.virtual_server_id.bind("<FocusIn>", self.handle_focus_in)
        self.virtual_server_id.bind("<FocusOut>", self.handle_focus_out)

        tk.Button(self, text="Submit",
                  command=lambda: master.login(self.get_api_key(), self.get_virtual_server_id())).grid(row=4, column=0)
        tk.Label(self, image=self.teamspeak_logo).grid(row=5, column=0)

    def handle_focus_in(self, _):
        if self.virtual_server_id.get() == "Default value: 1":
            self.virtual_server_id.delete(0, tk.END)
        self.virtual_server_id.config(fg='black')

    def handle_focus_out(self, _):
        if not self.virtual_server_id.get():
            self.virtual_server_id.delete(0, tk.END)  # what does end do? It marks where to stop.
            self.virtual_server_id.config(fg='grey')
            self.virtual_server_id.insert(0, "Default value: 1")

    def get_api_key(self):
        api_key = self.api_key.get()
        return api_key

    def get_virtual_server_id(self):
        ts_virtual_server_id = self.virtual_server_id.get()
        if ts_virtual_server_id == "Default value: 1" or not ts_virtual_server_id:
            return 1
        else:
            return ts_virtual_server_id

class HelpPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="See a list of available commands below").grid(row=0, column=0)
        tk.Button(self, text="Back to Query Page", command=lambda: master.login(master.api_key, master.server_id)).grid(row=1, column=0)
        tk.Button(self, text="Back to Home", command=lambda: master.switch_frame(StartPage)).grid(row=2, column=0)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
