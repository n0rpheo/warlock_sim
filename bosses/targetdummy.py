
class TargetDummy:

    def __init__(self, base_time):
        self.interval = base_time
        self.damage_taken_history = []
        self.active_debuffs = []        # name, time, charges

    def update(self, time):
        self.check_debuffs(time)

    def check_debuffs(self, time):
        self.active_debuffs = [debuff for debuff in self.active_debuffs if debuff["expiration"] > time]

        # remove_debuffs = list()
        # for debuff_id in range(len(self.active_debuffs)):
        #     if self.active_debuffs[debuff_id][1] < time:
        #         remove_debuffs.append(debuff_id)

        # remove_debuffs = sorted(remove_debuffs, reverse=True)

        # for rem in remove_debuffs:
        # self.active_debuffs.pop(rem)

    def take_damage(self, time, damage, type):

        # Test for CoS
        if (type is "shadow" or type is "arcane") and self.has_debuff("CoS"):
            damage = damage * 1.1

        # Test for iSB
        if type is "shadow" and self.has_debuff("isb"):
            damage = damage * 1.2

            debuff_id = self.get_debuff_id("isb")

            if self.active_debuffs[debuff_id]["charges"] == 1:
                self.active_debuffs.pop(debuff_id)
            else:
                self.active_debuffs[debuff_id]["charges"] -= 1

        self.damage_taken_history.append({"time": time, "damage": damage})

    def has_debuff(self, find_debuff):
        for debuff in self.active_debuffs:
            if find_debuff is debuff["name"]:
                return True
        return False

    def apply_debuff(self, current_time, debuff_name, debuff_time, charges=None):
        debuff_time = current_time + debuff_time/self.interval

        debuff = {"name": debuff_name,
                  "expiration": debuff_time,
                  "charges": charges
                  }

        if self.has_debuff(debuff_name):
            debuff_id = self.get_debuff_id(debuff_name)
            self.active_debuffs[debuff_id] = debuff
        else:
            self.active_debuffs.append(debuff)

    def get_debuff_id(self, debuff_name):
        for i in range(len(self.active_debuffs)):
            if debuff_name is self.active_debuffs[i]["name"]:
                return i
        return False
