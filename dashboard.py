# dashboard.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_dashboard(env, agent, monitor, attack_gen):
    """Create real-time dashboard"""
    
    st.set_page_config(
        page_title="🤖 Autonomous Cyber Defense System",
        page_icon="🛡️",
        layout="wide"
    )
    
    st.title("🤖 Autonomous AI Cyber Defense System")
    st.markdown("*Real-time AI-Powered Threat Detection & Response*")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Status")
        
        # Agent stats
        stats = agent.get_stats() 
        st.metric("Q-Table Size", stats['q_table_size'])
        st.metric("Exploration Rate (ε)", f"{stats['epsilon']:.3f}")
        st.metric("Training Steps", stats['training_steps'])
        
        st.divider()
        
        # Attack stats
        attack_stats = attack_gen.get_attack_stats()
        st.metric("Total Attacks Detected", attack_stats.get('total_attacks', 0))
        
        if 'attack_distribution' in attack_stats:
            st.write("Attack Distribution:")
            for attack_type, count in attack_stats['attack_distribution'].items():
                st.write(f"- {attack_type}: {count}")
    
    # Main content - 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🖥️ System Metrics")
        
        # CPU gauge
        current_state = monitor.get_current_state()
        cpu_value = current_state['cpu_usage'] * 100
        
        fig_cpu = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = cpu_value,
            title = {'text': "CPU Usage (%)"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ]
            }
        ))
        fig_cpu.update_layout(height=250)
        st.plotly_chart(fig_cpu, use_container_width=True)
        
        # Memory usage
        mem_value = current_state['memory_usage'] * 100
        st.metric("Memory Usage", f"{mem_value:.1f}%")
        st.progress(mem_value / 100)
    
    with col2:
        st.subheader("⚠️ Threat Level")
        
        # Threat gauge
        threat_value = current_state['threat_level'] * 100
        
        fig_threat = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = threat_value,
            title = {'text': "Current Threat Level (%)"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "orange"},
                    {'range': [70, 100], 'color': "darkred"}
                ]
            }
        ))
        fig_threat.update_layout(height=250)
        st.plotly_chart(fig_threat, use_container_width=True)
        
        # System health
        health_value = current_state['system_health'] * 100
        st.metric("System Health", f"{health_value:.1f}%")
    
    with col3:
        st.subheader("🤖 AI Agent Status")
        
        # Agent info
        st.info(f"""
        **Learning Algorithm:** Q-Learning  
        **State Size:** {env.state_size}  
        **Action Size:** {env.action_size}  
        **Q-Table Size:** {stats['q_table_size']}  
        **ε-Greedy:** {stats['epsilon']:.3f}
        """)
        
        # Last action
        if hasattr(st.session_state, 'last_action'):
            st.success(f"**Last Action:** {st.session_state.last_action}")
    
    # Recent attacks table
    st.subheader("📋 Recent Security Events")
    
    recent_attacks = attack_gen.get_recent_attacks(10)
    if recent_attacks:
        df = pd.DataFrame(recent_attacks)
        # Format for display
        display_cols = ['timestamp', 'type', 'severity', 'source_ip']
        df_display = df[display_cols].copy()
        df_display['severity'] = df_display['severity'].apply(lambda x: f"{x:.2f}")
        st.dataframe(df_display, use_container_width=True)
    
    # Training controls
    st.subheader("🎮 Training Controls")
    
    col_train1, col_train2, col_train3 = st.columns(3)
    
    with col_train1:
        if st.button("▶️ Start Training", use_container_width=True):
            st.session_state.training = True
            st.success("Training started!")
    
    with col_train2:
        if st.button("⏹️ Stop Training", use_container_width=True):
            st.session_state.training = False
            st.warning("Training stopped")
    
    with col_train3:
        if st.button("💾 Save Model", use_container_width=True):
            agent.save_model()
            st.success("Model saved!")
    
    # Real-time metrics
    if st.checkbox("Show Real-time Metrics"):
        st.subheader("📈 Real-time Metrics")
        
        # Create sample data for demonstration
        metrics_data = pd.DataFrame({
            'Time': [datetime.now() - timedelta(seconds=x) for x in range(20, 0, -1)],
            'Threat Level': [np.random.random() for _ in range(20)],
            'CPU Usage': [np.random.uniform(20, 80) for _ in range(20)]
        })
        
        fig = px.line(metrics_data, x='Time', y=['Threat Level', 'CPU Usage'], 
                      title="Real-time Metrics")
        st.plotly_chart(fig, use_container_width=True)