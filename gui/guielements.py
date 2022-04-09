import pygame as pg

from utils import Supply


def supplyToList(supply):
    maintext = [str(supply.cloth) + " cloth"]
    maintext += [str(supply.food) + " food"]
    maintext += [str(supply.medicine) + " meds"]
    return maintext


class InputBox:
    def __init__(self, left, right, width, height, basestr=''):
        self.input_box = pg.Rect(left, right, width, height)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = basestr
        self.font = pg.font.Font(None, 32)

        self.firstClick = True
        self.basestr = basestr

    def react(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.input_box.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                if self.firstClick:
                    self.text = self.basestr
                    self.firstClick = False
            else:
                self.active = False
            
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def render(self, screen, newv=None):
        # Render the current text.
        txt_surface = self.font.render(self.text, True, self.color)
        # Resize the box if the text is too long.
        v = 200
        if newv:
            v = newv

        width = max(v, txt_surface.get_width()+10)
        self.input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, self.color, self.input_box, 2)


class Button:
    def __init__(self, left, right, width, height, text):
        self.input_box = pg.Rect(left, right, width, height)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_active
        self.active = True
        self.text = text
        self.font = pg.font.Font(None, 32)

    def react(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.input_box.collidepoint(event.pos):
                return True

        return False

    def render(self, screen, newv=None):
        # Render the current text.
        txt_surface = self.font.render(self.text, True, self.color)
        # Resize the box if the text is too long.
        v = 200
        if newv:
            v = newv
        width = max(v, txt_surface.get_width()+10)
        self.input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (self.input_box.x+60, self.input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, self.color, self.input_box, 2)


class LogInScreen:
    def __init__(self):
        self.inbox1 = InputBox(100, 100, 140, 32)
        self.inbox2 = InputBox(100, 200, 140, 32)
        self.login = Button(100, 300, 140, 32, "LOGIN")
        self.inbox1.text = "username"
        self.inbox2.text = "password"

    def react(self, event):
        self.inbox1.react(event)
        self.inbox2.react(event)
        return self.login.react(event)

    def render(self, screen):
        self.inbox1.render(screen)
        self.inbox2.render(screen)
        self.login.render(screen)

    def getInfo(self):
        return self.inbox1.text, self.inbox2.text


class MutltiplyMessages:
    def __init__(self, left, right, width, height, messages):
        self.input_box = pg.Rect(left, right, width, height)
        self.color = pg.Color('lightskyblue3')
        self.font = pg.font.Font(None, 32)

        self.messages = messages


    def render(self, screen):
        y_disposition = 0
        for text in self.messages:    
            txt_surface = self.font.render(text, True, self.color)
            # Resize the box if the text is too long.
            width = max(150, txt_surface.get_width()+10)
            self.input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5 + y_disposition * 30))
            y_disposition += 1
        pg.draw.rect(screen, self.color, self.input_box, 2)


class CorrectUserPage:
    def __init__(self, username, received, remained):
        self.welcom = InputBox(50, 50, 140, 32)
        self.welcom.text = "Dear " + username + ", wlcome to USA!"
        
        
        maintext = ["Received:"]
        maintext += supplyToList(received)
        
        self.message = MutltiplyMessages(50, 100, 200, 120, maintext)

        
        maintext = ["Remained:"]
        maintext += supplyToList(remained)
        
        self.message1 = MutltiplyMessages(250, 100, 200, 120, maintext)

        self.received = received
        self.remained = remained

        # logout
        self.logout = Button(100, 300, 140, 32, "LOGOUT")
        self.getSupply = Button(100, 250, 140, 32, "Receive")

    def update(self, received):
        maintext = ["Received:"]
        maintext += supplyToList(received)
        self.message = MutltiplyMessages(50, 100, 200, 120, maintext)

        maintext = ["Remained:"]
        maintext += supplyToList(Supply())
        self.message1 = MutltiplyMessages(250, 100, 200, 120, maintext)
        

    def react(self, event):
        
        return self.logout.react(event), self.getSupply.react(event)

    def render(self, screen):
        self.welcom.render(screen)
        self.message.render(screen) 
        self.message1.render(screen)
        self.logout.render(screen)
        self.getSupply.render(screen)


class CorrectCharityPage:
    def __init__(self, donated):
        self.welcom = InputBox(50, 50, 140, 32)
        self.welcom.text = "Thank you for donations!"
        maintext = ["Donated:"]
        maintext += supplyToList(donated)
        self.logout = Button(100, 300, 140, 32, "LOGOUT")
        self.message = MutltiplyMessages(50, 100, 200, 120, maintext)
        self.donate = Button(100, 250, 140, 32, "Donate")

        self.clothIn = InputBox(230, 100, 90, 32, "Cloth:")
        self.foodIn = InputBox(230, 140, 90, 32, "Food:")
        self.medIn = InputBox(230, 180, 90, 32, "Med:")


    def resetInput(self):
        self.clothIn = InputBox(230, 100, 90, 32, "Cloth:")
        self.foodIn = InputBox(230, 140, 90, 32, "Food:")
        self.medIn = InputBox(230, 180, 90, 32, "Med:")

    def update(self, received):
        maintext = ["Donated:"]
        maintext += supplyToList(received)
        self.message = MutltiplyMessages(50, 100, 200, 120, maintext)

    def react(self, event):
        self.clothIn.react(event)
        self.foodIn.react(event)
        self.medIn.react(event)
        return self.logout.react(event), self.donate.react(event)


    def getDonation(self):
        cloth = 0
        med=0
        food=0

        if self.clothIn.text != self.clothIn.basestr:
            cloth = int(self.clothIn.text.split(":")[1])

        if self.medIn.text != self.medIn.basestr:
            med = int(self.medIn.text.split(":")[1])

        if self.foodIn.text != self.foodIn.basestr:
            food = int(self.foodIn.text.split(":")[1])

        return Supply(Supply.Config(cloth, food, med))
        

    def render(self, screen):
        self.welcom.render(screen)
        self.message.render(screen) 
        self.logout.render(screen)
        self.donate.render(screen)
        self.clothIn.render(screen, 110)
        self.foodIn.render(screen, 110)
        self.medIn.render(screen, 110)