import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from risk_engine import RiskEngine

class TestRiskEngine:
    
    def setup_method(self):
        self.engine = RiskEngine()

    def test_high_risk_detection(self):
        events = [
            {'timestamp': 'Dec 24 10:00:01', 'ip': '1.1.1.1', 'user': 'root', 'status': 'failed'}
        ] * 6  # 6 failures
        
        risks = self.engine.analyze(events)
        assert len(risks) == 1
        assert risks[0]['risk_level'] == 'HIGH'
        assert risks[0]['ip'] == '1.1.1.1'

    def test_medium_risk_detection(self):
        events = [
            {'timestamp': 'Dec 24 10:00:01', 'ip': '2.2.2.2', 'user': 'admin', 'status': 'failed'}
        ] * 3  # 3 failures
        
        risks = self.engine.analyze(events)
        assert len(risks) == 1
        assert risks[0]['risk_level'] == 'MEDIUM'
        assert risks[0]['ip'] == '2.2.2.2'

    def test_low_risk_ignored(self):
        events = [
            {'timestamp': 'Dec 24 10:00:01', 'ip': '3.3.3.3', 'user': 'user', 'status': 'failed'}
        ] * 1  # 1 failure
        
        risks = self.engine.analyze(events)
        assert len(risks) == 0
