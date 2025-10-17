from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_audit_report(results, output_dir="reports"):
    """Génère un rapport PDF simple à partir des résultats d'audit"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(output_dir, filename)

    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Rapport d'Audit - CloudGuard AI")

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "CloudGuard AI - Rapport d'Audit")
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Score global
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 750, f"Score de sécurité global : {results.get('overall_score', 0)}/100")

    # Détails des résultats
    c.setFont("Helvetica", 11)
    y = 720
    for key, value in results.items():
        # On ne réaffiche pas le score déjà affiché au-dessus
        if key != "overall_score" and key != "ai_summary":
            c.drawString(60, y, f"{key.replace('_', ' ').capitalize()} : {value}")
            y -= 20

    # 👉 ICI on ajoute la synthèse IA (à la fin du rapport)
    if "ai_summary" in results:
        y -= 40
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Synthèse IA :")
        y -= 20
        c.setFont("Helvetica", 10)

        text = c.beginText(60, y)
        text.textLines(results["ai_summary"])
        c.drawText(text)

    # Sauvegarde finale du PDF
    c.save()
    return path
