from collections import defaultdict
from typing import List, Dict

class RiskEngine:
    """
    Analyzes parsed log events to detect security risks.
    """
    
    # Thresholds
    HIGH_RISK_THRESHOLD = 5
    MEDIUM_RISK_THRESHOLD = 3
    TIME_WINDOW_MINUTES = 1

    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.risk_assessment = []

    def analyze(self, events: List[Dict]) -> List[Dict]:
        """
        Analyzes a list of parsed events.
        """
        for event in events:
            if event['status'] == 'failed':
                self._process_failure(event)
        
        return self._generate_assessment()

    def _process_failure(self, event: Dict):
        """
        Tracks failed attempts by IP.
        """
        ip = event['ip']
        timestamp_str = event['timestamp']
        # Note: parsing the timestamp string would depend on the year being present or inferred.
        # For this prototype, we'll assume the logs are recent and just count raw failures 
        # but in a real app we'd parse datetime objects to check the 1-minute window.
        # Here we will just store them.
        self.failed_attempts[ip].append(timestamp_str)

    def _generate_assessment(self) -> List[Dict]:
        """
        Generates risk assessment based on failure counts.
        """
        assessment = []
        for ip, attempts in self.failed_attempts.items():
            count = len(attempts)
            risk_level = "LOW"
            
            if count >= self.HIGH_RISK_THRESHOLD:
                risk_level = "HIGH"
            elif count >= self.MEDIUM_RISK_THRESHOLD:
                risk_level = "MEDIUM"
            
            if risk_level != "LOW":
                assessment.append({
                    'ip': ip,
                    'risk_level': risk_level,
                    'failed_attempts': count,
                    'description': f"Detected {count} failed login attempts from {ip}."
                })
        
        return assessment
