from tkinter import *
import tele_sendmsg

class PNGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Posting-Notifier')
        self.root.geometry('640x480')
        self.Tele_chatid = ''
        menubar = Menu(self.root)
        menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Menu',menu=menu)
        menu.add_command(label='Reset', command=self.Reset)
        menu.add_separator()
        menu.add_command(label='Exit', command=self.root.quit)
        self.root.config(menu=menubar)
        self.kakaoIDlabel = Label(self.root, width = 20, text='카카오톡 ID = 미등록', bg='white', relief='solid')
        self.kakaoIDlabel.place(x=5, y=5)
        self.kakaoRegButton = Button(self.root, width = 20, text='카카오톡 ID 등록하기')
        self.kakaoRegButton.place(x=5, y=30)
        self.TelegramIDlabel = Label(self.root, width = 20, text='텔레그램 ID = 미등록', bg='white', relief='solid')
        self.TelegramIDlabel.place(x=5, y=60)
        self.TeleRegButton = Button(self.root, width = 20, text='텔레그램 ID 등록하기', command=self.TeleRegister)
        self.TeleRegButton.place(x=5, y=85)
        self.notifyListbox = Listbox(self.root, width = 60, height= 29)
        self.notifyListbox.place(x=180, y=5)
        self.root.mainloop()
        
    def Reset(self):
        pass

    def TeleRegister(self):
        self.TeleRegButton.configure(state='disabled')
        self.tele_reg_window = Toplevel(self.root)
        self.tele_reg_window.title('사용자명을 입력한 후 Enter를 누르세요')
        self.tele_reg_window.geometry('400x40')
        self.tele_entry = Entry(self.tele_reg_window,width=40)
        self.tele_entry.bind('<Return>',self.tele_entry_function)
        self.tele_entry.pack()
        tele_label = Label(self.tele_reg_window,text='링크가 나오면 봇에게 말을 걸어 주세요')
        tele_label.pack()

    def tele_entry_function(self, event):
        tele_username = self.tele_entry.get()
        if tele_username == '':
            return
        try:
            chatid = tele_sendmsg.tele_register_v2_auto(tele_username)
            if chatid != 'Get_chatid_Failed':
                self.TelegramIDlabel.configure(text=tele_username)
                self.Tele_chatid = chatid
            else:
                self.TeleRegButton.configure(text='다시 시도하세요', state='normal')
            print(chatid)
        except:
            self.TeleRegButton.configure(text='다시 시도하세요', state='normal')
        self.tele_reg_window.withdraw()
        
if __name__ == "__main__":
    PNGUI()