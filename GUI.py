from tkinter import *
import tele_sendmsg
import kakao_token_server
from posting_monitor import monitor_posting

class PNGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Posting-Notifier')
        self.root.geometry('640x480')
        self.kakao_tokenName = ''
        self.Tele_chatid = ''
        self.ListboxIndex = 0
        self.kakaoIDlabel = Label(self.root, width = 20, text='카카오톡 토큰 미등록', bg='white', relief='solid')
        self.kakaoIDlabel.place(x=5, y=5)
        self.kakaoRegButton = Button(self.root, width = 20, text='카카오톡 토큰 등록하기', command=self.kakaoRegister)
        self.kakaoRegButton.place(x=5, y=30)
        self.TelegramIDlabel = Label(self.root, width = 20, text='텔레그램 ID = 미등록', bg='white', relief='solid')
        self.TelegramIDlabel.place(x=5, y=60)
        self.TeleRegButton = Button(self.root, width = 20, text='텔레그램 ID 등록하기', command=self.TeleRegister)
        self.TeleRegButton.place(x=5, y=85)
        self.notifyListbox = Listbox(self.root, width = 60, height= 29)
        self.notifyListbox.place(x=210, y=5)

        self.urlLabel = Label(self.root, text='모니터링할 URL 입력')
        self.urlLabel.place(x=5, y=150)
        self.urlEntry = Entry(self.root,width=28, relief='solid')
        self.urlEntry.place(x=5, y=175)
        self.keywordLabel = Label(self.root,text='모니터링할 키워드 입력')
        self.keywordLabel.place(x=5, y=200)
        self.keywordEntry = Entry(self.root,width=28, relief='solid')
        self.keywordEntry.place(x=5,y=225)

        self.urlRegisterButton = Button(self.root, width = 27, text = 'URL 등록하기', command=self.Register_URL)
        self.urlRegisterButton.place(x=5, y=250)

        self.RadioVariety = StringVar()
        self.radio1=Radiobutton(self.root,text='카카오톡',variable=self.RadioVariety, value='kakaotalk', state='disabled', command=self.StartButtonCheck)
        self.radio2=Radiobutton(self.root,text='텔레그램',variable=self.RadioVariety, value='telegram', state='disabled', command=self.StartButtonCheck)

        self.messengerLabel = Label(self.root,text='알림 받을 메신저 선택')
        self.messengerLabel.place(x=5,y=330)

        self.radio1.place(x=5,y=350)
        self.radio2.place(x=100,y=350)

        self.StartButton = Button(self.root, text='시작하기', width=27, state='disabled', command=self.monitor_start)
        self.StartButton.place(x=5,y=400)
        self.root.mainloop()

    def kakaoRegister(self):
        try:
            tokenName = kakao_token_server.run_token_server()
            self.kakao_tokenName = tokenName
            self.kakaoRegButton.configure(state='disabled')
            self.kakaoIDlabel.configure(text='카카오톡 토큰 등록됨')
            self.radio1.configure(state='normal')
            self.radio1.deselect()
        except:
            self.kakaoRegButton.configure(text='다시 시도하세요')
    
    def TeleRegister(self):
        self.tele_reg_window = Toplevel(self.root)
        self.tele_reg_window.grab_set()
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
                self.TeleRegButton.configure(state='disabled')
                self.radio2.configure(state='normal')
                self.radio2.deselect()
            else:
                self.TeleRegButton.configure(text='다시 시도하세요')
            print(chatid)
        except:
            self.TeleRegButton.configure(text='다시 시도하세요')
        self.tele_reg_window.destroy()

    def Register_URL(self):
        urlString = self.urlEntry.get()
        self.urlEntry.delete(0,'end')
        keyString = self.keywordEntry.get()
        self.keywordEntry.delete(0,'end')

        urlkeyList = [urlString,keyString]

        self.notifyListbox.insert(self.ListboxIndex,urlkeyList)
        self.ListboxIndex += 1
        self.StartButtonCheck()

    def StartButtonCheck(self):
        if self.notifyListbox.size() != 0 \
            and self.RadioVariety.get() != '':
            self.StartButton.configure(state='normal')

    def monitor_start(self):
        user = ''
        if self.RadioVariety.get() == 'kakaotalk':
            user = self.kakao_tokenName
        else:
            user = self.Tele_chatid
        urls = []
        keywords = []
        for i in range(0,self.notifyListbox.size()):
            urls.append(self.notifyListbox.get(i)[0])
            keywords.append(self.notifyListbox.get(i)[1])
        
        monitor_posting(self.RadioVariety,user,urls,keywords)
        
if __name__ == "__main__":
    PNGUI()