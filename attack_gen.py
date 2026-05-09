# attack_gen.py
import random
import time
from datetime import datetime

class AttackGenerator:
    """Generates various cyber attacks for training"""
    
    def __init__(self):
        self.attack_types = [
            'ddos', 'port_scan', 'brute_force', 
            'malware', 'phishing', 'normal'
        ]
        
        self.attack_log = []
        
    def generate_attack(self, intensity='medium'):
        """
        Generate attack data
        intensity: 'low', 'medium', 'high'
        """
        attack_type = random.choice(self.attack_types)
        
        if attack_type == 'normal':
            return self._normal_traffic()
        
        # Attack intensity scaling
        intensity_multiplier = {
            'low': 0.3,
            'medium': 0.6,
            'high': 1.0
        }.get(intensity, 0.6)
        
        attack_data = {
            'timestamp': datetime.now().isoformat(),
            'type': attack_type,
            'severity': random.uniform(0.3, 1.0) * intensity_multiplier,
            'source_ip': f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
            'target_port': random.choice([80, 443, 22, 3389, 8080])
        }
        
        # Attack-specific details
        if attack_type == 'ddos':
            attack_data['packets_per_second'] = random.randint(1000, 10000) * intensity_multiplier
            attack_data['unique_sources'] = random.randint(10, 500)
            
        elif attack_type == 'port_scan':
            attack_data['ports_scanned'] = random.randint(10, 1000)
            attack_data['scan_rate'] = random.uniform(10, 100) * intensity_multiplier
            
        elif attack_type == 'brute_force':
            attack_data['attempts'] = random.randint(100, 5000)
            attack_data['username'] = random.choice(['admin', 'root', 'user'])
            
        elif attack_type == 'malware':
            attack_data['malware_type'] = random.choice(['ransomware', 'trojan', 'worm'])
            attack_data['behavior'] = random.choice(['encrypt', 'exfiltrate', 'propagate'])
            
        elif attack_type == 'phishing':
            attack_data['target_url'] = random.choice(['/login', '/banking', '/email'])
            attack_data['click_rate'] = random.uniform(0.1, 0.8)
        
        # Log attack
        self.attack_log.append(attack_data)
        
        return attack_data
    
    def _normal_traffic(self):
        """Generate normal traffic pattern"""
        return {
            'timestamp': datetime.now().isoformat(),
            'type': 'normal',
            'severity': 0.0,
            'connections': random.randint(10, 100),
            'bandwidth_mbps': random.uniform(1, 50)
        }
    
    def get_recent_attacks(self, count=10):
        """Get most recent attacks"""
        return self.attack_log[-count:]
    
    def get_attack_stats(self):
        """Get attack statistics"""
        if not self.attack_log:
            return {'total_attacks': 0}
        
        attack_counts = {}
        for attack in self.attack_log:
            attack_type = attack['type']
            attack_counts[attack_type] = attack_counts.get(attack_type, 0) + 1
        
        return {
            'total_attacks': len(self.attack_log),
            'attack_distribution': attack_counts,
            'avg_severity': sum(a['severity'] for a in self.attack_log) / len(self.attack_log)
        }