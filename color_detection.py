import csv
import pandas as pd
import cv2

# img = 'image01.jpg'
img = 'color3.jpg'
clickFlag = False
red_val = 0
green_val = 0
blue_val = 0
xPosition = 0
yPosition = 0

# color matching
# http://www.colortools.net/color_matcher.html

colorsDF = pd.read_csv('colors.csv')
colorsDF.drop(colorsDF.iloc[:,5:8], inplace=True, axis=1)
colorsDF.rename(columns={'Hex (24 bit)':'Hex', 'Red (8 bit)':'Red', 'Green (8 bit)':'Green', 'Blue (8 bit)':'Blue'}, inplace=True)
image = cv2.imread(img)

def getColorOutput(red,green,blue):
    minVal = 10000
    originalHex = '#%02x%02x%02x' % (red, green, blue)
    for i in range(len(colorsDF)):
        rgbValue = abs(red- int(colorsDF.loc[i,"Red"])) + abs(green- int(colorsDF.loc[i,"Green"]))+ abs(blue- int(colorsDF.loc[i,"Blue"]))
        if(rgbValue <= minVal):
            minVal = rgbValue
            colorName = colorsDF.loc[i,"Name"]
            colorHexCode = colorsDF.loc[i,"Hex"]
            csv_rgb = str(colorsDF.loc[i,"Red"])+','+str(colorsDF.loc[i,"Green"])+','+str(colorsDF.loc[i,"Blue"])
    return 'Input (RGB):'+str(red)+','+str(green)+','+str(blue)+' '+originalHex+' | '+colorName+' : '+colorHexCode+' : '+' ('+csv_rgb+')'

def click_callback(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global blue_val, green_val, red_val, xPosition, yPosition, clickFlag
        clickFlag = True
        xPosition = x
        yPosition = y
        blue_val, green_val, red_val = image[yPosition, xPosition]
        blue_val = int(blue_val)
        green_val = int(green_val)
        red_val = int(red_val)

if __name__ == '__main__':
    cv2.namedWindow('Color Name')
    cv2.setMouseCallback('Color Name', click_callback)
    
    while (True):        
        if (clickFlag):            
            cv2.rectangle(image, (20, 20), (1050, 60), (blue_val, green_val, red_val), -1)
            colorName = getColorOutput(red_val, green_val, blue_val)
            cv2.putText(image, colorName, (50, 50), 2, 0.75, (255, 255, 255), 1, cv2.FONT_ITALIC)
            minVal = abs(red_val + green_val + blue_val)
            if (minVal >= 600):
                cv2.putText(image, colorName, (50, 50), 2, 0.75, (0, 0, 0), 1, cv2.FONT_ITALIC)
            clickFlag = False
        cv2.imshow("Color Name", image)
        # 'esc' key will close the window
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()

