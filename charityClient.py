from xxlimited import new
import pygame as pg
from gui.guielements import CorrectCharityPage, LogInScreen, CorrectUserPage
from gui.page import Page
from networkutils import DONATE, LOGINCHAR, RECEIVE, login as loginAction
from networkutils import receive as receiveAction
from networkutils import donate as donateAction
from networkutils import ERROR
from utils import strToSupplys

def charityLogin():
    ret = LogInScreen()
    ret.inbox1.text = "charityname"
    return ret

def main():
    screen = pg.display.set_mode((420, 480))
    clock = pg.time.Clock()
    
    loginscreen = charityLogin()
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
                    ret = loginAction(LOGINCHAR, username, passwd)

                    if ret != ERROR:
                        currentPage = Page.CORRECT
                        correctPage = CorrectCharityPage(strToSupplys(ret))

            elif currentPage == Page.CORRECT:
                logout, donate = correctPage.react(event)
                if (logout):
                    currentPage = Page.LOGIN
                    loginscreen = charityLogin()
                    correctPage = None
                elif donate:
                    resource = correctPage.getDonation()
                    
                    newTotal = donateAction(DONATE, username, resource)
                    newTotal = strToSupplys(newTotal)
                    correctPage.update(newTotal)
                    correctPage.resetInput()
                

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
