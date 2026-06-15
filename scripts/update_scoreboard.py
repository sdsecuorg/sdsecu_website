import json
import requests
import os

def main():
    base_dir = os.path.dirname(__file__)
    membres_path = os.path.abspath(os.path.join(base_dir, '..', 'membres.json'))
    
    if not os.path.exists(membres_path):
        raise FileNotFoundError(f"Fichier introuvable : {membres_path}")

    with open(membres_path, 'r', encoding='utf-8') as f:
        membres = json.load(f)
        
    liste_rootme = []
    liste_thm = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    for m in membres:
        pseudo_site = m.get("pseudo_lycee", "Inconnu")

        # ---- ROOT-ME ----
        if m.get("rootme_id"):
            url_rm = f"https://api.root-me.org/auteurs/{m['rootme_id']}"
            res = requests.get(url_rm, headers=headers, timeout=10, verify=False)
            
            # Si Root-Me bloque, on crash et on affiche pourquoi
            if res.status_code != 200:
                raise RuntimeError(f"Root-Me a bloqué la requête (Code {res.status_code}). Réponse : {res.text[:200]}")
                
            data = res.json()
            liste_rootme.append({
                "pseudo": pseudo_site,
                "score": int(data.get("score", 0)),
                "position": data.get("position", "N/A")
            })

        # ---- TRY HACK ME ----
        if m.get("thm_username"):
            url_thm = f"https://tryhackme.com/api/v2/user/profile/{m['thm_username']}"
            res = requests.get(url_thm, headers=headers, timeout=10)
            
            # Si THM bloque, on crash et on affiche pourquoi
            if res.status_code != 200:
                raise RuntimeError(f"TryHackMe a bloqué la requête (Code {res.status_code}). Réponse : {res.text[:200]}")
                
            data = res.json()
            liste_thm.append({
                "pseudo": pseudo_site,
                "score": int(data.get("points", 0)),
                "rank": data.get("userRank", "N/A"),
                "level": data.get("level", "N/A")
            })

    # Tri et sauvegarde
    liste_rootme.sort(key=lambda x: x['score'], reverse=True)
    liste_thm.sort(key=lambda x: x['score'], reverse=True)

    output_data = {"rootme": list_rootme, "thm": list_thm}
    output_path = os.path.abspath(os.path.join(base_dir, '..', 'html', 'static', 'js', 'scores.json'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()