import json

def analyze_cloud_data(file_path: str):
    with open(file_path, "r") as f:
        data = json.load(f)

    issues = []
    score = 100

    for user in data.get("users", []):
        if not user.get("mfa", False):
            issues.append(f"MFA disabled for {user['name']}")
            score -= 10
        if user.get("public_share", False):
            issues.append(f"Public share enabled for {user['name']}")
            score -= 5

    # ✅ le retour DOIT contenir ces trois clés
    return {
        "overall_score": max(score, 0),
        "issues": issues,
        "recommendations": [
            "Enable MFA for all users",
            "Review public sharing permissions"
        ]
    }
