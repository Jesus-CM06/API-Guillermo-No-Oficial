import imutils
import Functions.gammaFunction as gf
import Functions.align_images as align_images
import Functions.orientationFunctions as of

def sizesAndLight(image, template):

    bestValues = []
    values = [550, 650, 750, 800]
    print("Light adjustment...")
    for width in values:
        bestGammaValues = gf.ligthIteration(imutils.resize(image, width=width), template)
        for gamma in bestGammaValues:
            bestValues.append([width, gamma])
    return bestValues

def validateSizes(image, template):

    bestValues = []
    values = [550, 650, 750, 800, 950]
    print("Size adjustment...")
    for width in values:
        aligned = align_images.align_images(imutils.resize(image, width=width), template, debug=True)

        validate = of.faceSearch(aligned)
        if validate > 0:
            bestValues.append(width)
    return bestValues

def validateStrings(names, address, keys, curps, years, birthdays):

    bestStrings=[]
    bestName = validateNames(names)
    bestStrings.append(bestName)
    bestAddress = validateNames(address)
    bestStrings.append(bestAddress)
    bestKey = validateKeys(keys)
    bestStrings.append(bestKey)
    bestCurp = validateKeys(curps)
    bestStrings.append(bestCurp)
    bestYear = validateYears(years)
    bestStrings.append(bestYear)
    bestBirthday = validateBirthday(birthdays)
    bestStrings.append(bestBirthday)

    return bestStrings

def validateNames(names):

    strings3columns = []
    bool3cols = False
    sameString = True

    for name in names:
        divided = name.split(chr(10))
        if len(divided) == 4:
            strings3columns.append(name)
            bool3cols = True

    if bool3cols == True:
        for i in range(len(strings3columns)-1):
            if strings3columns[i] != strings3columns[i+1]:
                sameString = False
        if sameString == True:
            return strings3columns[0]
        else:
            # Return the longest string
            longestString = strings3columns[0]
            for i in range(len(strings3columns)-1):
                if len(strings3columns[i+1]) > len(longestString):
                    longestString = strings3columns[i+1]
            return longestString
    else:
        longestString = names[0]
        for i in range(len(names)-1):
            if len(names[i+1]) > len(longestString):
                longestString = names[i+1]
        return longestString

    return

def validateKeys(keys):

    strings18chars = []
    bool18chars = False
    sameString = True

    for key in keys:
        divided = key.split(chr(10))
        if len(divided[0]) == 18:
            strings18chars.append(key)
            bool18chars = True

    if bool18chars == True:
        for i in range(len(strings18chars)-1):
            if strings18chars[i] != strings18chars[i+1]:
                sameString = False
        if sameString == True:

            return strings18chars[0]
        else:
            longestString = strings18chars[0]
            for i in range(len(strings18chars)-1):
                if len(strings18chars[i+1]) > len(longestString):
                    longestString = strings18chars[i+1]
            return longestString
    else:
        longestString = keys[0]
        for i in range(len(keys)-1):
            if len(keys[i+1]) > len(longestString):
                longestString = keys[i+1]
        return longestString

    return

def validateYears(years):

    strings7chars = []
    bool7chars = False
    sameString = True

    for year in years:
        divided = year.split(chr(10))
        if len(divided[0]) == 7:
            strings7chars.append(year)
            bool7chars = True

    if bool7chars == True:
        for i in range(len(strings7chars)-1):
            if strings7chars[i] != strings7chars[i+1]:
                sameString = False
        if sameString == True:
            return strings7chars[0]
        else:
            # FUTURE: VALIDATE THE FORMAT "#### ##"

            longestString = strings7chars[0]
            for i in range(len(strings7chars)-1):
                if len(strings7chars[i+1]) > len(longestString):
                    longestString = strings7chars[i+1]
            return longestString
    else:
        longestString = years[0]
        for i in range(len(years)-1):
            if len(years[i+1]) > len(longestString):
                longestString = years[i+1]
        return longestString

    return

def validateBirthday(birthdays):

    strings10chars = []
    bool10chars = False
    sameString = True

    for birthday in birthdays:
        divided = birthday.split(chr(10))
        if len(divided[0]) == 10:
            strings10chars.append(birthday)
            bool10chars = True

    if bool10chars == True:
        for i in range(len(strings10chars)-1):
            if strings10chars[i] != strings10chars[i+1]:
                sameString = False
        if sameString == True:
            return strings10chars[0]
        else:
            # FUTURE: VALIDATE THE FORMAT "##/##/####"

            longestString = strings10chars[0]
            for i in range(len(strings10chars)-1):
                if len(strings10chars[i+1]) > len(longestString):
                    longestString = strings10chars[i+1]
            return longestString
    else:
        longestString = birthdays[0]
        for i in range(len(birthdays)-1):
            if len(birthdays[i+1]) > len(longestString):
                longestString = birthdays[i+1]
        return longestString

    return
