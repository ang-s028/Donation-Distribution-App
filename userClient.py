import pygame as pg
from gui.guielements import LogInScreen, CorrectUserPage
from gui.page import Page
from networkutils import RECEIVE, login as loginAction
from networkutils import receive as receiveAction
from networkutils import LOGINUSER, ERROR
from utils import strToSupplys


def main():
    screen = pg.display.set_mode((420, 480))
    clock = pg.time.Clock()
    
    loginscreen = LogInScreen()
    done = False
    currentPage = Page.LOGIN
    correctPage = None

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if currentPage == Page.LOGIN:
                tryLogin = loginscreen.react(event)
                if tryLogin:
                    # login ons
                    username, passwd = loginscreen.getInfo()
                    print("Trying logging")
                    ret = loginAction(LOGINUSER, username, passwd)

                    if ret != ERROR:
                        currentPage = Page.CORRECT
                        splitedRet = ret.split("\n")

                        correctPage = CorrectUserPage(username, strToSupplys(splitedRet[0]), strToSupplys(splitedRet[1]))

            elif currentPage == Page.CORRECT:
                logout, getSupply = correctPage.react(event)
                if (logout):
                    currentPage = Page.LOGIN
                    loginscreen = LogInScreen()
                    correctPage = None
                elif(getSupply):
                    username, passwd = loginscreen.getInfo()
                    received = receiveAction(RECEIVE, username)
                    received = strToSupplys(received)
                    correctPage.update(received)


        screen.fill((255, 255, 255))
        
        if currentPage == Page.LOGIN:
            loginscreen.render(screen)
        elif currentPage == Page.CORRECT:
            correctPage.render(screen)

        pg.display.flip()
        clock.tick(30)



if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
