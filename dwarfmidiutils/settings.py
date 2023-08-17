
class Settings:
    def __init__(self, jsonFile, funcs, monitor):
        self.pageCursor=0
        self.itemCursor=0
        self.monitor = monitor
        self.funcs = funcs
        with open(jsonFile) as json_file:
            self.data = json.load(json_file)
        self.monitor.printout(self.isSettingsPage(), self.prettyPage())
        self.addContentPage("title", "one\ntwo\nthree")
        
    def handleJoyStick(self, vert,horz, click):
        if click:
            self.runFunction()
            return
        if vert<0: self.nextItem()
        if vert>0:  self.prevItem()
        if horz>0:self.changeUp(horz==2)    
        if horz<0:self.changeDown(horz==-2)
        
        
    def nextItem(self):
        print("next item")
        self.itemCursor += 1
        if self.pageSettingsCt() == self.itemCursor:
            self.pageCursor += 1
            self.itemCursor = 0
            if self.pageCt() == self.pageCursor:
                self.pageCursor = 0
        self.monitor.printout(self.isSettingsPage(), self.prettyPage())
        
    def prevItem(self):
        print("prev item")
        self.itemCursor -= 1
        if self.itemCursor <0:
            self.pageCursor -= 1
            self.itemCursor = 0
            if self.pageCursor<0:
                self.pageCursor = self.pageCt()-1
        self.monitor.printout(self.isSettingsPage(), self.prettyPage())

    def goPage(self,num):
        self.pageCursor = num
        self.itemCursor = 0
        self.monitor.printout(self.isSettingsPage(), self.prettyPage())

    def pageSettingsCt(self):
        page = self.data["pages"][self.pageCursor]
        if not "settings" in page:
            return 0
        return len(page["settings"])

    def pageCt(self):
        return (len(self.data["pages"]))

    def getKvp(self,pgItemNum):
        item = self.data["pages"][self.pageCursor]["settings"][pgItemNum]
        key = item["key"]
        value = item["value"]
        return key + "|" + str(value)
    
    def getContent(self,pgItemNum):
        item = self.data["pages"][self.pageCursor]["content"][pgItemNum]
        return item["value"]


    def runFunction(self):
        page = self.data["pages"][self.pageCursor]
        item = self.data["pages"][self.pageCursor]["settings"][self.itemCursor]        
        fn =  item["function"]
        val = item["value"]
        if fn=="parent":
            fn = page["function"]
            allVals = ""
            for item in page["settings"]:
                allVals += str(item["value"]) + ","
            funcs.run_func("self." + fn + "('" + allVals.rstrip(',') + "')")
        else: funcs.run_func("self." + fn + "(" + str(val) + ")")
        
    def isContentPage(self):
        page = self.data["pages"][self.pageCursor]
        if "content" in page:
            return True
        return False
    
    def isSettingsPage(self):
        page = self.data["pages"][self.pageCursor]
        if "settings" in page:
            return True
        return False


    def prettyPage(self):
        retval = ""
        if self.isContentPage():
            return self.getContent(0)
            
        for i in range(self.pageSettingsCt()):
            line = ""
            if self.itemCursor==i:line+="*"
            line+=self.getKvp(i) + "\n"
            retval+=line
        return retval

    def changeUp(self, bigly):
        if self.isContentPage():return
        self.changeBy(self.getAmt(bigly))

    def changeDown(self, bigly):
        if self.isContentPage():return
        self.changeBy(self.getAmt(bigly)*-1)

    def getAmt(self, bigly):
        if self.isContentPage():return
        item = self.data["pages"][self.pageCursor]["settings"][self.itemCursor]
        if bigly: return item["bigInc"]
        else: return item["inc"]

    def changeBy(self,amt):
        if self.isContentPage():return
        item = self.data["pages"][self.pageCursor]["settings"][self.itemCursor]
        if not "max" in item and "min" in item and "value" in item:
            return
        itemMax = item["max"]
        itemMin = item["min"]
        currVal = item["value"]
        newVal =max(min (currVal + amt,itemMax),itemMin)
        item["value"] =newVal
        self.monitor.printout(self.isSettingsPage(), self.prettyPage())
        
    def addContentPage(self, title, content):
        item = {}
        setting = {}        
        setting["key"] = title
        setting["value"] = content
        item["content"] = [setting]
        item["title"] = "Lyrics"
        item["function"] = "lyrics"
        self.data["pages"].append(item)
        print(self.data)