import subprocess

def generate_summary_with_ai(issues, recommendations, model="llama3.1"):
    """
    Utilise Ollama pour générer un résumé IA à partir des vulnérabilités détectées.
    """
    prompt = f"""
    Voici les vulnérabilités détectées : {issues}.
    Voici les recommandations techniques : {recommendations}.
    Rédige une synthèse en français professionnel pour un rapport d’audit PME.
    Le ton doit être clair, concis et non technique.
    """

    try:
        # 🧠 nouvelle syntaxe Ollama : on envoie le prompt via stdin, plus de --prompt
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,          # prompt passé dans stdin
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print("❌ Erreur Ollama :", result.stderr)
            return "(Erreur : aucun texte généré par le modèle IA.)"

        output = result.stdout.strip()
        if not output:
            output = "(IA locale n'a renvoyé aucun texte.)"
        return output

    except FileNotFoundError:
        return "(Erreur : Ollama non trouvé. Vérifie l'installation avec 'ollama list'.)"
    except subprocess.TimeoutExpired:
        return "(Erreur : temps d'exécution IA dépassé.)"
