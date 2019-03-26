# [ch for ch in input() if type(ch)==str]
# print(str([ch.upper() for ch in input() if ch.isalnum())
class Car():
    def __init__(self,name,loss):
        self.name = name
        self.loss = loss
    def getName(self,name):
        return self.name
    def getPrice(self):
        self.price = self.loss[0]
        return self.price
    def getLoss(self):
        return self.loss[1]*self.loss[2]
    def getPrint(self):
        print("%s:%d,%d" % (self.name,self.loss[0],(self.loss[1])*(self.loss[2])))
Bmw = Car("宝马",[60,9,500])
Bmw.getPrint()
Benz = Car("奔驰",[80,7,600])
Benz.getPrint()
if Bmw.getPrice() < Benz.getPrice():
      print("宝马更便宜")
else:
      print("奔驰更便宜")
