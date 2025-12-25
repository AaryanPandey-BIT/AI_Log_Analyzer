import argparse
import sys
import os
from typing import List, Dict

# Add the src directory to the python path so we can import modules if running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from log_parser import LogParser
from risk_engine import RiskEngine
from reporter import ReportGenerator

# AI Integration
try:
    from google import genai
    from dotenv import load_dotenv
    load_dotenv() # Load environment variables from .env file
except ImportError:
    pass # Handle gracefully later if libraries are missing

def get_ai_insight(risks: List[Dict]) -> str:
    """
    Uses Google Gemini to generate a security insight summary.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_key_here":
        return "AI Insight skipped: No valid GEMINI_API_KEY found in environment."

    try:
        client = genai.Client(api_key=api_key)
        
        # Prepare the prompt
        if not risks:
            return "AI Insight: No risks detected. System appears secure."
            
        prompt = f"""
        You are a Cybersecurity Expert. Analyze these detected security incidents from a Linux SSH log:
        {risks}
        
        Provide a succinct, professional executive summary of the threat level and recommended actions. 
        Keep it under 3 sentences.
        """
        
        response = client.models.generate_content(
            model="gemini-flash-latest", # Use stable alias
            contents=prompt
        )
        return f"=== AI Smart Summary ===\n{response.text}\n"
    
    except Exception as e:
        return f"AI Insight skipped: Error connecting to AI service - {e}"

def main():
    parser = argparse.ArgumentParser(description="AI Log Analyzer - SSH Brute Force Detector")
    parser.add_argument("logfile", help="Path to the SSH auth.log file")
    
    args = parser.parse_args()
    
    filepath = args.logfile
    if not os.path.exists(filepath):
        print(f"Error: Log file not found: {filepath}")
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Analyzing {filepath}...")
    
    # 1. Parse Logs
    log_parser = LogParser()
    events = list(log_parser.parse_file(filepath))
    print(f"Parsed {len(events)} relevant events.")

    # 2. Analyze Risks
    risk_engine = RiskEngine()
    risks = risk_engine.analyze(events)
    
    # 3. Get AI Insight
    print("Consulting AI for insights...")
    ai_summary = get_ai_insight(risks)
    print(ai_summary)

    # 4. Generate & Save Reports
    # Append AI summary to the data passed to reporter? 
    # For now, we'll just print it to console and append to text report logic if we wanted, 
    # but the requirement was just to add the function. 
    # Let's attach it to the first item description or handle it in reporter?
    # Simpler: Just print it for now as requested.
    
    print("Generating reports...")
    ReportGenerator.save_reports(risks, output_dir)
    
    # Also print to console for immediate feedback
    print("\n" + ReportGenerator.generate_text_report(risks))

if __name__ == "__main__":
    main()
