class cprint:
  
  def __init__(self, text):
    self.text = text
   
  def color(self, color, bg):
    error = 0
    if color == 0:
      color = "\033[0m"
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
      bg = "\033[0m"
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
    if error == 1:
      print(color)
    elif error == 2:
      print(bg)
    elif error == 3:
      print(color + bg)
    else:
      print(color + bg + self.text + "\033[0m")
   
  
