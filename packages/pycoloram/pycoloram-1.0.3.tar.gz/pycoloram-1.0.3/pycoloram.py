class cprint:
  
  def __init__(self, text):
    self.text = text
   
  def color(self, color, bg, eff):
    error = 0
    if color == 0:
      color = "" 
    elif color == 1:
      color = "\033[30m"
    elif color == 2:
      color = "\033[31m"
    elif color == 3:
      color = "\033[32m"
    elif color == 4:
      color = "\033[33m"
    elif color == 5:
      color = "\033[34m"
    elif color == 6:
      color = "\033[35m"
    elif color == 7:
      color = "\033[36m"
    elif color == 8:
      color = "\033[37m"
    else:
      error += 1
      color = "\033[31mError: No color found under this number or incorrect number entered\033[0m\n"
     
    if bg == 0:
      bg = ""
    elif bg == 1:
      bg = "\033[40m"
    elif bg == 2:
      bg = "\033[41m"
    elif bg == 3:
      bg = "\033[42m"
    elif bg == 4:
      bg = "\033[43m"
    elif bg == 5:
      bg = "\033[44m"
    elif bg == 6:
      bg = "\033[45m"
    elif bg == 7:
      bg = "\033[46m"
    elif bg == 8:
      bg = "\033[47m"
    else:
      error += 2
      bg = "\033[31mError: No backgraund-color found under this number or incorrect number entered\033[0m\n"

    if eff == 0:
      eff = ""
    elif eff == 1:
      eff = "\033[1m"
    elif eff == 2:
      eff = "\033[2m"
    elif eff == 3:
      eff = "\033[3m"
    elif eff == 4:
      eff = "\033[4m"
    elif eff == 5:
      eff = "\033[5m"
    elif eff == 6:
      eff = "\033[6m"
    elif eff == 7:
      eff = "\033[7m"
    else:
      error += 4
      eff = "\033[31mError: No effect found under this number or incorrect number entered\033[0m\n" 

    if error == 1:
      print(color)
    elif error == 2:
      print(bg)
    elif error == 3:
      print(color + bg)
    elif error == 4:
      print(eff)
    elif error == 5:
      print(eff + color)
    elif error == 6:
      print(eff + bg)
    elif error == 7:
      print(eff + color + bg) 
    else:
      print(eff + color + bg + self.text + "\033[0m")
         
  


#1	Жирный
#2	Блёклый
#3	Курсив
#4	Подчёркнутый
#5	Редкое мигание
#6	Частое мигание
#7	Смена цвета фона с цветом текста