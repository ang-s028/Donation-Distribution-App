class Supply:
    class Config:
        def __init__(self, cloth, food, medicine):
            self.cloth = cloth
            self.food = food
            self.medicine = medicine

    def __init__(self, config=None):
        self.cloth = 0
        self.food = 0
        self.medicine = 0

        if config:
            self.cloth = config.cloth
            self.food = config.food
            self.medicine = config.medicine
    
    def add(self, other):
        self.cloth += other.cloth
        self.food += other.food
        self.medicine += other.medicine

    def subtract(self, other):
        config = Supply.Config(
            cloth=min(other.cloth, self.cloth),
            food=min(other.food, self.food),
            medicine=min(other.medicine, self.medicine),
        )

        subtracted = Supply(config)
        self.cloth -= subtracted.cloth
        self.food -= subtracted.food
        self.medicine -= subtracted.medicine

        return subtracted

    def __str__(self):
        return '{cloth:' + str(self.cloth) +' , food:' + str(self.food) + ' medicine:' + str(self.medicine) + '}'

    def __repr__(self):
        return self.__str__()


def supplysToStr(supplys):
    return (
        str(supplys.cloth) + "\t" +
        str(supplys.food) + "\t" +
        str(supplys.medicine)
    )


def strToSupplys(inputString):
    cloth, food, medicine = inputString.split("\t")
    return Supply(Supply.Config(int(cloth), int(food), int(medicine)))


def saveSupplys(supplys, file):
    file.write(supplysToStr(supplys))


def loadSupplys(file):
    return strToSupplys(file.readlines()[0])


def userToStr(username, l):
    return (
        username + "\t" +
        l[0] + "\t" +
        str(l[1]) + "\t" +
        str(l[2].cloth) + "\t" +
        str(l[2].food) + "\t" +
        str(l[2].medicine) + "\n"
    )


def strToUser(inputString):
    username, passwd, month, cloth, food, medicine = inputString.split("\t")
    sp = Supply(Supply.Config(int(cloth), int(food), int(medicine)))
    return username, [passwd, int(month), sp, 0]


def saveUsers(users, f):
    finalStr = ""
    for k in users.keys():
        finalStr += userToStr(k, users[k])

    f.write(finalStr)


def loadUsers(f):
    lines = f.readlines()
    ret = {}
    for line in lines:
        usr, l = strToUser(line)
        ret[usr] = l

    return ret


def charToStr(username, l):
    return (
        username + "\t" +
        l[0] + "\t" +
        str(l[1].cloth) + "\t" +
        str(l[1].food) + "\t" +
        str(l[1].medicine) + "\n"
    )


def strToChar(inputString):
    username, passwd, cloth, food, medicine = inputString.split("\t")
    return username, [passwd, Supply(Supply.Config(int(cloth), int(food), int(medicine))), 0]


def saveChars(users, f):
    finalStr = ""
    for k in users.keys():
        finalStr += charToStr(k, users[k])

    f.write(finalStr)

def loadChars(f):
    lines = f.readlines()
    ret = {}
    for line in lines:
        usr, l = strToChar(line)
        ret[usr] = l

    return ret

"""
def main():

    f = open("test.txt", "w")
    s = Supply(Supply.Config(1000, 32423, 25232))

    saveSupplys(s, f)
    f.close()
    f = open("test.txt", "r")

    s = loadSupplys(f)
    print(s)
    return 0


if __name__ == "__main__":
    main()
"""