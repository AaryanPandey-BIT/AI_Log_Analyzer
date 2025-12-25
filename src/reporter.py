import json
import os
from typing import List, Dict

class ReportGenerator:
    """
    Generates reports from risk assessment data.
    """

    @staticmethod
    def generate_text_report(risks: List[Dict]) -> str:
        """
        Generates a human-readable text report.
        """
        if not risks:
            return "No high-risk activity detected."

        report = ["=== Security Identification Report ==="]
        for item in risks:
            report.append(f"IP: {item['ip']}")
            report.append(f"Risk Level: {item['risk_level']}")
            report.append(f"Description: {item['description']}")
            report.append("-" * 30)
        
        return "\n".join(report)

    @staticmethod
    def generate_json_report(risks: List[Dict]) -> str:
        """
        Generates a JSON formatted report.
        """
        return json.dumps(risks, indent=4)

    @staticmethod
    def save_reports(risks: List[Dict], output_dir: str):
        """
        Saves both text and JSON reports to the output directory.
        """
        text_report = ReportGenerator.generate_text_report(risks)
        json_report = ReportGenerator.generate_json_report(risks)

        text_path = os.path.join(output_dir, "report.txt")
        json_path = os.path.join(output_dir, "report.json")

        with open(text_path, "w") as f:
            f.write(text_report)
        
        with open(json_path, "w") as f:
            f.write(json_report)
        
        print(f"Reports saved to {output_dir}")
