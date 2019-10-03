from bosses.targetdummy import TargetDummy
from classes.warlock import Warlock

####################
####################
####################

warlock_talents = {"ImprovedLifeTap": 2,        # Max 2
                   "Nightfall": 0,              # Max 2
                   "ShadowMastery": 0,          # Max 5
                   "DemonicSacrifice": 1,       # Max 1
                   "ImprovedShadowBolt": 5,     # Max 5
                   "Cataclysm": 2,              # Max 5
                   "Bane": 5,                   # Max 5
                   "Devastation": 5,            # Max 5
                   "Ruin": 1                    # Max 1
                   }

raid_buffs = {"BoK": True,  # Blessing of Kings
              "BoW": True,  # Blessing of Wisdom | not implemented yet
              "GotW": True, # Gift of the Wild
              "AI": True}   # Arcane Intellect

item_stats = {"intelligence": 113,  # Bonus Int from items, enchants, ...
              "spell_crit": 3.0,    # Bonus crit directly from items (no base crit, talents, int-crit,..)
              "spell_hit": 0.0,     # Bonus spell-hit
              "spell_damage": 247}  # Bonus spell damgage (include shadow spell damage)

simtime = 300          # combat time in seconds
num_passes = 1000

####################
####################
####################

iteration_time = 0.01
player = Warlock(base_time=iteration_time,
                 talents=warlock_talents,
                 raid_buffs=raid_buffs,
                 item_stats=item_stats)

targets = [TargetDummy(base_time=iteration_time) for i in range(num_passes)]

print("Start Simulation")
for n_pass in range(num_passes):
    print(f"Pass {n_pass}")
    for i in range(int(simtime/iteration_time)):
        player.update(i, targets[n_pass])
        targets[n_pass].update(i)
    player.reset()

avg_damage = sum([sum([entry["damage"] for entry in target.damage_taken_history]) for target in targets]) / len(targets)
print(f"Avg-Damage: {avg_damage}")
print(f"AvgDPS: {avg_damage / simtime}")