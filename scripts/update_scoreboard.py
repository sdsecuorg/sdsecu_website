import json
import requests
import os

def main():
    # Déterminer le dossier où se trouve ce script
    base_dir = os.path.dirname(__file__)
    
    # Forcer le chemin absolu propre vers la racine pour trouver membres.json
    membres_path = os.path.abspath(os.path.join(base_dir, '..', 'membres.json'))
    
    print(f"[*] Tentative de lecture du fichier : {membres_path}")
    
    # Si le fichier n'existe pas, on fait crasher proprement pour voir l'erreur sur GitHub
    if not os.path.exists(membres_path):
        raise FileNotFoundError(f"Erreur critique : Le fichier '{membres_path}' est introuvable à la racine !")

    with open(membres_path, 'r', encoding='utf-8') as f:
        membres = json.load(f)
        
    print(f"[*] Nombre de membres trouvés dans le JSON : {len(membres)}")

    liste_rootme = []
    liste_thm = []

    # User-Agent réaliste pour éviter les blocages basiques
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for m in membres:
        pseudo_site = m.get("pseudo_lycee", "Inconnu")
        print(f"\n[+] Traitement de l'utilisateur : {pseudo_site}")

        # ---- SECTION ROOT-ME ----
        if m.get("rootme_id"):
            url_rm = f"https://api.root-me.org/auteurs/{m['rootme_id']}"
            try:
                # verify=False permet de bypass le rejet TLS/SSL strict sur GitHub Actions
                res = requests.get(url_rm, headers=headers, timeout=10, verify=False)
                if res.status_code == 200:
                    data = res.json()
                    liste_rootme.append({
                        "pseudo": pseudo_site,
                        "score": int(data.get("score", 0)),
                        "position": data.get("position", "N/A")
                    })
                    print(f"    -> Root-Me OK ({data.get('score', 0)} pts)")
                else:
                    print(f"    -> Erreur Root-Me (Code {res.status_code})")
            except Exception as e:
                print(f"    -> Erreur connexion Root-Me : {e}")

        # ---- SECTION TRY HACK ME ----
        if m.get("thm_username"):
            url_thm = f"https://tryhackme.com/api/v2/user/profile/{m['thm_username']}"
            try:
                res = requests.get(url_thm, headers=headers, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    liste_thm.append({
                        "pseudo": pseudo_site,
                        "score": int(data.get("points", 0)),
                        "rank": data.get("userRank", "N/A"),
                        "level": data.get("level", "N/A")
                    })
                    print(f"    -> TryHackMe OK ({data.get('points', 0)} pts)")
                else:
                    print(f"    -> Erreur TryHackMe (Code {res.status_code})")
            except Exception as e:
                print(f"    -> Erreur connexion TryHackMe : {e}")

    # Trier les classements par score décroissant
    liste_rootme.sort(key=lambda x: x['score'], reverse=True)
    liste_thm.sort(key=lambda x: x['score'], reverse=True)

    # Structurer le dictionnaire de sortie
    output_data = {
        "rootme": liste_rootme,
        "thm": liste_thm
    }
    
    # Définir le chemin de sortie vers html/static/js/scores.json
    output_path = os.path.abspath(os.path.join(base_dir, '..', 'html', 'static', 'js', 'scores.json'))
    
    # S'assurer que l'arborescence de dossiers parents existe sur la machine virtuelle de GitHub
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Écriture du fichier final
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n[*] Succès ! Fichier écrit ici : {output_path}")

if __name__ == "__main__":
    # Désactiver les avertissements InsecureRequestWarning causés par verify=False
    requests.packages.urllib3.disable_warnings()
    main()