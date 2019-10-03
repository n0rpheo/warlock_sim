import random
import utils


class Warlock:
    def __init__(self,
                 base_time,
                 talents,
                 raid_buffs,
                 item_stats):

        self.talents = talents
        self.raid_buffs = raid_buffs
        self.item_stats = item_stats

        base_spell_crit = 3.51
        base_int = 110
        crit_per_int = 60.6

        bonus_int = (base_int
                     + self.item_stats["intelligence"]
                     + (10 if self.raid_buffs["GotW"] else 0)
                     + (31 if self.raid_buffs["AI"] else 0)) * (1.1 if self.raid_buffs["BoK"] else 1) - base_int

        self.spell_crit = (base_spell_crit + bonus_int/crit_per_int + self.item_stats["spell_crit"]) / 100
        self.spell_hit = (83 + min(16, self.item_stats["spell_hit"])) / 100
        self.spell_damage = self.item_stats["spell_damage"]
        self.intelligence = bonus_int

        self.interval = base_time

        self.action_queue = list()
        self.max_mana = 2743 + (bonus_int)*15
        self.mana = self.max_mana

        print(f"Total Spell-Hit: {self.spell_hit}")
        print(f"Total Spell-Crit: {self.spell_crit}")
        print(f"Total Spell-Damage: {self.spell_damage}")
        print(f"Total Mana: {self.mana}")

    def update(self, time, target):

        self.cast_prio(time, target)
        self.perform_action(time, target)

    def cast_prio(self, time, target):
        if len(self.action_queue) == 0:

            if not target.has_debuff("CoS"):
                self.cast_cos(target, time)
            else:
                self.cast_shadowbolt(time)

    def perform_action(self, time, target):
        if self.action_queue[0][1] <= time:
            action = self.action_queue.pop(0)[0]

            if action is "GCD":
                pass
            elif action is "SB":
                damgage, is_crit = self.fire_shadowbolt()
                target.take_damage(time, damgage, "shadow")

                if is_crit:
                    target.apply_debuff(current_time=time, debuff_name="isb", debuff_time=12, charges=4)

    def cast_cos(self, target, time):
        if self.mana >= 200:
            target.apply_debuff(time, "CoS", 300, None)
            self.action_queue.append(["GCD", time + 1.5 / self.interval])
            self.mana -= 200
        else:
            self.cast_lifetap(time)

    def cast_shadowbolt(self, time):
        sb_mana_cost = 370*(1-0.01*self.talents["Cataclysm"])
        if self.mana >= sb_mana_cost:
            self.action_queue.append(["SB", 2.5 / self.interval + time])
            self.mana -= sb_mana_cost
        else:
            self.cast_lifetap(time)

    def cast_lifetap(self, time):
        gained_mana = (424 + 0.8*self.spell_damage)*(1 + 0.1*self.talents["ImprovedLifeTap"])
        self.mana += gained_mana
        self.action_queue.append(["GCD", time + 1.5 / self.interval])

    def fire_shadowbolt(self):
        coeff = 1 + 0.15 * self.talents["DemonicSacrifice"] + 0.02 * self.talents["ShadowMastery"]
        base_damage = (random.randint(455, 508) + 0.8571 * self.spell_damage) * coeff

        if not utils.roll_random(self.spell_hit):
            return 0, False

        if utils.roll_random(self.spell_crit + 0.01 * self.talents["Devastation"]):
            return base_damage*(1.5 + self.talents["Ruin"]), True

        return base_damage, False

    def reset(self):
        self.action_queue = list()
        self.mana = self.max_mana
