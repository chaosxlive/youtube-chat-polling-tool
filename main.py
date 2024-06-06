import tkinter as tk
from tkinter import messagebox
from chat_downloader import ChatDownloader
import json
import re
import requests
import threading


htmlCode = """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Document</title><script src="https://unpkg.com/vue@3/dist/vue.global.js"></script></head><body><div id="app"><ul id="top"><li v-for="item in items"><a :href="'#' + item.name">{{item.name}}</a></li></ul><template v-for="item in items"><h1 :id="item.name">{{item.name}}</h1><a href="#top">To top</a><template v-for="chatItem in item.data"><yt-live-chat-membership-item-renderer class="style-scope yt-live-chat-item-list-renderer" show-only-header="" style="color:#fff" v-if="chatItem.message_type === 'membership_item'"><div id="card" class="style-scope yt-live-chat-membership-item-renderer member-msg"><div id="header" class="style-scope yt-live-chat-membership-item-renderer"><yt-img-shadow id="author-photo" height="40" width="40" class="style-scope yt-live-chat-membership-item-renderer no-transition" loaded="" style="background-color:transparent"><img id="img" draggable="false" class="style-scope yt-img-shadow" alt="" height="40" width="40" :src="chatItem.author.images[0].url"></yt-img-shadow><div id="header-content" class="style-scope yt-live-chat-membership-item-renderer"><div id="header-content-primary-column" class="style-scope yt-live-chat-membership-item-renderer"><div id="header-content-inner-column" class="style-scope yt-live-chat-membership-item-renderer"><yt-live-chat-author-chip class="style-scope yt-live-chat-membership-item-renderer"><span id="author-name" dir="auto" class="member style-scope yt-live-chat-author-chip">{{chatItem.author.name}}</span><span id="chat-badges" class="style-scope yt-live-chat-author-chip" v-if="!!chatItem.author.badges"><yt-live-chat-author-badge-renderer class="style-scope yt-live-chat-author-chip" type="member"><div v-if="chatItem.author.badges[0].title === 'Moderator'">&nbsp;MOD</div><div v-else-if="chatItem.author.badges[0].title === 'Verified'">&nbsp;Verified</div><div id="image" class="style-scope yt-live-chat-author-badge-renderer" v-else><img :src="chatItem.author.badges[0].icons[0].url" width="16" height="16" class="style-scope yt-live-chat-author-badge-renderer" :alt="chatItem.author.badges[0].title"></div></yt-live-chat-author-badge-renderer></span></yt-live-chat-author-chip></div><div id="header-subtext" class="style-scope yt-live-chat-membership-item-renderer"><template v-if="chatItem.header_primary_text">{{chatItem.header_primary_text}}</template><template v-if="chatItem.header_secondary_text">{{chatItem.header_secondary_text}}</template></div></div><div id="timestamp" class="style-scope yt-live-chat-membership-item-renderer">{{chatItem.time_text}}</div></div></div><div id="content" class="style-scope yt-live-chat-membership-item-renderer" v-if="chatItem.message!=null"><div id="message" dir="auto" class="style-scope yt-live-chat-membership-item-renderer"><template v-for="msgItem in getMsgs(chatItem, chatItem.message, chatItem.emotes)"><template v-if="msgItem.isEmt"><img class="emoji yt-formatted-string style-scope yt-live-chat-membership-item-renderer" :src="msgItem.msg" width="24" height="24"></template><template v-else>{{msgItem.msg}}</template></template></div></div></div></yt-live-chat-membership-item-renderer><ytd-sponsorships-live-chat-header-renderer id="header" class="style-scope ytd-sponsorships-live-chat-gift-purchase-announcement-renderer member-msg" style="color:#fff" v-else-if="chatItem.message_type === 'ticker_sponsor_item'"><div id="header" class="style-scope ytd-sponsorships-live-chat-header-renderer"><div id="content" class="style-scope ytd-sponsorships-live-chat-header-renderer"><yt-img-shadow id="author-photo" height="40" width="40" class="style-scope ytd-sponsorships-live-chat-header-renderer no-transition" style="background-color:transparent" loaded=""><img id="img" draggable="false" class="style-scope yt-img-shadow" alt="" height="40" width="40" :src="chatItem.sponsor_icons[0].url"></yt-img-shadow><div id="header-content" class="style-scope ytd-sponsorships-live-chat-header-renderer"><div id="header-content-primary-column" class="style-scope ytd-sponsorships-live-chat-header-renderer"><div id="header-content-inner-column" class="style-scope ytd-sponsorships-live-chat-header-renderer"><yt-live-chat-author-chip single-line="" class="style-scope ytd-sponsorships-live-chat-header-renderer"><span id="author-name" dir="auto" class="member single-line style-scope yt-live-chat-author-chip">{{chatItem.author.name}}</span></yt-live-chat-author-chip><div id="primary-text" class="style-scope ytd-sponsorships-live-chat-header-renderer">送出了 {{getGiftCnt(chatItem.ticker_duration)}} 個「洛可洛斯特Loco Lost」的會籍</div></div><div id="secondary-text" class="style-scope ytd-sponsorships-live-chat-header-renderer"></div></div></div></div><yt-img-shadow class="rhs-image style-scope ytd-sponsorships-live-chat-header-renderer no-transition" height="50" width="50" style="background-color:transparent" loaded=""><img id="img" draggable="false" class="style-scope yt-img-shadow" alt="" height="50" width="50" src="https://www.gstatic.com/youtube/img/sponsorships/sponsorships_gift_purchase_announcement_artwork.png"></yt-img-shadow></div></ytd-sponsorships-live-chat-header-renderer><yt-live-chat-paid-message-renderer class="style-scope yt-live-chat-item-list-renderer" style="margin:4px 0" :style="{'background-color': chatItem.body_background_colour, 'color': chatItem.body_text_colour}" v-else-if="!chatItem.sticker_images"><div id="card" class="style-scope yt-live-chat-paid-message-renderer"><div id="header" class="style-scope yt-live-chat-paid-message-renderer" :style="{'background-color': chatItem.header_background_colour, 'color': chatItem.header_text_colour}"><yt-img-shadow id="author-photo" height="40" width="40" class="style-scope yt-live-chat-paid-message-renderer no-transition" style="background-color:transparent"><img id="img" draggable="false" class="style-scope yt-img-shadow" alt="" height="40" width="40" :src="chatItem.author.images[0].url"></yt-img-shadow><div id="header-content" class="style-scope yt-live-chat-paid-message-renderer"><div id="header-content-primary-column" class="style-scope yt-live-chat-paid-message-renderer"><div id="author-name-chip" class="style-scope yt-live-chat-paid-message-renderer"><yt-live-chat-author-chip disable-highlighting="" class="style-scope yt-live-chat-paid-message-renderer"><span id="author-name" dir="auto" class="member style-scope yt-live-chat-author-chip">{{chatItem.author.name}}<span id="chip-badges" class="style-scope yt-live-chat-author-chip"></span></span><span id="chat-badges" class="style-scope yt-live-chat-author-chip"><yt-live-chat-author-badge-renderer class="style-scope yt-live-chat-author-chip" type="member" v-if="!!chatItem.author.badges"><div id="image" class="style-scope yt-live-chat-author-badge-renderer"><div v-if="chatItem.author.badges[0].title === 'Moderator'">&nbsp;MOD</div><div v-else-if="chatItem.author.badges[0].title === 'Verified'">&nbsp;Verified</div><div id="image" class="style-scope yt-live-chat-author-badge-renderer" v-else><img :src="chatItem.author.badges[0].icons[0].url" width="16" height="16" class="style-scope yt-live-chat-author-badge-renderer" :alt="chatItem.author.badges[0].title"></div></div></yt-live-chat-author-badge-renderer></span></yt-live-chat-author-chip></div><div id="purchase-amount-column" class="style-scope yt-live-chat-paid-message-renderer"><yt-img-shadow id="currency-img" height="16" width="16" class="style-scope yt-live-chat-paid-message-renderer no-transition" hidden=""><img id="img" draggable="false" class="style-scope yt-img-shadow" alt="" height="16" width="16"></yt-img-shadow><div id="purchase-amount" class="style-scope yt-live-chat-paid-message-renderer"><yt-formatted-string class="style-scope yt-live-chat-paid-message-renderer">{{chatItem.money.text}}</yt-formatted-string></div></div></div><span id="timestamp" class="style-scope yt-live-chat-paid-message-renderer">{{chatItem.time_text}}</span></div></div><div id="content" class="style-scope yt-live-chat-paid-message-renderer"><div id="message" dir="auto" class="style-scope yt-live-chat-paid-message-renderer"><template v-for="msgItem in getMsgs(chatItem, chatItem.message, chatItem.emotes)"><template v-if="msgItem.isEmt"><img class="emoji yt-formatted-string style-scope yt-live-chat-membership-item-renderer" :src="msgItem.msg" width="24" height="24"></template><template v-else>{{msgItem.msg}}</template></template></div><div id="input-container" class="style-scope yt-live-chat-paid-message-renderer"></div><yt-formatted-string id="deleted-state" class="style-scope yt-live-chat-paid-message-renderer" is-empty=""></yt-formatted-string><div id="footer" class="style-scope yt-live-chat-paid-message-renderer"></div></div></div><div id="buy-flow-button" class="style-scope yt-live-chat-paid-message-renderer" hidden=""></div><div id="inline-action-button-container" class="style-scope yt-live-chat-paid-message-renderer" aria-hidden="true"><div id="inline-action-buttons" class="style-scope yt-live-chat-paid-message-renderer"></div></div></yt-live-chat-paid-message-renderer><yt-live-chat-paid-sticker-renderer class="style-scope yt-live-chat-item-list-renderer" v-else><div id="card" class="style-scope yt-live-chat-paid-sticker-renderer" style="padding:8px 16px;margin:4px 0;color:#fff;flex-direction:revert;align-items:center" :style="{'background-color': chatItem.background_colour}"><div id="author-info" tabindex="0" class="style-scope yt-live-chat-paid-sticker-renderer" style="display:flex;align-items:center"><yt-img-shadow id="author-photo" class="no-transition style-scope yt-live-chat-paid-sticker-renderer" style="background-color:transparent" loaded=""><img id="img" draggable="false" class="style-scope yt-img-shadow" alt="" width="40" height="40" :src="chatItem.author.images[0].url"></yt-img-shadow><div id="content" class="style-scope yt-live-chat-paid-sticker-renderer"><span id="timestamp" class="style-scope yt-live-chat-paid-sticker-renderer">{{chatItem.time_text}}</span><div id="content-primary-column" class="style-scope yt-live-chat-paid-sticker-renderer"><div id="author-name-chip" class="style-scope yt-live-chat-paid-sticker-renderer"><yt-live-chat-author-chip disable-highlighting="" single-line="" class="style-scope yt-live-chat-paid-sticker-renderer"><span id="author-name" dir="auto" class="member single-line style-scope yt-live-chat-author-chip">{{chatItem.author.name}}</span><span id="chat-badges" class="style-scope yt-live-chat-author-chip"><yt-live-chat-author-badge-renderer class="style-scope yt-live-chat-author-chip" type="member" v-if="!!chatItem.author.badges"><div id="image" class="style-scope yt-live-chat-author-badge-renderer"><div v-if="chatItem.author.badges[0].title === 'Moderator'">&nbsp;MOD</div><div v-else-if="chatItem.author.badges[0].title === 'Verified'">&nbsp;Verified</div><div id="image" class="style-scope yt-live-chat-author-badge-renderer" v-else><img :src="chatItem.author.badges[0].icons[0].url" width="16" height="16" class="style-scope yt-live-chat-author-badge-renderer" :alt="chatItem.author.badges[0].title"></div></div></yt-live-chat-author-badge-renderer></span></yt-live-chat-author-chip></div><span id="price-column" class="style-scope yt-live-chat-paid-sticker-renderer" v-if="chatItem.money && chatItem.money.text"><yt-formatted-string id="purchase-amount-chip" class="style-scope yt-live-chat-paid-sticker-renderer">{{ chatItem.money.text }}</yt-formatted-string><yt-formatted-string id="deleted-state" class="style-scope yt-live-chat-paid-sticker-renderer" is-empty=""></yt-formatted-string></span></div></div></div><div id="sticker-container" class="style-scope yt-live-chat-paid-sticker-renderer sticker-loaded"><yt-img-shadow id="sticker" notify-on-loaded="" tabindex="0" class="style-scope yt-live-chat-paid-sticker-renderer no-transition" style="background-color:transparent" loaded=""><img id="img" draggable="false" class="style-scope yt-img-shadow" width="40" height="40" :src="chatItem.sticker_images[0].url"></yt-img-shadow></div></div></yt-live-chat-paid-sticker-renderer></template></template></div></body><script>const app = {
    data () {
      return {
        items: "###ITEM###"
      };
    },
    methods: {
      getMsgs: (c, msg, emts) => {
        let items = [{
          isEmt: false,
          msg: msg,
        }];
        if (!emts) {
          return items;
        }
        let isUpdate = false;
        do {
          isUpdate = false;
          for (let emt of emts) {
            const newItems = [];
            for (let item of items) {
              if (!item.isEmt) {
                const splitted = item.msg.split(emt.name);
                const temp = [];
                while (splitted.length > 1) {
                  temp.push({
                    isEmt: false,
                    msg: splitted.splice(0, 1)[0],
                  });
                  temp.push({
                    isEmt: true,
                    msg: emt.images[0].url,
                  });
                  isUpdate = true;
                }
                temp.push({
                  isEmt: false,
                  msg: splitted.splice(0, 1)[0],
                });
                newItems.push(...temp.filter(v => v.msg.length > 0));
              } else {
                newItems.push(item);
              }
            }
            items = newItems;
          }
        } while (isUpdate);
        return items;
      },
      getGiftCnt: (duration) => {
        switch (duration) {
          case 7200:
            return '50';
          case 3600:
            return '20';
          case 1800:
            return '10';
          case 600:
            return '5';
          default:
            return '不知道多少個(應該是1個?)';
        }
      }
    }
  };

  Vue.createApp(app).mount('#app');</script><style>yt-live-chat-renderer{position:relative;height:100%;z-index:0;--color-head:#00BFA5;--color-body:#1DE9B6}yt-live-chat-paid-message-renderer{position:relative;display:block;font-size:15px;-webkit-animation-name:insert;animation-name:insert;-webkit-animation-duration:1s;animation-duration:1s}#card{position:relative;border-radius:4px;display:flex;flex-direction:column;min-width:200px;overflow:hidden}.close{font-size:12px;position:absolute;right:5px;top:5px;display:none;z-index:1}#card:hover .close{display:block}#header{position:relative;padding:8px 16px;min-height:20px;display:flex;flex-direction:row;align-items:center;color:var(--color-head-txt);background-color:var(--color-head)}#header-content-primary-column{display:flex;flex-direction:column}#author-photo{width:40px;height:40px;overflow:hidden;border-radius:50%;background-color:#fff;--default-src:url(https://yt3.ggpht.com/ytc/AAUvwnh3aAJX95-LepOS4z_EYe8P-Iv3l0TkhRmotxV5vBk=s176-c-k-c0x00ffffff-no-rj)}#author-photo #img{max-width:100%;max-height:100%}#author-name{font-size:14px}#header-content{display:inline;min-width:16px;padding:0 8px}#content{padding:8px 16px;color:var(--color-body-txt)!important;background-color:var(--color-body)!important}#author-name{display:block;font-weight:500}#timestamp{display:inline;font-size:13px}.soundbutton{padding:3px;font-size:13px}.text-break{word-wrap:break-word;word-break:break-word}.scrank0{--color-head:#1565c0;--color-head-txt:#ffffff;--color-body:#1e88e5;--color-body-txt:#ffffff}.scrank1{--color-head:#00b8d4;--color-head-txt:#000000;--color-body:#00e5ff;--color-body-txt:#000000}.scrank2{--color-head:#00bfa5;--color-head-txt:#000000;--color-body:#1de9b6;--color-body-txt:#000000}.scrank3{--color-head:#ffb300;--color-head-txt:#000000;--color-body:#ffca28;--color-body-txt:#000000}.scrank4{--color-head:#e65100;--color-head-txt:#ffffff;--color-body:#f57c00;--color-body-txt:#ffffff}.scrank5{--color-head:#c2185b;--color-head-txt:#ffffff;--color-body:#e91e63;--color-body-txt:#ffffff}.scrank6{--color-head:#d00000;--color-head-txt:#ffffff;--color-body:#e62117;--color-body-txt:#ffffff}.yt-small-image{max-width:24px}body{background-color:rgba(0,0,0,0);padding:0;margin:0;overflow-y:scroll;overflow-x:hidden}#contents{display:flex;flex-direction:column-reverse}.sc-success{border-color:#28a745}.sc-fail{border-style:solid none none none;border-color:#dc3545}.member-msg{background-color:#0f9d58!important;margin:4px 0!important}yt-live-chat-author-chip{display:flex}#content.ytd-sponsorships-live-chat-header-renderer{padding-top:8px;padding-bottom:8px;padding-left:16px;display:flex;flex-direction:row;margin-right:auto}.yt-live-chat-author-badge-renderer{margin-left:2px}</style></html>
"""


class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.addedLines = 0
        self.jobs = {}

        self.initWidgetsFrame()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def initWidgetsFrame(self):
        self.frame = tk.Frame(self)

        rowCnt = 1
        self.labelVideoId = tk.Label(self.frame, pady=10, text='Video Id', width=10, font=('arial', 12))
        self.labelVideoId.grid(row=rowCnt, column=0)
        self.entryVideoId = tk.Entry(self.frame, width=30)
        self.entryVideoId.grid(row=rowCnt, column=1)

        rowCnt += 1
        self.labelTitle = tk.Label(self.frame, pady=10, text='Section title', anchor=tk.E, width=10, font=('arial', 12))
        self.labelTitle.grid(row=rowCnt, column=0)
        self.entryTitle = tk.Entry(self.frame, width=30)
        self.entryTitle.grid(row=rowCnt, column=1)

        rowCnt += 1
        self.buttonAdd = tk.Button(self.frame, pady=10, text='Add', width=50, command=self.onButtonAddClick)
        self.buttonAdd.grid(row=rowCnt, column=0, columnspan=2)

        rowCnt += 1
        self.buttonDelete = tk.Button(self.frame, pady=10, text='Delete', width=50, command=self.onButtonDeleteClick)
        self.buttonDelete.grid(row=rowCnt, column=0, columnspan=2)

        rowCnt += 1
        self.frameDisplay = tk.Frame(self.frame, pady=10, width=100)
        self.scrollbarDisplay = tk.Scrollbar(self.frameDisplay)
        self.scrollbarDisplay.pack(side=tk.RIGHT, fill=tk.Y)
        self.listboxDisplay = tk.Listbox(self.frameDisplay, width=50, height=15, yscrollcommand=self.scrollbarDisplay.set)
        self.listboxDisplay.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbarDisplay.config(command=self.listboxDisplay.yview)
        self.frameDisplay.grid(row=rowCnt, column=0, columnspan=2)

        rowCnt += 1
        self.buttonExecute = tk.Button(self.frame, pady=10, text='Execute', width=50, command=self.onButtonExecuteClick)
        self.buttonExecute.grid(row=rowCnt, column=0, columnspan=2)

        self.frame.grid(row=1, column=1)

    def onButtonAddClick(self):
        if len(self.entryVideoId.get()) == 0 or len(self.entryTitle.get()) == 0:
            return
        self.addedLines += 1
        text = f"{self.addedLines:>3}. [{self.entryVideoId.get():<13}] >>> {self.entryTitle.get()}"
        self.jobs[text] = {
            'id': self.entryVideoId.get(),
            'title': self.entryTitle.get(),
        }
        self.listboxDisplay.insert(tk.END, text)
        self.entryTitle.delete(0, tk.END)
        self.entryVideoId.delete(0, tk.END)
        print(self.jobs)

    def onButtonDeleteClick(self):
        curSelection = self.listboxDisplay.curselection()
        if len(curSelection) == 0:
            return
        self.jobs.pop(self.listboxDisplay.get(curSelection[0]), None)
        self.listboxDisplay.delete(curSelection[0])
        print(self.jobs)

    def onButtonExecuteClick(self):
        self.buttonExecute.config(state=tk.DISABLED)
        threading.Thread(target=self.startDownloadJob).start()

    def startDownloadJob(self):
        downloader = ChatDownloader()
        result = []
        for name, vid in map(lambda job: (job['title'], job['id']),self.jobs.values()):
            print(name)
            try:
                chat = downloader.get_chat(f'https://www.youtube.com/watch?v={vid}', message_types=[
                    'ticker_sponsor_item',
                    'membership_item',
                    'paid_message',
                    'paid_sticker',
                ])
                chatList = []
                for message in chat:
                    if message['message_type'] == 'ticker_sponsor_item':
                        if message['message'] != None:
                            continue
                        elif message['ticker_duration'] not in [7200, 3600, 1800, 600]:
                            continue
                        print("test chid: ", message['author']['id'])
                        res = requests.get(f"https://www.youtube.com/channel/{message['author']['id']}")
                        chName = re.search('"channelId":"[^"]*","title":"([^"]*)"', res.text)[1]
                        print("found name: ", chName)
                        message['author']['name'] = chName
                    chatList.append(message)
                result.append({
                    "name": name,
                    "data": chatList,
                })
            except:
                print(f"Error! {name}")
        returned = htmlCode.replace("\"###ITEM###\"", json.dumps(result, indent=4, ensure_ascii=False))
        with open(f'output.html', 'w', encoding='utf8') as f:
            f.write(returned)
        self.listboxDisplay.delete(0, tk.END)
        self.jobs.clear()
        self.addedLines = 0
        self.buttonExecute.config(state=tk.NORMAL)
        messagebox.showinfo('Complete', 'Complete!')



if __name__ == "__main__":
    appRoot = tk.Tk()
    appRoot.geometry('800x500')
    appRoot.title('Youtube SC 抓取工具')
    appRoot.resizable(width=False, height=False)
    MainFrame(appRoot).grid(sticky="nsew")
    appRoot.grid_rowconfigure(0, weight=1)
    appRoot.grid_columnconfigure(0, weight=1)

    appRoot.mainloop()



# pyinstaller: move custom_formats.json to replace the format.py content.