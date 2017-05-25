#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk


class vuePrincipale(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        panneau_vue_principale = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        liste_vue_principale = tk.Listbox(panneau_vue_principale)

        liste_vue_principale.insert(1, "En ce moment")
        liste_vue_principale.insert(2, "A acheter")
        liste_vue_principale.insert(3, "A voir")
        liste_vue_principale.insert(4, "ma collection")

        panneau_vue_principale.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=2, padx=2)
        panneau_vue_principale.add(liste_vue_principale)
        panneau_vue_principale.pack()


if __name__ == "__main__":
    vuePrincipaleFrame = tk.Tk()
    vuePrincipale(vuePrincipaleFrame).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    vuePrincipaleFrame.mainloop()
