# defense_env.py
import numpy as np
import random
from collections import deque
import time

class CyberDefenseEnvironment:
    """
    Custom cybersecurity environment without Gymnasium
    """
    
    def __init__(self):
        # State: [cpu_usage, memory_usage, network_traffic, 
        #         failed_logins, threat_score, defense_readiness]
        self.state_size = 6
        self.action_size = 4  # 0: No action, 1: Block IP, 2: Isolate, 3: Patch
        
        # Reset environment
        self.reset()
        
    def reset(self):
        """Reset environment to initial state"""
        self.state = np.array([0.2, 0.3, 0.1, 0.0, 0.0, 0.8], dtype=np.float32)
        self.threat_level = 0.0
        self.step_count = 0
        self.max_steps = 100
        self.reward_history = []
        
        return self.state
    
    def step(self, action):
        """
        Execute action and return (next_state, reward, done, info)
        """
        self.step_count += 1
        
        # Simulate threat evolution
        self._update_threat()
        
        # Calculate reward based on action and threat
        reward = self._calculate_reward(action)
        
        # Apply action effects
        self._apply_action(action)
        
        # Update state
        self._update_state()
        
        # Check if episode finished
        done = (self.threat_level > 0.95) or (self.step_count >= self.max_steps)
        
        info = {
            'threat_level': self.threat_level,
            'action_taken': self._get_action_name(action),
            'steps': self.step_count
        }
        
        return self.state.copy(), reward, done, info
    
    def _update_threat(self):
        """Random threat generation"""
        # 25% chance of new threat
        if random.random() < 0.25:
            threat_increase = random.uniform(0.1, 0.4)
            self.threat_level = min(1.0, self.threat_level + threat_increase)
        else:
            # Natural decay if no action
            self.threat_level = max(0.0, self.threat_level - 0.03)
    
    def _calculate_reward(self, action):
        """Custom reward function"""
        reward = 0
        
        # Base reward for survival
        reward += 0.1
        
        if self.threat_level > 0.7:  # Active high threat
            if action in [1, 2, 3]:  # Any defensive action
                reward += 15.0 - (self.threat_level * 10)
            else:  # No action during threat
                reward -= 25.0
        elif self.threat_level > 0.3:  # Medium threat
            if action in [1, 2]:
                reward += 8.0
            elif action == 0:
                reward -= 5.0
        else:  # Low threat / Normal
            if action == 0:  # Correct: no action
                reward += 2.0
            else:  # False positive
                reward -= 8.0
        
        # Bonus for effective defense
        if action in [1, 2, 3] and self.threat_level > 0.3:
            self.threat_level *= 0.6  # Reduce threat
            reward += 10.0
            
        return reward
    
    def _apply_action(self, action):
        """Apply defense action effects"""
        actions = {
            0: "no_action",
            1: "block_ip",
            2: "isolate_system", 
            3: "apply_patch"
        }
        
        action_name = actions[action]
        
        # Action-specific effects
        if action_name == "block_ip":
            # Slight performance improvement
            self.state[0] = max(0.1, self.state[0] - 0.05)
            
        elif action_name == "isolate_system":
            # Heavy performance impact but good security
            self.state[0] = min(1.0, self.state[0] + 0.15)
            self.state[5] = max(0, self.state[5] - 0.2)
            
        elif action_name == "apply_patch":
            # Medium impact, long-term benefit
            self.state[0] = min(1.0, self.state[0] + 0.05)
            self.state[5] = min(1.0, self.state[5] + 0.1)
    
    def _update_state(self):
        """Update state vector based on current conditions"""
        # CPU usage affected by threat
        self.state[0] = min(1.0, self.state[0] + (self.threat_level * 0.1))
        
        # Threat score in state
        self.state[4] = self.threat_level
        
        # Random variations for realism
        self.state[0] = np.clip(self.state[0] + random.uniform(-0.02, 0.02), 0, 1)
        self.state[1] = np.clip(self.state[1] + random.uniform(-0.01, 0.01), 0, 1)
    
    def _get_action_name(self, action):
        """Convert action ID to name"""
        names = {0: "🟢 No Action", 1: "🔴 Block IP", 2: "🟠 Isolate", 3: "🔵 Patch"}
        return names.get(action, "Unknown")