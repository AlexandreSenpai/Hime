###[EXTERNAL MODULES]###
import cv2

class TextFit(object):
    def __init__(self):
        pass

    def __repr__(self):
        return 'Class made to fit a text in a rectangle'

    # this tries to fit a single line of text (no new lines)
    # returns a boolean and the width and height of the line
    def tryToFitTextLine(self, text, width, height, fontType, fontSize):
        textSize, baseLine = cv2.getTextSize(text, fontType, fontSize, 2)
        return textSize[0] <= width and textSize[1] + 4 <= height, textSize[0], textSize[1] + 4
    
    # this do a binary search to partition the text to get the first line that fits
    # return the index of the last word in the first line and the height of the line
    def getFirstLine(self, text, width, height, fontType, fontSize):
        l = 0
        r = len(text) - 1
        ans = -1
        lineWidth = 0
        lineHeight = 0

        while l <= r:
            m = (l + r) // 2
            
            fit, w, h = self.tryToFitTextLine(" ".join(text[:m + 1]), width, height, fontType, fontSize)
            if fit:
                ans = m
                lineHeight = h
                lineWidth = w
                l = m + 1
            else:
                r = m - 1
        
        return ans, lineWidth, lineHeight
    
    # try to fill the whole text with the given font size
    # return a width, height and the splitted text
    def tryToFitText(self, text, width, height, fontType, fontSize):
        text = text.split()
        textWidth = 0
        textHeight = 0
        ans = []

        while len(text) > 0:
            firstLineIdx, firstLineWidth, firstLineHeight = self.getFirstLine(text, width, height, fontType, fontSize)
            if firstLineIdx == -1:
                textWidth = float("inf")
                textHeight = float("inf")
                ans.append(text[0])
                text = text[1:] if len(text) > 1 else []
            else:
                ans.append(" ".join(text[:firstLineIdx + 1]))
                text = text[firstLineIdx + 1:] if firstLineIdx < len(text) else []
                textHeight += firstLineHeight
                textWidth = max(textWidth, firstLineWidth)
            
        return textWidth, textHeight, ans
    
    # try different font sizes to fit the text
    # return the final string (with new lines chars), the font size and the spacing
    def fitText(self, text, width, height, fontType):
        fontSizes = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
        spacings = [16, 16, 26, 26, 36, 36, 47]
        finalText = ""
        bestSize = 0
        bestSpacing = 0
        shiftX = 0
        shiftY = 0
        for spacing, fontSize in zip(spacings, fontSizes):
            textWidth, textHeight, currText = self.tryToFitText(text, width, height, fontType, fontSize)
            if (textWidth <= width and textHeight <= height) or finalText == "":
                finalText = "\n".join(currText)
                bestSize = fontSize
                bestSpacing = spacing
                
                shiftX = int((width - textWidth) // 2) + 2 if textWidth < width else 2
                shiftY = int((height - textHeight) // 2) + 2 if textHeight < height else 2

            else:
                break
        
        return finalText, bestSize, bestSpacing, shiftX, shiftY



