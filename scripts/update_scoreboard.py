import json
import requests
import os

def main():
    base_dir = os.path.dirname(__file__)
    membres_path = os.path.abspath(os.path.join(base_dir, '..', 'membres.json'))
    
    if not os.path.exists(membres_path):
        print(f"[-] Erreur : Fichier introuvable : {membres_path}")
        return

    with open(membres_path, 'r', encoding='utf-8') as f:
        membres = json.load(f)
        
    print(f"[*] Membres chargés : {len(membres)}")

    liste_rootme = []
    liste_thm = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    for m in membres:
        pseudo_site = m.get("pseudo_lycee", "Inconnu")

        # ---- SECTION ROOT-ME (Sécurisée contre les crashs) ----
        if m.get("rootme_id"):
            url_rm = f"https://api.root-me.org/auteurs/{m['rootme_id']}"
            try:
                res = requests.get(url_rm, headers=headers, timeout=10, verify=False)
                if res.status_code == 200:
                    data = res.json()
                    liste_rootme.append({
                        "pseudo": pseudo_site,
                        "score": int(data.get("score", 0)),
                        "position": data.get("position", "N/A")
                    })
                    print(f"[+] Root-Me récupéré pour {pseudo_site}")
                else:
                    print(f"[-] Root-Me a répondu avec le code HTTP {res.status_code} pour {pseudo_site}")
            except Exception as e:
                # Si le SSL ou Cloudflare bloque, on ne crash pas, on log l'erreur gentiment
                print(f"[!] Impossible de joindre Root-Me pour {pseudo_site} (Blocage TLS/Filtre) : {e}")

        # ---- SECTION TRY HACK ME (Sécurisée contre les crashs) ----
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
                    print(f"[+] TryHackMe récupéré pour {pseudo_site}")
                else:
                    print(f"[-] TryHackMe a répondu avec le code HTTP {res.status_code} pour {pseudo_site}")
            except Exception as e:
                print(f"[!] Impossible de joindre TryHackMe pour {pseudo_site} : {e}")

    # Tri des scores
    liste_rootme.sort(key=lambda x: x['score'], reverse=True)
    liste_thm.sort(key=lambda x: x['score'], reverse=True)

    # Préparation du fichier final
    output_data = {
        "rootme": liste_rootme,
        "thm": liste_thm
    }
    
    output_path = os.path.abspath(os.path.join(base_dir, '..', 'html', 'static', 'js', 'scores.json'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print(f"[*] Sauvegarde réussie dans {output_path}")

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()