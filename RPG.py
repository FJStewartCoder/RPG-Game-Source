import time as t
from random import randint
from random import choice
import conversions as c
import missions as m
import merchant_missions as mm
import dialogue as d


try:
    open('Savecodes.txt', 'x')
except FileExistsError:
    pass


class Enemy:
    def __init__(self, type: str):
        self.type = type
        match type:
            case 'Zombie':
                self.damage = 2
                self.max_health = 5
            case 'Guard':
                self.damage = 4
                self.max_health = 30
            case 'Wild Boar':
                self.damage = 10
                self.max_health = 50
            case 'Boar Merchant':
                self.damage = 20
                self.max_health = 150
            case 'Bushcraft Warrior':
                self.damage = 5
                self.max_health = 200
            case 'MEGA GUARD':
                self.damage = 15
                self.max_health = 300
            case 'THE ALMIGHTY':
                self.damage = 100
                self.max_health = 2500

        self.health = self.max_health

# default player is 25 hp, 2 dmg. 1 dmg = 5 hp


class Player:
    def __init__(self, type, *, max_health=0, health=0, damage=0):
        self.type = type

        if max_health == 0:
            match type:
                case 'Wizard':
                    self.damage = 4
                    self.max_health = 15
                case 'Knight':
                    self.damage = 1
                    self.max_health = 30
                case 'Elf':
                    self.damage = 5
                    self.max_health = 10
                case 'Centaur':
                    self.damage = 2
                    self.max_health = 25
                case 'Dragon':
                    self.damage = 3
                    self.max_health = 20

            self.health = self.max_health
        else:
            self.max_health = max_health
            self.health = health
            self.damage = damage

    def fight(self, auto_enabled, *enemy_codes) -> bool:
        def auto_fight(enemies: list):
            print('Automatically defeating enemies... ')
            t.sleep(3)

            total_enemy_health = 0
            total_player_health = (self.max_health * 3) + self.health
            total_enemy_damage = 0

            for enemy in enemies:
                total_enemy_health += enemy.health
                total_enemy_damage += enemy.damage

            total_enemy_damage /= len(enemies)

            total_turns = total_enemy_health / self.damage

            total_enemy_damage *= total_turns
            total_enemy_damage /= 2

            if total_player_health - total_enemy_damage >= 0:
                self.health = round(total_player_health -
                                    total_enemy_damage) + 1

                if self.health > self.max_health:
                    self.health = self.max_health

                return True
            else:
                print('Defeating enemies failed.')
                return False

        print('\nFight initialised...\n')

        total_heals = 3
        enemies = []
        enemy_dict = {'z': 'Zombie',
                      'g': 'Guard',
                      'w': 'Wild Boar',
                      'm': 'Boar Merchant',
                      'b': 'Bushcraft Warrior',
                      'M': 'MEGA GUARD',
                      'a': 'THE ALMIGHTY'}

        for code in enemy_codes:
            print(f'There is {code[1:]}x {enemy_dict[code[0]]}')

            for _ in range(int(code[1:])):
                enemy = Enemy(enemy_dict[code[0]])
                enemies.append(enemy)

        for enemy in enemies:
            while enemy.health > 0:
                t.sleep(0.5)
                print(f'\nYou - {self.health}/{self.max_health}hp')
                print(f'{enemy.type} - {enemy.health}/{enemy.max_health}hp\n')
                t.sleep(0.5)

                if auto_enabled:
                    choices = ['Fight', 'Heal',
                               'Auto Enemy', 'Auto All', 'Run']
                else:
                    choices = ['Fight', 'Heal', 'Run']

                for option_num, option in enumerate(choices):
                    print(f'{option_num + 1} - {option}')

                while True:
                    try:
                        choice = int(input('>>> '))
                        break
                    except ValueError:
                        print('Try again!')
                        continue

                match choices[choice - 1]:
                    case 'Fight':
                        enemy.health -= self.damage
                    case 'Heal':
                        if self.health == self.max_health:
                            print('You already have max health.')
                            continue
                        elif total_heals > 0:
                            self.health = self.max_health
                            total_heals -= 1
                        else:
                            print('You have no heals left.')
                            continue
                    case 'Auto Enemy':
                        if auto_fight([enemy]):
                            enemy.health = 0
                            total_heals -= 1
                        else:
                            return False
                    case 'Auto All':
                        if auto_fight(enemies):
                            print('Well done! You defeated all the enemies.\n')
                            return True
                        else:
                            return False
                    case 'Run':
                        return False
                    case _:
                        print('Try again!')

                t.sleep(0.5)

                if enemy.health > 0:
                    if choice == 2:
                        if randint(1, 9) == 1:
                            print(f'{enemy.type} hit you.')
                            self.health -= enemy.damage
                        else:
                            print('You dodged.')

                        print(f'You have {total_heals} heals left')
                    else:
                        if randint(1, 2) == 1:
                            print(f'{enemy.type} hit you.')
                            self.health -= enemy.damage
                        else:
                            print('You dodged.')

                if self.health < 1:
                    if total_heals > 0:
                        print('You are injured. So, you run. Barely alive...')
                        t.sleep(4)
                        self.health = 1
                        return False
                    else:
                        print(
                            'Unforunately, you are out of heals. Therefore, you have died. This means, this is the end of the road for you...')
                        t.sleep(10)
                        quit()

            else:
                print('Enemy defeated.')
        else:
            print('Well done! You defeated all the enemies.\n')
            return True


code_randomiser = {'A': 123456789,
                   'B': 985412763,
                   'C': 192837465,
                   'D': 918273645,
                   'E': 132896475,
                   'F': 135792468,
                   'G': 389127546,
                   'H': 513249876,
                   'I': 873652914,
                   'J': 235684917}


def generate_save_code(player, merchants=0, missions=0) -> str:
    save_code = ''
    save_dmg = c.denary_to_hex(player.damage)
    if len(save_dmg) == 1:
        save_dmg = '0' + save_dmg
    save_hp = c.denary_to_hex(player.health)
    if len(save_hp) == 1:
        save_hp = '0' + save_hp
    save_max_hp = c.denary_to_hex(player.max_health)
    if len(save_max_hp) == 1:
        save_max_hp = '0' + save_max_hp

    if missions or merchants:
        final_part = int(str(merchants) + str(missions))
        final_part = c.denary_to_hex(final_part)

        final_part = '0' * (3 - len(final_part)) + final_part
    else:
        final_part = '000'

    shuffle_char = choice(list('ABCDEFGHIJ'))
    shuffle_code = code_randomiser[shuffle_char]

    shuffled_code = ''

    save_code = save_dmg + save_hp + save_max_hp + final_part

    for code_index in str(shuffle_code):
        shuffled_code += save_code[int(code_index) - 1]

    shuffled_code += shuffle_char

    with open('Savecodes.txt', 'r') as f:
        saved_save_codes = [code.strip() for code in f.readlines()]

    if len(saved_save_codes) >= 5:
        saved_save_codes.append(shuffled_code)
        saved_save_codes.pop(0)

        with open('Savecodes.txt', 'w') as f:
            f.write('\n'.join(saved_save_codes))
    else:
        with open('Savecodes.txt', 'a') as f:
            if len(saved_save_codes):
                f.write(f'\n{shuffled_code}')
            else:
                f.write(shuffled_code)

    return shuffled_code
    # 10 chars

    # 2 char hex for damage
    # 2 char hex for health
    # 2 char hex for max health
    # 3 char hex - concatinate merchants and missions, convert to hex
    # 1 char for shuffle


def load_game(shuffled_code) -> None:
    save_code = list('xxxxxxxxx')

    shuffle_char = shuffled_code[-1]
    shuffle_code = code_randomiser[shuffle_char]

    for save_index, code_index in enumerate(str(shuffle_code)):
        save_code[int(code_index) - 1] = shuffled_code[save_index]

    save_code = ''.join(save_code)

    dmg = c.hex_to_denary(save_code[:2])
    hp = c.hex_to_denary(save_code[2:4])
    max_hp = c.hex_to_denary(save_code[4:6])

    final_part = save_code[6:]
    final_part = str(c.hex_to_denary(final_part))

    if len(final_part) == 1:
        final_part = '0' + final_part

    merchants = int(final_part[0])
    missions = int(final_part[1:])

    player = Player('Loaded', max_health=max_hp, health=hp, damage=dmg)

    return player, merchants, missions


def merchant_menu(player, merchants):
    list_merchants = ['Swordsmith', 'Armourer', 'Witch']
    if merchants == 0:
        print('No merchants unlocked.')
        return

    list_merchants.append('Quit')

    for item in range(merchants):
        print(f'{item + 1} - {list_merchants[item]}')

    while True:
        try:
            choice = int(input('>>> '))
        except ValueError:
            print('Try again!')
            continue

        match list_merchants[choice - 1]:
            case 'Swordsmith':
                mm.swordsmith(player)
                return
            case 'Armourer':
                mm.armourer(player)
                return
            case 'Witch':
                mm.witch(player)
                return
            case 'Quit':
                print('Returning...')
                t.sleep(1)
                return
            case _:
                continue


def reading_menu():
    speed_cap = 1000

    print('Would you like to complete a reading speed test? Yes or no.')
    while True:
        choice: str = input('>>> ').lower()
        match choice:
            case 'yes':
                if d.reading_test() > speed_cap:
                    d.reading_speed = speed_cap

                    d.dialogue(
                        f'\nUnfortunately, your read speed is beyond that allowed by the game. Your speed is capped at {speed_cap} WPM.')
                return
            case 'no':
                print('Would you like to enter your reading speed? Yes or no.')
                break
            case _:
                print('Try again!')
                continue

    while True:
        choice: str = input('>>> ').lower()
        match choice:
            case 'yes':
                break
            case 'no':
                return
            case _:
                print('Try again!')
                continue

    print('Please enter you reading speed, in words per minute.')

    while True:
        try:
            speed = int(input('>>> '))
            break
        except ValueError:
            print('Try again!')
            continue

    if speed > speed_cap:
        d.reading_speed = speed_cap

        d.dialogue(
            f'\nUnfortunately, your read speed is beyond that allowed by the game. Your speed is capped at {speed_cap} WPM.')
    else:
        d.reading_speed = speed


def main(save_code):
    merchants = 0
    missions = 0

    player, merchants, missions = load_game(save_code)

    while True:
        print(
            f'\nStats - Health: {player.health}/{player.max_health}, Damage: {player.damage}\n')

        choices = ['Continue', 'Merchants', 'Save', 'Load', 'Reading Speed', 'Quit']

        if missions >= 10:
            choices.pop(0)

        for option_num, option in enumerate(choices):
            print(f'{option_num + 1} - {option}')

        while True:
            try:
                choice = int(input('>>> '))
                break
            except ValueError:
                print('Try again!')
                continue

        match choices[choice - 1]:
            case 'Continue':
                print(f'Mission {missions + 1}')
                print('Continuing...\n')
                t.sleep(2)
                eval(f'm.mission_{missions + 1}(player)')
                missions += 1
                if missions in (2, 4, 7):
                    merchants += 1

                save_code = generate_save_code(player, merchants, missions)

                continue
            case 'Merchants':
                merchant_menu(player, merchants)

            case 'Save':
                save_code = generate_save_code(player, merchants, missions)

                print('Your save code is', save_code)
                t.sleep(1)

            case 'Load':
                with open('Savecodes.txt', 'r') as f:
                    saved_save_codes = [code.strip() for code in f.readlines()]
                    if saved_save_codes:
                        print('Last 5 save codes:')

                        for code in saved_save_codes:
                            player, merchants, missions = load_game(code)
                            print(f'{code} - {player.damage}dmg, {player.health}/{player.max_health}hp. Mission {missions + 1}')

                        print()

                input_save_code = input(
                    'Enter your, 10 character, save code: ').upper()
                if len(input_save_code) == 10:
                    player, merchants, missions = load_game(input_save_code)
                else:
                    print('Try again!')
            case 'Reading Speed':
                reading_menu()
            case 'Quit':
                quit()
            case _:
                print('Try again!')


def prologue():
    d.dialogue('Welcome Adventurer! On this journey, you will complete tasks, fight enemies and most importantly make choices.\n')
    d.dialogue('So, to start this adventure you must make a choice...\n')
    print('Which would you like to be:')
    print('-Centaur - 2dmg, 25hp')
    print('-Wizard - 4dmg, 15hp')
    print('-Knight - 1dmg, 30hp')
    print('-Dragon - 3dmg, 20hp')
    print('-Elf - 5dmg, 10hp')

    while True:
        choice: str = input('>>> ').lower()
        match choice:
            case 'wizard':
                player = Player('Wizard')
            case 'knight':
                player = Player('Knight')
            case 'elf':
                player = Player('Elf')
            case 'centaur':
                player = Player('Centaur')
            case 'dragon':
                player = Player('Dragon')
            case _:
                print('Try again!')
                continue

        break

    d.dialogue(
        '\nNice choice. Now, we will continue towards the forest and where you will be staying - Laketree Village.')
    d.dialogue('However... we may encounter some zombies on the way.')
    d.dialogue('Oh here they are.')

    if player.fight(False, 'z3'):
        t.sleep(2)
        d.dialogue('Whew! Well done defeating the zombies.')

        if player.health < player.max_health:
            d.dialogue(
                'I see you took some damage. I will provide you with some armour, a 5hp bonus, and fully heal you.')
            player.max_health += 5
            player.health = player.max_health
        else:
            d.dialogue(
                'You wielded your weapon well. I will provide you with a sword, a 2dmg bonus.')
            player.damage += 2
    else:
        d.dialogue(
            '\nRunning was the cowardly option. We must now take the long way around.')

    d.dialogue(
        '\nWe have now arrived at Laketree Village. A small, yet beautiful, village.')
    d.dialogue('This will be the hub for your adventure. Here you will be able to complete quests, with merchants for armour and weapons. You will, also, be able to save and load your adventure. You may, also, want to change your reading speed.')

    return player


if __name__ == '__main__':
    with open('Savecodes.txt', 'r') as f:
        saved_save_codes = [code.strip() for code in f.readlines()]
        if saved_save_codes:
            print('Last 5 save codes:')

            for code in saved_save_codes:
                player, merchants, missions = load_game(code)
                print(f'{code} - {player.damage}dmg, {player.health}/{player.max_health}hp. Mission {missions + 1}')

            print('\nWould you like to enter a save code? Yes or no.')
            answer = input('>>> ').lower()
            if answer == 'yes':
                input_save_code = input(
                    'Enter your, 10 character, save code: ').upper()
                if len(input_save_code) == 10:
                    main(input_save_code)
            else:
                print()
                player = prologue()
                main(generate_save_code(player))
        else:
            player = prologue()
            main(generate_save_code(player))
