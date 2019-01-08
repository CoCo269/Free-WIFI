import os, sys

STR_SETMODE = "netsh wlan set hostednetwork mode=allow"
STR_SETNET = "netsh wlan set hostednetwork"
STR_STARTNET = "netsh wlan start hostednetwork"

STR_NAME_PREFIX = " ssid="
STR_CODE_PREFIX = " key="

STR_NAME = ""
STR_CODE = ""

STR_SHOWNET = "netsh wlan show hostednetwork"
STR_STOPNET = "netsh wlan stop hostednetwork"


#====================================================================================
def startWifi(*args):
    stopWifi() # close old wifi
    if not STR_NAME or not STR_CODE:
        print("Set Wifi Name And Code First!!!")
        return
    os.system(STR_SETMODE)
    os.system(STR_SETNET+STR_NAME_PREFIX+STR_NAME+STR_CODE_PREFIX+STR_CODE)
    os.system(STR_STARTNET)
    print("Wifi Start!!!")

def stopWifi(*args):
    os.system(STR_STOPNET)
    print("Wifi Stop!!!")

def showWifi(*args):
    print("Wifi State as follow:")
    print("Wifi Name: "+STR_NAME+"\nWifi Code: "+STR_CODE)
    os.system(STR_SHOWNET)

# ================================ Account Manage =================================== #

LOCAL_DATA_FILE = "free-wifi-data.csv"
TEMP_ACCOUNT_DATA = None
SELECTED_ACCOUNT_KEY = None

#==========================================================
def validateAccountInfo():
    if SELECTED_ACCOUNT_KEY == None:
        return
    dumpAccountFile()
    setSTRName()
    setSTRCode()

def dumpAccountFile():
    with open(LOCAL_DATA_FILE, "w") as fout:
        for line in TEMP_ACCOUNT_DATA:
            fout.write(line[0]+","+line[1])
            if len(line) > 2:
                fout.write(","+line[2])
            fout.write("\n")

def setSTRName():
    global STR_NAME
    STR_NAME = TEMP_ACCOUNT_DATA[SELECTED_ACCOUNT_KEY][0]

def setSTRCode():
    global STR_CODE
    STR_CODE = TEMP_ACCOUNT_DATA[SELECTED_ACCOUNT_KEY][1]

#================================================================
def newAccount(*args):
    global TEMP_ACCOUNT_DATA
    try:
        new_user = args[0].split(":")
        new_user[0] = new_user[0].strip()
        new_user[1] = new_user[1].strip()
        if new_user[0] and new_user[1]:
            TEMP_ACCOUNT_DATA.append(new_user)
            # makeSelection(len(TEMP_ACCOUNT_DATA)-1) # auto select the new one
            selectAccount(len(TEMP_ACCOUNT_DATA)-1) # auto select the new one
            print("New Succeed")
            return
        else:
            raise ValueError
    except:
        print("Illegal Format: "+args[0])

#================================================================
def deleteAccount(*args):
    global TEMP_ACCOUNT_DATA, SELECTED_ACCOUNT_KEY
    try:
        code = args[0]
        code = int(code)
        if len(TEMP_ACCOUNT_DATA) <= code or code < 0:
            raise ValueError
        if SELECTED_ACCOUNT_KEY > code:
            SELECTED_ACCOUNT_KEY = SELECTED_ACCOUNT_KEY-1
        elif SELECTED_ACCOUNT_KEY == code:
            makeSelection(0) # auto select the first one
        del TEMP_ACCOUNT_DATA[code]
        if not TEMP_ACCOUNT_DATA: # When None
            SELECTED_ACCOUNT_KEY = None
    except Exception as e:
        print("Delete Need A Number ...")
        print(e)

#================================================================
def selectAccount(*args):
    try:
        if needFresh():
            loadAccountFile()
        code = args[0]
        makeSelection(int(code))
        validateAccountInfo() # valid setting
        showSelectedAccount()
    except Exception as e:
        print("Select Need A Number ...")
        print(e)

def showSelectedAccount():
    tpls = TEMP_ACCOUNT_DATA[SELECTED_ACCOUNT_KEY]
    print("Selected %s:%s" % (tpls[0], tpls[1]))

def makeSelection(tag):
    global SELECTED_ACCOUNT_KEY, TEMP_ACCOUNT_DATA
    if not TEMP_ACCOUNT_DATA:
        SELECTED_ACCOUNT_KEY = None
        print("Account List is NULL ...")
        return
    if tag >= len(TEMP_ACCOUNT_DATA) or tag < 0:
        print("Your Number In Illegal Range ...")
        return
    if SELECTED_ACCOUNT_KEY != None and SELECTED_ACCOUNT_KEY < len(TEMP_ACCOUNT_DATA) and SELECTED_ACCOUNT_KEY >= 0:
        TEMP_ACCOUNT_DATA[SELECTED_ACCOUNT_KEY] = TEMP_ACCOUNT_DATA[SELECTED_ACCOUNT_KEY][:2]
    SELECTED_ACCOUNT_KEY = tag
    TEMP_ACCOUNT_DATA[SELECTED_ACCOUNT_KEY].append("#")

#===================================================================
def loadAccount(*args):
    global TEMP_ACCOUNT_DATA, SELECTED_ACCOUNT_KEY
    if needFresh():
        loadAccountFile()
    print("----------- Users Info -----------")
    for idx, user in enumerate(TEMP_ACCOUNT_DATA):
        print(str(idx)+" : "+user[0]+"  "+user[1], end="")
        if len(user) > 2:
            SELECTED_ACCOUNT_KEY = idx # current selection
            print("  "+user[2])
        else:
            print("")
    print("----------------------------------")

def needFresh():
    return TEMP_ACCOUNT_DATA == None

def loadAccountFile():
    global TEMP_ACCOUNT_DATA
    tp_ac_data = []
    if os.path.exists(LOCAL_DATA_FILE):
        with open(LOCAL_DATA_FILE, "r") as fin:
            for line in fin.readlines():
                line = line.strip()
                if not line:
                    continue
                tp_ac_data.append(line.split(","))
    TEMP_ACCOUNT_DATA = tp_ac_data # update


def clear(*args):
    os.system("cls")
    print("============== Free Wifi =============")
    print("""Support Command:\n  start | stop | state\n  new <name>:<code> | delete <tag>\n  list | select <tag>\n  clear | quit\n""")

ITEM_FUNCTIONS = {"start":startWifi, "stop":stopWifi, "state":showWifi,
                     "new":newAccount, "delete":deleteAccount, "list":loadAccount,
                      "select":selectAccount, "clear":clear, "quit":quit}

if __name__ == "__main__":
    clear()
    try:
        loadAccount()
        if SELECTED_ACCOUNT_KEY >= 0:
            selectAccount(SELECTED_ACCOUNT_KEY)
        else:
            print("Can't Find AccountList File, Please New One...")
    except Exception as e:
        print("Load Last Setting Failed ...")
    while 1:
        try:
            comd = input("\n>>")
            comd = comd.split(' ')
            if comd[0] in ITEM_FUNCTIONS:
                ITEM_FUNCTIONS[comd[0]](*(comd[1:] if len(comd) > 1 else []))
            else:
                print("Unknown Command ...")
        except Exception as e:
            print("Unknown Error in Command: ", e)
