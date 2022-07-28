import re
import inquirer


def clear():
  print("\033c")


def removeZero(num):
  newNum = ''
  num = num.split('.')
  if len(num) >= 1:
    while num[0].startswith('0'):
      num[0] = num[0][1:]
    if num[0]:
      newNum = newNum+num[0]
  if len(num) == 2:
    while num[1].endswith('0'):
      num[1] = num[1][:len(num[1])-1]
    if num[1]:
      newNum = newNum+'.'+num[1]
  if not newNum:
    newNum = '0'
  return newNum


def typeBasedValidate(TYPE, num):
  if TYPE == 'decimal' and re.sub("[0-9.]+", "", num) == "":
    return True
  if (TYPE == 'hex' or TYPE == 'hexadecimal') and re.sub("[0-9a-f.]+", "", num) == "":
    return True
  if TYPE == 'binary' and re.sub("[0-1.]+", "", num) == "":
    return True
  if TYPE == 'octal' and re.sub("[0-7.]+", "", num) == "":
    return True
  return False


def type1(num, inpBase):
  # converts binary, hex, octal -> decimal
  result = 0
  num = num.split('.')
  if len(num) >= 1:
    length = len(num[0])
    for x in reversed(range(length)):
      multiplyBy = 0
      try:
        multiplyBy = int(num[0][x])
      except:
        multiplyBy = ord(num[0][x])-87
      result = result+pow(inpBase, length-x-1)*multiplyBy  # no need to round here
  if len(num) == 2:
    length = len(num[1])
    for x in range(length):
      multiplyBy = 0
      try:
        multiplyBy = int(num[1][x])
      except:
        multiplyBy = ord(num[1][x])-87
      result = result+pow(inpBase, -x-1)*multiplyBy  # no need to round here
  return str(result)


def type2(num, outBase):
  # converts decimal -> octal, binary, hex
  num = num.split('.')
  result = ''
  if len(num) >= 1 and num[0]:
    intDone = False
    num[0] = int(num[0])
    while intDone != True:
      intRes = int(round(num[0]/outBase, 6))
      carryRes = num[0]-intRes*outBase
      num[0] = intRes
      if carryRes >= 10:
        result = chr(87+carryRes) + result
      else:
        result = str(carryRes)+result
      if intRes == 0:
        intDone = True
  if len(num) == 2 and num[1]:
    deciDone = False
    result = result+'.'
    num[1] = float('.'+num[1])
    times = 0
    while deciDone != True:
      Res = num[1]*outBase
      intRes = int(Res)
      if intRes >= 10:
        result = result+chr(87+intRes)
      else:
        result = result+str(intRes)
      times = times+1
      num[1] = Res-intRes
      if num[1] == 0 or times == 16:
        deciDone = True
  return result


def type3(num, outBit):
  # converts octal, hex -> binary
  deciPos = num.find('.')
  num = num.replace('.', '')
  result = ''
  while num != '':
    res = ''
    char = num[0]
    try:
      char = int(char)
    except:
      char = ord(char)-87
    for x in reversed(range(outBit)):
      y = pow(2, x)
      if char >= y:
        res = res+'1'
        char = char-y
      else:
        res = res+'0'
    result = result+res
    num = num[1:]
  if deciPos >= 0:
    deciPos = deciPos*outBit
    result = result[:deciPos] + '.' + result[deciPos:]
  return result


def type4(num, inpBit):
  # converts binary -> octal, hex
  num = num.split('.')
  result = ''
  if len(num) >= 1 and num[0]:
    done = False
    while done == False:
      length = len(num[0])
      if (length % inpBit) == 0:
        done = True
      else:
        num[0] = '0'+num[0]
    while num[0] != '':
      res = 0
      for x in reversed(range(inpBit)):
        intN = int(num[0][0])
        num[0] = num[0][1:]
        if intN == 1:
          res = res + pow(2, x)
      if res >= 10:
        result = result + chr(res-10+97)
      else:
        result = result+str(res)
  if len(num) == 2 and num[1]:
    done = False
    result = result+'.'
    while done == False:
      length = len(num[1])
      if (length % inpBit) == 0:
        done = True
      else:
        num[1] = num[1]+'0'
    while num[1] != '':
      res = 0
      for x in reversed(range(inpBit)):
        intN = int(num[1][0])
        num[1] = num[1][1:]
        if intN == 1:
          res = res + pow(2, x)
      if res >= 10:
        result = result + chr(res-10+97)
      else:
        result = result+str(res)

  return result


def fromDecimal(to, num):
  if to == 'binary':
    return removeZero(type2(num, 2))
  if to == 'octal':
    return removeZero(type2(num, 8))
  if to == 'hex':
    return removeZero(type2(num, 16)).upper()


def fromHex(to, num):
  if to == 'decimal':
    return removeZero(type1(num, 16))
  if to == 'binary':
    return removeZero(type3(num, 4))
  if to == 'octal':
    binary = type3(num, 4)
    return removeZero(type4(binary, 3))


def fromOctal(to, num):
  if to == 'decimal':
    return removeZero(type1(num, 8))
  if to == 'binary':
    return removeZero(type3(num, 3))
  if to == 'hex':
    binary = type3(num, 3)
    return removeZero(type4(binary, 4)).upper()


def fromBinary(to, num):
  if to == 'decimal':
    return removeZero(type1(num, 2))
  if to == 'octal':
    return removeZero(type4(num, 3))
  if to == 'hex':
    return removeZero(type4(num, 4)).upper()


def getNum():
  num = inquirer.prompt([inquirer.Text('num', 'Input the number')])
  num['num'] = (num['num']).lower()
  if num['num'] == '':
    print('No number provided.')
    return getNum()
  return removeZero(num['num'])


def getFrom(num):
  inp = inquirer.prompt([inquirer.List('inp', 'Provided number type', ['Binary', 'Decimal', 'Octal', 'Hex', 'Go Back'])])
  if inp['inp'] == 'Go Back':
    return inp['inp']
  inp['inp'] = (inp['inp']).lower()
  if not typeBasedValidate(inp['inp'], num):
    print(num+' isn\'t a ' + inp['inp']+' number.')
    return getFrom(num)
  return inp['inp']


def getTo():
  inp = inquirer.prompt([inquirer.List('inp', 'Convet into', ['Binary', 'Decimal', 'Octal', 'Hex', 'Go Back'])])
  if inp['inp'] == 'Go Back':
    return inp['inp']
  inp['inp'] = (inp['inp']).lower()
  return inp['inp']


def again():
  inp = inquirer.prompt([inquirer.List('inp', 'Convert another number?', ['Yes', 'No'])])
  if inp['inp'] == 'Yes':
    clear()
    return main()


def getInput(num, frm, to):
  if not num:
    num = getNum()
  if not frm:
    got = getFrom(num)
    if got == 'Go Back':
      return getInput(None, None, None)
    else:
      frm = got

  if not to:
    got = getTo()
    if got == 'Go Back':
      return getInput(num, None, None)
    else:
      to = got
  return [num, frm, to]


def main():
  num, frm, to = getInput(None, None, None)

  if frm == 'hexadecimal':
    frm = 'hex'
  if to == 'hexadecimal':
    to = 'hex'
  if frm == to:
    print(num.upper())
  elif frm == 'binary':
    print(fromBinary(to, num))
  elif frm == 'octal':
    print(fromOctal(to, num))
  elif frm == 'decimal':
    print(fromDecimal(to, num))
  elif frm == 'hex':
    print(fromHex(to, num))
  else:
    print('Some errors have occured.')
  again()


main()
