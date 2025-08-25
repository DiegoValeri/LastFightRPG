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

name = "Goblein"
epv = random.randint(40, 60)
esh = random.randint(10, 25)
ema = random.randint(20, 50)

#^^^^^^^importe les stats du joueur et de l'ennemi pour que le jeu puisse les utiliser partout.

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

#^^^^^^^^^^^Efface la console pour un affichage propre

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

#^^^^^^^^^^^^^^ Attaque basique, inflige des dégâts à l'ennemi

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
#^^^^^^^^^^^^^^ Défense temporaire, ajoute un bouclier

def cast_spell(attacker_name):
    while True:
        clear_console()
        print(f"{attacker_name} choisit quel sort lancer")
        spell_choice = input("---------------------------------------------------\n1: Sommeil (Stun: 1 Tour)\n2: Soin (Restaure 20 PV)\n3: Oblivion (Dégâts: 110 - PV du joueur.)\n4: Retour\n---------------------------------------------------\n")
        global epv, ppv, pma
        if spell_choice == "3":
            if pma < 20:
                print("Vous n'avez pas assez de magie pour lancer ce sort.")
                time.sleep(2)
                continue
            pma -= 30
            degats = max(0, 110 - ppv)
            print(f"Oblivion inflige {degats} points de dégâts à {name} !")
            epv -= degats
            print(f"{name} a maintenant {epv} points de vie.")
            time.sleep(2)
        clear_console()
        if spell_choice == "4":
            print("Retour au choix des actions")
            break

#^^^^^^^^^^^^Menu des sorts, permet de choisir un sort à lancer.

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
    


    
#^^^^^^^^^^^^^Passe le tour du joueur, ne fait rien.

def show_help():
    print("Voici les actions disponibles:\n1: Attaque - Lance une attaque contre l'ennemi.\n2: Défense - Se prépare à encaisser les coups.\n3: Envoyer un sort - Lancer un sort offensif ou défensif.\n4: Passer son tour - Ne rien faire pour ce tour.\nhelp: Afficher cette aide.\n Si vous souhaitez jouer en mode difficile, veuillez fermer la fenêtre des stats.")
    input("Tapez Entrée pour quitter la page d'aide...")
    clear_console()
    
#^^^^^^^^^^^^^Affiche l'aide pour les actions disponibles.

def round(player_name, enemy_name, epv, esh, ema):
    while True:
        clear_console()
        player_action = input("------------------- Votre tour -------------------\nChoisissez une action:\n1: Attaque\n2: Défense\n3: Envoyer un sort\n4: Passer son tour\n---------------------------------------------------\n")
        clear_console()
        if player_action == "1":
            attack(player_name)
        elif player_action == "2":
            defend(player_name)
        elif player_action == "3":
            cast_spell(player_name)
        elif player_action == "4":
            pass_turn(player_name)
        elif player_action == "help":
            show_help()
            continue
        else:
            print("Veuillez choisir une action valable. Écrivez help pour plus d'infos.")
            input("Appuyez sur Entrée pour continuer...")
            clear_console()
#^^^^^^^^^^^^^Gère le tour du joueur, demande une action et exécute la fonction correspondante.

def show_player_stats():
    global ppv, psh, pma
    print("\n\nVos stats:")
    print(f"PV: {ppv} | Bouclier: {psh} | Magie: {pma}")
    input("Appuyez sur Entrée pour continuer...")
    clear_console()
    
#^^^^^^^^^^^^^Affiche les stats du joueur.

def show_enemy_stats():
    global epv, esh, ema
    print("\n\nStats de l'ennemi:")
    print(f"PV: {epv} | Bouclier: {esh} | Magie: {ema}")
    input("Appuyez sur Entrée pour continuer...")
    clear_console()
    
#^^^^^^^^^^^^^Affiche les stats de l'ennemi.


class StatsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stats")
        self.geometry("300x180")
        self.maxsize(300, 180)
        self.minsize(300, 180)
        self.configure(bg="black")
        # Stats joueur
        self.label_pv = tk.Label(self, text="")
        self.label_psh = tk.Label(self, text="")
        self.label_pma = tk.Label(self, text="")
        # Stats ennemi
        self.label_epv = tk.Label(self, text="")
        self.label_esh = tk.Label(self, text="")
        self.label_ema = tk.Label(self, text="")
        # Placement
        tk.Label(self, text="--- Joueur ---").pack()
        self.label_pv.pack()
        self.label_psh.pack()
        self.label_pma.pack()
        tk.Label(self, text="--- Ennemi ---").pack()
        self.label_epv.pack()
        self.label_esh.pack()
        self.label_ema.pack()
        self.update_stats()

    def update_stats(self):
        self.label_pv.config(text=f"PV: {ppv}")
        self.label_psh.config(text=f"Bouclier: {psh}")
        self.label_pma.config(text=f"Magie: {pma}")
        self.label_epv.config(text=f"PV: {epv}")
        self.label_esh.config(text=f"Bouclier: {esh}")
        self.label_ema.config(text=f"Magie: {ema}")
        self.after(500, self.update_stats)

def start_stats_window():
    stats_win = StatsWindow()
    stats_win.mainloop()
    
#^^^^^^^^^^^^^Classe pour la fenêtre des stats, affiche les stats du joueur et de l'ennemi.

# Lance la fenêtre dans un thread séparé pour ne pas bloquer le jeu
threading.Thread(target=start_stats_window, daemon=True).start()

round("Joueur", name, epv, esh, ema)

#^^^^^^^^^^^^^Démarre le jeu en lançant le premier round.