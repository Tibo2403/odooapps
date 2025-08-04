# Odoo Apps – Modules communautaires pour Odoo 18

Ce dépôt rassemble une collection de modules communautaires pour Odoo 18 développés par **Odoo Mates**. Ils couvrent divers domaines tels que la comptabilité, la gestion budgétaire, les ressources humaines, et bien d’autres.

---

## 📦 Modules inclus

### Comptabilité

- **Accounting PDF Reports** : Rapports financiers prêts à l’emploi pour Odoo 18
- **Accounting Community** : Extensions comptables : rapports, immobilisations, budgets, paiements récurrents, relances clients, etc.
- **Assets Management** : Gestion et amortissement des actifs de l’entreprise
- **Budget Management** : Suivi des budgets et comparaison prévisionnel vs. réalisé
- **Cash/Day/Bank Book Reports** : Livre de caisse, livre de banque et journalier
- **Customer Follow Up Management** : Relance automatisée des clients en retard de paiement
- **Fiscal Year & Lock Date** : Gestion des exercices fiscaux et dates de verrouillage
- **Recurring Payment** : Création de paiements récurrents planifiés

### Ressources humaines

- **HR Payroll** : Module de paie pour l’édition communautaire d’Odoo 18
- **HR Payroll Accounting** : Intégration de la paie avec la comptabilité

### Divers

- **Remove Data** : Outils de nettoyage et réinitialisation de la base de données

---

## ⚙️ Installation

1. **Cloner** ce dépôt dans le chemin des modules d’Odoo 18 :
   ```bash
   git clone https://github.com/[votre-utilisateur]/odooapps.git
   ```

2. **Ajouter** le dossier cloné à la configuration d’Odoo, par exemple dans le fichier `odoo.conf` via l’option `addons_path` ou en utilisant `--addons-path` lors du lancement du serveur.

3. **Redémarrer** le serveur Odoo pour prendre en compte les nouveaux modules.

4. **Mettre à jour** la liste des applications depuis l’interface Odoo (mode développeur → *Mettre à jour la liste des applications*).

5. **Installer** les modules souhaités à partir du menu **Apps**.
