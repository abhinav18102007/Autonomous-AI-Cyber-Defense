# rl_agent.py
import numpy as np
import random
from collections import deque
import json

class CyberDefenseAgent:
    """
    Q-Learning agent for cyber defense
    """
    
    def __init__(self, state_size=6, action_size=4):
        self.state_size = state_size
        self.action_size = action_size
        
        # Q-table
        self.q_table = {}
        
        # Hyperparameters
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
        # Experience replay
        self.memory = deque(maxlen=2000)
        self.batch_size = 32
        
        self.training_steps = 0
        
    def _get_state_key(self, state):
        """Convert continuous state to discrete key"""
        # Discretize state for Q-table
        discrete_state = tuple(np.floor(state * 10).astype(int))
        return discrete_state
    
    def get_action(self, state, training=True):
        """Choose action using epsilon-greedy policy"""
        state_key = self._get_state_key(state)
        
        if training and random.random() < self.epsilon:
            # Explore: random action
            return random.randint(0, self.action_size - 1)
        
        # Exploit: best known action
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        
        return np.argmax(self.q_table[state_key])
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))
    
    def learn(self, state, action, reward, next_state, done):
        """Update Q-values"""
        state_key = self._get_state_key(state)
        next_state_key = self._get_state_key(next_state)
        
        # Initialize Q-values if not exist
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_size)
        
        # Q-learning update
        current_q = self.q_table[state_key][action]
        
        if done:
            target = reward
        else:
            target = reward + self.discount_factor * np.max(self.q_table[next_state_key])
        
        # Update Q-value
        self.q_table[state_key][action] += self.learning_rate * (target - current_q)
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        self.training_steps += 1
        
        # Experience replay
        if len(self.memory) > self.batch_size:
            self._replay()
    
    def _replay(self):
        """Experience replay for better learning"""
        batch = random.sample(self.memory, self.batch_size)
        
        for state, action, reward, next_state, done in batch:
            state_key = self._get_state_key(state)
            next_state_key = self._get_state_key(next_state)
            
            if state_key not in self.q_table:
                self.q_table[state_key] = np.zeros(self.action_size)
            if next_state_key not in self.q_table:
                self.q_table[next_state_key] = np.zeros(self.action_size)
            
            current_q = self.q_table[state_key][action]
            
            if done:
                target = reward
            else:
                target = reward + self.discount_factor * np.max(self.q_table[next_state_key])
            
            self.q_table[state_key][action] += self.learning_rate * (target - current_q)
    
    def save_model(self, filename="cyber_defense_model.json"):
        """Save Q-table to file"""
        # Convert numpy arrays to lists for JSON
        serializable_q_table = {}
        for key, value in self.q_table.items():
            serializable_q_table[str(key)] = value.tolist()
        
        with open(filename, 'w') as f:
            json.dump(serializable_q_table, f)
        
        print(f"✅ Model saved to {filename}")
    
    def load_model(self, filename="cyber_defense_model.json"):
        """Load Q-table from file"""
        try:
            with open(filename, 'r') as f:
                loaded_q_table = json.load(f)
            
            # Convert back to numpy arrays
            for key, value in loaded_q_table.items():
                # Parse tuple key
                tuple_key = tuple(map(int, key.strip('()').split(', ')))
                self.q_table[tuple_key] = np.array(value)
            
            print(f"✅ Model loaded from {filename}")
            return True
        except FileNotFoundError:
            print("⚠️ No existing model found, starting fresh")
            return False
    
    def get_stats(self):
        """Get agent statistics"""
        return {
            'q_table_size': len(self.q_table),
            'epsilon': self.epsilon,
            'training_steps': self.training_steps,
            'memory_size': len(self.memory)
        }