# Multi-frame tkinter application v2.3
import tkinter as tk
import requests
from WrappingLabel import WrappingLabel

# BACmE-38f66llPT9BDJAKPb_O_vkQ2COXxlA1Yt

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
        self.host = ""

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def login(self, api_key, server_id, host):
        self.api_key = api_key
        self.server_id = server_id
        self.host = host
        new_frame = QueryPage(self, api_key, server_id, host)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# pass the api key and id to the query page
class QueryPage(tk.Frame):
    def __init__(self, master, api_key, server_id, host):
        tk.Frame.__init__(self)
        self.api_key = "BACmE-38f66llPT9BDJAKPb_O_vkQ2COXxlA1Yt"
        self.server_id = server_id
        self.host = host
        self.teamspeak_logo = tk.PhotoImage(file='C:/Users/qqWha/Desktop/python/Teamspeak/logo.png')
        tk.Label(self, text="Type your command below").grid(row=0, column=0)
        self.query_field = tk.Entry(self, width=35)
        self.query_field.grid(row=1, column=0, pady=10)
        self.server_reply = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, height=10, cursor="arrow")
        self.server_reply.grid(row=2, column=0)
        self.scrollbar = tk.Scrollbar(self, command=self.server_reply.yview)
        self.scrollbar.grid(row=2, column=1, sticky="nsew")
        self.server_reply.config(yscrollcommand=self.scrollbar.set)
        tk.Button(self, text="Submit Query", command=lambda: self.send_query(self.query_field.get())).grid(row=3,
                                                                                                           column=0)
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
        url = f"http://{self.host}:10080/{self.server_id}/{queries[0]}?api-key={self.api_key}"
        print(url)
        try:
            if len(queries) == 1:
                data = requests.post(url)  # with params
            elif len(queries) == 3:
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
        tk.Label(self.frame1, text="Api-Key(Required): ").pack(side="left")
        self.api_key = tk.Entry(self.frame1)
        self.api_key.pack()

        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=3, column=0)
        tk.Label(self.frame2, text="Virtual Server ID:      ").pack(side="left")
        self.virtual_server_id = tk.Entry(self.frame2, fg="grey")
        self.virtual_server_id.insert(0, "Default value: 1")
        self.virtual_server_id.pack()

        self.frame3 = tk.Frame(self)
        self.frame3.grid(row=4, column=0)
        tk.Label(self.frame3, text="Server IP Address    ").pack(side="left")
        self.server_address = tk.Entry(self.frame3, fg="grey")
        self.server_address.insert(0, "Default: Localhost")
        self.server_address.pack()

        self.virtual_server_id.bind("<FocusIn>", self.handle_focus_in)
        self.virtual_server_id.bind("<FocusOut>", self.handle_focus_out)

        self.server_address.bind("<FocusIn>", self.handle_focus_in2)
        self.server_address.bind("<FocusOut>", self.handle_focus_out2)

        self.status = tk.Label(self, text="")
        self.status.grid(row=5, column=0)
        self.submit = tk.Button(self, text="Submit", command=lambda: self.validate(master, self.get_api_key(), self.get_virtual_server_id(), self.get_server_address()))
        self.submit.grid(row=6, column=0)
        tk.Button(self, text="Help?",
                  command=lambda: master.switch_frame(HelpPage)).grid(row=7, column=0)
        tk.Label(self, image=self.teamspeak_logo).grid(row=8, column=0)



    def validate(self, master, api_key, virtual_server_id, host):
        url = f"http://{host}:10080/{virtual_server_id}/clientlist?api-key={api_key}"
        try:
            data = requests.post(url)
            status_code = data.json()["status"]["code"]
            if (status_code == 0):
                master.login(api_key, virtual_server_id, host)
            else:
                self.status.config(text="Wrong API key or Virtual Server ID. Please try again")
        except Exception as e:
            self.status.config(text="Failed to connect to server. Make sure your server is running.")

    def handle_focus_in(self, _):
        if self.virtual_server_id.get() == "Default value: 1":
            self.virtual_server_id.delete(0, tk.END)
        self.virtual_server_id.config(fg='black')

    def handle_focus_in2(self, _):
        if self.server_address.get() == "Default: Localhost":
            self.server_address.delete(0, tk.END)
        self.server_address.config(fg='black')

    def handle_focus_out(self, _):
        if not self.virtual_server_id.get():
            self.virtual_server_id.delete(0, tk.END)  # what does end do? It marks where to stop.
            self.virtual_server_id.config(fg='grey')
            self.virtual_server_id.insert(0, "Default value: 1")

    def handle_focus_out2(self, _):
        if not self.server_address.get():
            self.server_address.delete(0, tk.END)
            self.server_address.config(fg='grey')
            self.server_address.insert(0, "Default: Localhost")

    def get_api_key(self):
        api_key = self.api_key.get()
        return api_key

    def get_virtual_server_id(self):
        ts_virtual_server_id = self.virtual_server_id.get()
        if ts_virtual_server_id == "Default value: 1" or not ts_virtual_server_id:
            return 1
        else:
            return ts_virtual_server_id

    def get_server_address(self):
        ts_server_address = self.server_address.get()
        if ts_server_address == "Default: Localhost" or not ts_server_address:
            return "Localhost"
        else:
            return ts_server_address


class HelpPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        #self.myscrollbar = tk.Scrollbar(self)
        #self.myscrollbar.pack(side="right", fill="y")

        self.info_font = ("Times New Roman", 12)
        tk.Label(self, text="About", font=("Times New Roman", 20)).pack()
        self.about = tk.Label(self, font=self.info_font,
                              text="WebQuery is a web based version of ServerQuery that allows you to execute ServerQuery commands as HTTP Post Requests. This tool uses pythons built in requests library to post these requests as well as the built-in GUI framework tkinter for displaying the Graphical User interface",
                              wraplength=400)
        self.about.pack()
        tk.Label(self, text="Usage Manual", font=("Times New Roman", 20)).pack()
        WrappingLabel(self, font=self.info_font,
                 text="Step 1) Enter your API key, Virtual Server ID and Teamspeak server address in the entry fields. You got your API-Key when you created your teamspeak server(see image)").pack(fill=tk.X, expand=True)
        #self.teamspeak_logo = tk.PhotoImage(file="C:/Users/qqWha/Desktop/python/Teamspeak/api_key.png")
        #WrappingLabel(self, image=self.teamspeak_logo).pack()
        WrappingLabel(self, font=self.info_font,
                 text="Step 2) Write your commands separated by a whitespace and press Send Query. Single-word commands have no parameters and require no whitespace").pack(fill=tk.X, expand=True)
        WrappingLabel(self, font=self.info_font,
                 text="Step 3) Read the response from the server in the text area. The response is in the form of a JSON response object").pack(fill=tk.X, expand=True)

        tk.Label(self, text="See a list of available commands below", font=("Times New Roman", 20)).pack()
        tk.Label(self, text="Unsupported commands", font=("Times New Roman", 12)).pack()
        self.unsupported_commands = tk.Text(self, height=10, wrap=tk.WORD)
        self.unsupported_commands.pack()
        self.unsupported_commands.insert("1.0", """Due to differences in operation, the following ServerQuery commands are currently unsupported in WebQuery:
* `ft*` e.g. (`ftcreatedir`, `ftdeletefile`)
* `help`
* `login` and `logout`
* `quit`
* `servernotifyregister` and `servernotifyunregister`
* `use`""")
        tk.Label(self, text="Supported commands/queries", font=("Times New Roman", 12)).pack()
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.supported_commands = tk.Text(self, wrap=tk.WORD, padx=10, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.supported_commands.yview)
        self.supported_commands.pack()
        self.supported_commands.insert("1.0",
                                       """Some commands are single-word commands, such as severlist, serverinfo and clientlist. Other commands take parameters such as channelcreate which take the parameter channel_name. Ex: channelcreate channel_name HelloWorld
* serverlist  :
Displays a list of virtual servers including their ID, status, number of clients online, etc. If you're using the -all option, the server will list all virtual servers stored in the database. This can be useful when multiple server instances with different machine IDs are using the same database. The machine ID is used to identify the server instance a virtual server is associated with. The status of a virtual server can be either online, offline, booting up, shutting down or virtual online. While most of them are self-explanatory, virtual online is a bit more complicated. Whenever you select a virtual server which is currently stopped with the -virtual parameter, it will be started in virtual mode which means you are able to change its configuration, create channels or change permissions, but no regular TeamSpeak 3 Client can connect. As soon as the last ServerQuery client deselects the virtual server, its status will be changed back to offline.
* channellist  :
Displays a list of channels created on a virtual server including their ID, order, name, etc. The output can be modified using several command options.
* serverinfo  :
Displays detailed configuration information about the selected virtual server including unique ID, number of clients online, configuration, etc. For detailed information, see Virtual Server Properties.
* clientlist  :
Displays a list of clients online on a virtual server including their ID, nickname, status flags, etc. The output can be modified using several command options. Please note that the output will only contain clients which are currently in channels you're able to subscribe to.
* channelcreate channel_name={channelName}  :
Creates a new channel using the given properties and displays its ID. Note that this command accepts multiple properties which means that you're able to specifiy all settings of the new channel at once. For detailed information, see Channel Properties.
* sendtextmessage targetmode={1-3} target={clientID} msg={text}  :
Sends a text message to a specified target. If targetmode is set to 1, a message is sent to the client with the ID specified by target. If targetmode is set to 2 or 3, the target parameter will be ignored and a message is sent to the current channel or server respectively.
* clientpoke clid={clientID} msg={text}  :
Sends a poke message to the client specified with clid.
* clientinfo clid={clientID}  :
Displays detailed configuration information about a client including unique ID, nickname, client version, etc.
        """)
        self.supported_commands.tag_add("start", "2.0", "2.end")
        self.supported_commands.tag_add("start", "4.0", "4.end")
        self.supported_commands.tag_add("start", "6.0", "6.end")
        self.supported_commands.tag_add("start", "8.0", "8.end")
        self.supported_commands.tag_add("start", "10.0", "10.end")
        self.supported_commands.tag_add("start", "12.0", "12.end")
        self.supported_commands.tag_add("start", "14.0", "14.end")
        self.supported_commands.tag_add("start", "16.0", "16.end")

        self.supported_commands.tag_config("start", font=("Default", 10, "bold"))

        self.unsupported_commands.config(state=tk.DISABLED)
        self.supported_commands.config(state=tk.DISABLED)
        tk.Button(self, text="Back to Query Page",
                  command=lambda: master.login(master.api_key, master.server_id, master.host)).pack()
        tk.Button(self, text="Back to Home", command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
