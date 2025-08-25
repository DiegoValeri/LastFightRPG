import os
import time
import random
import threading
import tkinter as tk
import time

os.system("")

attack_streak = 0  # Compteur de coups consécutifs
defend_streak = 0
combo_streak = 0   # alterner attaque/défense
player_max_pv = 0
enemy_max_pv = 0
enemy_special_cd = 0  # cooldown du spécial ennemi (en tours ennemis)

# === Codes couleurs ANSI ===

import re, sys, os, builtins

# Active (un peu) l’ANSI sous Windows
if os.name == "nt":
    try:
        os.system("")  # suffit souvent sur Windows 10+
    except Exception:
        pass

# Codes ANSI
RESET  = "\033[0m"
BLUE   = "\033[94m"   # Bouclier
RED    = "\033[91m"   # Dégâts
PINK   = "\033[95m"   # PV (rose / magenta clair)
PURPLE = "\033[35m"   # Magie (violet)
GREEN = "\033[32m"    # PV vert
YELLOW = "\033[33m" #Jaune pour la charte de difficulté

# Option pour couper la couleur si besoin
USE_COLORS = True


def colorize(text: str) -> str:
    if not USE_COLORS:
        return text
    # Remplacements mot entier, sensibles à la casse
    text = re.sub(r"\b[Bb]ouclier\b",   f"{BLUE}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Dd]effence\b",   f"{BLUE}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Dd]égâts\b", f"{RED}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Aa]ttaque\b",    f"{RED}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Pp][Vv]\b",  f"{GREEN}\\g<0>{RESET}", text)
    text = re.sub(r"\b[Mm]agie\b",  f"{PURPLE}\\g<0>{RESET}", text)
    return text

# Sauvegarde du print d’origine pour éviter la récursion
_original_print = print

def cprint(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
    # Concatène les args comme le print natif
    msg = sep.join(map(str, args))
    msg = colorize(msg)
    _original_print(msg, end=end, file=file, flush=flush)

# Remplace globalement print par cprint
builtins.print = cprint

# =================== Variables globales ===================
ppv = psh = pma = 0
name = ""
epv = esh = ema = 0
last_player_action = None  # Mémoire de la dernière action du joueur

# =================== Utilitaires ===================
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# =================== Configuration du mode ===================

giga_random_mode = False

#====================================================================










# =================== Fenêtre des stats ===================

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
        frame_ennemi = tk.LabelFrame(self, text=" Ennemi ", fg="#FF6347", bg="#1c1c1c", font=("Helvetica", 12, "bold"), bd=2, relief="groove")
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
        elif name == "La faucheuse":
            description += "La faucheuse, une entité si puissante que la voir signifie la mort imminente."
        elif name == "Le Slime visqueux":
            description += "Le Slime visqueux est une créature étrange et gélatineuse, il provient surement du labo au sous-sol. Sous sa masse gélatineuse se cache un cervau de la taille d'une noix, l'atteindre n'est pas une tâche facile"

        
        # insère le texte dans la zone scrollable
        self.text_description.config(state="normal")
        self.text_description.delete("1.0", tk.END)  # vider avant réécriture
        self.text_description.insert(tk.END, description)
        self.text_description.config(state="disabled")




def setup_characters():
    global ppv, psh, pma, name, epv, esh, ema  # <-- déclaration global tout en haut
    global giga_random_mode
    
    while True:
        clear_console()
        print("=== Menu principal ===")
        print("1 - Modes classiques")
        print("2 - Modes bonus")
        print("q - Quitter le jeu")
        print("======================")
        main_choice = input("\nEntrez votre choix : ")

        if main_choice == "1":
            # === MODES CLASSIQUES ===
            while True:
                clear_console()
                print("=== Choisissez un mode classique ===")
                print("\033[32m1 - Facile\033[0m")
                print("\033[32m1.5 - Simple\033[0m")
                print("\033[32m2 - Normal\033[0m")
                print("\033[33m2.5 - Intermédiaire\033[0m")
                print("\033[33m3 - Difficile\033[0m")
                print("\033[91m3.5 - Terrible\033[0m")
                print("\033[91m4 - Atroce\033[0m")
                print("\033[91m4.5 - Hardcore\033[0m")
                print("b - Retour")
                print("====================================")

                choice = input("\nEntrez le numéro du mode souhaité : ")

                if choice == "1":
                    ppv, psh, pma = 40, 20, 25
                    name = "Chef de Guerre Gobelin"
                    epv, esh, ema = 80, 20, 20
                    break
                elif choice == "1.5":
                    ppv, psh, pma = 45, 20, 25
                    name = "Le Slime visqueux"
                    epv, esh, ema = 100, 20, 30
                    break
                elif choice == "2":
                    ppv, psh, pma = 50, 20, 30
                    name = "Sorcier Squelette"
                    epv, esh, ema = 110, 30, 30
                    break
                elif choice == "2.5":
                    ppv, psh, pma = 60, 20, 30
                    name = "Combattant Orc"
                    epv, esh, ema = 125, 30, 35
                    break
                elif choice == "3":
                    ppv, psh, pma = 70, 25, 30
                    name = "Le Nécromancien"
                    epv, esh, ema = 140, 35, 45
                    break
                elif choice == "3.5":
                    ppv, psh, pma = 80, 30, 30
                    name = "L'archimage de l'ombre"
                    epv, esh, ema = 160, 40, 60
                    break
                elif choice == "4":
                    ppv, psh, pma = 85, 30, 25
                    name = "Le Seigneur des Ténèbres"
                    epv, esh, ema = 190, 50, 80
                    break
                elif choice == "4.5":
                    ppv, psh, pma = 90, 35, 20
                    name = "La faucheuse"
                    epv, esh, ema = 210, 55, 100
                    break
                elif choice.lower() == "b":
                    break
                else:
                    print("Veuillez choisir un nombre.")
                    input("Appuyez sur Entrée pour réessayer...")
            else:
                continue
            break  # Sortir du menu principal une fois un mode choisi

        elif main_choice == "2":
            # === MODES BONUS ===
            while True:
                clear_console()
                print("=== Choisissez un mode bonus ===")
                print("1 - Bac à sable")
                print("2 - La étrange trouvaille")
                print("3 - Randomiser")
                print("4 - Giga Randomiser")
                print("b - Retour")
                print("================================")

                choice = input("\nEntrez le numéro du mode bonus : ")

                if choice == "1":
                    clear_console()
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


                elif choice.lower() == "banerask le vilain":
                    print("...Tu n'es pas censé être là...")
                    time.sleep(2)
                    print("Une vilaine aura gèle tes os.")
                    ppv, psh, pma = 40, 25, -10
                    name = "Banerask le vilain"
                    epv, esh, ema = 20, 777, 70
                    time.sleep(1)
                    break

                elif choice.lower() == "b":
                    exit()
            else:
                continue
            break  # Sortir du menu principal une fois un mode choisi

        elif main_choice.lower() == "q":
            exit()
        else:
            print("Veuillez choisir un nombre.")
            input("Appuyez sur Entrée pour réessayer...")
        # Après avoir fixé ppv/psh/pma/epv/esh/ema
        global player_max_pv, enemy_max_pv
        player_max_pv = ppv
        enemy_max_pv  = epv

        
    # === Affichage final avant le jeu ===
    clear_console()
    print("=== Personnages configurés ===")
    print(f"Joueur  - PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
    print(f"{name} - PV: {epv} | Bouclier: {esh} | Magie: {ema}")
    input("\nAppuyez sur Entrée pour commencer le combat...")
    clear_console()



# Efface la console pour un affichage propre
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def enemy_attack():
    global ppv, psh, epv, esh, name, last_player_action

    print(f"{name} attaque le joueur !")
    damage = random.randint(13, 24)

    if last_player_action == "counter":
        # Le joueur contre-attaque
        print("L'épéeiste contre attaque!")
        reduced_damage = max(0, damage - psh)  # dégâts réduits par le bouclier
        ppv -= reduced_damage

        # Riposte : dégâts renvoyés à l’ennemi (ici 50% du bouclier)
        counter_damage = int(psh * 0.5)
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
        dmg = random.randint(18, 28)
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

#^^^^^^^^^^^^^ Gère le tour de l'ennemi, en fonction de la dernière action du joueur.


# Attaque basique, inflige des dégâts à l'ennemi
# compteur d'attaques consécutives

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
    global epv, esh, attack_streak, defend_streak, combo_streak, last_player_action

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

    last_player_action = "attack"
    input("Appuyez sur Entrée pour continuer...")


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
# Menu des sorts, permet de choisir un sort à lancer
def cast_spell(attacker_name):
    global epv, ppv, pma, esh, ema
    while True:
        clear_console()
        print(f"{attacker_name} choisit quel sort lancer")
        spell_choice = input(
"---------------------------------------------------\n"
"1: Soin [25 Magie] (Restaure 20 PV)\n"
"2: Sacrifice [20 PV] (Ajoute +50% de magie, cappé à 190)\n"
"3: Oblivion [50 Magie] (Dégâts: PV du joueur / 2)\n"
"4: Boule de feu [15 Magie] (13-18 dégâts, traverse le bouclier)\n"
"5: Mur magique [15 Magie] (Ajoute 15 Shield)\n"
"6: Croc de vampire [25 Magie] (Draine 15 PV à l’ennemi)\n"
"7: Chaîne du Chaos [30 Magie] (Effet aléatoire)\n"
"8: Retour\n"
"---------------------------------------------------\n"
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
                damage = random.randint(13, 18)
                epv -= damage
                print(f"Tu lances une Boule de Feu ! {name} perd {damage} PV. PV ennemi : {epv}")
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
        
                pma -= 50
            else:
                print("Pas assez de magie pour lancer Oblivion.")
            input("Appuyez sur Entrée pour continuer...")
            return False
#OBLIVION


        elif spell_choice == "8":
            print("Retour au choix des actions")
            time.sleep(1)
            return False  # => pas d'action effectuée, pas de fin de tour
        else:
            print("Choix invalide.")
            time.sleep(1)

#FOCUS//
def focus(attacker_name):
    global ppv, psh, pma
    clear_console()
    print(f"{attacker_name} se concentre pour récupérer 15 de magie.")
    pma += 15
    psh += 5
    
def counterattack(player_name):
    global last_player_action
    print(f"{player_name} adopte une posture défensive, prêt à contre-attaquer !")
    last_player_action = "counter"
    input("Appuyez sur Entrée pour continuer...")
    return True


def resolve_enemy_attack(enemy_name, enemy_damage):
    global ppv, epv, psh, last_player_action

    if last_player_action == "counter":
        # ✅ contre-attaque active
        print(f"{enemy_name} attaque, mais épéiste contre-attaque !")
        
        # Le joueur subit moins de dégâts
        reduced_damage = max(0, enemy_damage - psh)  
        ppv -= reduced_damage
        
        # L’ennemi prend un retour de dégâts (basé sur la défense ou force du joueur)
        counter_damage = int(psh * 0.5)
        epv -= counter_damage
        
        print(f"Joueur subit {reduced_damage} dégâts et renvoie {counter_damage} dégâts !")
        
        # Réinitialisation pour éviter que ça reste actif tout le combat
        last_player_action = None
    else:
        # ✅ pas de contre-attaque → dégâts normaux
        ppv -= enemy_damage
        print(f"{enemy_name} inflige {enemy_damage} dégâts à l'épéiste !")



# Gère le tour du joueur, demande une action et exécute la fonction correspondante

def round(player_name):
    global last_player_action
    global ppv, psh, pma  # joueur
    global epv, esh, ema  # ennemi
    global giga_random_mode

    while ppv > 0 and epv > 0:
        clear_console()
        player_did_something = False
        player_action = input(
            "------------------- Votre tour -------------------\n"
            "Choisissez une action:\n"
            "1: Attaque\n"
            "2: Défense\n"
            "3: Envoyer un sort\n"
            "4: Focus\n"
            "5: Contre-Attaquer\n"
            "---------------------------------------------------\n"
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
            print("Veuillez choisir une action valable. Écrivez help pour plus d'infos.")
            input("Appuyez sur Entrée pour continuer...")
            continue

        # Effet Giga Random après l'action du joueur
        if player_did_something and giga_random_mode:
            ppv, psh, pma = random.randint(10, 200), random.randint(0, 100), random.randint(0, 200)
            # globals ! (pas de variables locales qui masquent)
            epv, esh, ema = random.randint(10, 200), random.randint(0, 100), random.randint(0, 200)
            print("\nLe bouffon joue un mauvais tour...")
            print(f"Joueur -> PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
            print(f"{name} -> PV: {epv} | Bouclier: {esh} | Magie: {ema}")
            input("\nAppuyez sur Entrée pour continuer...")

        # Fin immédiate si l’ennemi est mort
        if epv <= 0:
            print("L'ennemi a été vaincu !")
            break

        # Tour ennemi
        if player_did_something:
            if enemy_turn():
                break



# Affiche les stats du joueur
def show_player_stats():
    global ppv, psh, pma
    print("\n\nVos stats:")
    print(f"PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
    input("Appuyez sur Entrée pour continuer...")
    clear_console()

# Affiche les stats de l'ennemi
def show_enemy_stats():
    global epv, esh, ema
    print("\n\nStats de l'ennemi:")
    print(f"PV: {epv} | Bouclier: {esh} | Magie: {ema}")
    input("Appuyez sur Entrée pour continuer...")
    clear_console()




# =================== Lancement du jeu ===================
if __name__ == "__main__":
    setup_characters()

    # UI Tkinter dans le thread principal
    app = StatsWindow()

    # Boucle de jeu dans un thread à part (pour ne pas bloquer l'UI)
    def game_loop():
        round("Joueur")

    threading.Thread(target=game_loop, daemon=True).start()

    #Démarre l'UI (dans le thread principal)
    app.mainloop()
