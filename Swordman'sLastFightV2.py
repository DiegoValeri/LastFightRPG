import random
import time
import tkinter as tk
import os
import threading

# Définition des stats du joueur et de l'ennemi en variables globales
global ppv, psh, pma, name, epv, esh, ema

ppv = 100
psh = 15
pma = 50


epv = random.randint(40, 60)
esh = random.randint(10, 25)
ema = random.randint(20, 50)


def setup_characters():
    global ppv, psh, pma, name, epv, esh, ema  # <-- déclaration global tout en haut

    while True:
        clear_console()
        print("=== Choisissez un mode de jeu ===")
        print("1 - Facile")
        print("2 - Normal")
        print("3 - Difficile")
        print("4 - Hardcore (Déconseillé)")
        print("5 - Bac à sable")
        print("6 - La étrange trouvaille")
        choice = input("Entrez le numéro du mode souhaité : ")

        if choice == "1":  # Facile
            ppv, psh, pma = 120, 30, 60
            name = "Chef de Guerre Gobelin"
            epv, esh, ema = 50, 10, 20
            break

        elif choice == "2":  # Normal
            ppv, psh, pma = 100, 20, 50
            name = "Combattant Orc"
            epv, esh, ema = 60, 15, 40
            break

        elif choice == "3":  # Difficile
            ppv, psh, pma = 80, 10, 20
            name = "Le Nécromancien"
            epv, esh, ema = 100, 30, 60
            break
        
        elif choice == "4":  # Hardcore
            ppv, psh, pma = 60, 5, 10
            name = "Le Seigneur des Ténèbres" 
            epv, esh, ema = 150, 50, 100
            print("Mode Hardcore activé! A vos risques et périls!")
            break
        
        elif choice == "6":  # Mode ???
            ppv, psh, pma = 20, 0, 10
            name = "Le fou"
            epv, esh, ema = 200, 100, 1000 
            break
        
        elif choice == "Banerask le vilain" or "banerask le vilain":  # Easter Egg
            ppv, psh, pma = 40, 25, -10
            name = "Banerask le vilain"
            epv, esh, ema = 20, 777, 70
            break
        
        elif choice == "5":  # Manuel
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

        else:
            print("Choix invalide. Veuillez entrer 1, 2, 3 , 4 ou 5... ?")
            time.sleep(2)

    # Afficher les stats choisies
    clear_console()
    print("=== Personnages configurés ===")
    print(f"Joueur  - PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
    print(f"{name} - PV: {epv} | Bouclier: {esh} | Magie: {ema}")
    input("\nAppuyez sur Entrée pour commencer le combat...")
    clear_console()
#^^^^^^^^^^^^^ Configure les stats du joueur et de l'ennemi selon le mode choisi.



# Efface la console pour un affichage propre
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def enemy_attack():
    global ppv, psh
    print(f"{name} attaque le joueur !")
    damage = random.randint(10, 20)
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
    if esh < 100:
        esh += 10
        print(f"{name} se défend et gagne 10 points de bouclier. Bouclier actuel : {esh}")
    else:
        print(f"{name} ne peut pas augmenter son bouclier, il est déjà au max.")
    input("Appuyez sur Entrée pour continuer...")

def enemy_pass_turn():
    global epv, esh, ema
    print(f"{name} passe son tour et se soigne.")
    if epv < 60:  # on suppose que l'ennemi n'a pas plus que 60 PV max
        soin = random.randint(5, 15)
        epv += soin
        epv = min(epv, 60)
        print(f"{name} récupère {soin} PV. PV actuel : {epv}")
    if esh < 100:
        esh += 5
        print(f"{name} récupère 5 points de bouclier. Bouclier actuel : {esh}")
    ema += 10
    print(f"{name} récupère 10 points de magie. Magie actuelle : {ema}")
    input("Appuyez sur Entrée pour continuer...")

    
    
    

# Attaque basique, inflige des dégâts à l'ennemi
def attack(attacker_name):
    print(f"{attacker_name} décide d'attaquer!")
    global epv, esh, ema
    damage = random.randint(10, 20)
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
    global epv, ppv, pma
    while True:
        clear_console()
        print(f"{attacker_name} choisit quel sort lancer")
        spell_choice = input("---------------------------------------------------\n1: Sommeil (Stun: 1 Tour)\n2: Soin (Restaure 20 PV)\n3: Oblivion (Dégâts: 110 - PV du joueur.)\n4: Retour\n---------------------------------------------------\n")
        
        if spell_choice == "1":
            print("Sort de sommeil pas encore implémenté.")
            input("Appuyez sur Entrée pour continuer...")
            return True
        
        elif spell_choice == "2":
            if pma >= 20:
                soin = 20
                ppv = min(100, ppv + soin)
                pma -= 20
                print(f"{attacker_name} lance Soin et récupère {soin} PV. PV actuel : {ppv}")
            else:
                print("Pas assez de magie pour Soin.")
            input("Appuyez sur Entrée pour continuer...")
            return True
        
        elif spell_choice == "3":
            if pma >= 50:
                damage = 90 - ppv
                if damage < 0:
                    damage = 0
            if esh > 0:
                esh -= damage
                print(f"{attacker_name} inflige {damage} points de dégâts à {name}. Bouclier restant: {esh}")
                if esh < 0:
                    epv += esh  # esh est négatif, donc on retire à epv
                    print(f"Le bouclier est brisé! {name} perd {-esh} points de vie. PV restant: {epv}")
                    esh = 0
                    input("Appuyez sur Entrée pour continuer...")
                    return



        elif spell_choice == "4":
            print("Retour au choix des actions")
            time.sleep(1)
            return False  # => pas d'action effectuée, pas de fin de tour

        else:
            print("Choix invalide.")
            time.sleep(1)

# Passe le tour du joueur, ne fait rien.
def pass_turn(attacker_name):
    print(f"{attacker_name} passe son tour et soigne!")
    global ppv, psh, pma
    if ppv < 100:
        soin = random.randint(5, 15)
        ppv += soin
        print(f"{attacker_name} récupère {soin} points de vie. PV actuel: {ppv}")
    if psh < 100:
        psh += 5
        print(f"{attacker_name} récupère 5 points de bouclier. Bouclier actuel: {psh}")
    pma += 10
    print(f"{attacker_name} récupère 10 points de magie. Magie actuelle: {pma}")
    input("Appuyez sur Entrée pour continuer...")

# Fonction pour le tour de l'ennemi
def enemy_turn():
    print("\n--- Tour de l'ennemi ---")
    action = random.choice(["attack", "defend", "pass"])
    if action == "attack":
        enemy_attack()
    elif action == "defend":
        enemy_defend()
    elif action == "pass":
        enemy_pass_turn()

    # Vérifier fin de partie
    if ppv <= 0:
        print("Vous avez été vaincu !")
        return True
    elif epv <= 0:
        print("L'ennemi a été vaincu !")
        return True
    return False


# Gère le tour du joueur, demande une action et exécute la fonction correspondante
def show_help():
    clear_console()
    print("Aide - Actions disponibles :\n")
    print("1: Attaque - Inflige des dégâts à l'ennemi.")
    print("2: Défense - Ajoute du bouclier temporaire.")
    print("3: Envoyer un sort - Choix entre différents sorts.")
    print("4: Passer son tour - Récupère PV, bouclier et magie.")
    print("help: Affiche cette aide.")
    print("\nSi vous souhaitez jouer en mode difficile, veuillez fermer la fenêtre des stats.")
    input("\nAppuyez sur Entrée pour retourner au menu...")
    clear_console()


def round(player_name, enemy_name, epv, esh, ema):
    while True:
        clear_console()
        player_action = input("------------------- Votre tour -------------------\nChoisissez une action:\n1: Attaque\n2: Défense\n3: Envoyer un sort\n4: Passer son tour\n---------------------------------------------------\n")
        clear_console()
        player_did_something = False

        if player_action == "1":
            attack(player_name)
            player_did_something = True
        elif player_action == "2":
            player_did_something = defend(player_name)
        elif player_action == "3":
            player_did_something = cast_spell(player_name)
        elif player_action == "4":
            pass_turn(player_name)
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
        # Mode Hardcore
        if epv == 150:
            description += "\nMode Hardcore activé! Bonne chance, vous en aurez besoin!"
        elif epv == 60:
            description += "\nMode Normal."
        elif epv == 100:
            description += "\nMode Difficile"
        elif epv == 50:
            description += "\nMode Facile"

        # Met à jour la description à afficher dans l'interface graphique
        self.label_description.config(text=description)


# Lancer la fenêtre des stats dans un thread séparé pour ne pas bloquer le jeu
def start_stats_window():
    stats_win = StatsWindow()
    stats_win.mainloop()

setup_characters()

threading.Thread(target=start_stats_window, daemon=True).start()

round("Joueur", name, epv, esh, ema)
