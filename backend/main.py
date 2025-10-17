from fastapi import FastAPI
from reports.generate_report import generate_audit_report
from audit_engine.engine import analyze_cloud_data
from ai_module.llm_engine import generate_summary_with_ai  # 👈 ajout IA

app = FastAPI(title="CloudGuard AI Backend")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API running"}

@app.get("/audit/local")
def local_audit():
    results = analyze_cloud_data("audit_engine/sample_data.json")

    # 🧠 Génère un résumé intelligent avec IA locale
    ai_summary = generate_summary_with_ai(
        issues=results["issues"],
        recommendations=results["recommendations"]
    )

    # Ajoute le texte au résultat global
    results["ai_summary"] = ai_summary

    report_path = generate_audit_report(results)

    return {
        "audit_results": results,
        "report_path": report_path
    }
