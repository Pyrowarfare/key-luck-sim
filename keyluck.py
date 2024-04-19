import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns

dungeons = ['Atal', 'BRH', 'WCM', 'Fall', 'DHT', 'EB', 'TOTT']
class Key():
    def __init__(self, level, dungeon):
        self.level = level
        self.dungeon = dungeon

    def upgrade_key(self):
        self.level += 1
        current_dungeon = self.dungeon
        self.dungeon = random.choice([d for d in dungeons if d != current_dungeon])

    def roll_key(self):
        current_dungeon = self.dungeon
        self.dungeon = random.choice([d for d in dungeons if d != current_dungeon])

    def drop_key(self):
        self.level -= 1


def rotate_through(num_dungeons_needed, current_keys):
    # Only +33 BRH or AD is possible to complete
    viable = any(key.level <= 33 and (key.dungeon == "Atal" or key.dungeon == "BRH") for key in current_keys)
    while viable:
        for key in current_keys:
            if key.level == 33 and (key.dungeon == "BRH" or key.dungeon == "Atal"):
                key.upgrade_key()
                num_dungeons_needed += 1

                if key.level == 34 and (key.dungeon == "Atal" or key.dungeon == "BRH"):
                    return num_dungeons_needed

                # If you get a +34 that is NOT AD or BRH, you should roll the other 33s that are not BRH or AD
                # and drop the useless +34
                else:
                    key.drop_key()
                    for other_key in current_keys:
                        if other_key != key or (key.dungeon == "Atal" or key.dungeon == "BRH"):
                            other_key.roll_key()
        viable = any(key.level == 33 and (key.dungeon == "Atal" or key.dungeon == "BRH") for key in current_keys)
    # If we have no more +33 Atal or BRH, we need to reroll
    else:
        return out_of_33s(num_dungeons_needed, current_keys)


def out_of_33s(num_dungeons_needed, current_keys):
    # We keep dropping and doing the key until we get a doable +33 BRH or Atal
    # Prioritising the most doable dungeon first (some are much harder than others)
    need_more = not any(key.level == 33 and (key.dungeon == "Atal" or key.dungeon == "BRH") for key in current_keys)
    while need_more:
        for key in current_keys:
            if key.level == 33 and key.dungeon == "WCM" or "Fall":
                while key.dungeon not in ["BRH", "Atal"]:
                    key.drop_key()
                    key.upgrade_key()
                    num_dungeons_needed += 1
            elif key.dungeon == "DHT":
                while key.level > 32:
                    key.drop_key()
                while key.dungeon not in ["BRH", "Atal", "WCM", "Fall"]:
                    key.drop_key()
                    key.upgrade_key()
                    num_dungeons_needed += 1
            elif key.dungeon == "EB":
                while key.level > 31:
                    key.drop_key()
                while key.dungeon not in ["BRH", "Atal", "WCM", "Fall", "DHT"]:
                    key.drop_key()
                    key.upgrade_key()
                    num_dungeons_needed += 1
            elif key.dungeon == "TOTT":
                while key.level > 30:
                    key.drop_key()
                while key.dungeon not in ["BRH", "Atal", "WCM", "Fall", "DHT", "EB"]:
                    key.drop_key()
                    key.upgrade_key()
                    num_dungeons_needed += 1

        need_more = not any(key.level == 33 and (key.dungeon == "Atal" or key.dungeon == "BRH") for key in current_keys)
    return rotate_through(num_dungeons_needed, current_keys)


def simulate_dungeon_attempts(num_keys):
    current_keys = [Key(32, "Atal") for _ in range(num_keys)]

    # We start the week with +32 Atals, and we always run them all first for max chances
    for key in current_keys:
        key.upgrade_key()
    num_dungeons_needed = num_keys
    findings = rotate_through(num_dungeons_needed, current_keys)
    return findings


def main(num_simulations):
    num_keys_list = [5, 4, 3, 2, 1]

    for num_keys in num_keys_list:
        dungeon_attempts = [simulate_dungeon_attempts(num_keys) for _ in range(num_simulations)]

        average_attempts = np.mean(dungeon_attempts)
        best_attempt = np.percentile(dungeon_attempts, 1)
        lucky_attempts = np.percentile(dungeon_attempts, 25)
        unlucky_attempts = np.percentile(dungeon_attempts, 75)
        worst_attempt = np.percentile(dungeon_attempts, 100)

        print("Average number of dungeons needed:", average_attempts)
        print("Lucky number of dungeons needed:", lucky_attempts)
        print("Unlucky number of dungeons needed:", unlucky_attempts)
        print("Best run of dungeons needed:", best_attempt)
        print("Worst run of dungeons needed:", worst_attempt)

        # Sort the dungeon attempts in ascending order
        dungeon_attempts_sorted = np.sort(dungeon_attempts)

        y_values = np.arange(1, len(dungeon_attempts_sorted) + 1) / len(dungeon_attempts_sorted)
        plt.plot(dungeon_attempts_sorted, y_values, label=f"{num_keys} keys")

    # Plot CDF
    # plt.plot(dungeon_attempts_sorted, y_values, marker='.', linestyle='none')
    plt.xlabel('Number of Dungeons Needed')
    plt.ylabel('Cumulative Probability')
    plt.title('The Odds of Getting a Doable +34')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    num_simulations = 1000
    main(num_simulations)
