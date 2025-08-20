# Enhanced metrics section with detailed explanations

# Create metric containers with futuristic styling and detailed explanations
metric_container = st.container()
with metric_container:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric("🎯 Neural Form Score", f"{latest_metrics.shooting_form_score:.3f}", 
                help="AI-calculated overall form rating (0.0-1.0)")
        with st.expander("📖 Form Score Analysis"):
            st.markdown("""
            **🎯 What it measures:** Overall shooting technique combining all biomechanical factors
            
            **📊 Score Ranges:**
            - 🟢 **0.80-1.00**: Elite form - Professional level technique
            - 🟡 **0.60-0.79**: Good form - Solid fundamentals with room for refinement
            - 🟠 **0.40-0.59**: Developing form - Key areas need attention
            - 🔴 **0.00-0.39**: Needs work - Focus on basic fundamentals
            
            **💡 Improvement Tips:**
            - Practice slow-motion shooting to build muscle memory
            - Focus on consistent pre-shot routine
            - Work with a coach to identify specific weaknesses
            - Film yourself from multiple angles for self-analysis
            """)
        
        st.metric("📏 Launch Height", f"{latest_metrics.release_height:.3f}", 
                help="Release point elevation metrics (relative to shoulders)")
        with st.expander("📖 Launch Height Analysis"):
            st.markdown("""
            **📏 What it measures:** How high you release the ball relative to your shoulder line
            
            **📊 Optimal Range:**
            - 🎯 **Target**: 0.1-0.3 above shoulder line
            - Higher release = harder to block, better arc
            - Lower release = quicker shot, less arc
            
            **💡 Improvement Tips:**
            - **Too Low**: Strengthen legs for better lift, practice jump shots
            - **Too High**: Work on shooting off the dribble, quick release drills
            - Practice shooting at different heights to find your sweet spot
            - Focus on consistent leg drive and follow-through
            """)
        
        st.metric("⚖️ Balance Matrix", f"{latest_metrics.balance_score:.3f}", 
                help="Stability analysis (0.0-1.0)")
        with st.expander("📖 Balance Analysis"):
            st.markdown("""
            **⚖️ What it measures:** Body alignment and stability throughout the shot
            
            **📊 Score Interpretation:**
            - 🟢 **0.80+**: Excellent balance and body control
            - 🟡 **0.60-0.79**: Good balance with minor adjustments needed
            - 🟠 **0.40-0.59**: Moderate balance issues affecting accuracy
            - 🔴 **<0.40**: Significant balance problems requiring attention
            
            **💡 Improvement Tips:**
            - Practice shooting with feet shoulder-width apart
            - Work on core strength and stability exercises
            - Focus on landing in the same spot you took off from
            - Practice shooting off balance to improve stability
            """)
    
    with col_b:
        st.metric("📐 Release Vector", f"{latest_metrics.release_angle:.1f}°", 
                help="Optimal shooting angle analysis")
        with st.expander("📖 Release Angle Analysis"):
            st.markdown("""
            **📐 What it measures:** The angle your shooting arm makes at ball release
            
            **📊 Optimal Ranges:**
            - 🎯 **90-105°**: Ideal range for most shots
            - **Free Throws**: 95-105° for optimal arc
            - **3-Pointers**: 85-95° for power and accuracy
            - **Close Range**: 105-120° for high arc over defenders
            
            **💡 Improvement Tips:**
            - **Too Low (<85°)**: Focus on getting under the ball, higher release
            - **Too High (>120°)**: Work on consistent elbow position
            - Practice wall shooting to feel proper angle
            - Use shooting machine or partner for consistent repetition
            """)
        
        st.metric("🎪 Joint Alignment", f"{latest_metrics.elbow_alignment:.3f}", 
                help="Biomechanical alignment score (0.0-1.0)")
        with st.expander("📖 Elbow Alignment Analysis"):
            st.markdown("""
            **🎪 What it measures:** How well your elbow stays aligned under the basketball
            
            **📊 Alignment Quality:**
            - 🟢 **0.85+**: Perfect alignment - elbow directly under ball
            - 🟡 **0.70-0.84**: Good alignment with minor drift
            - 🟠 **0.50-0.69**: Moderate misalignment affecting accuracy
            - 🔴 **<0.50**: Poor alignment - major form issue
            
            **💡 Improvement Tips:**
            - Practice "elbow under ball" drill against a wall
            - Focus on starting position before each shot
            - Use mirror or video to check alignment
            - Strengthen shoulder muscles for better control
            """)
        
        st.metric("🔄 Consistency Index", f"{latest_metrics.consistency_score:.3f}", 
                help="Repeatability factor (0.0-1.0)")
        with st.expander("📖 Consistency Analysis"):
            st.markdown("""
            **🔄 What it measures:** How repeatable your shooting motion is across attempts
            
            **📊 Consistency Levels:**
            - 🟢 **0.85+**: Highly consistent - minimal variation
            - 🟡 **0.70-0.84**: Good consistency with room for improvement
            - 🟠 **0.50-0.69**: Moderate consistency - focus on fundamentals
            - 🔴 **<0.50**: Inconsistent - needs mechanical work
            
            **💡 Improvement Tips:**
            - Develop a consistent pre-shot routine
            - Practice the same shot 100+ times daily
            - Focus on muscle memory through repetition
            - Record yourself to identify inconsistencies
            - Work on mental focus and concentration
            """)

# Enhanced AI Coaching System with detailed analysis
st.markdown('<div class="subsection-header">🧠 AI Coach Recommendations</div>', unsafe_allow_html=True)

# Create detailed coaching analysis
tips = []
detailed_analysis = []

# Release Angle Analysis
if latest_metrics.release_angle < 85:
    tips.append("🚀 **ELEVATION PROTOCOL**: Increase release trajectory")
    detailed_analysis.append({
        "issue": "Low Release Angle",
        "current": f"{latest_metrics.release_angle:.1f}°",
        "target": "90-105°",
        "priority": "HIGH",
        "drills": [
            "Wall shooting drill - Focus on high release point",
            "Chair shooting - Shoot over an imaginary defender",
            "Form shooting close to basket with emphasis on arc"
        ]
    })
elif latest_metrics.release_angle > 120:
    tips.append("📐 **ANGLE OPTIMIZATION**: Reduce release angle for better accuracy")
    detailed_analysis.append({
        "issue": "High Release Angle",
        "current": f"{latest_metrics.release_angle:.1f}°",
        "target": "90-105°",
        "priority": "MEDIUM",
        "drills": [
            "Line shooting drill for consistent angle",
            "Focus on elbow position under ball",
            "Practice with shooting hand placement"
        ]
    })

# Elbow Alignment Analysis
if latest_metrics.elbow_alignment < 0.7:
    tips.append("🎯 **ALIGNMENT SEQUENCE**: Maintain elbow positioning directly under ball pathway")
    detailed_analysis.append({
        "issue": "Poor Elbow Alignment",
        "current": f"{latest_metrics.elbow_alignment:.3f}",
        "target": "0.85+",
        "priority": "HIGH",
        "drills": [
            "Wall drill - Elbow touches wall throughout shot",
            "Mirror practice for visual feedback",
            "Slow motion form shooting"
        ]
    })

# Balance Analysis
if latest_metrics.balance_score < 0.7:
    tips.append("⚖️ **STABILITY MODULE**: Engage core stabilization throughout motion sequence")
    detailed_analysis.append({
        "issue": "Balance Issues",
        "current": f"{latest_metrics.balance_score:.3f}",
        "target": "0.80+",
        "priority": "MEDIUM",
        "drills": [
            "Balance beam shooting practice",
            "Core strengthening exercises",
            "Single-leg shooting drills"
        ]
    })

# Follow-through Analysis
if latest_metrics.follow_through_angle < 45:
    tips.append("🔄 **EXTENSION PROTOCOL**: Maximize follow-through extension for enhanced accuracy")
    detailed_analysis.append({
        "issue": "Insufficient Follow-through",
        "current": f"{latest_metrics.follow_through_angle:.1f}°",
        "target": "60-80°",
        "priority": "MEDIUM",
        "drills": [
            "Exaggerated follow-through practice",
            "Hold follow-through for 2 seconds",
            "Focus on wrist snap and finger direction"
        ]
    })

# Consistency Analysis
if latest_metrics.consistency_score < 0.7:
    tips.append("🎯 **PRECISION ENHANCEMENT**: Develop consistent shooting mechanics")
    detailed_analysis.append({
        "issue": "Inconsistent Mechanics",
        "current": f"{latest_metrics.consistency_score:.3f}",
        "target": "0.80+",
        "priority": "HIGH",
        "drills": [
            "100 shots per day with same form",
            "Pre-shot routine development",
            "Mental visualization practice"
        ]
    })

# Display coaching tips
if tips:
    for tip in tips:
        st.markdown(f'<div class="coaching-tip">{tip}</div>', unsafe_allow_html=True)
    
    # Detailed analysis section
    if detailed_analysis:
        with st.expander("🎯 Detailed Analysis & Training Plan"):
            for analysis in detailed_analysis:
                priority_color = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
                st.markdown(f"""
                **{priority_color.get(analysis['priority'], '⚪')} {analysis['issue']}**
                - **Current**: {analysis['current']} | **Target**: {analysis['target']}
                - **Priority**: {analysis['priority']}
                
                **Recommended Drills:**
                """)
                for drill in analysis['drills']:
                    st.markdown(f"• {drill}")
                st.markdown("---")
else:
    st.markdown('''
    <div class="coaching-tip">
    🎉 **ELITE PERFORMANCE DETECTED!** 🎉<br><br>
    All biomechanical systems are operating at optimal parameters. Your shooting form demonstrates:<br>
    • ✅ Excellent release mechanics<br>
    • ✅ Superior body alignment<br>
    • ✅ Consistent motion patterns<br>
    • ✅ Optimal balance control<br><br>
    <strong>Maintenance Protocol:</strong><br>
    • Continue current training routine<br>
    • Focus on mental game and shot selection<br>
    • Practice under game-like conditions<br>
    • Maintain physical conditioning
    </div>
    ''', unsafe_allow_html=True)
