#!/usr/bin/env python
# coding: utf-8

# In[11]:


# Import Libraries
import random
import time


# In[12]:


# Character class: This class is for both the player and the enemy
class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0


# Player Class: Inherits from the Character class
class Player(Character):
    def __init__(self, name, char_class):
        self.name = name
        # Different stats for depending on the class that is chosen
        if char_class == "Warrior":
            super().__init__(name, hp=100, attack=15)
        elif char_class == "Mage":
            super().__init__(name, hp=60, attack=25)
        self.char_class = char_class

        self.wins = 0
    
    def heal(self):
        self.hp = self.max_hp
        print(f"{self.name} healed to full HP!")

# Enemy Class: Also inherits from the Character class
class Enemy(Character):
    def __init__(self, name, hp, max_hp, attack):
        super().__init__(name, hp, attack)
        self.max_hp = max_hp
        """
        if char_class == "Goblin":
            super().__init__(name, hp=30, attack=8)
        elif char_class == "Skeleton":    
            super().__init__(name, hp=50, attack=12)
        """


# In[13]:


# This increases enemy dificulty based on the current level
def scale_enemy(enemy, level):
    enemy.hp += level * 5
    enemy.max_hp += level * 5
    enemy.attack += level * 2
    return enemy


# In[14]:


# Game Functions
def battle(player, enemy):
    print(f"\n-- A wild {enemy.name} appears! --")
    while player.is_alive() and enemy.is_alive():
        # Player's Turn: Player can either choose to attack or run away
        action = input("Action: [1] Attack [2] Run: ")
        if action == "1":
            damage = random.randint(player.attack - 5, player.attack + 5)
            enemy.take_damage(damage)
            print(f"You hit {enemy.name} for {damage} damage!")
            print(f"Enemy HP: {enemy.hp}/{enemy.max_hp}")
        else:
            print("You ran away!")
            return

        # Enemy's Turn
        if enemy.is_alive():
            e_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            player.take_damage(e_damage)
            print(f"{enemy.name} hits you for {e_damage}!")
            print(f"Your HP: {player.hp}/{player.max_hp}")

    # Determines an outcome after the loop ends
    if player.is_alive():
        print(f"{enemy.name} Defeated!")
        player.wins += 1
        return True
    else:
        print("You Have Been Defeated!")
        print("Game Over!")
        return False

# Returns a list of enemies
def get_enemies_for_level(level):
    if level == 1:
        return [
            Enemy("Goblin", 30, 30, 8),
            Enemy("Skeleton", 50, 50, 12),
            Enemy("Wizard", 90, 90, 20)
        ]
    elif level == 2:
        return [
            Enemy("Slime Monster", 10, 10, 5),
            Enemy("WereWolf", 35, 35, 10),
            Enemy("Orc", 60, 60, 14)
        ]
    elif level == 3:
        return [
            Enemy("Hob Goblin", 20, 20, 5),
            Enemy("Skeleton", 50, 50, 12),
            Enemy("Skeleton", 50, 50, 12)
        ]

# Saves the players results in a text file
def save_results(player):
    with open("game_results.txt", "a") as file:
        file.write(f"{player.name} ({player.char_class}) - Wins: ({player.wins}\n")


# In[15]:


# Main Game Loop
def main():
    # Welcomes the new player to the game
    print("Welcome to The Realm of Enemies")
    name = input("Enter character name: ")
    print("Welcome, " + name)
    # Players select a class to determine their stats
    char_class = input("Choose Class (Warrior/Mage): ")
    player = Player(name, char_class)

    level = 1

    while level <= 3 and player.is_alive():
        print(f"\n=== Level {level} ===")

        # Generates enemies for the current level
        enemies = get_enemies_for_level(level)

        # Each level has 2 battles
        for i in range(2):
            if not player.is_alive():
                break

            # Select and scale a random enemy 
            enemy = random.choice(enemies)
            enemy = scale_enemy(enemy, level)

            print(f"\nEnemy {i+1} of Level {level}")
            result = battle(player, enemy)

            # Heals player after winning
            if result:
                player.heal()
            else:
                break
        level += 1

    # Final Boss
    if player.is_alive():
        print("\n --- Final Boss ---")
        time.sleep(1)
        print("A massive shadow appears...")
        time.sleep(2)

        # Create and scale boss
        boss = Enemy("Dragon", 120, 120, 25)
        boss = scale_enemy(boss, level + 2)

        result = battle(player, boss)

        # Display results for the boss battle
        if result:
            print("\n You have defeated the Dragon!")
        else:
            print("\n The Dragon was too powerful.")

    # Game Summary: Displays final results
    print("\n --- Game Summary ---")
    print(f"Player: {player.name}")
    print(f"Class: {player.char_class}")
    print(f"Enemies Defeated: {player.wins}")

    save_results(player)
    print("Results saved to file")

    
    for enemy in enemies:
        if player.is_alive():
            battle(player, enemy)
        else:
            print("Game Over!")
            break

if __name__ == "__main__":
    main()


# In[ ]:




