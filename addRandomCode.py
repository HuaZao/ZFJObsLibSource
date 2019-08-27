#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import random, uuid, zfjTools
from singletonModel import ZFJPersoninfo
funHeadList = [
 'void', 'BOOL', 'CGFloat', 'CGRect', 'NSInteger',
 'NSObject', 'NSString', 'NSArray', 'NSDictionary', 'UIImage', 'NSNumber', 'NSURL', 'NSIndexPath',
 'UIView', 'UIControl', 'UIButton', 'UIDatePicker', 'UIPageControl', 'UISegmentedControl', 'UITextField', 'UISwitch', 'UISlider',
 'UILabel', 'UIImageView', 'UIViewController', 'UIFont', 'UICollectionView', 'UIColor']
assignList = [
 'BOOL', 'CGFloat', 'CGRect', 'NSInteger']
copyList = [
 'NSString', 'NSArray', 'NSDictionary', 'UIImage', 'NSNumber', 'NSURL', 'NSIndexPath']
_choseMap = {}

def getRandomStr(satrtIndex, endIndex):
    numbers = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    final = random.choice(numbers)
    index = random.randint(satrtIndex, endIndex)
    for i in range(index):
        final += random.choice(numbers)

    return final


def getMyUIID():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    suid = ''.join(random.sample(suid, 23))
    return suid.upper()


def getRandomRubFunName(className):
    if className in ('NSString', 'NSArray', 'NSDictionary'):
        return 'get' + zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize() + className[2:]
    if className in ('UILabel', 'UIView'):
        return 'create' + zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize() + className[2:]
    if className in ('void', ):
        return zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize() + 'Function'


def getMissObjName(old_objName):
    title_str = zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize()
    if old_objName.endswith('View') or old_objName.endswith('view'):
        return title_str + 'View'
    elif old_objName.endswith('Controller') or old_objName.endswith('controller') or old_objName.endswith('Controll') or old_objName.endswith('controll') or old_objName.endswith('Control') or old_objName.endswith('control'):
        return title_str + 'Controller'
    elif old_objName.endswith('Cell') or old_objName.endswith('cell'):
        return title_str + 'Cell'
    elif old_objName.endswith('Model') or old_objName.endswith('model'):
        return title_str + 'Model'
    elif 'Tool' in old_objName or 'tool' in old_objName:
        return title_str + 'Tools'
    elif old_objName.endswith('Label') or old_objName.endswith('label'):
        return title_str + 'Label'
    elif old_objName.endswith('Button') or old_objName.endswith('button') or old_objName.endswith('Btn') or old_objName.endswith('btn'):
        return title_str + 'Button'
    elif old_objName.endswith('Manager') or old_objName.endswith('manager'):
        return title_str + 'Manager'
    elif old_objName.endswith('Handler') or old_objName.endswith('handler'):
        return title_str + 'Handler'
    elif old_objName.endswith('Operation') or old_objName.endswith('operation'):
        return title_str + 'Operation'
    else:
        return title_str + 'Obj'


def getRandomNum(satrtIndex, endIndex):
    return random.randint(satrtIndex, endIndex)


def getUILabel():
    line = '- (UILabel *)' + getRandomRubFunName('UILabel') + '{\n'
    labelName = zfjTools.getWordFromLexicon() + 'Label'
    line += '    UILabel *' + labelName + ' = [[UILabel alloc] init];' + '\n'
    line += '    ' + labelName + '.frame = CGRectMake(' + str(getRandomNum(0, 300)) + ', ' + str(getRandomNum(0, 300)) + ', ' + str(getRandomNum(0, 300)) + ', ' + str(getRandomNum(0, 300)) + ');' + '\n'
    line += '    ' + labelName + '.backgroundColor = [UIColor groupTableViewBackgroundColor];' + '\n'
    line += '    ' + labelName + '.text = @"' + getRandomStr(15, 40) + '";' + '\n'
    line += '    ' + labelName + '.font = [UIFont systemFontOfSize:16];' + '\n'
    line += '    ' + labelName + '.textColor = [UIColor blackColor];' + '\n'
    line += '    ' + labelName + '.numberOfLines = ' + str(getRandomNum(0, 12)) + ';' + '\n'
    line += '    return ' + labelName + ';' + '\n}' + '\n\n'
    return line


def getRubbishFun(rubPrefix=''):
    global _choseMap
    global funHeadList
    createObjList = []
    index = random.randint(0, len(funHeadList) - 1)
    funHeadName = funHeadList[index]
    funHeadType = funHeadName if index <= 4 else funHeadName + ' *'
    funCode = '- (' + funHeadType + ')' + rubPrefix + zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize()
    parameterList = []
    for x in range(0, random.randint(1, 4)):
        indexPra = random.randint(1, len(funHeadList) - 1)
        praObjName = funHeadList[indexPra]
        praType = praObjName if indexPra <= 4 else praObjName + ' *'
        if praObjName not in createObjList:
            createObjList.append(praObjName)
        praName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
        if x == 0:
            funCode += ':(' + praType + ')' + praName + ' '
        else:
            funCode += praName + ':(' + praType + ')' + praName + ' '
        praType = praType.strip()
        parameterList.append(praType + '==' + praName)

    funCode = funCode.strip()
    funCode += '{\n\n'
    isAddNSDate = False
    for item in parameterList:
        notesStr = '//' + zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
        praType = item.split('==')[-1]
        if item.startswith('UI'):
            if 'UIFont' not in item:
                pass
        if 'UIColor' not in item:
            if 'UIImage' not in item:
                if 'UIViewController' not in item:
                    funCode += '    if(' + praType + ' != nil){' + '\n'
                    funCode += '        ' + praType + '.backgroundColor = [UIColor colorWithRed:arc4random_uniform(256)/255.0 green:arc4random_uniform(256)/255.0 blue:arc4random_uniform(256)/255.0 alpha:1];\n'
                    funCode += '    }\n'
                if item.startswith('UI'):
                    if 'UIViewController' in item:
                        funCode += '    ' + praType + '.title = @"' + zfjTools.getWordFromLexicon().capitalize() + '";\n'
                    if item.startswith('NS'):
                        if 'NSInteger' not in item:
                            if isAddNSDate == False:
                                isAddNSDate = True
                                zfjDate = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
                                aTimeInteger = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
                                funCode += '    NSDate *' + zfjDate + ' = [NSDate dateWithTimeIntervalSinceNow:0];\n'
                                funCode += '    NSInteger ' + aTimeInteger + ' = [' + zfjDate + ' timeIntervalSince1970];\n\n'
                            funCode += '    if (' + praType + '.hash != ' + aTimeInteger + '){\n'
                            funCode += '        ' + notesStr + '\n'
                            if 'NSString' in item:
                                funCode += '        ' + praType + ' = [NSString stringWithFormat:@"%ld",' + aTimeInteger + '];\n'
                            else:
                                funCode += '        ' + praType + ' = nil;\n'
                            funCode += '    }else{\n'
                            if 'NSDictionary' in item:
                                funCode += '        [' + praType + ' setValue:@"' + zfjTools.getWordFromLexicon() + '" forKey:@"' + zfjTools.getWordFromLexicon() + '"];\n'
                            funCode += '        NSLog(@"' + praType + '.hash != %ld",' + praType + '.hash);\n'
                            funCode += '    }\n'
                        if item.startswith('NS'):
                            if 'NSInteger' in item:
                                funCode += '    ' + praType + ' = ' + str(random.randint(30, 500)) + ';\n'
            funCode += '\n'

    funCode += '    //ZFJ_OTHER\n'
    if len(_choseMap) >= 1:
        index = random.randint(0, len(_choseMap.keys()) - 1)
        objName = list(_choseMap.keys())[index]
        newProName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + objName[:3].capitalize()
        funCode += '    ' + objName + ' *' + newProName + ' = [[' + objName + ' alloc] init];' + '\n'
        funCode += '    [' + newProName + ' ' + _choseMap[objName] + '];' + '\n'
    funCode += '\n'
    returnName = zfjTools.getWordFromLexicon() + funHeadName[2:]
    if 'void' not in funHeadType:
        pass
    if '*' in funHeadType:
        if 'UICollectionView' != funHeadName:
            funCode += '    ' + funHeadName + ' *' + returnName + ' = [[' + funHeadName + ' ' + 'alloc] init];' + '\n'
            funCode += '    return ' + returnName + ';\n'
        if 'void' not in funHeadType:
            pass
    if '*' in funHeadType:
        if 'UICollectionView' == funHeadName:
            flowLayoutName = zfjTools.getWordFromLexicon()
            funCode += '    UICollectionViewFlowLayout *' + flowLayoutName + ' = [[UICollectionViewFlowLayout alloc] init];\n'
            funCode += '    ' + flowLayoutName + '.itemSize = CGSizeMake(' + str(random.randint(0, 300)) + ', ' + str(random.randint(0, 300)) + ');\n'
            funCode += '    ' + flowLayoutName + '.minimumInteritemSpacing = ' + str(random.randint(1, 30)) + ';\n'
            funCode += '    ' + flowLayoutName + '.minimumLineSpacing = ' + str(random.randint(1, 30)) + ';\n'
            funCode += '    ' + flowLayoutName + '.scrollDirection = UICollectionViewScrollDirectionVertical;\n\n'
            funCode += '    ' + funHeadName + ' *' + returnName + ' = [[' + funHeadName + ' ' + 'alloc] initWithFrame:CGRectMake(' + str(random.randint(0, 300)) + ', ' + str(random.randint(0, 300)) + ', ' + str(random.randint(0, 300)) + ', ' + str(random.randint(0, 300)) + ') collectionViewLayout:' + flowLayoutName + '];' + '\n'
            funCode += '    return ' + returnName + ';\n'
        if 'BOOL' in funHeadType:
            parameterListPart = parameterList[random.randint(0, len(parameterList) - 1)]
            if '*' not in parameterListPart:
                funCode += '    ' + funHeadName + ' ' + returnName + ' = arc4random_uniform(100)%2 == 0 ? YES : NO;' + '\n'
                funCode += '    return ' + returnName + ';\n'
            else:
                par_name = parameterListPart.split('==')[-1]
                funCode += '    if(' + par_name + ' == nil){\n'
                funCode += '        return NO;\n'
                funCode += '    }else{\n'
                funCode += '        return YES;\n'
                funCode += '    }\n'
        else:
            if 'CGFloat' in funHeadType or 'NSInteger' in funHeadType:
                funCode += '    ' + funHeadName + ' ' + returnName + ' = arc4random_uniform(100);' + '\n'
                funCode += '    return ' + returnName + ';\n'
            else:
                if 'CGRect' in funHeadType:
                    x = random.randint(0, 200)
                    y = random.randint(0, 200)
                    width = random.randint(0, 200)
                    height = random.randint(0, 200)
                    funCode += '    ' + funHeadName + ' ' + returnName + ' = CGRectMake(' + str(x) + ', ' + str(y) + ', ' + str(width) + ', ' + str(height) + ');\n'
                    funCode += '    return ' + returnName + ';\n'
            funCode += '}\n\n'
    return (funCode, createObjList)


def getImportCode():
    global _choseMap
    personinfo = ZFJPersoninfo()
    _createFileMap = personinfo.rubbishFileMap
    if len(_createFileMap.keys()) > 3:
        random.seed(len(_createFileMap.keys()))
        keyList = random.sample(list(_createFileMap.keys()), 3)
        for key in keyList:
            _choseMap[key] = _createFileMap[key]

    else:
        _choseMap = _createFileMap
    importCode = ''
    for objClassName in _choseMap:
        importCode += '#import "' + objClassName + '.h"\n'

    return importCode


def addRandomClass(amount=1, rubPrefix=''):
    global assignList
    global copyList
    funNameMap = {}
    rubFunCode = ''
    interfaceRubProCode = ''
    rubbishProMap = {}
    createObjList = []
    importCode = getImportCode()
    for x in range(amount):
        rubbishTuple = getRubbishFun(rubPrefix)
        funName = rubbishTuple[0]
        createObjList.extend(rubbishTuple[1])
        funName_0 = funName[:funName.find('{')] + ';'
        funName_1 = funName[funName.find(')') + 1:funName.find('{')]
        rubFunCode += funName
        funNameMap[funName_0] = funName_1

    interfaceRubProCode += '\n//Start\n'
    for objName in createObjList:
        rubbishProName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
        propertyTypeWord = '  copy'
        asterisk = ' *'
        if objName in assignList:
            propertyTypeWord = 'assign'
            asterisk = ' '
        else:
            if objName in copyList:
                propertyTypeWord = '  copy'
                asterisk = ' *'
            else:
                if objName not in assignList:
                    if objName not in copyList:
                        propertyTypeWord = 'strong'
                        asterisk = ' *'
        interfaceRubProCode += '\n@property(nonatomic,' + propertyTypeWord + ') ' + objName + asterisk + rubbishProName + ';\n'
        rubbishProMap[objName] = rubbishProName

    interfaceRubProCode += '\n//End\n'
    interfaceRubProCode += '\n\n//Start\n\n'
    callProCode_FFile = interfaceRubProCode
    for funKey in funNameMap:
        callProCode_FFile += funKey + '\n'
        callFunName = funNameMap[funKey]
        new_callFunName = ''
        callFunNameList = callFunName.split(':')
        for index in range(0, len(callFunNameList)):
            callFunNameListItem = callFunNameList[index]
            if '(' in callFunNameListItem:
                if ')' in callFunNameListItem:
                    objName = callFunNameListItem.strip().replace('(', '')
                    objName = objName[:objName.find(')')].replace('*', '').strip()
                    rubbishProName = rubbishProMap[objName]
                    new_callFunNameListItem = '_' + rubbishProName
                    if ' ' in callFunNameListItem:
                        secondPra = callFunNameListItem.split(' ')[-1]
                        if '*' not in secondPra:
                            new_callFunNameListItem += ' ' + secondPra
                    callFunNameList[index] = new_callFunNameListItem

        new_callFunName = ':'.join(callFunNameList)
        funNameMap[funKey] = new_callFunName

    masterFunName = rubPrefix + 'master' + zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize()
    rubFunCode += '- (void)' + masterFunName + '{\n'
    for key in funNameMap:
        rubFunCode += '    [self ' + funNameMap[key] + '];' + '\n'

    rubFunCode += '}\n'
    callProCode_FFile += '\n- (void)' + masterFunName + ';\n'
    callProCode_FFile += '\n//End\n\n'
    return (
     callProCode_FFile, rubFunCode, masterFunName, funNameMap, importCode)