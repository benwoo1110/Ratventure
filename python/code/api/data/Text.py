######################################
# Import and initialize the librarys #
######################################
import textwrap
import re
from code.api.core import os, log, coreFunc, PgEss, pygame
from code.api.actions import Alert
from code.api.data.Frame import Frame
from code.api.data.Sound import sound


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)


class TextFormat(coreFunc):
    def __init__(self, fontType:str = PgEss.font.knigqst, fontSize:int = 36, colour:tuple = PgEss.colour.black, 
    warpText:int = None, align:str = 'left', pos:str = 'top', lineSpacing:int = 1):
        self.fontType = fontType
        self.fontSize = fontSize
        self.colour = colour
        self.warpText = warpText
        self.align = align
        self.pos = pos
        self.lineSpacing = lineSpacing
        self.font = pygame.font.Font(self.fontType, self.fontSize)

    def modifyFont(self, fontSize:int = None, fontType:str = None):
        # set new font size and type (if any)
        if fontSize != None: self.fontSize = fontSize
        if fontType != None: self.fontType = fontType

        # Regen the font
        self.font = pygame.font.Font(self.fontType, self.fontSize)


class TextValidate(coreFunc):
    def __init__(self, charsAllowed:list = list(range(32,65)) + list(range(91,127)) + [8], 
    inAscii:bool = True, regex:str = '[\w\D.]+', defaultText:str = 'default', customMethod:any = None, invalidPrompt:str = None):
        self.charsAllowed = charsAllowed
        self.inAscii = inAscii
        self.regex = re.compile(regex)
        self.defaultText = defaultText
        self.customMethod = customMethod
        self.invalidPrompt = invalidPrompt

class Text(coreFunc):
    def __init__(self, frame:Frame, text:str = '', prefix:str = '', suffix:str = '', name=None, item=None,
    format:TextFormat = TextFormat(), validation:TextValidate = TextValidate(), editable:bool = True):
        self.name = name
        self.item = item
        self.frame = frame
        self.text = text
        self.prefix = prefix
        self.suffix = suffix
        self.format = format
        self.validation = validation
        self.editable = editable
        self.loaded = False

    def validateChar(self, char, inAscii = True):
        # Ensure that character is alloweed for that textfield
        if self.validation.inAscii and not inAscii: char = ord(char)
        elif not self.validation.inAscii and inAscii: char = chr(char)

        return char in self.validation.charsAllowed

    def validateText(self):
        # Check for regex matching
        valid = self.validation
        regexTexts = valid.regex.findall(self.text)
        logger.debug('[{}] Regex matching result of {}'.format(self.item.name, regexTexts))

        # Full match
        if len(regexTexts) == 1 and regexTexts[0] == self.text: 
            if callable(valid.customMethod): return valid.customMethod(self.text)
            return True

        # Invalid based on regex
        else:
            if self.validation.invalidPrompt != None:
                # Error sound
                sound.error.play()

                # Tell user is invalid
                Alert(
                    type='notify', 
                    title='Invalid Input',
                    content=self.validation.invalidPrompt
                ).do()

            return False

    def getText(self):
        # Combine prefix, text and suffix
        try:
            if self.item.state == 'Selected' and self.editable: return self.prefix+self.text+'_'+self.suffix
            else: return self.prefix+self.text+self.suffix
        
        # Error, usually due to prefix, text or suffix not being str
        except:
            logger.error('Error getting text for {}'.format(self.name), exc_info=True)
            return 'Error'

    def setText(self, text:str = None, prefix:str = None, suffix:str = None, withDisplay: bool = True):
        if text != None: self.text = str(text)
        if prefix != None: self.prefix = str(prefix)
        if suffix != None: self.suffix = str(suffix)

        if withDisplay: self.item.display()
        # else: self.item.load()

    def renderText(self):
        # Generate surface for text
        text_surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        # Get text with prefix and suffix
        text = self.getText()
        
        # Set \n as a new line when display
        line_text = text.split('\n')

        # Warp the text
        if self.format.warpText == None: warpped_text = line_text
        
        else:
            warpped_text = []
            for line in line_text:
                warpped_text += textwrap.wrap(line, width=self.format.warpText)
        
        # Print text to surface
        h = 0
        for line in warpped_text:
            # Size of text line
            text_w, text_h = self.format.font.size(line)

            # Render the text line and store to text surface
            rendered_text = self.format.font.render(line, True, self.format.colour)

            # Render line based on alignment
            if self.format.align == 'left': text_surface.blit(rendered_text, (0, h))
            elif self.format.align == 'right': text_surface.blit(rendered_text, (self.frame.w - text_w, h))
            elif self.format.align == 'center': text_surface.blit(rendered_text, (int((self.frame.w - text_w)/2), h))

            self.textHeight = h
            # Set hight of next line
            h += text_h * self.format.lineSpacing

        self.textHeight += text_h
            
        return text_surface

    def unload(self):
        self.loaded = False

    def load(self):
        # Get the text
        text_surface = self.renderText()
        # Get surface
        Surface = self.item.surface.Surface

        # Output to surface with postion
        if self.format.pos == 'top': Surface.blit(text_surface, self.frame.coord())
        elif self.format.pos == 'bottom': Surface.blit(text_surface, (self.frame.x, self.frame.y + (self.frame.h - self.textHeight)))
        elif self.format.pos == 'center': Surface.blit(text_surface, (self.frame.x, self.frame.y + int((self.frame.h - self.textHeight)/2)))
        else: logger.error('Unknown text postion type: "{}"'.format(self.format.pos))

        self.loaded = True

    def display(self):
        self.item.display(datas=[self.name])
