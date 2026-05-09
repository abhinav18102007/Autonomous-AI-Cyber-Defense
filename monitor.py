# monitor.py
import psutil
import time
import threading
from collections import deque
import numpy as np

class SystemMonitor:
    """Real-time system monitoring"""
    
    def __init__(self): 
        self.cpu_history = deque(maxlen=100)
        self.memory_history = deque(maxlen=100)
        self.network_history = deque(maxlen=100)
        self.running = False
        
    def start_monitoring(self):
        """Start monitoring in background thread"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
        
    def _monitor_loop(self):
        """Continuous monitoring loop"""
        while self.running:
            # Get system metrics
            cpu = psutil.cpu_percent(interval=1) / 100
            memory = psutil.virtual_memory().percent / 100
            network = psutil.net_io_counters()
            
            self.cpu_history.append(cpu)
            self.memory_history.append(memory)
            
            time.sleep(1)
    
    def get_current_state(self):
        """Get current system state"""
        return {
            'cpu_usage': self.cpu_history[-1] if self.cpu_history else 0.0,
            'memory_usage': self.memory_history[-1] if self.memory_history else 0.0,
            'threat_level': self._calculate_threat_level(),
            'system_health': self._calculate_health()
        }
    
    def _calculate_threat_level(self):
        """Calculate threat level based on anomalies"""
        if len(self.cpu_history) < 10:
            return 0.0
        
        # Simple anomaly detection
        recent_cpu = list(self.cpu_history)[-10:]
        mean_cpu = np.mean(recent_cpu)
        std_cpu = np.std(recent_cpu)
        current_cpu = recent_cpu[-1]
        
        if current_cpu > mean_cpu + 2 * std_cpu:
            return min(1.0, (current_cpu - mean_cpu) / (2 * std_cpu))
        
        return 0.0
    
    def _calculate_health(self):
        """Calculate system health score"""
        if not self.cpu_history:
            return 1.0
        
        recent_cpu = list(self.cpu_history)[-10:]
        avg_cpu = np.mean(recent_cpu)
        
        # Lower CPU usage = better health
        health = 1.0 - avg_cpu
        return max(0.0, min(1.0, health))