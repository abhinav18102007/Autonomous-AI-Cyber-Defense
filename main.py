# main.py
import streamlit as st
import time
import numpy as np
from defense_env import CyberDefenseEnvironment
from rl_agent import CyberDefenseAgent
from attack_gen import AttackGenerator
from monitor import SystemMonitor
from dashboard import create_dashboard
import threading

class AutonomousCyberDefense:
    """Main system orchestrator"""
    
    def __init__(self):
        self.env = CyberDefenseEnvironment()
        self.agent = CyberDefenseAgent()
        self.attack_gen = AttackGenerator()
        self.monitor = SystemMonitor()
        
        self.training = False
        self.episode_rewards = []
        
        # Try to load existing model
        self.agent.load_model()
        
    def train_episode(self, max_steps=100):
        """Train for one episode"""
        state = self.env.reset()
        total_reward = 0
        episode_actions = []
        
        for step in range(max_steps):
            # Get action from agent
            action = self.agent.get_action(state, training=True)
            
            # Generate attack (for training diversity)
            attack = self.attack_gen.generate_attack()
            
            # Execute action
            next_state, reward, done, info = self.env.step(action)
            
            # Store experience and learn
            self.agent.remember(state, action, reward, next_state, done)
            self.agent.learn(state, action, reward, next_state, done)
            
            total_reward += reward
            episode_actions.append(info['action_taken'])
            
            state = next_state
            
            if done:
                break
        
        self.episode_rewards.append(total_reward)
        
        return {
            'total_reward': total_reward,
            'steps': step + 1,
            'actions': episode_actions,
            'final_threat': self.env.threat_level
        }
    
    def evaluate(self, episodes=10):
        """Evaluate agent performance"""
        print("\n📊 Evaluating Agent Performance...")
        
        eval_results = []
        
        for ep in range(episodes):
            state = self.env.reset()
            total_reward = 0
            steps = 0
            
            while True:
                action = self.agent.get_action(state, training=False)
                next_state, reward, done, info = self.env.step(action)
                total_reward += reward
                steps += 1
                state = next_state
                
                if done:
                    break
            
            eval_results.append({
                'episode': ep + 1,
                'reward': total_reward,
                'steps': steps,
                'success': total_reward > 0
            })
            
            print(f"Episode {ep+1}: Reward = {total_reward:.2f}, Steps = {steps}")
        
        # Calculate statistics
        avg_reward = np.mean([r['reward'] for r in eval_results])
        success_rate = np.sum([r['success'] for r in eval_results]) / episodes * 100
        
        print(f"\n📈 Evaluation Summary:")
        print(f"   Average Reward: {avg_reward:.2f}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Best Episode: {max(eval_results, key=lambda x: x['reward'])['reward']:.2f}")
        
        return eval_results
    
    def continuous_training(self, episodes=1000, save_interval=100):
        """Train continuously"""
        print("🤖 Starting Autonomous Cyber Defense Training...")
        print("=" * 50)
        
        for episode in range(1, episodes + 1):
            result = self.train_episode()
            
            # Print progress
            if episode % 10 == 0:
                avg_reward = np.mean(self.episode_rewards[-10:])
                print(f"Episode {episode:4d} | "
                      f"Reward: {result['total_reward']:7.2f} | "
                      f"Avg (10): {avg_reward:7.2f} | "
                      f"ε: {self.agent.epsilon:.3f}")
            
            # Save model periodically
            if episode % save_interval == 0:
                self.agent.save_model(f"cyber_defense_model_ep{episode}.json")
        
        print("\n✅ Training Complete!")
        self.agent.save_model("cyber_defense_final.json")
    
    def run_dashboard(self):
        """Run Streamlit dashboard"""
        # Initialize session state
        if 'last_action' not in st.session_state:
            st.session_state.last_action = "None"
        
        # Create dashboard
        create_dashboard(self.env, self.agent, self.monitor, self.attack_gen)
        
        # Update last action periodically
        if st.session_state.get('training', False):
            state = self.env.reset()
            action = self.agent.get_action(state, training=False)
            st.session_state.last_action = self.env._get_action_name(action)

def main():
    """Main entry point"""
    import sys
    
    # Initialize system
    defense_system = AutonomousCyberDefense()
    
    # Start monitoring
    defense_system.monitor.start_monitoring()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'train':
            # Training mode
            defense_system.continuous_training(episodes=500)
        elif sys.argv[1] == 'evaluate':
            # Evaluation mode
            defense_system.evaluate(episodes=20)
        elif sys.argv[1] == 'dashboard':
            # Dashboard mode
            defense_system.run_dashboard()
    else:
        # Interactive menu
        print("\n🤖 Autonomous Cyber Defense System")
        print("=" * 40)
        print("1. Train Agent")
        print("2. Evaluate Agent")
        print("3. Launch Dashboard")
        print("4. Quick Test")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == '1':
            defense_system.continuous_training()
        elif choice == '2':
            defense_system.evaluate()
        elif choice == '3':
            defense_system.run_dashboard()
        elif choice == '4':
            # Quick test
            state = defense_system.env.reset()
            for _ in range(20):
                action = defense_system.agent.get_action(state, training=False)
                state, reward, done, info = defense_system.env.step(action)
                print(f"Action: {info['action_taken']:15} | "
                      f"Reward: {reward:6.2f} | "
                      f"Threat: {defense_system.env.threat_level:.2f}")
                if done:
                    break

if __name__ == "__main__":
    main()