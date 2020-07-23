class PartyAnimal:
    x = 0
    name = ""
    def __init__(self,z):
        self.name = z
        print(self.name,"constructed")

    def party(self):
        self.x += 1
        print(self.name,"party count",self.x)

class FootballFan(PartyAnimal): #class footballfan extends partyanimal
    points = 0
    def touchdown(self):
        self.points = self.points + 7
        self.party()
        print(self.name,"points",self.points)

s = PartyAnimal("Sally")
s.party()

j = FootballFan("Jim") #FootballFan has the capability of PartyAnimal and the method touchdown
j.party()
j.touchdown()
