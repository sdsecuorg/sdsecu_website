import json
import requests
import os

def main():
    base_dir = os.path.dirname(__file__)
    
    # Charger les membres (on remonte d'un cran si le JSON est à la racine)
    membres_path = os.path.join(base_dir, '../membres.json')
    if not os.path.exists(membres_path):
        # Si tu l'as mis dans le dossier scripts par erreur, on gère :
        membres_path = os.path.join(base_dir, 'membres.json')

    with open(membres_path, 'r', encoding='utf-8') as f:
        membres = json.load(f)

    liste_rootme = []
    liste_thm = []

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for m in membres:
        # ---- ROOT-ME ----
        if m.get("rootme_id"):
            url_rm = f"https://api.root-me.org/auteurs/{m['rootme_id']}"
            try:
                res = requests.get(url_rm, headers=headers, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    liste_rootme.append({
                        "pseudo": m["pseudo_lycee"],
                        "score": int(data.get("score", 0)),
                        "position": data.get("position", "N/A")
                    })
            except Exception as e:
                print(f"Erreur Root-Me pour {m['pseudo_lycee']}: {e}")

        # ---- TRY HACK ME ----
        if m.get("thm_username"):
            url_thm = f"https://tryhackme.com/api/v2/user/profile/{m['thm_username']}"
            try:
                res = requests.get(url_thm, headers=headers, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    liste_thm.append({
                        "pseudo": m["pseudo_lycee"],
                        "score": int(data.get("points", 0)),
                        "rank": data.get("userRank", "N/A"),
                        "level": data.get("level", "N/A")
                    })
            except Exception as e:
                print(f"Erreur THM pour {m['pseudo_lycee']}: {e}")

    # Trier les classements par score décroissant
    liste_rootme.sort(key=lambda x: x['score'], reverse=True)
    liste_thm.sort(key=lambda x: x['score'], reverse=True)

    output_data = {
        "rootme": list_rootme,
        "thm": list_thm
    }
    
    # Sauvegarde dans html/static/js/scores.json
    output_path = os.path.join(base_dir, '../html/static/js/scores.json')
    
    # S'assurer que le dossier static/js existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print("Scores mis à jour avec succès dans html/static/js/scores.json !")

if __name__ == "__main__":
    main()