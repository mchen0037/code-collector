import random

class Person(object):
    def __init__(self):
        self.got_prize = False
        self.roll = 0
        self.prize_roll = 0
        self.vend()

    def vend(self):
        while not self.got_prize:
            self.roll += 1
            prize = 1
            self.prize_roll = self.roll
            num = random.randint(1,6)
            if(num==prize):
                self.got_prize = True

people = []

for x in range (0,1000):
    person = Person()
    people.append(person.prize_roll)
    
print(people)