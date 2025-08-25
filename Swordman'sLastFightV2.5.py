import random
import time
import tkinter as tk
import os
import threading

# Définition des stats du joueur et de l'ennemi en variables globales
global ppv, psh, pma, name, epv, esh, ema


epv = random.randint(40, 60)
esh = random.randint(10, 25)
ema = random.randint(20, 50)

last_player_action = None  # Mémoire de la dernière action du joueur


def setup_characters():
    global ppv, psh, pma, name, epv, esh, ema  # <-- déclaration global tout en haut

    while True:
        clear_console()
        print("=== Menu principal ===")
        print("1 - Modes classiques")
        print("2 - Modes bonus")
        print("q - Quitter le jeu")
        main_choice = input("Entrez votre choix : ")

        if main_choice == "1":
            # === MODES CLASSIQUES ===
            while True:
                clear_console()
                print("=== Choisissez un mode classique ===")
                print("1 - Facile")
                print("1.5 - Simple")
                print("2 - Normal")
                print("2.5 - Intermédiaire")
                print("3 - Difficile")
                print("3.5 - Terrible")
                print("4 - Atroce")
                print("4.5 - Hardcore")
                print("b - Retour")

                choice = input("Entrez le numéro du mode souhaité : ")

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
                    print("Choix invalide.")
                    time.sleep(2)
            else:
                continue
            break  # Sortir du menu principal une fois un mode choisi

        elif main_choice == "2":
            # === MODES BONUS ===
            while True:
                clear_console()
                print("=== Choisissez un mode bonus ===")
                print("5 - Bac à sable")
                print("6 - La étrange trouvaille")
                print("7 - Randomiser")
                print("b - Retour")

                choice = input("Entrez le numéro du mode bonus : ")

                if choice == "5":
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

                elif choice == "6":
                    ppv, psh, pma = 20, 20, 10
                    name = "Le fou"
                    epv, esh, ema = 200, 100, 1000
                    break

                elif choice == "7":
                    print("Alea jacta est...")
                    time.sleep(1)
                    ppv, psh, pma = random.randint(10, 150), random.randint(10, 150), random.randint(10, 110)
                    name = "le joker"
                    epv, esh, ema = random.randint(10, 150), random.randint(10, 150), random.randint(10, 110)
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
                    break
                else:
                    print("Choix invalide.")
                    time.sleep(2)
            else:
                continue
            break  # Sortir du menu principal une fois un mode choisi

        elif main_choice.lower() == "q":
            print("À bientôt, aventurier !")
            exit()
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou q.")
            time.sleep(2)

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
    global ppv, psh
    print(f"{name} attaque le joueur !")
    damage = random.randint(13, 24)
    if psh > 0:
        psh -= damage
        print(f"{name} inflige {damage} points de dégâts. Bouclier du joueur restant : {psh}")
        if psh < 0:
            ppv += psh  # psh est négatif, donc on retire à ppv
            print(f"Le bouclier du joueur est brisé ! Le joueur perd {-psh} PV. PV restants : {ppv}")
            psh = 0
    else:
        ppv -= damage
        print(f"{name} inflige {damage} points de dégâts au joueur. PV restants : {ppv}")
    input("Appuyez sur Entrée pour continuer...")

def enemy_defend():
    global esh
    print(f"{name} se défend et gagne 10 points de bouclier. Bouclier actuel : {esh}")

def enemy_pass_turn():
    global epv, esh, ema
    print(f"{name} puise dans le déséspoir pour reprendre des forces.")
    epv += 10
    esh += 3
    ema += 5


def enemy_turn():
    global ppv, epv, esh, ema, last_player_action

    print("\n--- Tour de l'ennemi ---")
    input("Appuyez sur Entrée pour continuer...")
    # Réactions à l'action précédente du joueur
    if last_player_action == "attack":
        if epv <= 30:
            print(f"{name} est blessé après l'attaque, il cherche à se soigner.")
            enemy_pass_turn()
        elif esh <= 10:
            print(f"{name} tente de se proteger en urgence.")
            enemy_defend()
        else:
            print(f"{name} répond par une contre-attaque !")
            enemy_attack()

    elif last_player_action == "defend":
        if ema >= 20:
            print(f"{name} profite de la défense du joueur pour recharger.")
            enemy_pass_turn()
        else:
            print(f"{name} tente de casser la défense du joueur.")
            enemy_attack()

    elif last_player_action == "spell":
        print(f"{name} est déstabilisé par la magie, mais garde son sang-froid.")
        if epv < 25:
            enemy_defend()
        elif epv < 35:
            enemy_pass_turn()
        else:
            enemy_attack()

    elif last_player_action == "pass":
        print(f"{name} voit le joueur se reposer, c’est le moment de frapper.")
        enemy_attack()

    else:
        # Tour de début ou erreur, IA basique
        actions = ["attack"] * 3 + ["defend"] + ["pass"]
        action = random.choice(actions)
        if action == "attack":
            enemy_attack()
        elif action == "defend":
            enemy_defend()
        elif action == "pass":
            enemy_pass_turn()

    # Vérifie fin de partie
    if ppv <= 0:
        print("L'aventure de l'épéiste a pris fin brutalement, tué par " + name)
        time.sleep(9999)
    elif epv <= 0:
        print("L'épéiste a triomphé, " + name + " a été vaincu.")
        time.sleep(9999)

    return False
#^^^^^^^^^^^^^ Gère le tour de l'ennemi, en fonction de la dernière action du joueur.

# Attaque basique, inflige des dégâts à l'ennemi
def attack(attacker_name):
    print(f"{attacker_name} décide d'attaquer!")
    global epv, esh, ema
    damage = random.randint(15, 24)
    if esh > 0:
        esh -= damage
        print(f"{attacker_name} inflige {damage} points de dégâts à {name}. Bouclier restant: {esh}")
        if esh < 0:
            epv += esh  # esh est négatif, donc on retire à epv
            print(f"Le bouclier est brisé! {name} perd {-esh} points de vie. PV restant: {epv}")
            esh = 0
            input("Appuyez sur Entrée pour continuer...")
            return
    else:
        epv -= damage
        print(f"{attacker_name} inflige {damage} points de dégâts à {name}. PV restant: {epv}")
        input("Appuyez sur Entrée pour continuer...")
        return

# Défense temporaire, ajoute un bouclier
def defend(attacker_name):
    print(f"{attacker_name} décide de se défendre!")
    global psh
    if psh < 100:
        psh += 10
        print(f"{attacker_name} augmente son bouclier de 10 points. Bouclier actuel: {psh}")
        input("Appuyez sur Entrée pour continuer...")
        return True  # Action effectuée, revenir au menu
    else:
        print(f"{attacker_name} ne peut pas augmenter son bouclier car il est déjà à son maximum.")
        input("Appuyez sur Entrée pour continuer...")
        return False  # Action non effectuée, revenir au menu

# Menu des sorts, permet de choisir un sort à lancer
def cast_spell(attacker_name):
    global epv, ppv, pma, enemy_stun_next_turn, enemy_stunned, esh, ema
    while True:
        clear_console()
        print(f"{attacker_name} choisit quel sort lancer")
        spell_choice = input("---------------------------------------------------\n1: Soin [25 Magie] (Restaure 20 PV)\n2: Sacrifice [20 PV] (Ajoute +50% de magie, cappé a 190) \n3: Oblivion [50 Magie] (Dégâts: Nombre de PV du joueur/2.)\n4: Retour\n---------------------------------------------------\n")
        
        if spell_choice == "1":
            if pma >= 25:
                print(f"{attacker_name} lance Soin et récupère 20 PV.")
                ppv += 20
                if ppv > 100:
                    ppv = 100
                print(f"PV actuel: {ppv}")
                pma -= 25
            else:
                print("Pas assez de magie pour lancer Soin.")
            input("Appuyez sur Entrée pour continuer...")
            return True
#SOIN
        
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
                return True
            else:
                print("Pas assez de magie pour lancer le sort de magie.")
                input("Appuyez sur Entrée pour continuer...")
                return True
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
            return True
#OBLIVION


        elif spell_choice == "4":
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


# Gère le tour du joueur, demande une action et exécute la fonction correspondante
def show_help():
    clear_console()
    print("Aide - Actions disponibles :\n")
    print("1: Attaque - Inflige des dégâts à l'ennemi.")
    print("2: Défense - Ajoute du bouclier temporaire.")
    print("3: Envoyer un sort - Choix entre différents sorts.")
    print("4: Focus - Récupère 10 de magie")
    print("help: Affiche cette aide.")
    print("\nSi vous souhaitez jouer en mode difficile, veuillez fermer la fenêtre des stats.")
    input("\nAppuyez sur Entrée pour retourner au menu...")
    clear_console()


def round(player_name, enemy_name, epv, esh, ema):
    while True:
        clear_console()
        player_action = input("------------------- Votre tour -------------------\nChoisissez une action:\n1: Attaque\n2: Défense\n3: Envoyer un sort\n4: Focus\n---------------------------------------------------\n")
        clear_console()
        player_did_something = False

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
        
        elif player_action == "help":
            show_help()
            continue
        else:
            print("Veuillez choisir une action valable. Écrivez help pour plus d'infos.")
            input("Appuyez sur Entrée pour continuer...")
            continue

        # Fin du tour joueur seulement si action faite
        if player_did_something:
            if epv <= 0:
                print("L'ennemi a été vaincu !")
                break

            if enemy_turn():  # L'ennemi joue
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

# Classe pour la fenêtre des stats, affiche les stats du joueur et de l'ennemi
class StatsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stats")
        self.geometry("400x300")
        self.maxsize(400, 300)
        self.minsize(400, 300)
        self.configure(bg="black")
        
        # Stats du joueur
        self.label_pv = tk.Label(self, text="PV: ", fg="white", bg="black")
        self.label_psh = tk.Label(self, text="Bouclier: ", fg="white", bg="black")
        self.label_pma = tk.Label(self, text="Magie: ", fg="white", bg="black")
        
        # Stats de l'ennemi
        self.label_epv = tk.Label(self, text="PV: ", fg="white", bg="black")
        self.label_esh = tk.Label(self, text="Bouclier: ", fg="white", bg="black")
        self.label_ema = tk.Label(self, text="Magie: ", fg="white", bg="black")
        
        # Section des descriptions
        self.label_description = tk.Label(self, text="Description des personnages et modes", fg="white", bg="black", wraplength=350)
        
        # Placement des éléments dans la fenêtre
        tk.Label(self, text="--- Joueur ---", fg="white", bg="black").pack()
        self.label_pv.pack()
        self.label_psh.pack()
        self.label_pma.pack()
        tk.Label(self, text="--- Ennemi ---", fg="white", bg="black").pack()
        self.label_epv.pack()
        self.label_esh.pack()
        self.label_ema.pack()
        
        self.label_description.pack(pady=10)  # Ajoute un espace au-dessus de la description
        self.update_stats()

    def update_stats(self):
        self.label_pv.config(text=f"PV: {ppv}")
        self.label_psh.config(text=f"Bouclier: {psh}")
        self.label_pma.config(text=f"Magie: {pma}")
        self.label_epv.config(text=f"PV: {epv}")
        self.label_esh.config(text=f"Bouclier: {esh}")
        self.label_ema.config(text=f"Magie: {ema}")
        self.update_description()
        self.after(500, self.update_stats)  # Met à jour les stats toutes les 500 ms

    def update_description(self):
        # Mise à jour de la description en fonction des stats du joueur et de l'ennemi
        description = f"L'épéiste possède {ppv} PV, {psh} bouclier et {pma} points de magie.\n"
        description += f"{name} a {epv} PV, {esh} bouclier et {ema} points de magie.\n"

        # Ajouter des descriptions selon le mode choisi
        if name == "Chef de Guerre Gobelin":
            description += "Dans le donjon, les murs sont parfois friables, et caché sous les murs, des kilomètres de tunnels gobelins sont creusés. Leur chef? C'est le chef de guerre est un combattant agile, rapide et rusé."
        elif name == "Combattant Orc":
            description += "L'Orc est un combattant redoutable, pendant des années dans le donjon ce féroce Orc a gagné bataille sur batailles et s'est forgé un nom dans tout le continent."
        elif name == "Le Nécromancien":
            description += "Le nécromancien depuis de millénaires veille a ce que les morts restent morts, et que tout ceux qui pénètre le donjons y fassent partie"
        elif name == "Le Seigneur des Ténèbres":
            description += "Père de tous les maux, il est l'une des créatures les plus redoutées de ce monde, la légende racconte qu'il aurait vaincu le fils d'un dieu et l'aurait enfermé dans le donjon jusqu'à la folie."
        elif name == "Le fou":
            description += "Le fou est un personnage mystérieux, il erre dans le donjon, parlant à voix haute et riant de manière incontrôlable. Sa force est paradoxalement surhumaine."
        elif name == "Banerask le vilain":
            description += "Banerask le vilain était autrefois l'homme le plus cruel de son village, par conséquent, les habitans l'ont jeté dans le donjon pour le punir de ses cruel actes. Il est devenu encore plus vilain et jure d'éliminer le prochain passant."
        elif name == "le joker":
            description += "Le joker est un personnage imprévisible, il apparaît dans le donjon sans prévenir et sème le chaos. Ses attaques sont aléatoires et il aime jouer avec ses adversaires."
        elif name == "Sorcier Squelette":
            description += "Le sorcier squelette est un ancien mage qui a été maudit et transformé en squelette. Il utilise sa magie pour semer la terreur."
        elif name == "L'archimage de l'ombre":
            description += "L'archimage de l'ombre est un puissant sorcier ayant pactisé avec les forces obscures. Il utilise sa magie pour contrôler les ombres."
        elif name == "La faucheuse":
            description += "La faucheuse est une entité si puissante que l'on racconte que si on la voit, notre fin est imminente."
        elif name == "Le Slime visqueux":
            description += "Le Slime visqueux est une créature étrange et gélatineuse, il provient surement du labo au sous-sol."

        # Met à jour la description à afficher dans l'interface graphique
        self.label_description.config(text=description)


# Lancer la fenêtre des stats dans un thread séparé pour ne pas bloquer le jeu
def start_stats_window():
    stats_win = StatsWindow()
    stats_win.mainloop()

setup_characters()

threading.Thread(target=start_stats_window, daemon=True).start()

round("Joueur", name, epv, esh, ema)
