import sys
import signal

from utils import Supply, loadSupplys, loadChars, loadUsers, saveChars, saveSupplys, saveUsers, strToSupplys, supplysToStr
from networkutils import DONATE, LOGINCHAR, RECEIVE, serverConnect, LOGINUSER, ERROR

class Database:
    def __init__(self, userInfoFile=None, charityInfoFile=None, supplyInfoFile=None, load=False):
        # dictionary from string to a list
        # the list contains password & months in system & received supply & if logged in
        self.users = {}
        
        # dictionary from string to a list
        # the list contains password & donated supply & if logged in
        self.charities = {}

        # remaining supply
        self.supplys = Supply()

        # every month, a person can receive 1 unit of cloth, 5 unit of food, and 3 units of medicine
        self.quota = {"cloth":1, "food":5, "medicine":3}

        # save filename to save later
        self.userInfoFile = userInfoFile
        self.charityInfoFile = charityInfoFile
        self.supplyInfoFile = supplyInfoFile

        # load if filenames are given
        if userInfoFile and load:
            fileUsers = open(userInfoFile, "r")
            self.users = loadUsers(fileUsers)
            fileUsers.close()

        if charityInfoFile and load:
            fileChars = open(charityInfoFile, "r")
            self.charities = loadChars(fileChars)
            fileChars.close()

        if supplyInfoFile and load:
            fileSupps = open(supplyInfoFile, "r")
            self.supplys = loadSupplys(fileSupps)
            fileSupps.close()


    def save(self):
        if self.userInfoFile:
            fileUsers = open(self.userInfoFile, "w")
            saveUsers(self.users, fileUsers)
            fileUsers.close()

        if self.charityInfoFile:
            fileChars = open(self.charityInfoFile, "w")
            saveChars(self.charities, fileChars)
            fileChars.close()

        if self.supplyInfoFile:
            fileSupps = open(self.supplyInfoFile, "w")
            saveSupplys(self.supplys, fileSupps)
            fileSupps.close()


    def userLogin(self, username, password):
        # add a user if not found
        if username not in self.users.keys():
            self.users[username] = [password, 1, Supply(), 0]

        userEntry = self.users[username]

        if userEntry[0] != password:
            return None

        remainedSupply = self.getRemainingSuppy(userEntry)

        # login success
        self.users[username][3] = 1
        return [userEntry[2], remainedSupply]

    def charityLogin(self, username, password):
        # add a charity if not found
        if username not in self.charities.keys():
            self.charities[username] = [password, Supply(), 0]

        userEntry = self.charities[username]

        if userEntry[0] != password:
            return None

        self.charities[username][2] = 1

        return userEntry[1]

    def userLogOut(self, username):
        if username not in self.users.keys():
            return None

        userEntry = self.users[username]
        if userEntry[3] == 0:
            return None

        self.users[username][3] = 0

        return 0

    def charityLogOut(self, username):
        if username not in self.charities.keys():
            return None

        userEntry = self.charities[username]
        if userEntry[2] == 0:
            return None

        self.charities[username][2] = 0
        return 0


    def receive(self, username):
        if username not in self.users.keys():
            return None

        userEntry = self.users[username]
        if userEntry[3] == 0:
            return None

        receivedSupply = self.getRemainingSuppy(userEntry)
        self.users[username][2].add(receivedSupply)
        self.supplys.subtract(receivedSupply)

        return receivedSupply


    def donate(self, username, supply):
        if username not in self.charities.keys():
            return None

        userEntry = self.charities[username]
        if userEntry[2] == 0:
            return None

        self.charities[username][1].add(supply)
        self.supplys.add(supply)
        return self.charities[username][1]

    def getRemainingSuppy(self, userEntry):
        monthStayed = userEntry[1]
        receivedSupply = userEntry[2]
        config = Supply.Config(
            cloth=min(max(0, monthStayed*self.quota["cloth"] - receivedSupply.cloth), self.supplys.cloth),
            food=min(max(0, monthStayed*self.quota["food"] - receivedSupply.food), self.supplys.food),
            medicine=min(max(0, monthStayed*self.quota["medicine"] - receivedSupply.medicine), self.supplys.medicine),
        )
        return Supply(config)

    def __str__(self):
        return (
            "Total Remaining Supplies: " 
            + str(self.supplys) 
            + "\nList of Charities" 
            + str(self.charities)  
            + "\nList of Users" 
            + str(self.users)
        )


# exit funciton
def exitFunc(signum, frame):
    print("Contl-c was pressed, saving databases & exiting")
    if server:
        server.save()

    s.close()
    sys.exit(0)



def main(args):
    global server
    server = Database(
        userInfoFile="data/users.txt", 
        charityInfoFile="data/charities.txt", 
        supplyInfoFile="data/supplys.txt",
        load=True,
    )
    print(server)

    global s 
    s = serverConnect()
    signal.signal(signal.SIGINT, exitFunc)
    print("Database booting up")

    while True:
        s.listen()
        newS, addr = s.accept()
        
        message = newS.recv(1024).decode().split("\t")
        print(message)
        if message[0] == LOGINUSER:
            ret = server.userLogin(message[1], message[2])
            if ret != None:
                received, remained = ret
                newS.send(str.encode(supplysToStr(received) + "\n" + supplysToStr(remained)))
            else:
                newS.send(str.encode(ERROR))

        elif message[0] == RECEIVE:
            ret = server.receive(message[1])
            newS.send(str.encode(supplysToStr(received)))
        elif message[0] == LOGINCHAR:
            ret = server.charityLogin(message[1], message[2])
            print(ret)
            if ret != None:
                donated = ret
                newS.send(str.encode(supplysToStr(donated)))
            else:
                newS.send(str.encode(ERROR))
        elif message[0] == DONATE:
            donated = Supply(Supply.Config(int(message[2]), int(message[3]), int(message[4])))
            ret = server.donate(message[1], donated)
            newS.send(str.encode(supplysToStr(ret)))
        else:
            newS.send(str.encode("sure\n"))

        newS.close()
    s.close()



if __name__ == "__main__":
    main(None)