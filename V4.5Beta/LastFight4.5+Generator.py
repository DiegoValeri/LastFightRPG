
import os
import time
import random
import threading
import tkinter as tk
import time
import requests
import re
import sys
import os
import builtins

os.system("")

focus_streak = 0
attack_streak = 0  # Compteur de coups consécutifs
defend_streak = 0
combo_streak = 0   # alterner attaque/défense
player_max_pv = 0
enemy_max_pv = 0
enemy_special_cd = 0  # cooldown du spécial ennemi (en tours ennemis)
effects = {}
training = 0
giga_random_mode = False

#======MODE ONLINE============
FIREBASE_URL = "https://weeklylf-5a450-default-rtdb.europe-west1.firebasedatabase.app/weeklyChallenge/current.json"

def get_weekly_challenge():
    try:
        res = requests.get(FIREBASE_URL)
        if res.status_code == 200:
            return res.json()
        else:
            print("Erreur, nous n'avons pas pu récupérer les données en ligne. :", res.status_code)
            return None
    except Exception as e:
        print("Erreur de connection, vérifiez votre conenction internet :", e)
        return None

challenge = get_weekly_challenge()
#==========================================

_old_input = input

def patched_input(prompt=""):
    user = _old_input(prompt).strip().lower()
    if user == "r":
        clear_console()
        os.execv(sys.executable, ["python"] + sys.argv)
    return user

builtins.input = patched_input

# === Codes couleurs ANSI ==================
# Active (un peu) l’ANSI sous Windows
if os.name == "nt":
    try:
        os.system("")  # suffit souvent sur Windows 10+
    except Exception:
        pass

# Codes ANSI
RESET  = "\033[0m"    # Reset la couleur
BLUE   = "\033[94m"   # Bouclier
RED    = "\033[91m"   # Dégâts
PINK   = "\033[95m"   # PV (rose / magenta clair)
PURPLE = "\033[35m"   # Magie (violet)
GREEN = "\033[32m"    # PV vert
GREENER = "\033["
YELLOW = "\033[33m"   #Jaune pour la charte de difficulté
DEEPGREEN = "\033[32m"
GRAY = "\033[90m"
BLACK = "\033[30m"
DARK_GRAY = "\033[38;5;233m"

# Option pour couper la couleur
USE_COLORS = True

def colorize(text: str) -> str:
    if not USE_COLORS:
        return text
    # Remplacements mot entier, sensibles à la casse
    text = re.sub(r"\b[Bb]ouclier\b",  f"{BLUE}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Dd]effence\b",  f"{BLUE}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Dd]égâts\b",    f"{RED}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Aa]ttaque\b",   f"{RED}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Pp][Vv]\b",     f"{GREEN}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Pp][Vv]s\b",    f"{GREEN}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Mm]agie\b",     f"{PURPLE}\\g<0>{RESET}", text)
    return text

# Sauvegarde du print d’origine pour éviter la récursion
_original_print = print

def cprint(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
    # Concatène les args comme le print natif
    msg = sep.join(map(str, args))
    msg = colorize(msg)
    _original_print(msg, end=end, file=file, flush=flush)

builtins.print = cprint

# =================== Variables globales ===================
ppv = psh = pma = 0
name = ""
epv = esh = ema = 0
last_player_action = None  # Mémoire de la dernière action du joueur

# =================== Utilitaires ===================
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

if os.name == "nt":
    import msvcrt
RESET = "\033[0m"
BLUE_SHADES = [
    "\033[94m",  # Bleu clair
    "\033[36m",  # Cyan
    "\033[96m",  # Cyan clair
]
logo = [
" _               _  ______ _       _     _   _   _    ___ ",
"| |             | | |  ___(_)     | |   | | | | | |  /   |",
"| |     __ _ ___| |_| |_   _  __ _| |__ | |_| | | | / /| |",
"| |    / _` / __| __|  _| | |/ _` | '_ \\| __| | | |/ /_| |",
"| |___| (_| \\__ \\ |_| |   | | (_| | | | | |_\\ \\_/ /\\___  |",
"\\_____/\\__,_|___/\\__\\_|   |_|\\__, |_| |_|\\__|\\___/ o  |_/ ",
"                              __/ |                       ",
"                             |___/                        ",
"                                                          "
]
footer = "          \033[36mVersion: 4 'Colors and GUIs'  (25/08/25)\033[0m\n                       \033[36mPRESS ENTER\033[0m"
def colorize_line(line, colors, offset=0):
    result = ""
    for i, ch in enumerate(line):
        color = colors[(i + offset) % len(colors)]
        result += f"{color}{ch}{RESET}"
    return result
def key_pressed():
    if os.name == "nt":  # Windows
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in [b"\r", b"\n"]:
                return True
    return False
def animate_logo():
    offset = 0
    lines_count = len(logo) + 2  
    try:
        while True:
            if offset > 0:
                sys.stdout.write(f"\033[{lines_count}A")  # Remonte au début
            for idx, line in enumerate(logo):
                print(colorize_line(line, BLUE_SHADES, offset + idx))
            print(footer)
            sys.stdout.flush()

            time.sleep(0.1)
            offset += 1

            if key_pressed():
                break
    except KeyboardInterrupt:
        pass
animate_logo()
#Fais avec ChatGPT a 100% ^^^^^^^^^^^^^^
# =================== Fenêtre des stats ===================

def start_FF():
    app = StatsWindow()

    def game_loop():
        round("Joueur")

    threading.Thread(target=game_loop, daemon=True).start()
    app.mainloop()

def main_menu():
    os.system("mode con: cols=140 lines=40")
    clear_console()
    print("\033[94m=== Menu Principal ===\033[0m")
    print("\033[36m1. Combat Libre\033[0m")
    print("\033[96m2. Mode Aventure\033[0m")
    choix = input("Choisis ton mode: ")

    if choix == "1":
        setup_characters()
        start_FF()
    elif choix == "2":
        start_story_mode()
    else:
        print("Choix invalide")
        main_menu()


#============================================================================================ FREE FIGHT MODE ======================================================================================================================
def setup_characters():
    global ppv, psh, pma, name, epv, esh, ema
    global giga_random_mode
    global training
    

    
    while True:
        clear_console()
        print("\033[33m=== Menu principal ===\033[0m")
        print("\033[36m1 - Modes classiques\033[0m")
        print("\033[94m2 - Modes bonus\033[0m")
        print("\033[34m3 - Challenge de la semaine (Internet requis)\033[0m")
        print("\033[91mq - Quitter le jeu\033[0m")
        print("\033[33m======================\033[0m")
        main_choice = input("\nEntrez votre choix : ")

        if main_choice == "1":
            # === MODES CLASSIQUES ===
            while True:
                clear_console()
                print("\033[33m=== Choisissez un mode classique ===\033[0m")
                print("\033[32m1 - Facile\033[0m")
                print("\033[32m1.5 - Simple\033[0m")
                print("\033[32m2 - Normal\033[0m")
                print("\033[33m2.5 - Intermédiaire\033[0m")
                print("\033[33m3 - Difficile\033[0m")
                print("\033[91m3.5 - Ardu\033[0m")
                print("\033[91m4 - Féroce\033[0m")
                print("b - Retour")
                print("\033[33m====================================\033[0m")

                choice = input("\nEntrez le numéro du mode souhaité : ")

                if choice == "1":
                    ppv, psh, pma = 40, 20, 25
                    name = "Chef de Guerre Gobelin"
                    epv, esh, ema = 50, 20, 20
                    break
                elif choice == "1.5":
                    ppv, psh, pma = 45, 20, 25
                    name = "Le Slime visqueux"
                    epv, esh, ema = 60, 25, 30
                    break
                elif choice == "2":
                    ppv, psh, pma = 50, 25, 30
                    name = "Sorcier Squelette"
                    epv, esh, ema = 70, 35, 30
                    break
                elif choice == "2.5":
                    ppv, psh, pma = 60, 30, 30
                    name = "Combattant Orc"
                    epv, esh, ema = 75, 40, 35
                    break
                elif choice == "3":
                    ppv, psh, pma = 70, 25, 30
                    name = "Le Nécromancien"
                    epv, esh, ema = 90, 35, 45
                    break
                elif choice == "3.5":
                    ppv, psh, pma = 80, 30, 30
                    name = "L'archimage de l'ombre"
                    epv, esh, ema = 100, 30, 60
                    break
                elif choice == "4":
                    ppv, psh, pma = 85, 30, 25
                    name = "Le Seigneur des Ténèbres"
                    epv, esh, ema = 105, 50, 80
                    break

                elif choice.lower() == "b":
                    exit() 
                else:
                    print("Veuillez choisir un nombre.")
                    input("Appuyez sur Entrée pour réessayer...")
            break  # Sortir du menu principal une fois un mode choisi



        elif main_choice == "3":
            while True:
                clear_console()
                updatedAt = challenge["updatedAt"]
                print("\033[33m========= Mode online  ==========\033[0m")
                print("Défi mis a jour le: " + updatedAt)
                print("1 - Challenge temporaire")
                print("\033[33m=================================\033[0m")
                choice = input("Entrez votre choix : ")
                if choice == "1":
                    print("Récupération du défi temporaire...")
                    if not challenge:
                        print("Erreur : aucun défi trouvé.")
                        input("Appuie sur Entrée pour continuer…")
                        continue
                    # Stats
                    ppv, psh, pma = challenge["ppv"], challenge["psh"], challenge["pma"]
                    name = challenge["name"]
                    epv, esh, ema = challenge["epv"], challenge["esh"], challenge["ema"]  
                    # Effets
                    def as_bool(x): 
                        return str(x).lower() in ("1", "true", "vrai", "oui", "on")
                    effects.clear()
                    if as_bool(challenge.get("enervé", False)):
                        effects["enervé"] = True
                        print("Berserker : ses dégâts sont 50% plus puissants sil il déscend sous 30 PVs.")

                    if as_bool(challenge.get("réflexion", False)):
                        effects["réflexion"] = True
                        print("Mirroir: L'enemi renvoie 25% des dégâts recus.")
                        
                    if as_bool(challenge.get("regen", False)):
                        effects["regen"] = True
                        print("Cicatrisant: L'enemi se regénère de 5 PV par tour")

                    if as_bool(challenge.get("lifesteal", False)):
                        effects["lifesteal"] = True
                        print("Vampirisme: L'enemi se soigne jusqu'à 20% des dégâts qu'il inflige.")

                    if as_bool(challenge.get("affaiblissement", False)):
                        effects["affaiblissement"] = True
                        print("Drainage: À chaque tour, le joueur perd 5 de magie.")
                        
                    input("Appuie sur Entrée pour lancer le combat…")
                else:
                    input("Erreur, vuillez choisir un nombre valide.")
                    break
                return # on sort du menu online pour démarrer le combat

        elif main_choice == "2":
            # === MODES BONUS ===
            while True:
                clear_console()
                print("\033[33m=== Choisissez un mode bonus ===\033[0m")
                print(f"1 - {GREEN}Bac à sable{RESET}")
                print(f"2 - {PINK}La étrange trouvaille{RESET}")
                print(f"3 - {PURPLE}Randomiser{RESET}")
                print(f"4 - {RED}Giga Randomiser{RESET}")
                print(f"r - {BLUE}Retour{RESET}")
                print("\033[33m================================\033[0m")

                choice = input("\Entrez votre choix : ")

                if choice == "1":
                    clear_console()
                    choix = input("Mode entraînement ? (L'enemi ne fais rien)\n Non: 1\n Oui: 2\n")
                    if choix == "1":
                        print("=== Configuration du joueur ===")
                        while True:
                            try:
                                ppv = int(input("PV du joueur : "))
                                psh = int(input("Bouclier du joueur : "))
                                pma = int(input("Magie du joueur : "))
                                break
                            except ValueError:
                                print("Entrez uniquement des nombres.")

                        clear_console()
                        print("=== Configuration de l'ennemi ===")
                        name = input("Nom de l'ennemi : ")
                        while True:
                            try:
                                epv = int(input(f"PV de {name} : "))
                                esh = int(input(f"Bouclier de {name} : "))
                                ema = int(input(f"Magie de {name} : "))
                                break
                            except ValueError:
                                print("Entrez uniquement des nombres.")
                        break
                    elif choix == "2":
                        training = 1
                        print("=== Configuration du joueur ===")
                        while True:
                            try:
                                ppv = int(input("PV du joueur : "))
                                psh = int(input("Bouclier du joueur : "))
                                pma = int(input("Magie du joueur : "))
                                break
                            except ValueError:
                                print("Entrez uniquement des nombres.")

                        clear_console()
                        print("=== Configuration de l'ennemi ===")
                        name = "Bim le mannequin"
                        while True:
                            try:
                                epv = int(input(f"PV de {name} : "))
                                esh = int(input(f"Bouclier de {name} : "))
                                ema = int(input(f"Magie de {name} : "))
                                break
                            except ValueError:
                                print("Entrez uniquement des nombres.")
                        break



                elif choice == "2":
                    ppv, psh, pma = 20, 20, 10
                    name = "Le fou"
                    epv, esh, ema = 200, 100, 1000
                    break

                elif choice == "3":
                    print("Alea jacta est...")
                    time.sleep(1)
                    ppv, psh, pma = random.randint(10, 150), random.randint(10, 150), random.randint(10, 110)
                    name = "le joker"
                    epv, esh, ema = random.randint(10, 150), random.randint(10, 150), random.randint(10, 110)
                    break
                
                elif giga_random_mode:
                    ppv, psh, pma = random.randint(10, 200), random.randint(0, 100), random.randint(0, 200)
                    epv, esh, ema = random.randint(10, 200), random.randint(0, 200), random.randint(0, 200)
                    print("\nLe bouffon joue un mauvais tour...")

                    # Flag spécial pour activer le random à chaque tour
                    giga_random_mode = True
                    break

                elif choice == "4":
                    giga_random_mode = True



                elif choice.lower() == "banerask le vilain":
                    print("...Tu n'es pas censé être là...")
                    time.sleep(2)
                    print("Une vilaine aura gèle tes os.")
                    ppv, psh, pma = 40, 25, -10
                    name = "Banerask le vilain"
                    epv, esh, ema = 250, 777, 70
                    time.sleep(1)
                    break

                elif choice.lower() == "b":
                    exit()
            break  # Sortir du menu principal une fois un mode choisi

        elif main_choice == "4":
            while True:
                clear_console()
                print("\033[33m=== Choisissez mode extreme ===\033[0m")
                print(f"1 - {RED}La Faucheuse{RESET}")
                print(f"1.5 - {YELLOW}Le Minautaure{RESET}")
                print(f"2 - {PURPLE}Le Stalker{RESET}")
                print(f"2.5 - {BLUE}L'Architecte{RESET}")
                print(f"3 - {PINK}Le Fou Condamné{RESET}")
                print(f"r - {GREEN}Retour{RESET}")
                print("\033[33m====================================\033[0m")
                
                choice = input("Choisissez la créature a afronter.")
                                
                if choice == "1":
                    ppv, psh, pma = 90, 35, 20
                    name = "La Faucheuse"
                    epv, esh, ema = 120, 60, 100
                    break
                elif choice == "1.5":
                    ppv, psh, pma = 95, 50, 25
                    name = "La Minautaure"
                    epv, esh, ema = 125, 70, 100
                    break
                elif choice == "2":
                    ppv, psh, pma = 100, 55, 30
                    name = "Le Stalker"
                    epv, esh, ema = 130, 75, 100
                    break
                elif choice == "2.5":
                    ppv, psh, pma = 110, 65, 30
                    name = "L'Architecte"
                    epv, esh, ema = 150, 80, 100
                    break
                elif choice == "3":
                    ppv, psh, pma = 120, 100, 50
                    name = "Le Fou Condamné"
                    epv, esh, ema = 230, 200, 666
                    break
            break

        elif main_choice.lower() == "b":
            exit()
        else:
            print("Veuillez choisir un nombre.")
            input("Appuyez sur Entrée pour réessayer...")

        
    # === Affichage final avant le jeu ===
    clear_console()
    print("\033[33m=== Stats des combattants ===\033[0m")
    print(f"Joueur  - PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
    print(f" {name} - PV: {epv} | Bouclier: {esh} | Magie: {ema}")
    input("\nAppuyez sur Entrée pour commencer le combat...")
    clear_console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def enemy_attack():
    global ppv, psh, effects, epv, esh, name, last_player_action

    print(f"{name} attaque le joueur !")
    damage = random.randint(13, 24)
    
    if effects.get("enervé"):
        damage *= 1.5
        print("Enervé, les dégâts de l'ennemi sont 50% plus forts.")
    
    if effects.get("lifesteal"):
        epv += int(damage*0.2)
        print(f"{name} vous a volé " + str(int(damage*0.2)) + " PVs.")

    if last_player_action == "counter":
        # Le joueur contre-attaque
        print("L'épéeiste contre attaque!")
        # Le joueur subit moins de dégâts
        reduced_damage = random.randint(13, 24)*0.5
        psh -= reduced_damage
        if psh < 0:
            ppv += psh
            psh = 0
        else:
            ppv -= reduced_damage

        counter_damage = reduced_damage*0.3
        epv -= counter_damage

        print(f"Tu subis {reduced_damage} dégâts et renvoies {counter_damage} dégâts à {name} !")
        last_player_action = None  # on consomme la contre-attaque

    else:
        # comportement normal (comme avant)
        if psh > 0:
            psh -= damage
            print(f"{name} inflige {damage} points de dégâts. Bouclier du joueur restant : {psh}")
            if psh < 0:
                ppv += psh  # psh est négatif → on retire aux PV
                print(f"Le bouclier du joueur est brisé ! Le joueur perd {-psh} PV. PV restants : {ppv}")
                psh = 0
        else:
            ppv -= damage
            print(f"{name} inflige {damage} points de dégâts au joueur. PV restants : {ppv}")

    input("Appuyez sur Entrée pour continuer...")

def enemy_defend():
    global esh, name
    esh += 10
    if esh > 150:
        esh = 150
    print(f"{name} se défend et gagne 10 points de bouclier. Bouclier actuel : {esh}")
    input("Appuyez sur Entrée pour continuer...")

def enemy_pass_turn():
    global epv, esh, ema, enemy_max_pv, name
    print(f"{name} puise dans le désespoir pour reprendre des forces.")
    epv = min(enemy_max_pv, epv + 5)
    esh += 3
    ema += 5
    input("Appuyez sur Entrée pour continuer...")

def enemy_decision():
    """Retourne 'attack' | 'defend' | 'heal' | 'special' selon l'état."""
    hp_ratio = epv / max(1, enemy_max_pv)
    actions = []

    # Base selon PV
    if hp_ratio > 0.4:
        actions += ["attack"] * 6 + ["defend"] * 2
    else:
        actions += ["attack"] * 4 + ["defend"] * 3 + ["heal"]

    # Réactivité simple à l'action du joueur
    if last_player_action == "defend":
        actions += ["attack"] * 2
    if last_player_action == "attack" and esh < 10:
        actions += ["defend"] * 2

    # Spécial si dispo (cooldown terminé)
    if enemy_special_cd == 0:
        actions += ["special"]

    return random.choice(actions)

def enemy_turn():
    """Joue le tour ennemi. Retourne True si le combat se termine."""
    global ppv, psh, pma, epv, esh, ema, enemy_special_cd

    print("\n--- Tour de l'ennemi ---")
    input("Appuyez sur Entrée pour continuer...")

        
    if effects.get("regen"):
        print("Regen: l'enemi se soigne de 5 PVs")
        epv += 5

    action = enemy_decision()

    if action == "attack":
        enemy_attack()

    elif action == "defend":
        enemy_defend()

    elif action == "heal":
        # réutilise ton "pass turn" qui rend PV/Mana/Bouclier
        enemy_pass_turn()

    elif action == "special" and enemy_special_cd == 0:
        # Spécial : Brise-Garde — dégâts directs qui ignorent le bouclier
        dmg = random.randint(13, 19)
        ppv -= dmg
        print(f"{name} exécute Brise-Garde ! {dmg} dégâts directs ignorent le bouclier. PV joueur : {ppv}")
        enemy_special_cd = 2  # 2 tours ennemis avant de pouvoir relancer
        input("Appuyez sur Entrée pour continuer...")
    else:
        # Si spécial pas dispo, fallback agressif
        enemy_attack()

    # Tick du cooldown en fin de tour ennemi
    if enemy_special_cd > 0:
        enemy_special_cd -= 1

    # Conditions de fin
    if ppv <= 0:
        print("L'aventure de l'épéiste a pris fin brutalement, tué par " + name)
        input("Appuyez sur entrée pour quitter.")
        return True
    if epv <= 0:
        print("L'épéiste a triomphé, " + name + " a été vaincu.")
        input("Appuyez sur entrée pour quitter.")
        return True

    return False

def compute_efficiency(action_type, base_value):
    """Retourne la valeur ajustée et affiche un message si malus appliqué"""
    global attack_streak, defend_streak, combo_streak

    value = base_value

    # Malus attaque
    if action_type == "attack":
        if attack_streak == 2:
            value = int(value * 0.7)
            print("Tu commence a fâtiguer, ton attaque est réduite ! (-30%)")
        elif attack_streak >= 3:
            value = int(value * 0.4)
            print("Tu es essoufflé, ton attaque est grandement réduite !")
        elif attack_streak >= 5:
            value = int(value * 0.1)
            print("Tu es épuisé, ton attaque est presque inefficace ! (-90%)")
    # Malus défense
    elif action_type == "defend":
        if defend_streak == 2:
            value = int(value * 0.7)
            print("Tu commence a fâtiguer, ta deffence est réduite ! (-30%)")
        elif defend_streak >= 3:
            value = int(value * 0.4)
            print("Tu es à bout de souffle, ton bouclier grandement réduit !")
        elif defend_streak >= 5:
            value = int(value * 0.1)
            print("Tu es épuisé, ton bouclier est presque inefficace ! (-90%)")

    # Malus combo (spam attaque/défense en alternance)
    if combo_streak >= 3:
        value = int(value * 0.6)
        print("Tu t’épuises à alterner attaque/défense, efficacité réduite ! (-40%)")
    elif combo_streak >= 5:
        value = int(value * 0.1)
        print("Tu es épuisé par l'alternance, efficacité grandement réduite ! (-90%)")

    return value

def attack(attacker_name):
    global ppv, epv, esh, attack_streak, defend_streak, combo_streak, last_player_action

    # Gestion des streaks
    if last_player_action == "attack":
        attack_streak += 1
    else:
        attack_streak = 1
    defend_streak = 0
    combo_streak = combo_streak + 1 if last_player_action == "defend" else 0

    print(f"{attacker_name} décide de mettre des dégâts!")

    # Calcul dégâts avec malus
    damage = random.randint(15, 24)
    damage = compute_efficiency("attack", damage)

    # Application des dégâts
    if esh > 0:
        esh -= damage
        print(f"{attacker_name} inflige {damage} points de dégâts à {name}. Bouclier restant: {esh}")
        if esh < 0:
            epv += esh
            print(f"Le bouclier est brisé! {name} perd {-esh} points de vie. PV restant: {epv}")
            esh = 0
    else:
        epv -= damage
        print(f"{attacker_name} inflige {damage} points de dégâts à {name}. PV restant: {epv}")

    if effects.get("réflexion"):
        print(f"L'adveraire réfléchit 10% des dégâts recus, vous perdez " + str(damage*0.10) + "PVs!")
        ppv -= int(damage*0.10)

    last_player_action = "attack"
    input("Appuyez sur Entrée pour continuer...")
    return True

def defend(attacker_name):
    global psh, attack_streak, defend_streak, combo_streak, last_player_action

    print(f"{attacker_name} décide de se mettre du bouclier!")

    # Gestion des streaks
    if last_player_action == "defend":
        defend_streak += 1
    else:
        defend_streak = 1
    attack_streak = 0
    combo_streak = combo_streak + 1 if last_player_action == "attack" else 0

    # Gain de base
    shield_gain = 10
    shield_gain = compute_efficiency("defend", shield_gain)

    # Application
    if psh < 100:
        psh += shield_gain
        print(f"{attacker_name} augmente son bouclier de {shield_gain} points. Bouclier actuel: {psh}")
    else:
        print(f"{attacker_name} ne peut pas augmenter son bouclier car il est déjà au maximum.")

    last_player_action = "defend"
    input("Appuyez sur Entrée pour continuer...")
    return True

def cast_spell(attacker_name):
    global epv, ppv, pma, esh, ema
    while True:
        clear_console()
        print(f"{attacker_name} choisit quel sort lancer")
        spell_choice = input(
            
    f"{YELLOW}==================== Liste de sorts ==============={RESET}\n"
    f"1: Soin [{PURPLE}25 Magie{RESET}] (Restaure {GREEN}20 PV{RESET})\n"
    f"2: Sacrifice [{RED}20 PV{RESET}] (Ajoute +50% de {PURPLE}magie{RESET}, cappé à {PURPLE}190{RESET})\n"
    f"3: Oblivion [{PURPLE}50 Magie{RESET}] (Dégâts: {PINK}PV du joueur{RESET} / 2)\n"
    f"4: Boule de feu [{PURPLE}15 Magie{RESET}] ({RED}13-18 dégâts{RESET}, traverse le {BLUE}bouclier{RESET})\n"
    f"5: Mur magique [{PURPLE}15 Magie{RESET}] (Ajoute {BLUE}15 Shield{RESET})\n"
    f"6: Croc de vampire [{PURPLE}25 Magie{RESET}] (Draine {GREEN}15 PV{RESET} à l'ennemi)\n"
    f"7: Chaîne du Chaos [{PURPLE}30 Magie{RESET}] (Effet aléatoire)\n"
    f"8: Fracture [{PURPLE}45 Magie{RESET}] (Inflige {RED}35 dégâts{RESET} au {BLUE}bouclier ennemi{RESET})\n"
    f"9: Retour\n"
    f"{YELLOW}==================================================={RESET}\n"
)
        
        if spell_choice == "1":
            if pma >= 25:
                print(f"{attacker_name} lance Soin et récupère 20 PV.")
                ppv = min(player_max_pv, ppv + 20)
                print(f"PV actuel: {ppv}")
                pma -= 25
            else:
                print("Pas assez de magie pour lancer Soin.")
            input("Appuyez sur Entrée pour continuer...")
            return False
#SOIN

        elif spell_choice == "4":
            if pma >= 15:
                pma -= 15
                damage = random.randint(15, 20)
                epv -= damage
                print(f"Tu lances une Boule de Feu ! {name} perd {damage} PV. PV ennemi : {epv}")
                if effects.get("réflexion"):
                    print(f"L'adveraire réfléchit 10% des dégâts recus, vous perdez " + str(damage*0.10) + "PVs!")
                    ppv -= int(damage*0.10)
            else:
                print("Pas assez de magie pour lancer Boule de Feu.")
            input("Appuyez sur Entrée pour continuer...")
            return False

        elif spell_choice == "5":
            if pma >= 15:
                pma -= 15
                psh += 15
                print(f"Tu invoques un Mur Magique ! Tu gagnes 15 points de bouclier. Bouclier actuel : {psh}")
            else:
                print("Pas assez de magie pour lancer Mur Magique.")
            input("Appuyez sur Entrée pour continuer...")
            return False

        elif spell_choice == "6":
            if pma >= 25:
                pma -= 25
                drain = 15
                epv -= drain
                ppv += drain
                if effects.get("réflexion"):
                    print(f"L'adveraire réfléchit 10% des dégâts recus, vous perdez " + str(drain*0.10) + "PVs!")
                    ppv -= int(drain*0.10)
                print(f"Tu lances Drain de Vie ! {name} perd {drain} PV et tu gagnes {drain} PV. PV ennemi : {epv}, PV joueur : {ppv}")
            else:
                print("Pas assez de magie pour lancer Drain de Vie.")
            input("Appuyez sur Entrée pour continuer...")
            return False

        elif spell_choice == "7":
            if pma >= 30:
                pma -= 30
                effet = random.choice(["degat", "soin", "perte_magie", "gain_bouclier"])
                if effet == "degat":
                    dmg = random.randint(5, 18)
                    epv -= dmg
                    if effects.get("réflexion"):
                        print(f"L'adveraire réfléchit 10% des dégâts recus, vous perdez " + str(dmg*0.10) + "PVs!")
                        ppv -= int(dmg*0.10)
                    print(f"Chaîne du Chaos ! Une explosion frappe {name} pour {dmg} dégâts.")
                elif effet == "soin":
                    heal = random.randint(5, 15)
                    ppv += heal
                    print(f"Chaîne du Chaos ! Tu récupères {heal} PV.")
                elif effet == "perte_magie":
                    if random.randint(1, 100) == 100:
                        print("Le conte du Joker\nIl était une fois dans la grande ville de Limbhourg, un homme enchainait les petits boulots pour survivre, il a tout essayé et rien ne lui plaisait. Un jour comme a son habitude il décrocha un nouvel emploi: Bouffon du roi. Mais le roi était un homme froid et sans humour, il ne riait jamais aux blagues du bouffon. Un jour le bouffon décida de faire une blague au roi, il lui dit: 'Votre majesté, vous êtes si laid que même les miroirs ont peur de vous regarder.' Le roi furieux ordonna l'exécution du bouffon. Sa tête fut tranchée et le roi fit jetter son corps dans le donjon. Depuis ce jour, le bouffon hante le donjon, cherchant à se venger du roi. Maintenant surnommé 'Joker', il est devenu un esprit sournois et malicieux. Prêt a tout pour mettre a bien sa quête de vengeance.")
                    else:
                        print("Cela n'a eu aucun effet.")
                elif effet == "gain_bouclier":
                    gain = random.randint(5, 12)
                    psh += gain
                    print(f"Chaîne du Chaos ! Ton bouclier augmente de {gain} points (total : {psh}).")
                input("Appuyez sur Entrée pour continuer...")
                return True
            else:
                print("Pas assez de magie pour lancer Chaîne du Chaos.")
                input("Appuyez sur Entrée pour continuer...")
                return False   # <-- très important

        
        elif spell_choice == "2":
            if ppv >= 21 and pma >= 10:
                print(f"{attacker_name} vous puisez dans vos veines comme sacrifice pour doubler votre magie.")
                ppv -= 20
                pma *= 1.5
                pma = int(pma)  # Convertit en entier
                if pma > 190:
                    pma = 190
                print(f"Magie actuelle: {pma}")
                input("Appuyez sur Entrée pour continuer...")
                return True
            elif ppv <= 20:
                print(f"{attacker_name} vous n'avez pas assez de PV pour lancer le sort")
                input("Appuyez sur Entrée pour continuer...")
                return False
            else:
                print("Pas assez de magie pour lancer le sort de magie.")
                input("Appuyez sur Entrée pour continuer...")
                return False
#SACRIFICE

        elif spell_choice == "3":
            if pma >= 50:
                damage = int(ppv/2)
                if damage < 0:
                    damage = 0
        
                print(f"{attacker_name} lance le sort Oblivion et inflige {damage} points de dégâts à {name}.")
        
                if esh > 0:
                    esh -= damage
                    print(f"{name} perd {damage} points de bouclier. Bouclier restant: {esh}")
                    if esh < 0:
                        epv += esh  # esh est négatif, on retire le surplus aux PV
                        print(f"Le bouclier est brisé ! {name} perd {-esh} PV. PV restant : {epv}")
                        esh = 0
                else:
                    epv -= damage
                    print(f"{name} n’a plus de bouclier. Il perd {damage} PV. PV restant : {epv}")
                if effects.get("réflexion"):
                    print(f"L'adveraire réfléchit 10% des dégâts recus, vous perdez " + str(damage*0.10) + "PVs!")
                    ppv -= int(damage*0.10)
                pma -= 50
            else:
                print("Pas assez de magie pour lancer Oblivion.")
            input("Appuyez sur Entrée pour continuer...")
            return False
        
#OBLIVION
        elif spell_choice == "8":
            if pma >= 45:
                print("Vous frapper le point faible de l'enemi et lui détruisez 35 de bouclier")
                esh -= 35
                if esh < 0:
                    esh = 0
            else:
                print("Pas assez de magie pour fracturer le bouclier adverse")
            input("Appuyez sur Entrée pour continuer...")
            return False
        

        elif spell_choice == "9":
            print("Retour au choix des actions")
            time.sleep(1)
            return False  # => pas d'action effectuée, pas de fin de tour
        else:
            print("Choix invalide.")
            time.sleep(1)
            
            
        return True # tres important.

def focus(attacker_name):
    global ppv, psh, pma, focus_streak, last_player_action, combo_streak
    clear_console()

    last_player_action = "focus"
    
    if last_player_action == "focus":
        focus_streak += 1
    else:
        focus_streak = 1  # remettre à 1 si on vient de commencer un nouveau focus

    combo_streak = combo_streak + 1 if last_player_action == "defend" else 0

    if focus_streak == 2:
        print("Vous commencez à avoir de la peine à vous concentrer")
        pma += 10
    elif focus_streak > 3:
        print("Vous êtes déconcentré.")
    else:
        pma += 15
        psh += 5
        ppv += 5
        print(f"{attacker_name} se concentre pour récupérer 15 de magie et reprend légèrement ses forces.")

    return True

 
    
def counterattack(player_name):
    global last_player_action
    print(f"{player_name} adopte une posture défensive, prêt à contre-attaquer !")
    last_player_action = "counter"
    input("Appuyez sur Entrée pour continuer...")
    return True

def round(player_name):
    global last_player_action
    global ppv, psh, pma  # joueur
    global epv, esh, ema  # ennemi
    global giga_random_mode
    global training

    while ppv > 0 and epv > 0:
        clear_console()
        player_did_something = False
        player_action = input(
            "\033[33m==================== Votre tour ===================\n\033[0m"
            "Choisissez une action:\n\033[0m"
            "\033[31m1: Attaque\n\033[0m"
            "\033[94m2: Défense\n\033[0m"
            "\033[35m3: Envoyer un sort\n\033[0m"
            "\033[95m4: Focus\n\033[0m"
            "\033[91m5: Contre-Attaquer\n\033[0m"
            "\033[33m===================================================\n\033[0m"
        )
        clear_console()

        if player_action == "1":
            attack(player_name)
            last_player_action = "attack"
            player_did_something = True

        elif player_action == "2":
            player_did_something = defend(player_name)
            if player_did_something:
                last_player_action = "defend"

        elif player_action == "3":
            player_did_something = cast_spell(player_name)
            if player_did_something:
                last_player_action = "spell"

        elif player_action == "4":
            focus(player_name)
            last_player_action = "pass"
            player_did_something = True

        elif player_action == "5":
            player_did_something = counterattack(player_name)

        else:
            print("Veuillez choisir une action valable.")
            input("Appuyez sur Entrée pour continuer...")
            continue
        
        if effects.get("affaiblissement"):
            pma -= 5
            print("5 points de votre magie ont étés siphonnés.")

        # Effet Giga Random après l'action du joueur
        if player_did_something and giga_random_mode:
            ppv, psh, pma = random.randint(10, 200), random.randint(0, 100), random.randint(0, 200)
            # globals ! (pas de variables locales qui masquent)
            epv, esh, ema = random.randint(10, 200), random.randint(0, 100), random.randint(0, 200)
            print("\nLe bouffon joue un mauvais tour...")
            print(f"Joueur -> PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
            print(f"{name} -> PV: {epv} | Bouclier: {esh} | Magie: {ema}")
            input("\nAppuyez sur Entrée pour continuer...")

        # Tour ennemi
        if player_did_something:
            if training == 1:
                input("Appuyez sur Entrée pour continuer...")
                continue
            else:
                enemy_turn()

def show_player_stats():
    global ppv, psh, pma
    print("\n\nVos stats:")
    print(f"PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
    input("Appuyez sur Entrée pour continuer...")
    clear_console()

def show_enemy_stats():
    global epv, esh, ema
    print("\n\nStats de l'ennemi:")
    print(f"PV: {epv} | Bouclier: {esh} | Magie: {ema}")
    input("Appuyez sur Entrée pour continuer...")
    clear_console()
#====================================================================================================================================================================================================================================

class StatsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Statistiques du combat")
        self.geometry("480x360")
        self.resizable(False, False)
        self.configure(bg="#1c1c1c")
        # --- Styles généraux ---
        self.style_label = {"fg": "white", "bg": "#1c1c1c", "font": ("Consolas", 12)}

        # --- Cadre Joueur ---
        frame_joueur = tk.LabelFrame(self, text=" Joueur ", fg="#00FF7F", bg="#1c1c1c", font=("Helvetica", 12, "bold"), bd=2, relief="groove")
        frame_joueur.pack(fill="x", padx=10, pady=5)

        self.label_pv = tk.Label(frame_joueur, **self.style_label)
        self.label_psh = tk.Label(frame_joueur, **self.style_label)
        self.label_pma = tk.Label(frame_joueur, **self.style_label)

        self.label_pv.pack(anchor="w", padx=10)
        self.label_psh.pack(anchor="w", padx=10)
        self.label_pma.pack(anchor="w", padx=10)

        # --- Cadre Ennemi ---
        frame_ennemi = tk.LabelFrame(self, text= name , fg="#FF6347", bg="#1c1c1c", font=("Helvetica", 12, "bold"), bd=2, relief="groove")
        frame_ennemi.pack(fill="x", padx=10, pady=5)

        self.label_epv = tk.Label(frame_ennemi, **self.style_label)
        self.label_esh = tk.Label(frame_ennemi, **self.style_label)
        self.label_ema = tk.Label(frame_ennemi, **self.style_label)

        self.label_epv.pack(anchor="w", padx=10)
        self.label_esh.pack(anchor="w", padx=10)
        self.label_ema.pack(anchor="w", padx=10)

        # --- Cadre Description avec scrollbar ---
        frame_desc = tk.Frame(self, bg="#1c1c1c")
        frame_desc.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_desc)
        scrollbar.pack(side="right", fill="y")

        self.text_description = tk.Text(frame_desc, wrap="word", fg="lightgray", bg="#1c1c1c",
                                        font=("Arial", 10, "italic"), yscrollcommand=scrollbar.set,
                                        relief="flat", state="disabled")
        self.text_description.pack(fill="both", expand=True)

        scrollbar.config(command=self.text_description.yview)

        # Lancer la mise à jour
        self.update_stats()

    def update_stats(self):
        self.label_pv.config(text=f"PV: {ppv}")
        self.label_psh.config(text=f"Bouclier: {psh}")
        self.label_pma.config(text=f"Magie: {pma}")


        self.label_epv.config(text=f"PV: {epv}")
        self.label_esh.config(text=f"Bouclier: {esh}")
        self.label_ema.config(text=f"Magie: {ema}")

        self.update_description()
        self.after(500, self.update_stats)

    def update_description(self):
        description = f"\"L'épéiste possède {ppv} PV, {psh} bouclier et {pma} points de magie.\n"
        description += f"\"{name} a {epv} PV, {esh} bouclier et {ema} points de magie.\n\n"
        if name == "Chef de Guerre Gobelin":
            description += "Dans le donjon, les murs sont parfois friables, et caché sous les murs, des kilomètres de tunnels gobelins sont creusés. Leur chef? C'est le chef de guerre, un combattant agile, rapide et rusé, il serait proche du roi des gobelins."
        elif name == "Combattant Orc":
            description += "L'Orc est un combattant redoutable, pendant des années dans le donjon ce féroce Orc a gagné bataille sur batailles et s'est forgé un nom dans tout le continent. Il vous fixe avec haine, il n'a dans la tête que colère et violence. C'est a se demander comment il a pu en arriver la."
        elif name == "Le Nécromancien":
            description += "Le nécromancien depuis de millénaires veille a ce que les morts restent morts, et que tout ceux qui pénètre le donjons y fassent partie. Il serait le disciple d'un seigneur des ténèbres. Et l'idolâtre comme dans une secte."
        elif name == "Le Seigneur des Ténèbres":
            description += "Père de tous les maux, il est l'une des créatures les plus redoutées de ce monde, la légende racconte qu'il aurait vaincu le fils d'un dieu et l'aurait enfermé dans le donjon jusqu'à la folie. Le vaincre signifierait la fin du grand reigne des ténèbres et la libération des âmes torturées du donjon."
        elif name == "Le fou":
            description += "Le fou est un personnage mystérieux, il erre dans le donjon, parlant à voix haute et riant de manière incontrôlable. Sa force est paradoxalement surhumaine et son intelligence est hors du commun. Derrière ses yeux ensanglantés, on peut encore y apercevoir brièvement une lueur, au fond du tunel."
        elif name == "Banerask le vilain":
            description += "Banerask le vilain était autrefois l'homme le plus cruel de son village, par conséquent, les habitans l'ont jeté dans le donjon pour le punir de ses cruel actes. Il est devenu encore plus vilain et jure d'éliminer le prochain passant."
        elif name == "le joker":
            description += "Le joker est un personnage imprévisible, il apparaît dans le donjon sans prévenir et sème le chaos. Ses attaques sont aléatoires et il aime jouer avec ses adversaires. Il est accésoirement assez drôle et ne semble pas avoir d'envie de tuer."
        elif name == "Sorcier Squelette":
            description += "Le sorcier squelette est un ancien mage qui a été maudit et transformé en squelette. Il sert le Seigneur des ténèbres en faisant le garde dans les couloirs sinistres du donjon. Des rumeurs circulent comme quoi il sortirait de temps en temps pour brûler des villages et terroriser la population."
        elif name == "L'archimage de l'ombre":
            description += "L'archimage de l'ombre est un puissant sorcier ayant pactisé avec les forces obscures. Il utilise sa magie pour contrôler les ombres. Il serait une âme damnée, cherchant la rédemption auprès du seigneur des ténèbres. Malgré cela, personne ne sait qui se cache réellent derrière son grand chapeau."
        elif name == "La Faucheuse":
            description += "La faucheuse, une entité si puissante que la voir signifie la mort imminente."
        elif name == "Le Slime visqueux":
            description += "Le Slime visqueux est une créature étrange et gélatineuse, il provient surement du labo au sous-sol. Sous sa masse gélatineuse se cache un cervau de la taille d'une noix, l'atteindre n'est pas une tâche facile"
        elif name == "Le Minautaure":
            description += "Après avoir vaincu le monstre le plus puissant du donjon, l'épéiste à pris beaucoup d'expérience en combat et a décider d'aller chasser les derniers monstres qui terrifient ce monde. Le premier sur la liste est le minautaure, une chimère féroce habitant au fond du grand labyrinthe."
        elif name == "Le Stalker":
            description += "Caché au fond de la forêt dense dans les aléentours de la capitale se cache le stalker: un spectre surpuissant capable de comprimer les os de tous les malheureux passants. Il a été banni dans cet endroit il y a longtemps par les dieux."
        elif name == "L'Architecte":
            description += "Pendant que l'épéiste racourcit la liste des plus grands monstres de ce monde. Un observa ce périple depuis le début: l'architecte, l'esclave ayant construit le donjon de ses propres mains. Ayant cédé a sa soif de liberté il a essayé de s'enfuir mais fut retrouvé par les dieux et son corp fut scélé dans ce lieux a tout jamais. On dit qu'il a tellement entrainé son esprit qu'il est maintenant devenu omniscient."
        elif name == "Le Fou Condamné":
            description += "Le Fou après son combat dans le donjon a finalement sombré irreversiblement dans les ténèbres. Il a absorbé la puissance de tous lesmonstres défunts jus'qu ici. Il est devenu inarrêtable et a réussi a décidé de se venger de tous ceux qui on blessé des habitants du donjon. A commencer par l'épéiste. Il est insurmontable et sa force dépasse maintenant bien celle d'un dieux"
        elif name == challenge["name"]:
            description += challenge["description"]
        elif name == "Bim le mannequin":
            description += "Bim le mannuequin, (Frère de 'Bam le sac de frappe' et de 'Boom la punching bag') passe sa journée a se faire frapper dans le dojo de la montage. L'épéiste, au top de sa forme va s'y entraîner pendant son temps libre"
            
            
            
        # insère le texte dans la zone scrollable
        self.text_description.config(state="normal")
        self.text_description.delete("1.0", tk.END)  # vider avant réécriture
        self.text_description.insert(tk.END, description)
        self.text_description.config(state="disabled")

#============================================================================================= STORY MODE ===========================================================================================================================
from map_generator import generate_structured_map

# --- couleurs ---

DARK_GRAY = "\033[38;5;239m"
RESET = "\033[0m"

TILE_COLORS = {
    "#": YELLOW,
    "▇": BLACK,
    "=": YELLOW,
    "*": BLUE,
    "▉": GRAY,
    "s": DARK_GRAY,   # <- ombre
    ",": GREEN,
    "·": GREEN,
    "E": RED,
    "C": RESET,
    "%": PURPLE,
    "8": RED
}

import shutil

def get_terminal_size():
    cols, rows = shutil.get_terminal_size()
    return cols, rows

def start_story_mode():
    global ppv, psh, pma, epv, esh, ema, item_slot1, item_slot2, item_1
    os.system("mode con: cols=140 lines=40")
    def new_map():
        return [list(row) for row in generate_structured_map(140, 40)]

    maps = [new_map() for _ in range(3)]
    story_map = random.choice(maps)
    player_pos = [5, 5]

    def move_cursor(y, x):
        sys.stdout.write(f"\033[{y+1};{x+1}H")
        sys.stdout.flush()

    def draw_full_map():
        sys.stdout.write("\033[H\033[J")
        for y, line in enumerate(story_map):
            row = ""
            for x, char in enumerate(line):
                if [y, x] == player_pos:
                    row += f"{TILE_COLORS['8']}8{RESET}"
                else:
                    display_char = "▉" if char == "s" else char
                    color = TILE_COLORS.get(char, RESET)
                    row += f"{color}{display_char}{RESET}"
            print(row)
            
    def draw_tile(y, x, char):
        move_cursor(y, x)
        display_char = "▉" if char == "s" else char
        color = TILE_COLORS.get(char, RESET)
        sys.stdout.write(f"{color}{display_char}{RESET}")
        sys.stdout.flush()


    def load_new_map():
        nonlocal story_map, player_pos
        story_map = new_map()
        player_pos = [5, 5]
        draw_full_map()

    def move_player(dx, dy):
        new_y = player_pos[0] + dy
        new_x = player_pos[1] + dx
        if 0 <= new_y < len(story_map) and 0 <= new_x < len(story_map[0]):
            if story_map[new_y][new_x] not in ["▇", "*"]:
                # efface ancienne position
                draw_tile(player_pos[0], player_pos[1], story_map[player_pos[0]][player_pos[1]])

                # update position
                player_pos[0] = new_y
                player_pos[1] = new_x
                # dessine joueur
                draw_tile(player_pos[0], player_pos[1], "8")
                # check event
                tile = story_map[new_y][new_x]
                if tile == "%":
                    load_new_map()
                elif tile == "C":
                    print()

    # =================== BOUCLE ===================
    sys.stdout.write("\033[?25l")  # cache le curseur
    sys.stdout.flush()

    try:
        draw_full_map()
        while True:
            key = msvcrt.getch().decode("utf-8").lower()
            time.sleep(0.07)
            if key == "w":
                move_player(0, -1)
            elif key == "s":
                move_player(0, 1)
            elif key == "d":
                move_player(1, 0)
            elif key == "a":
                move_player(-1, 0)
            elif key == "q":
                move_cursor(len(story_map)+2, 0)
                print("Tu quittes le mode histoire...")
                break
    finally:
        sys.stdout.write("\033[?25h")  # réaffiche curseur
        sys.stdout.flush()

#====================================================================================================================================================================================================================================

if __name__ == "__main__":
    main_menu()