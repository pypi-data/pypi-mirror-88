class color:
  
  def __init__(self, text):
    self.text = text
  
  def Black(self):
    print("\033[30m{}\033[0m" .format(self.text))
    
  def Red(self):
    print("\033[31m{}\033[0m" .format(self.text))
  
  def Green(self):
    print("\033[32m{}\033[0m" .format(self.text))
    
  def Yellow(self):
    print("\033[33m{}\033[0m" .format(self.text))
    
  def Blue(self):
    print("\033[34m{}\033[0m" .format(self.text))
    
  def Мagenta(self):
    print("\033[35m{}\033[0m" .format(self.text))
  
  def Cyan(self):
    print("\033[36m{}" .format(self.text))
  
  def White(self):
    print("\033[37m{}" .format(self.text))
