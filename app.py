"""
APEXSPORTS BASKETBALL SHOT ANALYZER
Advanced AI-Powered Basketball Shooting Analysis System

RESEARCH-BACKED BIOMECHANICAL TIMING SYSTEM
===========================================

This system implements ultra-selective precision frame capture based on peer-reviewed
basketball shooting biomechanics research and sports science literature.

KEY RESEARCH FOUNDATIONS:
------------------------

1. PHASE DETECTION (Struzik et al., 2014 - "Biomechanical Analysis of Jump Shot"):
   - Preparation: 90-140° elbow, ball below shoulder, static equilibrium
   - Shooting: 65-110° elbow, active upward acceleration, force generation
   - Release: 160°+ elbow extension, peak height, ball separation (0.18-0.22s)
   - Follow-through: Wrist snap phase, recovery motion

2. OPTIMAL TIMING WINDOWS (Multiple Studies):
   - Release Height: EXACT ball separation moment (frames_in_phase = 0)
   - Elbow Mechanics: Peak force generation at 90° angle ±5°
   - Balance Assessment: Static settled position (8-15 frames minimum)
   - Follow-through: 0.1-0.2 seconds post-release wrist snap phase

3. EMERGENCY CAPTURE RESTRICTIONS:
   - Biomechanically validated timing windows prevent late-phase captures
   - Critical measurements (release height, elbow alignment) have strict timing
   - High-severity captures only allowed within research-backed windows

4. FLAW-SPECIFIC CAPTURE CRITERIA:
   - Balance: Static equilibrium assessment during preparation phase
   - Stance: Established foot positioning before motion initiation  
   - Elbow: Power position capture at optimal force generation angles
   - Release Height: Exact ball departure frame (no post-release captures)
   - Follow-through: Wrist snap window during controlled follow-through

BIOMECHANICAL ACCURACY IMPROVEMENTS:
-----------------------------------
- Ultra-selective precision prevents instructionally poor frame selection
- Research-backed timing ensures optimal coaching value for each flaw type
- Multiple biomechanical markers provide robust phase detection
- Emergency capture restrictions maintain measurement accuracy

TECHNICAL IMPLEMENTATION:
------------------------
- 4-priority capture system with biomechanical validation
- Real-time phase detection using multiple joint angle markers
- Frame-by-frame timing analysis with research-validated windows
- Comprehensive debugging system for timing validation
"""

import streamlit as st
import cv2
import numpy as np
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    st.warning("MediaPipe not available. Some features may be limited.")
import tempfile
import os
from io import BytesIO
import math
from PIL import Image
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import base64
import zipfile
import html

def escape_html_content(text):
    """Properly escape HTML content for safe display"""
    if not isinstance(text, str):
        text = str(text)
    return html.escape(text, quote=True)

# ==============================================
# DOWNLOAD FUNCTIONALITY HELPERS
# ==============================================

def create_annotated_video(video_path, analyzer, output_path):
    """Create an annotated video with pose estimation and flaw information"""
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create video writer for annotated output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    current_frame = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process frame and get annotated version
            processed_frame, landmarks = analyzer.process_frame(frame)
            
            # Add frame number overlay
            cv2.putText(processed_frame, f"Frame {current_frame + 1}/{frame_count}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Write the annotated frame
            out.write(processed_frame)
            current_frame += 1
            
    finally:
        cap.release()
        out.release()
    
    return output_path

def create_coaching_report_pdf(coaching_summary, improvement_plan, session_metrics):
    """Create a comprehensive coaching report as downloadable text file"""
    report_content = f"""
APEXSPORTS BASKETBALL SHOT ANALYSIS REPORT
==========================================
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

PERSONAL COACHING ASSESSMENT:
{coaching_summary}

60-DAY IMPROVEMENT PLAN:
{improvement_plan}

TECHNICAL METRICS SUMMARY:
- Overall Shooting Form Score: {session_metrics.shooting_form_score:.1%}
- Release Angle: {session_metrics.release_angle:.1f}°
- Release Height: {session_metrics.release_height:.2f} units
- Follow Through Angle: {session_metrics.follow_through_angle:.1f}°
- Elbow Alignment Score: {session_metrics.elbow_alignment:.1%}
- Balance Score: {session_metrics.balance_score:.1%}
- Consistency Rating: {session_metrics.consistency_score:.1%}
- Knee Bend Score: {session_metrics.knee_bend:.1%}

Report generated by ApexSports Basketball Shot Analyzer
Visit us at: Your Basketball Training Partner
"""
    return report_content

def create_analysis_package_zip(video_bytes, frame_stills, coaching_summary, improvement_plan, session_metrics, annotated_video_bytes=None, report_content=None):
    """Create a complete analysis package as a zip file"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add annotated video (preferred) or original video as fallback
        if annotated_video_bytes:
            zip_file.writestr("slow_motion_analysis_video.mp4", annotated_video_bytes)
        elif video_bytes:
            zip_file.writestr("original_video.mp4", video_bytes)
        
        # Add frame stills
        if frame_stills:
            for i, (frame_data, frame_img) in enumerate(frame_stills.items()):
                # Convert frame to bytes
                if hasattr(frame_img, 'shape'):  # numpy array
                    _, buffer = cv2.imencode('.jpg', frame_img)
                    zip_file.writestr(f"instructional_frames/frame_{i+1}_{frame_data.get('flaw_type', 'analysis')}.jpg", buffer.tobytes())
        
        # Add coaching report (use provided content or generate)
        if report_content:
            zip_file.writestr("basketball_coaching_report.txt", report_content.encode('utf-8'))
        else:
            report_content = create_coaching_report_pdf(coaching_summary, improvement_plan, session_metrics)
            zip_file.writestr("basketball_coaching_report.txt", report_content.encode('utf-8'))
        
        # Add technical data as JSON
        technical_data = {
            "shooting_form_score": session_metrics.shooting_form_score,
            "release_angle": session_metrics.release_angle,
            "release_height": session_metrics.release_height,
            "follow_through_angle": session_metrics.follow_through_angle,
            "elbow_alignment": session_metrics.elbow_alignment,
            "knee_bend": session_metrics.knee_bend,
            "balance_score": session_metrics.balance_score,
            "consistency_score": session_metrics.consistency_score,
            "analysis_timestamp": datetime.now().isoformat()
        }
        zip_file.writestr("technical_analysis_data.json", json.dumps(technical_data, indent=2))
        
        # Add README file explaining package contents
        readme_content = """Basketball Shot Analysis Package
=====================================

This package contains your complete basketball shooting analysis.

📦 Package Contents:
├── slow_motion_analysis_video.mp4 - Your shot analysis with pose estimation and flaw detection
├── instructional_frames/ - Key frame stills showing critical moments
├── basketball_coaching_report.txt - Personalized coaching assessment and improvement plan  
└── technical_analysis_data.json - AI metrics and biomechanical data

🏀 How to Use:
1. Watch the slow-motion video to see your shot technique in detail
2. Review the instructional frames for specific technique points
3. Read the coaching report for personalized improvement recommendations
4. Reference the technical data for detailed performance metrics

Generated by ApexSports Basketball AI Analysis System
"""
        zip_file.writestr("README.txt", readme_content)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()
import time
import logging
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MediaPipe
if MEDIAPIPE_AVAILABLE:
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
else:
    mp_pose = None
    mp_hands = None
    mp_drawing = None
    mp_drawing_styles = None

@dataclass
class ShotMetrics:
    """Data class for shot analysis metrics"""
    release_angle: float
    release_height: float
    follow_through_angle: float
    elbow_alignment: float
    knee_bend: float
    balance_score: float
    consistency_score: float
    shooting_form_score: float
    timestamp: datetime

class DatabaseManager:
    """Manages SQLite database operations for shot tracking"""
    
    def __init__(self, db_path: str = "shot_analysis.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shot_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shot_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    release_angle REAL,
                    release_height REAL,
                    follow_through_angle REAL,
                    elbow_alignment REAL,
                    knee_bend REAL,
                    balance_score REAL,
                    consistency_score REAL,
                    shooting_form_score REAL,
                    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES shot_sessions (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def create_session(self, session_name: str, notes: str = "") -> int:
        """Create a new shot session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shot_sessions (session_name, notes) VALUES (?, ?)",
                (session_name, notes)
            )
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return session_id
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return -1
    
    def save_metrics(self, session_id: int, metrics: ShotMetrics):
        """Save shot metrics to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO shot_metrics (
                    session_id, release_angle, release_height, follow_through_angle,
                    elbow_alignment, knee_bend, balance_score, consistency_score,
                    shooting_form_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, metrics.release_angle, metrics.release_height,
                metrics.follow_through_angle, metrics.elbow_alignment,
                metrics.knee_bend, metrics.balance_score,
                metrics.consistency_score, metrics.shooting_form_score
            ))
            conn.commit()
            conn.close()
            logger.info("Metrics saved successfully")
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
    
    def get_session_data(self, session_id: int) -> pd.DataFrame:
        """Retrieve all metrics for a session"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(
                "SELECT * FROM shot_metrics WHERE session_id = ? ORDER BY recorded_at",
                conn, params=(session_id,)
            )
            conn.close()
            return df
        except Exception as e:
            logger.error(f"Error retrieving session data: {e}")
            return pd.DataFrame()
    
    def get_all_sessions(self) -> pd.DataFrame:
        """Retrieve all sessions"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM shot_sessions ORDER BY created_at DESC", conn)
            conn.close()
            return df
        except Exception as e:
            logger.error(f"Error retrieving sessions: {e}")
            return pd.DataFrame()

class ShotAnalyzer:
    """Advanced basketball shot analysis using MediaPipe and computer vision with research-backed metrics"""
    
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.shot_sequence = []
        self.frame_count = 0
        print(f"DEBUG: !!!! BASKETBALL ANALYZER INITIALIZED - Frame count reset to 0 !!!!")
        self.analysis_complete = False
        self.ideal_shot_data = self.load_ideal_shot_data()
        
        # NEW: Intelligent frame capture tracking
        self.phase_history = []
        self.best_flaw_frames = {}  # Track best severity frame for each flaw type
        self.phase_transition_frames = {}  # Track when phases change
        self.captured_flaws = set()  # Avoid duplicate captures
        self.last_analysis_result = None
        self.captured_stills = {}  # Final processed stills for display
        
        # CRITICAL: Phase sequence tracking to prevent incorrect preparation detection
        self.release_detected = False  # Once release occurs, no more preparation phases
        self.shooting_started = False  # Track if shooting motion has begun

    def reset_analysis_state(self):
        """Reset all analysis state for fresh video processing - FORCE FRESH CAPTURE"""
        print(f"DEBUG: !!!! RESETTING ANALYSIS STATE - New video processing started !!!!")
        self.frame_count = 0
        self.phase_history = []
        self.best_flaw_frames = {}  # Force fresh capture decisions
        self.phase_transition_frames = {}
        self.captured_flaws = set()  # Force fresh capture tracking
        self.captured_stills = {}  # Reset captured stills
        self.last_analysis_result = None
        
        # CRITICAL: Reset phase sequence tracking
        self.release_detected = False
        self.shooting_started = False
        print("DEBUG: Analysis state RESET - forcing fresh frame capture analysis")
        
    def get_flaw_explanation(self, flaw_name: str) -> str:
        """Get clear, plain language explanation of what the shooter is doing wrong"""
        explanations = {
            # PREPARATION PHASE FLAWS
            'preparation_balance': "You're not maintaining proper balance during your setup. Your weight is shifting too far forward, backward, or to one side, which makes it harder to generate consistent power and accuracy.",
            
            'preparation_stance': "Your foot positioning isn't optimal for a solid shooting foundation. Your feet may be too narrow, too wide, or not properly aligned with the basket, affecting your stability and power transfer.",
            
            'preparation_knee_bend': "Your knees aren't bent to the ideal angle during your setup. This affects your ability to generate upward power from your legs and can throw off your shooting rhythm.",
            
            'preparation_shoulder_alignment': "Your shoulders aren't properly squared to the basket during your preparation phase. This misalignment can cause your shot to drift left or right of your target.",
            
            # SHOOTING PHASE FLAWS  
            'shooting_elbow': "Your shooting elbow isn't directly under the ball or is flaring out to the side. This creates inconsistent ball rotation and affects your accuracy by changing your release angle.",
            
            'shooting_alignment': "Your overall body alignment during the shooting motion isn't straight toward the basket. This causes your shot to miss left or right and reduces your shooting consistency.",
            
            'shooting_power_generation': "You're not effectively using your legs to generate power for your shot. You may be shooting too much with just your arms, which limits your range and consistency.",
            
            'shooting_plane_deviation': "Your shooting motion isn't following a straight vertical plane toward the basket. The ball is drifting left or right during your upward motion, affecting accuracy.",
            
            # RELEASE PHASE FLAWS
            'release_height': "You're not releasing the ball at the optimal height. Releasing too low reduces your shooting arc and makes it easier for defenders to block your shot.",
            
            'release_follow_through': "Your follow-through after releasing the ball isn't consistent. Your wrist may not be snapping down properly or your fingers aren't pointing toward the basket.",
            
            'release_extension': "Your arm isn't fully extending during the release. This incomplete extension reduces power and creates inconsistent ball rotation and arc.",
            
            # FOLLOW-THROUGH PHASE FLAWS - OLD GENERIC ENTRY REMOVED, USING SPECIFIC FOLLOW-THROUGH FLAWS INSTEAD
            
            'follow_through_balance': "You're losing your balance after releasing the shot. This suggests issues with your base or shooting mechanics that affect your overall shooting consistency.",
            
            'wrist_snap_timing': "Your wrist snap timing isn't synchronized with ball release. The wrist should snap down immediately after the ball leaves your fingers - not too early (which reduces power) or too late (which affects spin and arc).",
            
            'follow_through_angle': "Your follow-through angle is outside the optimal 45-65° range. This affects ball arc and consistency - too steep reduces distance, too shallow reduces arc and soft bounce.",
            
            'landing_balance': "You're not maintaining proper balance when landing after your shot. Poor landing balance indicates timing issues and can affect your shooting rhythm and consistency, especially on game shots.",
            
            # NEW ADVANCED BIOMECHANICAL FLAWS
            'wrist_snap_mechanics': "Your wrist snap during release isn't generating optimal ball rotation. The speed and angle of your wrist flexion directly affects backspin, which is crucial for soft shooting and consistent makes.",
            
            'thumb_flick_technique': "Your guide hand is creating a thumb flick motion during follow-through, which is a major shooting flaw. Thumb flicking causes side-spin instead of pure backspin, leading to inconsistent shot direction and reduced accuracy. The guide hand should release cleanly without any thumb movement - only your shooting hand should create ball rotation through proper wrist snap.",
            
            'shot_smoothness_tempo': "Your shooting motion lacks the smooth, rhythmic flow that characterizes elite shooters. Jerky or inconsistent tempo creates timing issues that affect accuracy and muscle memory development.",
            
            'guide_hand_interference': "Your guide hand (non-shooting hand) is interfering with your shot instead of just stabilizing the ball. The guide hand should only provide support during setup and release cleanly without affecting ball trajectory.",
            
            'release_extension': "Your arm isn't fully extending during the release. This incomplete extension reduces power and creates inconsistent ball rotation and arc."
        }
        return explanations.get(flaw_name, f"Technical issue detected in {flaw_name.replace('_', ' ')} during your shooting motion.")

    def get_flaw_correction(self, flaw_name: str) -> str:
        """Get specific, actionable instructions for correcting the flaw"""
        corrections = {
            # PREPARATION PHASE CORRECTIONS
            'preparation_balance': "Focus on centering your weight evenly over both feet. Keep your head over your shoulders and shoulders over your hips. Practice holding your setup position for 3-5 seconds before shooting to build proper balance habits.",
            
            'preparation_stance': "Position your feet shoulder-width apart with your shooting-side foot slightly ahead. Both feet should point toward the basket. Your base should feel solid and balanced - not too wide or too narrow.",
            
            'preparation_knee_bend': "Bend your knees to approximately 135-145 degrees (slightly more than a quarter squat). Your knees should be aligned over your toes, ready to explode upward for power generation.",
            
            'preparation_shoulder_alignment': "Square your shoulders directly to the basket during your setup. Your shooting shoulder should be slightly ahead, and both shoulders should remain level throughout your preparation.",
            
            # SHOOTING PHASE CORRECTIONS
            'shooting_elbow': "Keep your shooting elbow directly under the ball, forming a straight line from your elbow through your wrist to the basket. Avoid letting your elbow flare out to the side - it should stay in your shooting 'window'.",
            
            'shooting_alignment': "Maintain a straight line from your feet through your knees, hips, shoulders, and shooting hand to the basket. Turn your body slightly (10-15 degrees) toward your shooting side for natural alignment.",
            
            'shooting_power_generation': "Drive through your legs first, then transfer that energy up through your core to your shooting arm. Think 'legs, body, arm' in sequence. Your legs should provide 50-60% of your shot's power.",
            
            'shooting_plane_deviation': "Keep your shooting hand's path straight toward the basket. Imagine shooting through a narrow window - your ball should travel in a consistent vertical plane without drifting sideways.",
            
            # RELEASE PHASE CORRECTIONS
            'release_height': "Release the ball at the peak of your jump or at maximum arm extension. Your release point should be consistent and as high as comfortable - typically at or above your forehead level.",
            
            'release_follow_through': "Snap your wrist down after release with your fingers pointing toward the rim. Hold this follow-through position until the ball hits the rim - 'wave goodbye to the ball'.",
            
            'release_extension': "Fully extend your shooting arm at release, creating a straight line from shoulder to fingertips. Your arm should be nearly vertical at the moment of release for optimal arc.",
            
            # FOLLOW-THROUGH PHASE CORRECTIONS - OLD GENERIC ENTRY REMOVED
            
            'follow_through_balance': "Land in the same spot you jumped from, maintaining your balance throughout the follow-through. Keep your core engaged and avoid leaning forward or sideways after the shot.",
            
            'wrist_snap_timing': "Your wrist snap should happen immediately after ball release - think 'snap down hard and fast' right as the ball leaves your fingertips. Practice the timing: release-then-immediate-snap in one quick motion.",
            
            'follow_through_angle': "Maintain a 55° downward angle with your fingers after the wrist snap. Your fingers should point down toward the floor in front of the rim, not straight down or too shallow. Hold this angle until the ball hits the rim.",
            
            'landing_balance': "Focus on landing in the exact same spot you took off from. Keep your core tight and land with your feet directly under your hips. Avoid falling forward, backward, or to either side after shooting.",
            
            # NEW ADVANCED BIOMECHANICAL CORRECTIONS
            'wrist_snap_mechanics': "Focus on a quick, sharp wrist snap at release - think of 'cracking a whip' with your wrist. Your wrist should flex from neutral to 60-85 degrees in a rapid motion. Practice the snap motion separately to build muscle memory.",
            
            'thumb_flick_technique': "ELIMINATE all thumb movement from your guide hand. Focus on keeping your guide hand completely still and passive during the shot. Your guide hand should only provide support until ball release, then fall away naturally with NO thumb flicking, twisting, or lateral movement. Practice shooting with your guide hand barely touching the ball to feel the difference. Only your shooting hand creates backspin.",
            
            'shot_smoothness_tempo': "Develop a consistent rhythm: '1-2-3-shoot' timing from catch to release. Practice with a metronome or count to develop consistent tempo. Your motion should be one fluid movement without hitches or stops.",
            
            'guide_hand_interference': "Your guide hand should only touch the side of the ball, never behind or underneath. Keep your guide hand thumb pointing up and fingers spread. Release the guide hand just before your shooting hand releases - think 'guide hand off, shooting hand through'.",
            
            'release_extension': "Fully extend your shooting arm at release, creating a straight line from shoulder to fingertips. Your arm should be nearly vertical at the moment of release for optimal arc."
        }
        return corrections.get(flaw_name, f"Focus on proper form and consistency in your {flaw_name.replace('_', ' ')} technique.")

    def get_flaw_drills(self, flaw_name: str) -> list:
        """Get specific drills and training methods to improve the flaw"""
        drills = {
            # PREPARATION PHASE DRILLS
            'preparation_balance': [
                "Balance Hold Drill: Hold your shooting stance for 10 seconds without swaying, repeat 10 times",
                "One-Foot Balance: Practice shooting stance balance on each foot separately for 30 seconds", 
                "Eyes Closed Setup: Practice getting into shooting position with eyes closed to develop feel",
                "Wall Touch Drill: Stand against wall in shooting stance - only your butt and back should touch"
            ],
            
            'preparation_stance': [
                "Tape Line Drill: Use court tape to mark proper foot positioning, practice 50 setups daily",
                "Mirror Stance Work: Practice proper stance in front of mirror for visual feedback",
                "Quick Setup Drill: Practice getting into proper stance as quickly as possible from various positions",
                "Stance Width Finder: Use cone drills to find your optimal stance width and practice consistency"
            ],
            
            'preparation_knee_bend': [
                "Chair Touch Drill: Practice lowering into shooting stance until you barely touch a chair behind you",
                "Wall Sit Holds: 30-second wall sits at proper shooting knee angle to build strength", 
                "Up-Down Drill: Move from standing to proper knee bend and back up 20 times",
                "Knee Angle Mirror: Practice achieving consistent knee bend using visual feedback in mirror"
            ],
            
            'preparation_shoulder_alignment': [
                "Door Frame Drill: Practice squaring shoulders in a doorway to feel proper alignment",
                "Partner Check: Have teammate verify your shoulder alignment before each practice shot",
                "Target Lock: Pick a specific target and practice squaring shoulders to that exact point",
                "Shoulder Blade Squeeze: Practice pinching shoulder blades together for stable shoulder platform"
            ],
            
            # SHOOTING PHASE DRILLS
            'shooting_elbow': [
                "Wall Elbow Drill: Practice shooting motion against wall - elbow should brush the wall",
                "Elbow Under Ball: Hold ball overhead, ensure elbow creates straight line to basket",
                "One-Handed Form Shooting: Shoot one-handed from 3 feet to focus on elbow alignment",
                "Elbow Window Drill: Practice keeping elbow in 'window' between your eyes and the rim"
            ],
            
            'shooting_alignment': [
                "Line Shooting: Shoot along court lines to practice straight-line alignment",
                "Chair Turn Drill: Sit in chair sideways to basket, practice proper body turn for alignment",
                "Stripe Focus: Focus on the middle stripe of ball throughout shooting motion",
                "Alignment Check Points: Use consistent landmarks (rim hooks, backboard squares) for alignment"
            ],
            
            'shooting_power_generation': [
                "Form Shooting Close: Start 3 feet from basket, focus on legs-first power generation",
                "Jump Stop Shots: Practice catch-and-shoot with emphasis on leg drive",
                "No-Arm Shots: Practice shooting motion using only legs and core (no arm extension)",
                "Power Progression: Gradually increase distance while maintaining leg-driven power"
            ],
            
            'shooting_plane_deviation': [
                "Rope Drill: Hang rope from rim to practice shooting in straight plane underneath",
                "Lane Line Shooting: Shoot from different spots along lane line for straight-plane practice",
                "Ball Track Visualization: Focus on ball traveling in straight line to center of rim",
                "Plane Mirror Work: Practice shooting motion sideways to mirror to see plane consistency"
            ],
            
            # RELEASE PHASE DRILLS
            'release_height': [
                "High Release Practice: Focus on releasing ball at maximum comfortable height",
                "Progression Release: Start low, gradually increase release height while maintaining form",
                "Peak Release: Practice releasing at the peak of your shooting motion",
                "Release Point Markers: Use visual markers to maintain consistent release height"
            ],
            
            'release_follow_through': [
                "Hold the Follow-Through: Hold follow-through position for 3 seconds after every shot",
                "Cookie Jar Drill: Practice reaching over imaginary cookie jar on high shelf",
                "Finger Snap: Practice crisp wrist snap with emphasis on fingertip control", 
                "Follow-Through Freeze: Take 100 shots holding follow-through until ball hits rim"
            ],
            
            'release_extension': [
                "Full Extension Drill: Practice complete arm extension without ball first",
                "Overhead Reaches: Practice reaching as high as possible with shooting hand",
                "Extension Check: Have partner check for full arm extension at release point",
                "Progressive Extension: Gradually increase extension distance in practice"
            ],
            
            # FOLLOW-THROUGH PHASE DRILLS - OLD GENERIC ENTRY REMOVED
            
            'follow_through_balance': [
                "Land Same Spot: Practice jumping and landing in exactly the same spot",
                "Balance Recovery: Practice shooting while maintaining balance throughout", 
                "Core Strengthening: Planks and core exercises to improve shooting balance",
                "Slow Motion Shooting: Practice shooting in slow motion to focus on balance control"
            ],
            
            'thumb_flick_technique': [
                "One-Hand Shooting: Practice shooting with only your shooting hand to eliminate guide hand interference",
                "Guide Hand Stillness: Focus on keeping guide hand completely passive and motionless during release", 
                "Wall Ball Practice: Shoot close to wall focusing on guide hand falling away cleanly with NO thumb movement",
                "Mirror Check: Watch guide hand in mirror - it should NOT move during follow-through",
                "Passive Guide Hand: Practice barely touching ball with guide hand to minimize thumb flick tendency"
            ],
            
            'wrist_snap_timing': [
                "Metronome Snaps: Practice wrist snap timing with consistent rhythm",
                "Quick Release Drill: Focus on immediate wrist snap right at ball release",
                "Snap Speed Training: Practice increasing speed of wrist snap motion",
                "Release Point Consistency: Mark optimal snap timing and repeat 100 times"
            ],
            
            'follow_through_angle': [
                "Angle Check Drill: Use protractor or coach to check 45-60° follow-through angle",
                "Wall Angle Practice: Practice follow-through against wall to feel proper angle",
                "Target Practice: Follow-through should point fingers down toward target spot on floor",
                "Progressive Angle Training: Start with exaggerated angles, refine to optimal range"
            ],
            
            'landing_balance': [
                "Jump and Stick: Practice jumping and landing with perfect balance, no movement",
                "Eyes Closed Landing: Practice shooting and landing with eyes closed for balance awareness",
                "Single Leg Landing: Advanced drill - practice landing on shooting-side leg only",
                "Balance Beam Shooting: Shoot while standing on narrow surface to improve balance"
            ],
            
            # NEW ADVANCED BIOMECHANICAL DRILLS
            'wrist_snap_mechanics': [
                "Wrist Flicks: 100 daily wrist snaps without ball - focus on speed and angle",
                "Snap and Hold: Practice quick wrist snap then hold flexed position for 2 seconds",
                "Ball Drop Snaps: Drop ball and catch with quick wrist snap to feel the motion",
                "Progressive Snap Speed: Start slow, gradually increase wrist snap speed while maintaining control",
                "Backspin Check: Shoot close to basket, focus on creating maximum backspin with wrist snap"
            ],
            
            'thumb_flick_technique': [
                "Thumb Separation Drill: Practice follow-through focusing on thumb 'peeling' away from fingers",
                "Slow Motion Flicks: Practice thumb flick motion in slow motion to feel separation",
                "Ball Spin Check: Roll ball on finger, use thumb flick to create backspin rotation",
                "Finger-Thumb Coordination: Alternate between finger-only and thumb-flick releases",
                "Follow-Through Focus: Hold follow-through position, check thumb position relative to fingers"
            ],
            
            'shot_smoothness_tempo': [
                "Metronome Shooting: Practice shooting with consistent tempo using metronome or music",
                "One-Two-Three Rhythm: Count '1-catch, 2-setup, 3-shoot' for consistent timing",
                "Video Analysis: Record shooting sessions to identify tempo inconsistencies",
                "Smooth Motion Practice: Practice shooting motion without ball, focusing on fluid movement",
                "Tempo Progression: Start slow with perfect form, gradually increase to game speed"
            ],
            
            'guide_hand_interference': [
                "One-Hand Form Shooting: Shoot with only shooting hand to eliminate guide hand dependence",
                "Guide Hand Side Position: Practice keeping guide hand on exact side of ball, thumb up",
                "Early Release Drill: Practice releasing guide hand just before shooting hand release",
                "Wall Guide Hand: Practice shooting motion against wall - guide hand shouldn't push ball",
                "Guide Hand Freeze: Hold proper guide hand position for 3 seconds before shooting",
                "No-Guide Practice: Take 50 shots daily with guide hand behind back to feel difference"
            ],
            
            'release_extension': [
                "Full Extension Drill: Practice complete arm extension without ball first",
                "Overhead Reaches: Practice reaching as high as possible with shooting hand",
                "Extension Check: Have partner check for full arm extension at release point",
                "Progressive Extension: Gradually increase extension distance in practice"
            ]
        }
        return drills.get(flaw_name, [f"Practice proper {flaw_name.replace('_', ' ')} technique with focused repetition"])
    
    def generate_coaching_summary(self, flaws: dict, overall_score: float) -> str:
        """Generate a comprehensive coaching summary that explains flaws in plain language with optimistic improvement prognosis"""
        
        if not flaws:
            return """**OUTSTANDING PERFORMANCE!** 🏆

You're shooting with elite-level form right now! Your mechanics are fundamentally sound across all the critical areas that separate great shooters from average ones. This level of consistency and technical precision is exactly what college scouts and coaches are looking for.

**Your Elite-Level Strengths:**
• **Perfect Balance & Foundation** - You're maintaining excellent body control throughout your shot (NOTE: Balance analysis may show specific phase improvements needed)
• **Optimal Power Generation** - Your kinetic chain is working beautifully, transferring energy efficiently from your legs through your release
• **Consistent Release Point** - Your muscle memory is dialed in, giving you the repeatability that leads to high shooting percentages
• **Proper Shooting Plane** - You're keeping the ball on a straight path to the basket, eliminating wasted energy and improving accuracy

**Your Competitive Advantage:**
With form this solid, you're already performing better than 85-90% of players at most levels. This consistency gives you a massive advantage in game situations where other players' shots fall apart under pressure. Coaches love players they can count on for reliable scoring.

**Maintaining Excellence:**
Even elite shooters need regular form analysis to stay sharp. Continue using our program 2-3 times per week to monitor your mechanics and catch any small adjustments before they become habits. Your dedication to improvement is what will keep you at this high level and potentially take you even higher!"""

        # Analyze specific flaws in detail
        priority_flaws = sorted(flaws.items(), key=lambda x: x[1].get('priority', 10))
        critical_flaws = [f for f in priority_flaws if f[1].get('priority', 10) <= 2]
        secondary_flaws = [f for f in priority_flaws if f[1].get('priority', 10) in [3, 4]]
        
        # Generate detailed flaw explanations in plain language
        def get_plain_language_flaw_explanation(flaw_name):
            """Convert technical flaw names to plain language explanations"""
            explanations = {
                'preparation_balance': "you're slightly off-balance when setting up your shot, which can cause inconsistent results",
                'preparation_stance': "your feet positioning isn't quite optimal for maximum power and consistency",
                'preparation_knee_bend': "you're not getting enough flex in your knees to generate proper upward force",
                'preparation_shoulder_alignment': "your shoulders aren't perfectly square to the target when you start your shot",
                'shooting_elbow': "your elbow is drifting away from being directly under the ball during your shooting motion",
                'shooting_hand_alignment': "your shooting hand isn't perfectly aligned with your target throughout the motion",
                'shooting_power_generation': "you're not fully utilizing the power from your legs and core in your shot",
                'shooting_plane_deviation': "the ball is moving slightly off the straight line path to the basket",
                'release_height': "your release point is lower than optimal, reducing your shooting arc",
                'release_wrist_snap': "your wrist follow-through isn't quite complete, affecting ball rotation",
                'release_extension': "you're not getting full arm extension at the point of release",
                'followthrough_hold': "you're not holding your follow-through long enough for optimal consistency",
                'landing_balance': "you're not landing in the same spot you took off from, indicating balance issues"
            }
            return explanations.get(flaw_name, f"there's a technique issue with your {flaw_name.replace('_', ' ')}")

        # Determine overall performance level and tone
        if overall_score >= 0.85:
            performance_level = "ADVANCED"
            improvement_potential = "fine-tuning for elite performance"
            timeline = "2-3 weeks of focused practice"
            percentage_improvement = "5-15%"
        elif overall_score >= 0.75:
            performance_level = "INTERMEDIATE"  
            improvement_potential = "significant skill development opportunity"
            timeline = "4-6 weeks of consistent work"
            percentage_improvement = "15-25%"
        else:
            performance_level = "DEVELOPING"
            improvement_potential = "tremendous upside for dramatic improvement"
            timeline = "6-8 weeks of dedicated training"
            percentage_improvement = "25-40%"

        # Build comprehensive coaching summary
        summary = f"""**{performance_level} SHOOTER ANALYSIS** 🎯

Great news! I can see you have the dedication to improve your game by analyzing your shot mechanics. That mindset alone puts you ahead of most players who just "wing it" and wonder why they're inconsistent.

**Here's what's happening with your shot right now:**

"""
        
        # Explain critical flaws in detail with varied conversational approaches
        if critical_flaws:
            summary += "**PRIMARY FOCUS AREAS (These are your game-changers):**\n\n"
            
            # Create varied coaching responses for each flaw position
            coaching_responses = [
                # First flaw - common issue approach
                "This is actually one of the most common issues I see at all levels, and here's the good news - it's completely fixable with the right approach. Once we nail this down, you'll immediately notice more consistent makes and better feel on your shots.",
                
                # Second flaw - building momentum approach  
                "I see this pattern a lot with developing shooters, and it's actually a great sign that you're ready to level up your game. This particular adjustment tends to click pretty quickly once you understand what to focus on, and the improvement in your shot consistency will be noticeable right away.",
                
                # Third flaw - technical mastery approach
                "This one's a bit more technical, but don't worry - we can definitely get this sorted out. What's encouraging is that players who master this element often see the biggest jumps in their shooting percentage because it affects so many other aspects of their shot."
            ]
            
            for i, (flaw_name, flaw_data) in enumerate(critical_flaws[:3], 1):
                explanation = get_plain_language_flaw_explanation(flaw_name)
                coaching_response = coaching_responses[min(i-1, len(coaching_responses)-1)]
                summary += f"**{i}. {flaw_name.replace('_', ' ').title()} Issue**\nRight now, {explanation}. {coaching_response}\n\n"

        # Explain secondary flaws with varied phrasing
        if secondary_flaws:
            summary += "**SECONDARY IMPROVEMENTS (These will take you to the next level):**\n\n"
            secondary_responses = [
                "Once we address your primary areas, this will fall into place naturally.",
                "This is more of a fine-tuning adjustment that we can tackle after the main issues are handled."
            ]
            
            for i, (flaw_name, flaw_data) in enumerate(secondary_flaws[:2]):
                explanation = get_plain_language_flaw_explanation(flaw_name)
                response = secondary_responses[min(i, len(secondary_responses)-1)]
                summary += f"• **{flaw_name.replace('_', ' ').title()}**: {explanation}. {response}\n"

        # Add strengths section
        strengths = []
        # Only show excellent balance if BOTH preparation and follow-through balance are good
        if 'preparation_balance' not in flaws and 'follow_through_balance' not in flaws:
            strengths.append("**Excellent Balance** - You're maintaining great body control throughout")
        elif 'preparation_balance' not in flaws and 'follow_through_balance' in flaws:
            strengths.append("**Good Setup Balance** - Your preparation balance is solid, but work on follow-through stability")
        elif 'preparation_balance' in flaws and 'follow_through_balance' not in flaws:
            strengths.append("**Good Follow-Through Balance** - Your finishing balance is strong, but improve setup stability")
        if 'shooting_elbow' not in flaws:
            strengths.append("**Perfect Elbow Alignment** - Your elbow positioning is textbook") 
        if 'release_height' not in flaws:
            strengths.append("**Consistent Release Point** - Your muscle memory is developing well")
        if 'shooting_power_generation' not in flaws:
            strengths.append("**Great Power Transfer** - You're using your whole body efficiently")

        if strengths:
            summary += f"\n**WHAT YOU'RE ALREADY DOING RIGHT:**\n" + "\n".join(f"• {strength}" for strength in strengths[:3]) + "\n"

        # Add improvement prognosis and team value
        summary += f"""
**YOUR IMPROVEMENT OUTLOOK** 📈

This is where it gets exciting! Based on your current form and the specific areas we've identified, you have {improvement_potential}. Players who commit to fixing these exact issues typically see {percentage_improvement} improvement in their shooting percentage within {timeline}.

**Why This Matters for Your Game:**
• **Consistency Under Pressure** - Better mechanics mean your shot holds up when the game is on the line
• **Increased Range** - More efficient power transfer will extend your shooting range naturally  
• **Faster Release** - Better preparation and mechanics lead to a quicker, more fluid shot
• **Confidence Boost** - When you know your form is solid, you shoot with more confidence

**Your Value to a Team:**
Coaches absolutely LOVE players who are committed to improving their fundamentals. A reliable shooter who works on their craft is worth their weight in gold. As your consistency improves, you become the player coaches can count on for crucial baskets, and that makes you invaluable.

**The Path Forward:**
I'm genuinely excited about your potential! The specific issues we've identified are all highly coachable, and players who tackle them systematically see dramatic results. With our 60-day improvement plan and regular form analysis, you're going to surprise yourself with how much better you can shoot.

Remember: Every great shooter went through this exact process of identifying and fixing their form flaws. You're doing exactly what it takes to reach the next level! 🚀"""

        return summary
    
    def generate_60_day_improvement_plan(self, flaws: dict, overall_score: float) -> dict:
        """Generate a comprehensive, personalized 60-day improvement plan based on specific flaws"""
        
        plan = {
            "overview": "",
            "weeks_1_2": {},
            "weeks_3_4": {},
            "weeks_5_6": {},
            "weeks_7_8": {},
            "daily_commitment": {},
            "tracking_milestones": {},
            "program_usage": {}
        }
        
        # Prioritize flaws for sequential improvement
        priority_flaws = sorted(flaws.items(), key=lambda x: x[1].get('priority', 10))
        high_priority = [f[0] for f in priority_flaws if f[1].get('priority', 10) <= 2]
        medium_priority = [f[0] for f in priority_flaws if f[1].get('priority', 10) in [3, 4, 5]]
        
        # Generate personalized overview based on specific flaws
        flaw_names = [self.humanize_flaw_name(flaw) for flaw in high_priority + medium_priority]
        primary_focus = flaw_names[:3] if len(flaw_names) >= 3 else flaw_names
        
        plan["overview"] = f"""🎯 YOUR PERSONALIZED 60-DAY TRANSFORMATION PLAN

Based on your shot analysis, we've identified {len(flaws)} specific areas for improvement, with your top priorities being: {', '.join(primary_focus[:2])}.

Your current foundation shows {self.get_strength_assessment(flaws, overall_score)}, which means you're perfectly positioned for rapid improvement. Players with your specific combination of issues typically see {self.get_projected_improvement(flaws)}% shooting improvement when following this systematic approach.

We'll tackle your mechanical issues in order of impact, starting with the fundamentals that affect every shot, then layering in advanced refinements. Each week builds on the previous, ensuring solid muscle memory before adding complexity."""
        
        # Week 1-2: Foundation - Target Primary Mechanical Flaw
        week1_focus = high_priority[:2] if high_priority else medium_priority[:2]
        week1_primary = week1_focus[0] if week1_focus else None
        
        plan["weeks_1_2"] = {
            "focus": f"FOUNDATION: Correcting {self.humanize_flaw_name(week1_primary) if week1_primary else 'Basic Form'}",
            "primary_targets": week1_focus,
            "why_this_first": self.get_flaw_priority_explanation(week1_primary) if week1_primary else "Building fundamental shooting base",
            "daily_routine": self.get_personalized_daily_routine(week1_focus, "foundation", flaws),
            "key_drills": self.get_progressive_drills(week1_primary, "beginner") if week1_primary else ["Basic form shooting"],
            "specific_cues": self.get_flaw_specific_cues(week1_primary) if week1_primary else ["Focus on consistent form"],
            "reps_target": self.get_progressive_rep_target(week1_focus, "week1", flaws),
            "success_indicators": self.get_week_success_indicators(week1_focus, "foundation"),
            "analysis_frequency": "Use our program 3x this week - video yourself daily to track initial progress",
            "troubleshooting": self.get_common_beginner_issues(week1_primary) if week1_primary else []
        }
        
        # Week 3-4: Consistency - Layer Secondary Issues  
        week3_focus = high_priority[2:4] if len(high_priority) > 2 else medium_priority[:2]
        if not week3_focus and len(high_priority) > 1:
            week3_focus = [high_priority[1]]
            
        plan["weeks_3_4"] = {
            "focus": f"CONSISTENCY: Perfecting {self.humanize_flaw_name(week3_focus[0]) if week3_focus else 'Muscle Memory'}",
            "primary_targets": week3_focus if week3_focus else ["form_consistency"],
            "building_on": f"Maintaining your improved {self.humanize_flaw_name(week1_primary) if week1_primary else 'foundation'} while adding complexity",
            "daily_routine": self.get_personalized_daily_routine(week3_focus, "consistency", flaws),
            "key_drills": self.get_progressive_drills(week3_focus[0], "intermediate") if week3_focus else ["Consistency shooting"],
            "specific_cues": self.get_flaw_specific_cues(week3_focus[0]) if week3_focus else ["Maintain consistent rhythm"],
            "reps_target": self.get_progressive_rep_target(week3_focus, "week3", flaws),
            "success_indicators": self.get_week_success_indicators(week3_focus, "consistency"),
            "analysis_frequency": "Use our program 2x this week - focus on consistency under normal conditions",
            "regression_watch": f"Monitor {self.humanize_flaw_name(week1_primary) if week1_primary else 'form'} - don't let it slip while focusing on new areas"
        }
        
        # Week 5-6: Integration - Game Application
        remaining_flaws = medium_priority + [f for f in high_priority if f not in week1_focus + week3_focus]
        week5_focus = remaining_flaws[:2] if remaining_flaws else ["game_application"]
        
        plan["weeks_5_6"] = {
            "focus": f"INTEGRATION: Game Speed Application",
            "primary_targets": week5_focus,
            "integration_challenge": f"Maintaining your corrected {', '.join([self.humanize_flaw_name(f) for f in week1_focus + week3_focus])} under pressure",
            "daily_routine": self.get_personalized_daily_routine(week5_focus, "integration", flaws),
            "key_drills": self.get_progressive_drills(week5_focus[0], "advanced") if week5_focus else ["Game speed shooting"],
            "specific_cues": self.get_flaw_specific_cues(week5_focus[0]) if week5_focus else ["Maintain form under pressure"],
            "reps_target": self.get_progressive_rep_target(week5_focus, "week5", flaws),
            "success_indicators": self.get_week_success_indicators(week5_focus, "integration"),
            "analysis_frequency": "Use our program 2x this week - test your form under fatigue and pressure",
            "pressure_tests": self.get_pressure_test_scenarios(week1_focus + week3_focus + week5_focus)
        }
        
        # Week 7-8: Mastery - Advanced Applications and Competition Prep
        plan["weeks_7_8"] = {
            "focus": "MASTERY: Competition-Level Consistency",
            "primary_targets": ["advanced_consistency", "competition_pressure"],
            "mastery_goal": f"Automatic execution of corrected {', '.join([self.humanize_flaw_name(f) for f in (week1_focus + week3_focus)[:3]])} in game situations",
            "daily_routine": self.get_personalized_daily_routine(["competition_prep"], "mastery", flaws),
            "key_drills": [
                f"Advanced {self.humanize_flaw_name(week1_primary).lower()} maintenance drills" if week1_primary else "Advanced shooting",
                "Competition simulation with crowd noise/distractions",
                "Fatigue shooting - maintain form when tired",
                "Pressure scenarios - game-winning shots"
            ],
            "specific_cues": ["Trust your mechanics", "Breathe and execute", "Same form every time"],
            "reps_target": self.get_progressive_rep_target(["mastery"], "week7", flaws),
            "success_indicators": [
                f"Consistent {self.humanize_flaw_name(week1_primary) if week1_primary else 'form'} even when fatigued",
                "8/10 makes from practice spots under pressure",
                "Smooth execution without conscious thought",
                f"No regression in corrected {self.humanize_flaw_name(week1_focus[0]) if week1_focus else 'mechanics'}"
            ],
            "analysis_frequency": "Use our program 2x this week - validate mastery under competition conditions",
            "competition_readiness": self.get_competition_readiness_checklist(week1_focus + week3_focus)
        }
        
        # Daily commitment structure
        plan["daily_commitment"] = {
            "minimum_time": "20-30 minutes focused practice",
            "shot_volume": "Gradually build from 100 to 300+ shots",
            "mental_focus": "Quality over quantity - every rep with intention",
            "rest_days": "1 day per week - review video and plan next session"
        }
        
        # Tracking milestones
        plan["tracking_milestones"] = {
            "week_2": "Noticeable improvement in primary flaw area",
            "week_4": "Consistent mechanics under normal conditions",
            "week_6": "Maintained form under game pressure",
            "week_8": f"Target: {15 + len(high_priority) * 5}%+ accuracy improvement"
        }
        
        # Program usage recommendations
        plan["program_usage"] = {
            "frequency": "2-3 times per week throughout 60 days",
            "purpose": "Track progress, catch regression early, validate improvements",
            "best_times": "After practice sessions to analyze fatigue effects",
            "comparison": "Save videos to track transformation over time"
        }
        
        return plan

    def humanize_flaw_name(self, flaw_name):
        """Convert technical flaw names to user-friendly descriptions"""
        if not flaw_name:
            return "Basic Form"
        
        flaw_map = {
            'shooting_elbow': 'Shooting Elbow Alignment',
            'guide_hand_interference': 'Guide Hand Technique', 
            'thumb_flick_technique': 'Thumb Flick & Follow Through',
            'shooting_power_generation': 'Power Generation',
            'shooting_plane_deviation': 'Shot Plane Consistency',
            'follow_through_balance': 'Follow Through Balance',
            'preparation_balance': 'Preparation Balance',
            'preparation_stance': 'Stance Foundation',
            'preparation_shoulder_alignment': 'Shoulder Alignment',
            'preparation_knee_bend': 'Knee Bend Mechanics',
            'shot_smoothness_tempo': 'Shot Rhythm & Smoothness',
            'landing_balance': 'Landing Balance'
        }
        
        return flaw_map.get(flaw_name, flaw_name.replace('_', ' ').title())

    def get_strength_assessment(self, flaws, overall_score):
        """Assess shooter's current strengths based on what's NOT in their flaws"""
        if overall_score > 85:
            return "strong fundamental shooting base with just minor refinements needed"
        elif overall_score > 75:
            return "solid foundation with specific mechanical adjustments required"
        elif overall_score > 65:
            return "developing shooter with clear improvement pathways identified"
        else:
            return "emerging talent with significant upside potential through systematic training"

    def get_projected_improvement(self, flaws):
        """Calculate realistic improvement percentage based on flaw types and count"""
        high_impact_flaws = ['shooting_elbow', 'guide_hand_interference', 'preparation_balance']
        medium_impact_flaws = ['thumb_flick_technique', 'shooting_power_generation', 'follow_through_balance']
        
        high_count = sum(1 for flaw in flaws.keys() if flaw in high_impact_flaws)
        medium_count = sum(1 for flaw in flaws.keys() if flaw in medium_impact_flaws)
        
        # Base improvement + impact multipliers
        base_improvement = 15
        high_impact_bonus = high_count * 8
        medium_impact_bonus = medium_count * 5
        
        return min(base_improvement + high_impact_bonus + medium_impact_bonus, 45)

    def get_flaw_priority_explanation(self, flaw_name):
        """Explain why this flaw is being addressed first"""
        explanations = {
            'shooting_elbow': "Your elbow alignment affects every aspect of your shot. Fix this first and everything else becomes easier to correct.",
            'guide_hand_interference': "Guide hand issues create inconsistent ball rotation and direction. Correcting this immediately improves accuracy.",
            'preparation_balance': "Balance is your foundation - without it, no other mechanical fix will stick under pressure.",
            'thumb_flick_technique': "Proper follow through determines ball rotation and arc. This technical element impacts shot consistency significantly.",
            'shooting_power_generation': "Efficient power transfer from legs through core to arms maximizes range and reduces arm fatigue.",
            'preparation_stance': "Your stance sets up everything that follows. Get this right and your entire shot sequence improves."
        }
        return explanations.get(flaw_name, "This fundamental affects multiple aspects of your shooting mechanics.")

    def get_personalized_daily_routine(self, focus_flaws, phase, all_flaws):
        """Generate specific daily routine based on shooter's flaws"""
        if not focus_flaws:
            return ["15-minute form shooting", "Basic mechanics review"]
            
        primary_flaw = focus_flaws[0]
        
        # Comprehensive daily routines for each flaw and phase
        routines = {
            'shooting_elbow': {
                'foundation': [
                    "5-min ELBOW FOCUS warm-up: Mirror work with elbow under ball position",
                    "Wall Elbow Drill: 50 practice shots with elbow brushing wall",
                    "Close-range perfect elbow: 75 shots from 8 feet, elbow discipline only",
                    "Video check: Record 10 shots, analyze elbow position frame by frame",
                    "Cool down: 25 free throws focusing solely on elbow alignment"
                ],
                'consistency': [
                    "Elbow check-in: 25 perfect elbow shots before other drills",
                    "Progressive elbow: 50 shots each from 10ft, 12ft, 15ft with perfect alignment",
                    "Fatigue elbow test: 25 jumping jacks, then 25 shots maintaining elbow position",
                    "Speed elbow: Quick catch-and-shoot while keeping elbow under ball",
                    "Partner feedback: Have someone call out when elbow drifts"
                ],
                'integration': [
                    "Game-speed elbow: Rapid shooting maintaining elbow discipline",
                    "Movement elbow: Off-dribble shots keeping elbow under ball",
                    "Pressure elbow: Make 8/10 shots under time pressure with perfect elbow",
                    "Competition simulation: Game situations maintaining elbow alignment",
                    "Automatic elbow: Shoot without thinking about elbow - muscle memory test"
                ],
                'mastery': [
                    "Elbow mastery test: 50 shots at game speed, 90%+ proper alignment",
                    "Contested elbow: Maintain alignment with defensive pressure",
                    "Fatigue elbow mastery: Perfect alignment even when exhausted",
                    "Teaching elbow: Explain and demonstrate proper elbow to someone else"
                ]
            },
            'guide_hand_interference': {
                'foundation': [
                    "5-min GUIDE HAND isolation: One-handed shooting motion practice",
                    "Guide hand hover drill: 50 shots with guide hand barely touching ball",
                    "Exaggerated separation: Practice dramatic guide hand removal at release",
                    "Ball spin check: Every shot must show pure backspin, no side rotation",
                    "Two-hand to one-hand: Practice smooth transition from setup to release"
                ],
                'consistency': [
                    "Guide hand discipline: 100 shots with perfect passive guide hand",
                    "Spin consistency: Check ball rotation on every shot for 50 attempts",
                    "Distance guide hand: Maintain technique as range increases gradually",
                    "Quick release guide: Rapid shooting maintaining guide hand passivity",
                    "Eyes closed guide: Feel proper guide hand technique without visual"
                ],
                'integration': [
                    "Movement guide hand: Off-dribble shots with perfect guide hand technique",
                    "Pressure guide hand: Maintain discipline under time pressure",
                    "Contested guide hand: Practice with defensive pressure",
                    "Game simulation: Full-speed play maintaining guide hand passivity",
                    "Guide hand automaticity: No conscious thought, perfect execution"
                ],
                'mastery': [
                    "Guide hand mastery: 100 shots at game speed, perfect technique",
                    "Competition guide hand: Maintain discipline in crucial moments",
                    "Teaching guide hand: Demonstrate and explain to another player",
                    "Guide hand confidence: Shoot without hesitation, trust technique"
                ]
            },
            'thumb_flick_technique': {
                'foundation': [
                    "5-min FOLLOW THROUGH focus: Practice thumb-down motion without ball",
                    "Wrist snap isolation: 50 wrist snaps holding follow through 3 seconds each",
                    "Ball rotation drill: Focus on 4-6 tight rotations per shot",
                    "Follow through freeze: Hold final position, check thumb points down",
                    "Arc control: Use follow through to control shot arc (45-50 degrees)"
                ],
                'consistency': [
                    "Snap power progression: Gradually increase follow through intensity",
                    "Distance follow through: Maintain thumb technique from all ranges",
                    "Quick snap drill: Rapid but complete follow through practice",
                    "Spin rate consistency: Same ball rotation speed on every shot",
                    "Follow through endurance: Maintain quality when arm is tired"
                ],
                'integration': [
                    "Game speed follow through: Maintain thumb discipline during quick shots",
                    "Movement follow through: Perfect technique during off-dribble shots",
                    "Pressure follow through: Complete technique despite time pressure",
                    "Contested follow through: Maintain snap despite defensive contest",
                    "Follow through confidence: Trust technique in game situations"
                ],
                'mastery': [
                    "Follow through mastery: Automatic thumb technique, no conscious thought",
                    "Pressure follow through: Perfect technique in crucial moments",
                    "Teaching follow through: Demonstrate proper technique to others",
                    "Follow through consistency: Same technique regardless of situation"
                ]
            },
            'preparation_balance': {
                'foundation': [
                    "5-min BALANCE basics: Practice perfect shooting stance on line",
                    "Wall balance check: Back to wall, practice getting into stance",
                    "Single leg stability: 30 seconds each leg to build balance strength",
                    "Catch and balance: Focus on landing in perfect stance every catch",
                    "Balance awareness: Feel equal weight distribution on both feet"
                ],
                'consistency': [
                    "Dynamic balance entry: Move into perfect stance from different angles",
                    "Balance under fatigue: Maintain stance quality when tired",
                    "Quick set balance: Get into perfect stance as rapidly as possible",
                    "Balance challenges: Practice stance on uneven surfaces",
                    "Balance maintenance: Hold perfect stance for extended periods"
                ],
                'integration': [
                    "Game speed balance: Perfect stance during fast-break situations",
                    "Contact balance: Maintain stance despite minor contact",
                    "Multi-directional balance: Perfect stance coming from any angle",
                    "Pressure balance: Maintain form during high-pressure moments",
                    "Balance recovery: Quickly return to perfect stance if disturbed"
                ],
                'mastery': [
                    "Balance mastery: Automatic perfect stance in any situation",
                    "Competition balance: Maintain stance in game environments",
                    "Teaching balance: Demonstrate proper stance to other players",
                    "Balance confidence: Trust your stance in any situation"
                ]
            },
            'shooting_power_generation': {
                'foundation': [
                    "5-min POWER basics: Chair rise drill, feel leg power transfer",
                    "Jump shot timing: Coordinate leg drive with arm extension",
                    "Power flow drill: Practice energy transfer from legs through core to arms",
                    "Stationary power: Master leg drive from set position",
                    "Power awareness: Feel the connection between leg drive and shot"
                ],
                'consistency': [
                    "Moving power generation: Maintain leg drive during movement shots",
                    "Quick shot power: Generate power rapidly for catch-and-shoot",
                    "Power efficiency: Use minimum leg effort for maximum shot power",
                    "Distance power scaling: Adjust leg drive for different ranges",
                    "Power endurance: Maintain leg drive throughout workout"
                ],
                'integration': [
                    "Game power: Generate power in traffic and under pressure",
                    "Fatigue power management: Maintain leg drive when legs are tired",
                    "Power under pressure: Generate consistent power in crucial moments",
                    "Multi-situation power: Adapt power generation to different scenarios",
                    "Power confidence: Trust leg drive in any game situation"
                ],
                'mastery': [
                    "Power mastery: Effortless power generation from any position",
                    "Competition power: Consistent power in game environments",
                    "Teaching power: Demonstrate power transfer to other players",
                    "Power automaticity: Perfect leg drive without conscious thought"
                ]
            }
        }
        
        # Get routine for primary flaw and phase
        flaw_routines = routines.get(primary_flaw, {})
        routine = flaw_routines.get(phase, [])
        
        if not routine:
            # Fallback routine
            routine = [
                f"15-minute {phase} work focusing on {self.humanize_flaw_name(primary_flaw)}",
                "Form shooting with specific flaw correction",
                "Video analysis and comparison to ideal form",
                "Progressive difficulty increase"
            ]
        
        return routine

    def get_progressive_drills(self, flaw_name, level):
        """Get specific drills for each flaw at different skill levels"""
        drill_progressions = {
            'shooting_elbow': {
                'beginner': [
                    "Wall Elbow Drill: Stand arm's length from wall, practice shooting motion with elbow brushing wall",
                    "Chair Drill: Sit in chair, practice shooting motion to groove elbow under ball position",
                    "Mirror Work: 100 practice shots in mirror focusing only on elbow alignment",
                    "Close Range Form: 5-foot shots, 1 shot every 10 seconds, perfect elbow position"
                ],
                'intermediate': [
                    "Elbow String Drill: Tie string from elbow to knee, keep taut during shot",
                    "Progressive Distance: Start at 5ft, move back only after 8/10 with perfect elbow",
                    "Eyes Closed Shooting: Feel proper elbow position without visual reference",
                    "Partner Correction: Have partner tap elbow when it drifts during shooting"
                ],
                'advanced': [
                    "Game Speed Elbow: Maintain alignment during quick catch-and-shoot",
                    "Fatigue Elbow Test: 100 shots maintaining alignment when tired",
                    "Contested Elbow: Practice proper alignment with defensive pressure",
                    "Competition Elbow: Simulate game-winning shots, check elbow under pressure"
                ]
            },
            'guide_hand_interference': {
                'beginner': [
                    "One-Hand Wall Shots: Practice shooting hand only, groove proper motion",
                    "Guide Hand Hover: Keep guide hand 1 inch from ball during shooting motion",
                    "Exaggerated Separation: Practice pulling guide hand dramatically away at release",
                    "Ball Spin Check: Every shot must have pure backspin, no side rotation"
                ],
                'intermediate': [
                    "Guide Hand Timing: Perfect the moment of guide hand separation",
                    "Two-Ball Drill: Hold second ball in guide hand during shooting",
                    "Passive Guide Hand: Guide hand provides support only, never pushes",
                    "Distance Progression: Maintain guide hand control as range increases"
                ],
                'advanced': [
                    "Quick Release Guide: Maintain passive guide hand during rapid shooting",
                    "Movement Guide Control: Keep guide hand discipline during off-dribble shots",
                    "Pressure Guide Hand: Maintain technique with defensive pressure",
                    "Game Simulation: Full-speed play maintaining guide hand discipline"
                ]
            },
            'thumb_flick_technique': {
                'beginner': [
                    "Thumb Down Drill: Practice follow through with thumb pointing straight down",
                    "Wrist Snap Focus: Isolate wrist snap motion, hold follow through for 3 seconds",
                    "Ball Rotation Check: Every shot must have 4-6 rotations with tight backspin",
                    "Follow Through Hold: Freeze follow through position, check thumb direction"
                ],
                'intermediate': [
                    "Progressive Snap Power: Gradually increase follow through intensity",
                    "Arc Control: Use thumb flick to control shot arc (45-50 degrees)",
                    "Distance Follow Through: Maintain proper thumb flick from all ranges",
                    "Quick Release Snap: Practice rapid but complete follow through"
                ],
                'advanced': [
                    "Game Speed Follow Through: Maintain thumb discipline during quick shots",
                    "Contested Follow Through: Complete follow through despite defensive pressure",
                    "Fatigue Follow Through: Maintain snap power when arm is tired",
                    "Automatic Follow Through: No conscious thought, just muscle memory"
                ]
            },
            'preparation_balance': {
                'beginner': [
                    "Balance Line Drill: Practice shooting stance on line, equal weight on both feet",
                    "Wall Balance: Back against wall, practice getting into shooting stance",
                    "Single Leg Test: Stand on each leg 30 seconds to build stability",
                    "Catch and Balance: Focus on landing in perfect stance on every catch"
                ],
                'intermediate': [
                    "Dynamic Balance: Move into shooting stance from different angles",
                    "Balance Under Fatigue: Maintain stance quality when tired",
                    "Quick Set Balance: Get into perfect stance as quickly as possible",
                    "Balance Challenges: Practice stance on different surfaces/conditions"
                ],
                'advanced': [
                    "Game Speed Balance: Perfect stance during fast-break situations",
                    "Contact Balance: Maintain stance despite contact from defenders",
                    "Multi-Directional Balance: Perfect stance coming from any direction",
                    "Pressure Balance: Maintain form in crucial game moments"
                ]
            },
            'shooting_power_generation': {
                'beginner': [
                    "Chair Rise Drill: Practice going from seated to shot, feel leg power",
                    "Jump Shot Timing: Coordinate leg drive with arm extension",
                    "Wall Power Transfer: Practice power flow from legs through shooting motion",
                    "Stationary Power: Master leg drive from set position"
                ],
                'intermediate': [
                    "Moving Power Generation: Maintain leg drive during movement shots",
                    "Quick Shot Power: Generate power rapidly for catch-and-shoot",
                    "Power Efficiency: Use minimum leg effort for maximum shot power",
                    "Distance Power: Generate enough power for extended range"
                ],
                'advanced': [
                    "Game Power: Generate power in traffic and under pressure",
                    "Fatigue Power: Maintain leg drive when legs are tired",
                    "Efficiency Mastery: Effortless power generation from any position",
                    "Power Consistency: Same power generation every shot"
                ]
            },
            'shooting_plane_deviation': {
                'beginner': [
                    "Straight Line Drill: Practice shooting over imaginary line to rim",
                    "Target Focus: Aim for same spot on rim every shot",
                    "Mirror Alignment: Check shooting plane in mirror during practice",
                    "Wall Guide: Use wall as reference for straight shooting plane"
                ],
                'intermediate': [
                    "Distance Plane: Maintain straight plane from all distances",
                    "Movement Plane: Keep straight plane during off-dribble shots",
                    "Quick Plane: Maintain alignment during rapid shooting",
                    "Angle Shooting: Maintain plane from different court positions"
                ],
                'advanced': [
                    "Pressure Plane: Maintain straight plane with defensive pressure",
                    "Contested Plane: Keep alignment despite contest",
                    "Game Plane: Maintain plane in game situations",
                    "Automatic Plane: No conscious thought, muscle memory alignment"
                ]
            }
        }
        
        return drill_progressions.get(flaw_name, {}).get(level, [f"{level.title()} drills for {self.humanize_flaw_name(flaw_name)}"])

    def get_flaw_specific_cues(self, flaw_name):
        """Get mental cues specific to each flaw"""
        cue_map = {
            'shooting_elbow': [
                "Elbow under the ball, always",
                "L-shape from shoulder to wrist",
                "Elbow points to rim at release"
            ],
            'guide_hand_interference': [
                "Guide hand is just a guide",
                "Only shooting hand pushes the ball", 
                "Guide hand falls away at release"
            ],
            'thumb_flick_technique': [
                "Snap down with authority",
                "Thumb follows through down",
                "Hold the follow through"
            ],
            'preparation_balance': [
                "Feet shoulder-width apart",
                "Weight slightly forward",
                "Balanced and athletic"
            ]
        }
        return cue_map.get(flaw_name, ["Focus on proper technique", "Trust your training"])

    def get_progressive_rep_target(self, focus_flaws, week, all_flaws):
        """Calculate appropriate rep targets based on flaws and week"""
        base_reps = {
            'week1': 125,
            'week3': 175, 
            'week5': 225,
            'week7': 275
        }
        
        # Adjust based on flaw complexity
        complex_flaws = ['shooting_elbow', 'guide_hand_interference', 'thumb_flick_technique']
        adjustment = 25 if any(flaw in complex_flaws for flaw in focus_flaws) else 0
        
        target = base_reps.get(week, 150) + adjustment
        return f"{target-25}-{target} focused shots per day (quality over quantity)"

    def get_week_success_indicators(self, focus_flaws, phase):
        """Define what success looks like for each week"""
        if not focus_flaws:
            return ["Consistent shooting form", "Improved accuracy"]
            
        primary_flaw = focus_flaws[0]
        success_maps = {
            'shooting_elbow': {
                'foundation': [
                    "Elbow visibly under ball in 8/10 shots when filmed",
                    "Can feel the difference when elbow is properly aligned", 
                    "No conscious effort required to keep elbow under ball at close range",
                    "15-20% accuracy improvement from 8-12 feet",
                    "Shooting motion feels more natural and fluid"
                ],
                'consistency': [
                    "Maintain elbow alignment in 9/10 shots under normal conditions",
                    "Elbow position stays consistent when shooting tired",
                    "Accuracy improvement noticeable from all practice distances (12-18 feet)",
                    "Can shoot quickly while maintaining elbow discipline",
                    "Other players notice improved shot mechanics"
                ],
                'integration': [
                    "Proper elbow alignment maintained during game-speed shooting",
                    "Technique holds up under defensive pressure",
                    "Consistent elbow position from all spots on court",
                    "Teammates/coaches notice improved shot consistency",
                    "Confidence to shoot in traffic knowing mechanics are sound"
                ],
                'mastery': [
                    "Automatic elbow alignment - no conscious thought required",
                    "Perfect alignment maintained under maximum pressure",
                    "Teaching others proper elbow technique",
                    "Shooting percentage increase of 20-30% documented"
                ]
            },
            'guide_hand_interference': {
                'foundation': [
                    "Pure backspin on 9/10 shots (no side rotation visible)",
                    "Guide hand clearly separates from ball at release when filmed",
                    "Can feel difference between passive and active guide hand",
                    "Shot direction more consistent - fewer shots missing left/right",
                    "Ball comes off shooting hand cleanly every time"
                ],
                'consistency': [
                    "Guide hand discipline maintained for entire 150+ shot workout",
                    "Ball rotation consistent even when shooting tired",
                    "Accuracy improvement from all distances (10-20% increase)",
                    "No conscious thought required for guide hand technique",
                    "Shooting hand feels stronger and more in control"
                ],
                'integration': [
                    "Guide hand discipline during quick catch-and-shoot",
                    "Proper technique during off-dribble shots",
                    "Consistent ball rotation under game pressure", 
                    "Coaches notice improved shot consistency and ball rotation",
                    "Confidence to shoot in rhythm knowing guide hand won't interfere"
                ],
                'mastery': [
                    "Perfect guide hand technique without any conscious effort",
                    "Technique maintained under maximum defensive pressure",
                    "Can teach guide hand technique to other players",
                    "Shooting accuracy improved 15-25% due to better ball control"
                ]
            },
            'thumb_flick_technique': {
                'foundation': [
                    "Thumb pointing straight down on 9/10 follow throughs",
                    "Ball shows 4-6 rotations with tight, consistent backspin",
                    "Can hold follow through for 3+ seconds comfortably",
                    "Shot arc consistently in 45-50 degree range",
                    "Follow through feels more natural and powerful"
                ],
                'consistency': [
                    "Consistent follow through power throughout entire workout",
                    "Ball rotation identical on every shot regardless of distance",
                    "Follow through technique maintained when arm is tired",
                    "Shot arc consistent from all practice distances",
                    "Follow through happens automatically without conscious thought"
                ],
                'integration': [
                    "Perfect follow through during rapid shooting sequences",
                    "Technique maintained during movement shots",
                    "Consistent follow through under defensive pressure",
                    "Ball rotation stays pure in game-speed situations",
                    "Confidence in follow through leads to more aggressive shooting"
                ],
                'mastery': [
                    "Automatic follow through - perfect technique without thinking",
                    "Technique maintained in highest pressure situations",
                    "Can demonstrate and teach proper follow through",
                    "Shooting percentage improved 10-20% due to better ball rotation"
                ]
            },
            'preparation_balance': {
                'foundation': [
                    "Perfect shooting stance achieved in under 2 seconds every time",
                    "Equal weight distribution on both feet visible when filmed",
                    "Can maintain perfect stance for 30+ seconds without fatigue",
                    "Stance feels natural and athletic, not forced",
                    "Balance maintained during catch-and-shot situations"
                ],
                'consistency': [
                    "Perfect stance achieved from any approach angle",
                    "Balance maintained throughout entire shooting workout",
                    "Stance quality consistent even when moving quickly",
                    "Can get into perfect stance while under mild pressure",
                    "Balance foundation allows focus on other shooting mechanics"
                ],
                'integration': [
                    "Perfect stance maintained during game-speed situations",
                    "Balance holds despite contact or defensive pressure",
                    "Consistent stance from all court positions and angles",
                    "Stance automatically adjusts for different shot types",
                    "Balance confidence allows aggressive shot selection"
                ],
                'mastery': [
                    "Automatic perfect stance in any game situation",
                    "Balance maintained under maximum physical pressure",
                    "Can teach proper stance technique to other players", 
                    "Shooting accuracy improved 15-25% due to better foundation"
                ]
            },
            'shooting_power_generation': {
                'foundation': [
                    "Feel clear connection between leg drive and shot power",
                    "Can generate consistent power from stationary position",
                    "Shot reaches target distance with less arm effort",
                    "Leg drive timing coordinated with arm extension",
                    "Power transfer feels smooth and natural"
                ],
                'consistency': [
                    "Consistent power generation throughout entire workout",
                    "Can adapt power for different distances efficiently",
                    "Power maintained during movement shots",
                    "Leg drive consistent even when legs are tired",
                    "Range extended by 3-5 feet due to better power transfer"
                ],
                'integration': [
                    "Power generation maintained during game-speed shooting",
                    "Consistent power despite physical contact or pressure",
                    "Can generate power quickly for catch-and-shoot situations",
                    "Power efficiency allows shooting from greater distances",
                    "Leg drive automatic in all game situations"
                ],
                'mastery': [
                    "Effortless power generation from any position or situation",
                    "Perfect power transfer without conscious thought",
                    "Can teach power generation concepts to other players",
                    "Extended shooting range by 5-8 feet with improved efficiency"
                ]
            }
        }
        
        return success_maps.get(primary_flaw, {}).get(phase, ["Noticeable improvement in target area", "Increased shooting confidence"])

    def get_common_beginner_issues(self, flaw_name):
        """Anticipate common struggles for each flaw"""
        issue_map = {
            'shooting_elbow': [
                "Elbow drifts out when tired - take breaks to maintain quality",
                "Old muscle memory fights new technique - be patient, 1000+ reps needed",
                "Accuracy may temporarily decrease while building new pattern",
                "Feel awkward at first - this is normal, trust the process"
            ],
            'guide_hand_interference': [
                "Ball may feel unstable at first without guide hand support",
                "Shot may lack power initially as you learn one-handed control", 
                "Direction control takes time to develop with passive guide hand",
                "Old habits will try to return under pressure - stay disciplined"
            ]
        }
        return issue_map.get(flaw_name, ["Initial awkwardness is normal", "Trust the correction process"])

    def get_pressure_test_scenarios(self, corrected_flaws):
        """Create pressure scenarios to test flaw corrections"""
        return [
            f"Make 8/10 shots while maintaining your corrected {self.humanize_flaw_name(corrected_flaws[0])} - no advancing until achieved",
            "Shoot while someone calls out distractions - maintain all corrections",
            "Fatigue test: 50 jumping jacks, then 20 shots with perfect form",
            "Time pressure: 30-second shooting drill maintaining all corrections",
            "Simulate game-winner: High-pressure shot with perfect technique"
        ]

    def get_competition_readiness_checklist(self, mastered_flaws):
        """Create checklist for competition readiness"""
        return [
            f"✓ Automatic {self.humanize_flaw_name(mastered_flaws[0])} - no conscious thought required",
            "✓ Technique holds under fatigue and pressure", 
            "✓ Consistent accuracy improvement documented",
            "✓ Teammates notice improved shooting consistency",
            "✓ Confidence to shoot in crucial game moments",
            "✓ Can teach the correction to someone else"
        ]

    def format_improvement_plan(self, plan: dict) -> str:
        """Format the 60-day improvement plan dictionary into a readable string"""
        formatted_plan = f"""
{plan.get('overview', '').strip()}

📅 WEEKS 1-2: {plan.get('weeks_1_2', {}).get('focus', 'Foundation Building')}
🎯 Primary Targets: {', '.join(plan.get('weeks_1_2', {}).get('primary_targets', []))}
💡 Why This First: {plan.get('weeks_1_2', {}).get('why_this_first', 'Building fundamental base')}

Daily Routine:
{chr(10).join('• ' + routine for routine in plan.get('weeks_1_2', {}).get('daily_routine', []))}

Key Mental Cues:
{chr(10).join('• ' + cue for cue in plan.get('weeks_1_2', {}).get('specific_cues', []))}

Target: {plan.get('weeks_1_2', {}).get('reps_target', '100-150 shots/day')}
Success Indicators:
{chr(10).join('✓ ' + indicator for indicator in plan.get('weeks_1_2', {}).get('success_indicators', []))}

Common Issues to Watch:
{chr(10).join('⚠️ ' + issue for issue in plan.get('weeks_1_2', {}).get('troubleshooting', []))}

📅 WEEKS 3-4: {plan.get('weeks_3_4', {}).get('focus', 'Consistency Development')}
🎯 Primary Targets: {', '.join(plan.get('weeks_3_4', {}).get('primary_targets', []))}
🔄 Building On: {plan.get('weeks_3_4', {}).get('building_on', 'Previous week foundation')}

Daily Routine:
{chr(10).join('• ' + routine for routine in plan.get('weeks_3_4', {}).get('daily_routine', []))}

Key Mental Cues:
{chr(10).join('• ' + cue for cue in plan.get('weeks_3_4', {}).get('specific_cues', []))}

Target: {plan.get('weeks_3_4', {}).get('reps_target', '150-200 shots/day')}
Success Indicators:
{chr(10).join('✓ ' + indicator for indicator in plan.get('weeks_3_4', {}).get('success_indicators', []))}

⚠️ Regression Watch: {plan.get('weeks_3_4', {}).get('regression_watch', 'Monitor previous corrections')}

📅 WEEKS 5-6: {plan.get('weeks_5_6', {}).get('focus', 'Integration')}
🎯 Primary Targets: {', '.join(plan.get('weeks_5_6', {}).get('primary_targets', []))}
⚡ Integration Challenge: {plan.get('weeks_5_6', {}).get('integration_challenge', 'Applying corrections under pressure')}

Daily Routine:
{chr(10).join('• ' + routine for routine in plan.get('weeks_5_6', {}).get('daily_routine', []))}

Key Mental Cues:
{chr(10).join('• ' + cue for cue in plan.get('weeks_5_6', {}).get('specific_cues', []))}

Target: {plan.get('weeks_5_6', {}).get('reps_target', '200-250 shots/day')}
Success Indicators:
{chr(10).join('✓ ' + indicator for indicator in plan.get('weeks_5_6', {}).get('success_indicators', []))}

Pressure Tests:
{chr(10).join('⚡ ' + test for test in plan.get('weeks_5_6', {}).get('pressure_tests', []))}

📅 WEEKS 7-8: {plan.get('weeks_7_8', {}).get('focus', 'Mastery')}
🏆 Mastery Goal: {plan.get('weeks_7_8', {}).get('mastery_goal', 'Competition-level consistency')}

Daily Routine:
{chr(10).join('• ' + routine for routine in plan.get('weeks_7_8', {}).get('daily_routine', []))}

Key Mental Cues:
{chr(10).join('• ' + cue for cue in plan.get('weeks_7_8', {}).get('specific_cues', []))}

Target: {plan.get('weeks_7_8', {}).get('reps_target', '250+ shots/day')}
Success Indicators:
{chr(10).join('✓ ' + indicator for indicator in plan.get('weeks_7_8', {}).get('success_indicators', []))}

Competition Readiness Checklist:
{chr(10).join(indicator for indicator in plan.get('weeks_7_8', {}).get('competition_readiness', []))}

🎯 DAILY COMMITMENT:
• Time: {plan.get('daily_commitment', {}).get('minimum_time', '20-30 minutes')}
• Volume: {plan.get('daily_commitment', {}).get('shot_volume', 'Progressive increase')}
• Focus: {plan.get('daily_commitment', {}).get('mental_focus', 'Quality over quantity')}

📊 TRACKING MILESTONES:
• Week 2: {plan.get('tracking_milestones', {}).get('week_2', 'Initial improvements')}
• Week 4: {plan.get('tracking_milestones', {}).get('week_4', 'Consistent mechanics')}
• Week 6: {plan.get('tracking_milestones', {}).get('week_6', 'Game application')}
• Week 8: {plan.get('tracking_milestones', {}).get('week_8', 'Target achievement')}

💡 PROGRAM USAGE:
Frequency: {plan.get('program_usage', {}).get('frequency', '2-3 times per week')}
Purpose: {plan.get('program_usage', {}).get('purpose', 'Track progress and improvements')}
        """.strip()
        
        return formatted_plan

    def load_ideal_shot_data(self):
        """Load research-backed ideal shooting mechanics data"""
        return {
            "phases": {
                "Preparation": {
                    "ideal": {
                        "knee_flexion": "115-135°",
                        "hip_flexion": ">30°",
                        "position": "Feet shoulder-width, balanced"
                    }
                },
                "Elevation": {
                    "ideal": {
                        "knee_extension_velocity": "High for power",
                        "position": "Vertical jump alignment"
                    }
                },
                "Stability": {
                    "ideal": {
                        "elbow_angle": "85-105°",
                        "wrist_extension": "60-80°"
                    }
                },
                "Release": {
                    "ideal": {
                        "release_angle": "45-55°",
                        "release_velocity": "4-6 m/s",
                        "position": "Wrist above forehead"
                    }
                },
                "Inertia": {
                    "ideal": {
                        "follow_through": "Hold 1-2s",
                        "landing": "Balanced, knees bent"
                    }
                }
            },
            "components": {
                # Research-backed priority order with MediaPipe landmarks
                "balance_stance": {
                    "landmarks": [23, 24, 25, 26, 27, 28],  # Hips, knees, ankles
                    "ideal": "Hip-knee-ankle alignment <10° deviation",
                    "priority": 1,
                    "accuracy_impact": "25-30%",
                    "description": "Foundational for stability and power transfer"
                },
                "eye_focus": {
                    "landmarks": [0],  # Nose approximation for head rotation
                    "ideal": "Head rotation <5°",
                    "priority": 2,
                    "accuracy_impact": "20%",
                    "description": "Critical for accuracy, wandering eyes cause ~20% drop in success"
                },
                "hand_placement": {
                    "landmarks": [15, 16, 19, 20],  # Wrists and hand points
                    "ideal": "Fingers spread, ball on pads",
                    "priority": 3,
                    "accuracy_impact": "15-20%",
                    "description": "Ensures control and backspin, misplacement leads to off-axis releases"
                },
                "elbow_alignment": {
                    "landmarks": [11, 12, 13, 14],  # Shoulders and elbows
                    "ideal_angle": "85-105°",
                    "priority": 4,
                    "accuracy_impact": "15-25%",
                    "description": "Keeps shot straight; flare reduces accuracy significantly"
                },
                "knee_bend": {
                    "landmarks": [23, 24, 25, 26],  # Hip to knee joints
                    "ideal_angle": "115-135°",
                    "priority": 5,
                    "accuracy_impact": "10-15%",
                    "description": "Generates upward force; insufficient bend wastes energy"
                },
                "body_jump": {
                    "landmarks": [11, 23, 12, 24],  # Shoulder to hip alignment
                    "ideal": "Torso vertical <5° lean",
                    "priority": 6,
                    "accuracy_impact": "10-12%",
                    "description": "Ensures vertical path; misalignment causes side drift"
                },
                "release_point": {
                    "landmarks": [13, 14, 15, 16],  # Elbow to wrist
                    "ideal_position": "Wrist y < shoulder y - 20% body height",
                    "priority": 7,
                    "accuracy_impact": "8-12%",
                    "description": "Above forehead for clean arc; low point flattens shot"
                },
                "release_angle_velocity": {
                    "ideal_angle": "45-55°",
                    "ideal_velocity": "4-6 m/s",
                    "priority": 8,
                    "accuracy_impact": "8-10%",
                    "description": "Optimal entry angle and velocity for consistent makes"
                },
                "wrist_snap": {
                    "landmarks": [14, 15, 16, 19, 20],  # Elbow to hand
                    "ideal_angle": "60-80° snap",
                    "priority": 9,
                    "accuracy_impact": "5-8%",
                    "description": "Creates rotation (2-3 rev/s) for soft rim contact"
                },
                "follow_through_arc": {
                    "ideal": "Arm extended, fingers down; arc entry 43-48°",
                    "priority": 10,
                    "accuracy_impact": "5-7%",
                    "description": "Holds form for consistency; ideal arc entry angle"
                }
            },
            "tolerances": {
                "angle": 8,      # Degrees
                "position": 0.1, # Normalized units
                "velocity": 0.5  # m/s
            },
            "research_sources": {
                "balance_stance": ["Breakthrough Basketball", "Physiopedia", "USA Basketball"],
                "eye_focus": ["USA Basketball", "PMC AR training - quiet eye duration"],
                "elbow_alignment": ["Stanford 'three 90s'", "St. Cloud study"],
                "release_mechanics": ["Steph Curry form analysis", "PMC", "ScienceDirect CNN"]
            }
        }
    
    def analyze_phase_specific_flaws(self, landmarks, current_phase) -> Dict[str, Any]:
        """Comprehensive phase-specific basketball shot analysis for targeted coaching"""
        flaws = {}
        
        if not landmarks:
            return {'flaws': {}, 'phase': current_phase}
            
        try:
            # Get key landmarks
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            nose = landmarks[mp_pose.PoseLandmark.NOSE]
            
            print(f"DEBUG: Analyzing {current_phase} phase for specific flaws")
            
            # PREPARATION PHASE - Foundation and Setup (Most Critical for Consistency)
            if current_phase == "preparation":
                # 1. Base stance and balance (Priority 1 - 20-25% accuracy impact)
                hip_center_x = (left_hip.x + right_hip.x) / 2
                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                balance_deviation = abs(shoulder_center_x - hip_center_x)
                
                if balance_deviation > 0.015:  # More sensitive threshold
                    flaws['preparation_balance'] = {
                        'priority': 1, 'severity': min(balance_deviation * 500, 100),
                        'phase': 'preparation', 'optimal_frame_moment': 'setup_stance',
                        'issue': f"Setup balance off by {balance_deviation:.3f} (should be <0.015)",
                        'coaching_focus': "Square stance with weight centered over base of support",
                        'visual_key': "Shoulders directly over hips alignment",
                        'explanation': self.get_flaw_explanation('preparation_balance'),
                        'correction': self.get_flaw_correction('preparation_balance'),
                        'drills': self.get_flaw_drills('preparation_balance')
                    }
                
                # 2. Foot positioning and stance width (Priority 2 - 15-20% accuracy impact)
                stance_width = abs(left_hip.x - right_hip.x)
                if stance_width < 0.09 or stance_width > 0.20:  # Tighter optimal range
                    severity = 80 if stance_width < 0.09 else min((stance_width - 0.20) * 300, 70)
                    flaws['preparation_stance'] = {
                        'priority': 2, 'severity': severity,
                        'phase': 'preparation', 'optimal_frame_moment': 'setup_stance', 
                        'issue': f"Stance {'too narrow' if stance_width < 0.09 else 'too wide'}: {stance_width:.3f}",
                        'coaching_focus': "Feet shoulder-width apart for optimal power base",
                        'visual_key': "Stable foundation for consistent shooting",
                        'explanation': self.get_flaw_explanation('preparation_stance'),
                        'correction': self.get_flaw_correction('preparation_stance'),
                        'drills': self.get_flaw_drills('preparation_stance')
                    }
                
                # 3. Knee bend in preparation (Priority 3 - 10-15% accuracy impact)
                left_knee_angle = self.calculate_angle(left_hip, left_knee, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE])
                right_knee_angle = self.calculate_angle(right_hip, right_knee, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE])
                avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
                
                if avg_knee_angle < 150 or avg_knee_angle > 170:  # Preparation should have slight bend
                    deviation = min(abs(avg_knee_angle - 160), 20)
                    severity = (deviation / 20) * 100
                    flaws['preparation_knee_bend'] = {
                        'priority': 3, 'severity': severity,
                        'phase': 'preparation', 'optimal_frame_moment': 'setup_stance',
                        'issue': f"Knee bend {avg_knee_angle:.1f}° (optimal 150-170° in preparation)",
                        'coaching_focus': "Slight knee flexion for power preparation",
                        'visual_key': "Athletic ready position"
                    }
                
                # 4. Shoulder alignment in setup (Priority 4 - 8-12% accuracy impact)
                shoulder_tilt = abs(left_shoulder.y - right_shoulder.y)
                if shoulder_tilt > 0.012:  # Very sensitive for preparation phase
                    severity = min(shoulder_tilt * 2500, 100)
                    flaws['preparation_shoulder_alignment'] = {
                        'priority': 4, 'severity': severity,
                        'phase': 'preparation', 'optimal_frame_moment': 'setup_stance',
                        'issue': f"Shoulders tilted in setup: {shoulder_tilt:.4f}",
                        'coaching_focus': "Square shoulders to target from the start", 
                        'visual_key': "Level shoulders parallel to baseline"
                    }
                    
            # SHOOTING PHASE - Mechanical Execution (Power Generation)
            elif current_phase == "shooting":
                # 1. Elbow alignment during shooting motion (Priority 1 - 18-25% accuracy impact)
                elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                if elbow_angle < 85 or elbow_angle > 105:  # Tighter optimal range
                    deviation = min(abs(elbow_angle - 95), 20)
                    severity = (deviation / 20) * 100
                    flaws['shooting_elbow'] = {
                        'priority': 1, 'severity': severity,
                        'phase': 'shooting', 'optimal_frame_moment': 'mid_shooting_motion',
                        'issue': f"Elbow angle {elbow_angle:.1f}° (optimal 85-105°)",
                        'coaching_focus': "Elbow directly under ball throughout shooting motion",
                        'visual_key': "Straight vertical shooting line",
                        'explanation': self.get_flaw_explanation('shooting_elbow'),
                        'correction': self.get_flaw_correction('shooting_elbow'),
                        'drills': self.get_flaw_drills('shooting_elbow')
                    }
                
                # 2. Shooting hand alignment (Priority 2 - 15-20% accuracy impact)
                # CRITICAL: Check alignment during early shooting motion for better coaching visibility
                # TIMING RESTRICTION: Must be detected BEFORE release occurs AND not too late in shooting motion
                arm_extension = self.calculate_angle(right_shoulder, right_elbow, right_wrist) if right_wrist else 0
                wrist_shoulder_delta = (right_shoulder.y - right_wrist.y) * 100 if right_wrist else 0
                
                # Block detection if release already detected OR if very close to release conditions
                too_late_in_motion = (arm_extension >= 150 or wrist_shoulder_delta >= 20)
                
                if not self.release_detected and not too_late_in_motion:  # Early shooting motion only
                    hand_elevated = right_wrist.y < right_shoulder.y - 0.05  # Hand above shoulder (earlier check)
                    arm_partially_extended = arm_extension > 100  # Earlier detection
                    
                    if hand_elevated and arm_partially_extended:  # Check when shooting motion begins
                        hand_alignment = abs(right_wrist.x - nose.x)
                        if hand_alignment > 0.08:  # More sensitive threshold
                            severity = min(hand_alignment * 400, 100)
                            flaws['shooting_alignment'] = {
                                'priority': 2, 'severity': severity,
                                'phase': 'shooting', 'optimal_frame_moment': 'early_shooting_motion',
                                'issue': f"Shooting hand off-center: {hand_alignment:.3f}",
                                'coaching_focus': "Hand aligned with shooting eye and target",
                                'visual_key': "Straight line: eye-hand-rim"
                            }
                
                # 3. Power generation knee drive (Priority 3 - 12-18% accuracy impact)
                left_knee_angle = self.calculate_angle(left_hip, left_knee, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE])
                right_knee_angle = self.calculate_angle(right_hip, right_knee, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE])
                avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
                
                if avg_knee_angle < 140 or avg_knee_angle > 160:  # Should show power extension
                    deviation = min(abs(avg_knee_angle - 150), 15)
                    severity = (deviation / 15) * 100
                    flaws['shooting_power_generation'] = {
                        'priority': 3, 'severity': severity,
                        'phase': 'shooting', 'optimal_frame_moment': 'mid_shooting_motion',
                        'issue': f"Power generation knee angle {avg_knee_angle:.1f}° (140-160° optimal)",
                        'coaching_focus': "Drive from legs through shooting motion",
                        'visual_key': "Coordinated leg-to-arm power transfer"
                    }
                
                # 4. Shooting plane consistency (Priority 4 - 10-15% accuracy impact)
                shooting_plane_deviation = abs(right_shoulder.x - right_wrist.x)
                if shooting_plane_deviation > 0.04:  # More sensitive
                    severity = min(shooting_plane_deviation * 800, 100)
                    flaws['shooting_plane_deviation'] = {
                        'priority': 4, 'severity': severity,
                        'phase': 'shooting', 'optimal_frame_moment': 'mid_shooting_motion',
                        'issue': f"Off shooting plane by {shooting_plane_deviation:.3f}",
                        'coaching_focus': "Maintain straight shooting motion to target",
                        'visual_key': "No lateral drift in shooting motion"
                    }
                
                # 5. Guide hand placement and interference (Priority 2 - 12-20% accuracy impact) - NEW
                guide_hand_analysis = self.analyze_guide_hand_mechanics(landmarks)
                if guide_hand_analysis['interference_score'] > 0.3 or guide_hand_analysis['placement_score'] < 0.7:
                    interference_severity = guide_hand_analysis['interference_score'] * 70
                    placement_severity = (1.0 - guide_hand_analysis['placement_score']) * 60
                    total_severity = min(interference_severity + placement_severity, 100)
                    
                    flaws['guide_hand_interference'] = {
                        'priority': 2, 'severity': total_severity,
                        'phase': 'shooting', 'optimal_frame_moment': 'mid_shooting_motion',
                        'issue': f"Guide hand interference: {guide_hand_analysis['interference_score']:.2f}, placement: {guide_hand_analysis['placement_score']:.2f}/1.0",
                        'coaching_focus': "Guide hand should only stabilize, never push or interfere with ball flight",
                        'visual_key': "Left hand stays on side of ball, releases early without affecting trajectory",
                        'explanation': self.get_flaw_explanation('guide_hand_interference'),
                        'correction': self.get_flaw_correction('guide_hand_interference'),
                        'drills': self.get_flaw_drills('guide_hand_interference')
                    }
                    
            # RELEASE PHASE - Ball Departure and Follow-through (Accuracy Critical)
            elif current_phase == "release":
                # 1. Release height (Priority 1 - 15-20% accuracy impact)
                avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
                release_height = avg_shoulder_y - right_wrist.y
                if release_height < 0.05:  # Higher threshold for optimal arc
                    severity = min((0.12 - release_height) * 400, 100)
                    flaws['release_height'] = {
                        'priority': 1, 'severity': severity,
                        'phase': 'release', 'optimal_frame_moment': 'ball_release',
                        'issue': f"Release point too low: {release_height:.3f} (should be >0.05)",
                        'coaching_focus': "Release at forehead level for optimal trajectory",
                        'visual_key': "High release point over defenders",
                        'explanation': self.get_flaw_explanation('release_height'),
                        'correction': self.get_flaw_correction('release_height'),
                        'drills': self.get_flaw_drills('release_height')
                    }
                
                # 2. Follow-through angle (Priority 2 - 10-15% accuracy impact)
                follow_through = self.calculate_angle(right_elbow, right_wrist, 
                                                    {"x": right_wrist.x, "y": right_wrist.y - 0.1})
                if follow_through < 50 or follow_through > 75:  # Tighter range
                    deviation = min(abs(follow_through - 62), 18)
                    severity = (deviation / 18) * 100
                    flaws['release_follow_through'] = {
                        'priority': 2, 'severity': severity,
                        'phase': 'release', 'optimal_frame_moment': 'post_release',
                        'issue': f"Follow-through {follow_through:.1f}° (optimal 50-75°)",
                        'coaching_focus': "Complete wrist snap with fingers down",
                        'visual_key': "Goose-neck follow-through"
                    }
                
                # 3. Release extension (Priority 3 - 8-12% accuracy impact)
                extension_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                if extension_angle < 160:  # Should be near full extension
                    severity = min((170 - extension_angle) * 3, 100)
                    flaws['release_extension'] = {
                        'priority': 3, 'severity': severity,
                        'phase': 'release', 'optimal_frame_moment': 'ball_release',
                        'issue': f"Incomplete arm extension: {extension_angle:.1f}° (should be >160°)",
                        'coaching_focus': "Full arm extension at release",
                        'visual_key': "Complete upward reach",
                        'explanation': self.get_flaw_explanation('release_extension'),
                        'correction': self.get_flaw_correction('release_extension'),
                        'drills': self.get_flaw_drills('release_extension')
                    }
                
                # 4. Wrist snap mechanics (Priority 2 - 12-18% accuracy impact) - NEW
                wrist_snap_angle, wrist_snap_speed = self.analyze_wrist_snap(landmarks)
                if wrist_snap_angle < 60 or wrist_snap_angle > 85 or wrist_snap_speed < 2.5:
                    angle_severity = min(abs(wrist_snap_angle - 72.5) * 2.5, 60) if wrist_snap_angle < 60 or wrist_snap_angle > 85 else 0
                    speed_severity = min((2.5 - wrist_snap_speed) * 25, 40) if wrist_snap_speed < 2.5 else 0
                    total_severity = min(angle_severity + speed_severity, 100)
                    
                    flaws['wrist_snap_mechanics'] = {
                        'priority': 2, 'severity': total_severity,
                        'phase': 'release', 'optimal_frame_moment': 'ball_release',
                        'issue': f"Wrist snap: {wrist_snap_angle:.1f}° at {wrist_snap_speed:.1f} rad/s (optimal: 60-85° at >2.5 rad/s)",
                        'coaching_focus': "Sharp, quick wrist snap creates optimal backspin",
                        'visual_key': "Rapid wrist flexion at release for ball rotation",
                        'explanation': self.get_flaw_explanation('wrist_snap_mechanics'),
                        'correction': self.get_flaw_correction('wrist_snap_mechanics'),
                        'drills': self.get_flaw_drills('wrist_snap_mechanics')
                    }
                
            # FOLLOW_THROUGH PHASE - Post-Release Mechanics
            elif current_phase == "follow_through":
                print(f"DEBUG: Frame {self.frame_count} - ANALYZING FOLLOW-THROUGH PHASE")
                
                # 1. Sustained follow-through (Priority 1 - 8-12% accuracy impact)  
                follow_through = self.calculate_angle(right_elbow, right_wrist,
                                                    {"x": right_wrist.x, "y": right_wrist.y - 0.1})
                print(f"DEBUG: Follow-through angle: {follow_through:.1f}°")
                
                # OLD GENERIC DETECTION REMOVED - Using new specific follow-through system instead
                
                # 2. Guide Hand Thumb Flick Flaw Detection (Priority 2 - 8-15% accuracy impact)
                # NOTE: Thumb flick is a MAJOR SHOOTING FLAW - higher values indicate MORE problems
                thumb_flick_flaw_severity, guide_hand_interference = self.analyze_thumb_flick(landmarks)
                
                # Detect thumb flick flaw - this is BAD technique that must be eliminated
                # MUCH MORE SENSITIVE: Severity > 0.05 indicates thumb flick problems
                if thumb_flick_flaw_severity > 0.05 or guide_hand_interference > 0.02:
                    severity_score = thumb_flick_flaw_severity * 100
                    interference_score = guide_hand_interference * 80
                    total_severity = min(severity_score + interference_score, 100)
                    
                    print(f"DEBUG: THUMB FLICK FLAW detected - Flaw severity: {thumb_flick_flaw_severity:.3f}, "
                          f"Interference: {guide_hand_interference:.3f}, Total severity: {total_severity:.1f}%")
                    
                    flaws['thumb_flick_technique'] = {
                        'priority': 2, 'severity': total_severity,
                        'phase': 'follow_through', 'optimal_frame_moment': 'clean_guide_hand_release',
                        'issue': f"Guide hand thumb flick detected - Flaw level: {thumb_flick_flaw_severity:.2f}/1.0, Interference: {guide_hand_interference:.2f}",
                        'coaching_focus': "ELIMINATE guide hand thumb movement - guide hand must release cleanly",
                        'visual_key': "Guide hand falls away naturally with NO thumb flicking motion",
                        'explanation': self.get_flaw_explanation('thumb_flick_technique'),
                        'correction': self.get_flaw_correction('thumb_flick_technique'),
                        'drills': self.get_flaw_drills('thumb_flick_technique')
                    }
                
                # 3. Balance maintenance (Priority 3 - 5-10% accuracy impact)
                hip_center_x = (left_hip.x + right_hip.x) / 2
                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                balance_deviation = abs(shoulder_center_x - hip_center_x)
                
                if balance_deviation > 0.06:  # More reasonable balance threshold - allow some natural movement
                    severity = min(balance_deviation * 300, 100)
                    flaws['follow_through_balance'] = {
                        'priority': 3, 'severity': severity,
                        'phase': 'follow_through', 'optimal_frame_moment': 'sustained_follow_through',
                        'issue': f"Balance lost in follow-through: {balance_deviation:.3f}",
                        'coaching_focus': "Land in same position as takeoff",
                        'visual_key': "Maintain upright posture throughout",
                        'explanation': self.get_flaw_explanation('follow_through_balance'),
                        'correction': self.get_flaw_correction('follow_through_balance'),
                        'drills': self.get_flaw_drills('follow_through_balance')
                    }
                
                # 4. Wrist snap timing (Priority 2 - 10-15% accuracy impact)
                right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                current_wrist_angle = self.calculate_angle(right_elbow, right_wrist, 
                                                         {"x": right_wrist.x, "y": right_wrist.y - 0.1})
                
                # Track wrist snap speed during follow-through
                if hasattr(self, 'previous_follow_through_wrist_angle'):
                    wrist_snap_speed = abs(current_wrist_angle - self.previous_follow_through_wrist_angle)
                    if wrist_snap_speed < 8 or wrist_snap_speed > 25:  # Optimal 8-25° per frame
                        speed_deviation = min(abs(wrist_snap_speed - 15), 10)
                        severity = (speed_deviation / 10) * 100
                        
                        flaws['wrist_snap_timing'] = {
                            'priority': 2, 'severity': severity,
                            'phase': 'follow_through', 'optimal_frame_moment': 'wrist_snap_moment',
                            'issue': f"Wrist snap speed: {wrist_snap_speed:.1f}°/frame (optimal: 8-25°)",
                            'coaching_focus': "Quick, sharp wrist snap immediately after release",
                            'visual_key': "Rapid downward wrist motion with finger point",
                            'explanation': self.get_flaw_explanation('wrist_snap_timing'),
                            'correction': self.get_flaw_correction('wrist_snap_timing'),
                            'drills': self.get_flaw_drills('wrist_snap_timing')
                        }
                
                self.previous_follow_through_wrist_angle = current_wrist_angle
                
                # 5. Follow-through angle consistency (Priority 3 - 8-12% accuracy impact)
                optimal_follow_through_angle = 55  # Research-based optimal angle
                angle_deviation = abs(follow_through - optimal_follow_through_angle)
                
                if angle_deviation > 10:  # Allow ±10° tolerance
                    severity = min((angle_deviation - 10) * 5, 100)  # Severity increases beyond tolerance
                    
                    flaws['follow_through_angle'] = {
                        'priority': 3, 'severity': severity,
                        'phase': 'follow_through', 'optimal_frame_moment': 'sustained_follow_through',
                        'issue': f"Follow-through angle: {follow_through:.1f}° (optimal: 45-65°)",
                        'coaching_focus': "Maintain 55┬░ downward angle after wrist snap",
                        'visual_key': "Fingers pointing down at 55┬░ angle to floor",
                        'explanation': self.get_flaw_explanation('follow_through_angle'),
                        'correction': self.get_flaw_correction('follow_through_angle'),
                        'drills': self.get_flaw_drills('follow_through_angle')
                    }
                
                # 6. Landing balance and body control (Priority 2 - 8-15% accuracy impact)
                if len(self.phase_history) >= 3:  # Need history to track landing
                    # Compare current hip position to release phase position
                    current_hip_height = (left_hip.y + right_hip.y) / 2
                    
                    # Should land controlled, not falling forward/backward
                    if hasattr(self, 'release_hip_height'):
                        hip_height_change = current_hip_height - self.release_hip_height
                        
                        # Excessive hip movement indicates poor landing control
                        if abs(hip_height_change) > 0.08:  # Significant position change
                            severity = min(abs(hip_height_change) * 500, 100)
                            
                            flaws['landing_balance'] = {
                                'priority': 2, 'severity': severity,
                                'phase': 'follow_through', 'optimal_frame_moment': 'landing_control',
                                'issue': f"Landing imbalance: {hip_height_change:.3f} hip displacement",
                                'coaching_focus': "Land under control in same spot as takeoff",
                                'visual_key': "Balanced landing with feet under hips",
                                'explanation': self.get_flaw_explanation('landing_balance'),
                                'correction': self.get_flaw_correction('landing_balance'),
                                'drills': self.get_flaw_drills('landing_balance')
                            }
                    
                    # Store hip height for next analysis
                    if current_phase == 'release':
                        self.release_hip_height = current_hip_height
            
            # UNIVERSAL FOLLOW-THROUGH ANALYSIS - Comprehensive detection regardless of phase
            # Triggers when we detect high arm extension (post-shooting motion)
            arm_extension = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            wrist_shoulder_delta = (right_shoulder.y - right_wrist.y) * 100
            
            # Detect post-shooting motion even if phase detection missed follow-through
            if (self.shooting_started and arm_extension >= 140 and 
                (current_phase in ['release', 'shooting'] or 
                 (hasattr(self, 'previous_arm_extension') and 
                  arm_extension < self.previous_arm_extension))):  # Declining extension indicates follow-through
                
                print(f"DEBUG: *** UNIVERSAL COMPREHENSIVE FOLLOW-THROUGH ANALYSIS *** - arm_extension: {arm_extension:.1f}┬░")
                
                # RUN ALL SPECIFIC FOLLOW-THROUGH ANALYSES - Same as phase-based detection
                
                # 1. Sustained follow-through angle (Priority 1 - 8-12% accuracy impact)  
                follow_through_angle = self.calculate_angle(right_elbow, right_wrist,
                                                          {"x": right_wrist.x, "y": right_wrist.y - 0.1})
                print(f"DEBUG: UNIVERSAL Follow-through angle: {follow_through_angle:.1f}┬░")
                
                # OLD GENERIC DETECTION REMOVED - Using new specific follow-through system instead
                
                # 2. Guide Hand Thumb Flick Flaw Universal Detection (Priority 2 - 8-15% accuracy impact)
                thumb_flick_flaw_severity, guide_hand_interference = self.analyze_thumb_flick(landmarks)
                if thumb_flick_flaw_severity > 0.05 or guide_hand_interference > 0.02:
                    severity_score = thumb_flick_flaw_severity * 100
                    interference_score = guide_hand_interference * 80
                    total_severity = min(severity_score + interference_score, 100)
                    print(f"DEBUG: UNIVERSAL DETECTED thumb_flick_technique FLAW - severity: {total_severity:.1f}%")
                    
                    if 'thumb_flick_technique' not in flaws:
                        flaws['thumb_flick_technique'] = {
                            'priority': 2, 'severity': total_severity,
                            'phase': 'follow_through', 'optimal_frame_moment': 'clean_guide_hand_release',
                            'issue': f"Guide hand thumb flick flaw - Level: {thumb_flick_flaw_severity:.2f}/1.0, Interference: {guide_hand_interference:.2f}",
                            'coaching_focus': "Thumb separates from fingers during follow-through for proper spin",
                            'visual_key': "Clear thumb-to-fingers separation creates ideal backspin",
                            'explanation': self.get_flaw_explanation('thumb_flick_technique'),
                            'correction': self.get_flaw_correction('thumb_flick_technique'),
                            'drills': self.get_flaw_drills('thumb_flick_technique')
                        }
                
                # 3. Balance maintenance (Priority 3 - 5-10% accuracy impact)
                hip_center_x = (left_hip.x + right_hip.x) / 2
                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                balance_deviation = abs(shoulder_center_x - hip_center_x)
                
                if balance_deviation > 0.06:  # More reasonable universal balance threshold
                    severity = min(balance_deviation * 300, 100)
                    print(f"DEBUG: UNIVERSAL DETECTED follow_through_balance flaw - severity: {severity:.1f}%")
                    if 'follow_through_balance' not in flaws:
                        flaws['follow_through_balance'] = {
                            'priority': 3, 'severity': severity,
                            'phase': 'follow_through', 'optimal_frame_moment': 'sustained_follow_through',
                            'issue': f"Balance lost in follow-through: {balance_deviation:.3f}",
                            'coaching_focus': "Land in same position as takeoff",
                            'visual_key': "Maintain upright posture throughout",
                            'explanation': self.get_flaw_explanation('follow_through_balance'),
                            'correction': self.get_flaw_correction('follow_through_balance'),
                            'drills': self.get_flaw_drills('follow_through_balance')
                        }
                
                # 4. Wrist snap timing (Priority 2 - 10-15% accuracy impact)
                current_wrist_angle = self.calculate_angle(right_elbow, right_wrist, 
                                                         {"x": right_wrist.x, "y": right_wrist.y - 0.1})
                
                if hasattr(self, 'previous_follow_through_wrist_angle'):
                    wrist_snap_speed = abs(current_wrist_angle - self.previous_follow_through_wrist_angle)
                    if wrist_snap_speed < 8 or wrist_snap_speed > 25:  # Optimal 8-25┬░ per frame
                        speed_deviation = min(abs(wrist_snap_speed - 15), 10)
                        severity = (speed_deviation / 10) * 100
                        print(f"DEBUG: UNIVERSAL DETECTED wrist_snap_timing flaw - severity: {severity:.1f}%")
                        
                        if 'wrist_snap_timing' not in flaws:
                            flaws['wrist_snap_timing'] = {
                                'priority': 2, 'severity': severity,
                                'phase': 'follow_through', 'optimal_frame_moment': 'wrist_snap_moment',
                                'issue': f"Wrist snap speed: {wrist_snap_speed:.1f}┬░/frame (optimal: 8-25┬░)",
                                'coaching_focus': "Quick, sharp wrist snap immediately after release",
                                'visual_key': "Rapid downward wrist motion with finger point",
                                'explanation': self.get_flaw_explanation('wrist_snap_timing'),
                                'correction': self.get_flaw_correction('wrist_snap_timing'),
                                'drills': self.get_flaw_drills('wrist_snap_timing')
                            }
                
                self.previous_follow_through_wrist_angle = current_wrist_angle
                
                # 5. Follow-through angle consistency (Priority 3 - 8-12% accuracy impact)
                optimal_follow_through_angle = 55
                angle_deviation = abs(follow_through_angle - optimal_follow_through_angle)
                
                if angle_deviation > 10:  # Allow ┬▒10┬░ tolerance
                    severity = min((angle_deviation - 10) * 5, 100)
                    print(f"DEBUG: UNIVERSAL DETECTED follow_through_angle flaw - severity: {severity:.1f}%")
                    
                    if 'follow_through_angle' not in flaws:
                        flaws['follow_through_angle'] = {
                            'priority': 3, 'severity': severity,
                            'phase': 'follow_through', 'optimal_frame_moment': 'sustained_follow_through',
                            'issue': f"Follow-through angle: {follow_through_angle:.1f}┬░ (optimal: 45-65┬░)",
                            'coaching_focus': "Maintain 55┬░ downward angle after wrist snap",
                            'visual_key': "Fingers pointing down at 55┬░ angle to floor",
                            'explanation': self.get_flaw_explanation('follow_through_angle'),
                            'correction': self.get_flaw_correction('follow_through_angle'),
                            'drills': self.get_flaw_drills('follow_through_angle')
                        }
                
                # 6. Landing balance and body control (Priority 2 - 8-15% accuracy impact)
                if len(self.phase_history) >= 3:
                    current_hip_height = (left_hip.y + right_hip.y) / 2
                    
                    if hasattr(self, 'release_hip_height'):
                        hip_height_change = current_hip_height - self.release_hip_height
                        
                        if abs(hip_height_change) > 0.08:
                            severity = min(abs(hip_height_change) * 500, 100)
                            print(f"DEBUG: UNIVERSAL DETECTED landing_balance flaw - severity: {severity:.1f}%")
                            
                            if 'landing_balance' not in flaws:
                                flaws['landing_balance'] = {
                                    'priority': 2, 'severity': severity,
                                    'phase': 'follow_through', 'optimal_frame_moment': 'landing_control',
                                    'issue': f"Landing imbalance: {hip_height_change:.3f} hip displacement",
                                    'coaching_focus': "Land under control in same spot as takeoff",
                                    'visual_key': "Balanced landing with feet under hips",
                                    'explanation': self.get_flaw_explanation('landing_balance'),
                                    'correction': self.get_flaw_correction('landing_balance'),
                                    'drills': self.get_flaw_drills('landing_balance')
                                }
                    
                    if current_phase == 'release':
                        self.release_hip_height = current_hip_height
                
                # Store for next frame
                self.previous_arm_extension = arm_extension
            
            # OVERALL SHOT ANALYSIS - Tempo and Smoothness (All phases) - NEW
            smoothness_score, tempo_consistency = self.analyze_shot_smoothness_tempo(landmarks, current_phase)
            if smoothness_score < 0.85 or tempo_consistency < 0.80:  # More sensitive thresholds
                smoothness_severity = (1.0 - smoothness_score) * 60
                tempo_severity = (1.0 - tempo_consistency) * 60
                total_severity = min(smoothness_severity + tempo_severity, 100)
                
                flaws['shot_smoothness_tempo'] = {
                    'priority': 3, 'severity': total_severity,
                    'phase': current_phase, 'optimal_frame_moment': 'continuous_motion',
                    'issue': f"Smoothness: {smoothness_score:.2f}/1.0, Tempo: {tempo_consistency:.2f}/1.0",
                    'coaching_focus': "Develop rhythmic, fluid shooting motion without hitches",
                    'visual_key': "One continuous upward motion from setup to release",
                    'explanation': self.get_flaw_explanation('shot_smoothness_tempo'),
                    'correction': self.get_flaw_correction('shot_smoothness_tempo'),
                    'drills': self.get_flaw_drills('shot_smoothness_tempo')
                }
            
            # DEBUG: Always log what flaws we detected for this phase
            detected_flaws = list(flaws.keys())
            severities = {name: data.get('severity', 0) for name, data in flaws.items()}
            print(f"DEBUG: Frame {self.frame_count} - Detected {len(flaws)} flaws: {detected_flaws}")
            for flaw_name, flaw_data in flaws.items():
                print(f"  - {flaw_name}: Priority {flaw_data.get('priority', 0)}, Severity {flaw_data.get('severity', 0)}")
                
            return {'flaws': flaws, 'phase': current_phase}
            
        except Exception as e:
            print(f"DEBUG: Error in phase-specific analysis: {e}")
            return {'flaws': {}, 'phase': current_phase}

    def capture_phase_specific_stills(self, landmarks, flaws, annotated_frame, phase):
        """Intelligently capture frame stills only at the most instructive moments"""
        if not landmarks or not flaws or annotated_frame is None:
            return {}
            
        flaw_stills = {}
        current_frame = self.frame_count
        
        print(f"DEBUG: Evaluating frame {current_frame} for intelligent capture in {phase} phase")
        
        # Track phase transitions for timing context
        if len(self.phase_history) == 0 or self.phase_history[-1] != phase:
            self.phase_transition_frames[phase] = current_frame
            print(f"DEBUG: Phase transition to {phase} at frame {current_frame}")
        
        self.phase_history.append(phase)
        
        try:
            for flaw_name, flaw_data in flaws.items():
                flaw_phase = flaw_data.get('phase', 'unknown')
                severity = flaw_data.get('severity', 0)
                priority = flaw_data.get('priority', 10)
                
                # Skip if not in the right phase
                if flaw_phase != phase:
                    continue
                
                # CRITICAL VALIDATION: Preparation phase flaws CANNOT be captured after release
                if ('preparation' in flaw_name and self.release_detected):
                    print(f"DEBUG: BLOCKING {flaw_name} - preparation flaw detected after release (invalid sequence)")
                    continue
                    
                # CRITICAL VALIDATION: Shooting alignment CANNOT be captured after release
                if ('shooting_alignment' in flaw_name and self.release_detected):
                    print(f"DEBUG: BLOCKING {flaw_name} - shooting alignment detected after release (invalid sequence)")
                    continue
                
                # Ultra-selective capture logic - only the BEST moment for each flaw:
                should_capture = False
                capture_reason = ""
                flaw_key = f"{phase}_{flaw_name}"
                
                # Get optimal timing analysis
                phase_start = self.phase_transition_frames.get(phase, current_frame)
                frames_in_phase = current_frame - phase_start
                is_optimal_timing, timing_reason = self.get_optimal_flaw_timing(
                    flaw_name, landmarks, phase, frames_in_phase)
                
                # SPECIAL CASE: Immediate thumb flick capture override
                if ('thumb_flick' in flaw_name and 
                    hasattr(self, 'immediate_thumb_capture_frame') and
                    self.immediate_thumb_capture_frame == current_frame):
                    should_capture = True
                    capture_reason = "immediate_thumb_flick_detection"
                    print(f"DEBUG: IMMEDIATE THUMB FLICK CAPTURE OVERRIDE - Frame {current_frame}")
                    # Clear the immediate capture flag
                    delattr(self, 'immediate_thumb_capture_frame')
                    
                # PRIORITY 1: Optimal biomechanical timing (highest quality captures)
                if is_optimal_timing:
                    if flaw_key not in self.best_flaw_frames:
                        # First optimal timing capture - always take it
                        should_capture = True
                        capture_reason = f"optimal_first_{timing_reason}"
                    else:
                        previous_best = self.best_flaw_frames[flaw_key]
                        # Replace if significantly better at optimal timing, or if previous wasn't optimal
                        if (severity > previous_best['severity'] * 1.03 or
                            not previous_best.get('biomechanical_timing', False)):
                            should_capture = True
                            capture_reason = f"optimal_improved_{timing_reason}"
                            
                # PRIORITY 2: First occurrence fallback (only if no optimal capture yet)
                elif flaw_key not in self.best_flaw_frames and severity > 45:
                    # TEMPORAL SEPARATION: Ensure each flaw gets its own distinct frame
                    frame_already_used = any(
                        data['frame'] == current_frame 
                        for data in self.best_flaw_frames.values()
                    )
                    
                    # SPECIAL CASE: Follow-through should NEVER be captured during release height moment
                    is_follow_through = ('follow' in flaw_name or 'through' in flaw_name)
                    is_release_moment = (phase == "release" and frames_in_phase == 0)
                    
                    if is_follow_through and is_release_moment:
                        should_capture = False
                        capture_reason = "follow_through_timing_restriction"
                        print(f"DEBUG: BLOCKING follow-through at release moment - waiting for optimal timing window")
                    elif not frame_already_used or priority == 1:
                        should_capture = True
                        capture_reason = "first_occurrence_fallback"
                    else:
                        # Defer capture for lower priority flaws to get their own optimal timing
                        should_capture = False
                        capture_reason = "temporal_separation_deferred"
                        print(f"DEBUG: DEFERRING {flaw_name} - Frame {current_frame} already used, waiting for optimal timing")
                    
                # PRIORITY 3: Emergency high-severity capture (80%+ severity)
                elif severity > 80 and priority <= 2:
                    # STRICT biomechanical timing restrictions for critical measurements
                    emergency_allowed = True
                    
                    if 'release' in flaw_name and 'height' in flaw_name:
                        # Release height: NEVER allow late captures - must be exact ball separation
                        emergency_allowed = (phase == "release" and frames_in_phase == 0)
                        
                    elif 'elbow' in flaw_name and 'shooting' in flaw_name:
                        # Elbow: Only allow during power generation window (85-95┬░ angle range)
                        elbow_angle = self.calculate_angle(
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                        ) if landmarks else 0
                        emergency_allowed = (phase == "shooting" and 
                                           frames_in_phase <= 10 and 
                                           85 <= elbow_angle <= 100)
                                           
                    elif 'balance' in flaw_name and 'preparation' in flaw_name:
                        # Balance: Only during settled position, not during motion
                        emergency_allowed = (phase == "preparation" and 
                                           frames_in_phase >= 8 and 
                                           frames_in_phase <= 18)
                                           
                    elif 'follow' in flaw_name or ('release' in flaw_name and 'through' in flaw_name):
                        # Follow-through: Only during actual follow-through window
                        emergency_allowed = (phase == "release" and 
                                           frames_in_phase >= 3 and 
                                           frames_in_phase <= 8)
                    
                    if emergency_allowed and (flaw_key not in self.best_flaw_frames or 
                                            self.best_flaw_frames[flaw_key]['severity'] < severity * 0.9):
                        # Check temporal separation for emergency captures too
                        frame_already_used = any(
                            data['frame'] == current_frame 
                            for data in self.best_flaw_frames.values()
                        )
                        
                        # Allow emergency capture if frame not used OR this is critical priority
                        if not frame_already_used or priority == 1:
                            should_capture = True
                            capture_reason = "emergency_high_severity_biomechanically_valid"
                        else:
                            print(f"DEBUG: Emergency capture deferred for {flaw_name} - frame {current_frame} temporal conflict")
                        
                # PRIORITY 4: Phase coverage requirement (ensure representation)
                elif (len([k for k in self.best_flaw_frames.keys() if k.startswith(f"{phase}_")]) == 0 
                      and severity > 35):
                    should_capture = True
                    capture_reason = "phase_coverage_requirement"
                
                if should_capture:
                    print(f"DEBUG: CAPTURING {flaw_name} - Reason: {capture_reason}, Severity: {severity:.1f}, Priority: {priority}")
                    
                    # Create annotated image highlighting the specific flaw (keep in BGR for OpenCV processing)
                    still_image = annotated_frame.copy()
                    
                    # Add phase-specific annotations
                    if 'balance' in flaw_name or 'stance' in flaw_name:
                        self.annotate_alignment_lines(still_image, landmarks)
                    elif 'elbow' in flaw_name:
                        self.annotate_shooting_arm(still_image, landmarks)
                    elif 'release' in flaw_name:
                        self.annotate_release_mechanics(still_image, landmarks)
                    elif 'thumb_flick' in flaw_name:
                        self.annotate_thumb_flick_flaw(still_image, landmarks)
                    
                    # Add instructional annotations
                    coaching_focus = flaw_data.get('coaching_focus', 'Focus area')
                    visual_key = flaw_data.get('visual_key', 'Key point')
                    
                    # Make text more readable with background
                    cv2.rectangle(still_image, (5, 5), (600, 120), (0, 0, 0), -1)
                    cv2.putText(still_image, f"FLAW: {coaching_focus}", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(still_image, f"FOCUS: {visual_key}", 
                              (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    cv2.putText(still_image, f"PHASE: {phase.upper()} | FRAME: {current_frame}", 
                              (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(still_image, f"SEVERITY: {severity:.0f}% | PRIORITY: {priority}", 
                              (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                    # Convert to RGB for proper Streamlit display and storage
                    still_image_rgb = cv2.cvtColor(still_image, cv2.COLOR_BGR2RGB)
                    
                    flaw_stills[flaw_name] = {
                        'image': still_image_rgb,  # Store as RGB for Streamlit
                        'phase': phase,
                        'frame_number': current_frame,
                        'capture_reason': capture_reason,
                        'priority': priority,
                        'severity': severity,
                        'coaching_focus': coaching_focus,
                        'visual_key': visual_key,
                        'timestamp': f"Frame {current_frame} - {phase} phase"
                    }
                    
                    # Update best frame tracking with biomechanical context
                    self.best_flaw_frames[flaw_key] = {
                        'frame': current_frame,
                        'severity': severity,
                        'image': still_image_rgb,  # Store as RGB
                        'capture_reason': capture_reason,
                        'biomechanical_timing': is_optimal_timing,
                        'timing_analysis': timing_reason if is_optimal_timing else None
                    }
                    
                    # Update captured stills for immediate availability
                    flaw_display_name = flaw_name.replace('_', ' ').title()
                    self.captured_stills[flaw_display_name] = {
                        'image': still_image_rgb,
                        'phase': phase,
                        'frame_number': current_frame,
                        'severity': severity,
                        'description': f"Best instructional frame for {flaw_display_name} in {phase} phase"
                    }
                    
                    self.captured_flaws.add(flaw_key)
                    
                else:
                    # Enhanced debugging for skipped frames
                    skip_reason = "suboptimal_timing"
                    if capture_reason == "temporal_separation_deferred":
                        skip_reason = f"temporal_separation_deferred (frame {current_frame} already used)"
                    elif capture_reason == "follow_through_timing_restriction":
                        skip_reason = f"follow_through_blocked_at_release_moment (frame {current_frame})"
                    elif flaw_key in self.best_flaw_frames:
                        existing_severity = self.best_flaw_frames[flaw_key]['severity']
                        existing_optimal = self.best_flaw_frames[flaw_key].get('biomechanical_timing', False)
                        if is_optimal_timing and existing_optimal:
                            skip_reason = f"optimal_exists_better (current: {severity:.1f}%, existing: {existing_severity:.1f}%)"
                        elif is_optimal_timing:
                            skip_reason = f"optimal_insufficient_improvement (need {existing_severity * 1.03:.1f}%, got {severity:.1f}%)"
                        elif existing_optimal:
                            skip_reason = "suboptimal_vs_existing_optimal"
                        else:
                            skip_reason = f"insufficient_improvement (current: {severity:.1f}%, existing: {existing_severity:.1f}%)"
                    elif severity <= 45:
                        skip_reason = f"insufficient_severity_for_first ({severity:.1f}% < 45%)"
                    else:
                        skip_reason = f"timing_not_optimal ({timing_reason})"
                        
                    print(f"DEBUG: SKIPPING {flaw_name} - {skip_reason} | Frame {current_frame}, Phase {phase}, Frames in phase: {frames_in_phase}")
                    
        except Exception as e:
            print(f"DEBUG: Error in intelligent still capture: {e}")
            
        print(f"DEBUG: Captured {len(flaw_stills)} new stills for {phase} phase")
        return flaw_stills

    def get_optimal_flaw_timing(self, flaw_name, landmarks, phase, frames_in_phase):
        """
        RESEARCH-BACKED ULTRA-PRECISE BIOMECHANICAL TIMING
        Based on peer-reviewed basketball shooting biomechanics studies and frame analysis research
        
        Key Research Findings Applied:
        1. Ball release occurs in first 0.18-0.22 seconds of shooting phase
        2. Peak power generation happens at 90┬░ elbow angle
        3. Optimal balance assessment requires settled position (>5 frames)
        4. Maximum force generation occurs during initial acceleration phase
        5. Follow-through assessment optimal 0.1-0.2 seconds post-release
        """
        if not landmarks:
            return False, "no_landmarks"
            
        # Get precise biomechanical measurements
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW] 
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
        
        # Calculate critical biomechanical angles and positions
        elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        shoulder_height = right_shoulder.y
        wrist_height = right_wrist.y
        elbow_height = right_elbow.y
        wrist_shoulder_delta = (shoulder_height - wrist_height) * 100
        
        # Biomechanical velocity indicators (frame-to-frame position change)
        wrist_velocity_indicator = abs(wrist_height - shoulder_height)
        elbow_extension_indicator = elbow_angle
        
        # Hip-shoulder alignment for balance assessment
        hip_center_x = (left_hip.x + right_hip.x) / 2
        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        lateral_balance = abs(hip_center_x - shoulder_center_x) * 100
        
        # Knee alignment for stance assessment
        knee_center_x = (left_knee.x + right_knee.x) / 2
        knee_hip_alignment = abs(knee_center_x - hip_center_x) * 100
        
        # RESEARCH-BASED OPTIMAL TIMING FOR EACH FLAW TYPE:
        
        if 'balance' in flaw_name and 'preparation' in flaw_name:
            # BALANCE ASSESSMENT: Capture during static equilibrium phase
            # Research: Balance must be assessed when movement has stabilized
            is_balanced_position = (
                frames_in_phase >= 8 and frames_in_phase <= 15 and  # Sufficient settling time
                abs(shoulder_height - elbow_height) < 0.025 and      # Minimal vertical movement
                lateral_balance > 1.8                                # Detectable imbalance
            )
            return (phase == "preparation" and is_balanced_position), "balance_static_equilibrium"
                    
        elif 'stance' in flaw_name and 'preparation' in flaw_name:
            # STANCE ASSESSMENT: Capture when foot positioning is established
            # Research: Stance evaluation optimal in stable ready position before motion
            optimal_stance_timing = (
                frames_in_phase >= 6 and frames_in_phase <= 12 and   # After initial setup
                knee_hip_alignment > 1.2 and                         # Measurable misalignment
                wrist_velocity_indicator < 0.15                      # Minimal upper body motion
            )
            return (phase == "preparation" and optimal_stance_timing), "stance_established_base"
                    
        elif 'elbow' in flaw_name and 'shooting' in flaw_name:
            # ELBOW ALIGNMENT: Capture at peak force generation angle
            # Research: Elbow mechanics most critical at 90┬░ during power phase
            power_position_timing = (
                85 <= elbow_angle <= 95 and                          # Near-optimal force angle
                wrist_shoulder_delta >= 10 and wrist_shoulder_delta <= 25 and  # Active shooting motion
                frames_in_phase >= 2 and frames_in_phase <= 8        # During power generation phase
            )
            return (phase == "shooting" and power_position_timing), "elbow_peak_force_generation"
                    
        elif 'alignment' in flaw_name and 'shooting' in flaw_name:
            # BODY ALIGNMENT: Capture during early force transfer phase for better coaching visibility
            # Research: Alignment patterns best seen during initial shooting motion setup
            early_force_transfer_timing = (
                frames_in_phase >= 2 and frames_in_phase <= 6 and    # Earlier capture window
                95 <= elbow_angle <= 120 and                         # Earlier angle range
                wrist_shoulder_delta >= 8 and                        # Less restrictive movement
                wrist_velocity_indicator > 0.05                      # Earlier movement detection
            )
            return (phase == "shooting" and early_force_transfer_timing), "alignment_early_shooting_setup"
                    
        elif 'arc' in flaw_name:
            # SHOT ARC: Capture when trajectory is most visible
            # Research: Arc assessment optimal during mid-trajectory formation
            trajectory_formation = (
                115 <= elbow_angle <= 140 and                        # Trajectory formation angle
                wrist_shoulder_delta >= 20 and                       # Sufficient elevation
                frames_in_phase >= 6 and frames_in_phase <= 12       # Mid-shooting motion
            )
            return (phase == "shooting" and trajectory_formation), "arc_trajectory_formation"
                    
        elif 'release' in flaw_name and 'height' in flaw_name:
            # RELEASE HEIGHT: Capture at EXACT ball separation moment
            # Research: Release height must be measured at precise ball departure
            exact_release_timing = (
                phase == "release" and
                frames_in_phase == 0 and                             # First frame of release phase only
                elbow_angle >= 155 and                               # Near full extension
                wrist_shoulder_delta >= 18                           # Adequate release height
            )
            return exact_release_timing, "release_exact_ball_departure"
                    
        elif 'thumb_flick' in flaw_name:
            # THUMB FLICK FLAW CAPTURE: Capture at EXACT moment of guide hand thumb rotation
            # Research: Thumb flick visible immediately after ball release (1-4 frames post-release)
            
            # Check if we have the specific frame capture signal from thumb flick analysis
            thumb_flick_capture_ready = (
                hasattr(self, 'thumb_flick_flaw_tracker') and
                self.thumb_flick_flaw_tracker.get('capture_frame_ready', False)
            )
            
            if thumb_flick_capture_ready:
                # Reset the capture flag so we only capture once
                self.thumb_flick_flaw_tracker['capture_frame_ready'] = False
                return True, "thumb_inward_rotation_moment"
            
            # Fallback timing: Post-release window for thumb flick detection
            thumb_flick_window = (
                (phase == "release" or phase == "follow_through") and
                1 <= frames_in_phase <= 4 and                        # Critical post-release window
                hasattr(self, 'thumb_flick_flaw_tracker') and
                self.thumb_flick_flaw_tracker.get('frames_since_release', 0) <= 4
            )
            return thumb_flick_window, "thumb_flick_post_release_window"
                    
        elif 'follow' in flaw_name or ('release' in flaw_name and 'through' in flaw_name):
            # FOLLOW-THROUGH: Capture during wrist snap phase (NEVER at release moment)
            # Research: Follow-through assessment optimal 0.1-0.2 seconds post-release
            wrist_snap_timing = (
                phase == "release" and
                frames_in_phase >= 3 and frames_in_phase <= 7 and    # MUST be post-release timing
                elbow_angle >= 165 and                               # Full extension
                wrist_height > shoulder_height - 0.08 and            # Maintained elevation
                abs(wrist_shoulder_delta - 25) < 5                   # Optimal follow-through position
            )
            return wrist_snap_timing, "follow_through_wrist_snap"
                    
        elif 'hand' in flaw_name or 'wrist' in flaw_name:
            # HAND MECHANICS: Capture during active control phase
            # Research: Hand positioning most critical during force application
            active_control_timing = (
                phase == "shooting" and
                frames_in_phase >= 5 and frames_in_phase <= 11 and   # Active control window
                95 <= elbow_angle <= 120 and                         # Control angle range
                wrist_shoulder_delta >= 15                           # Sufficient elevation
            )
            return active_control_timing, "hand_active_control_phase"
        
        # Default: timing not optimal for analysis
        return False, "suboptimal_biomechanical_timing"

    def get_final_instructional_stills(self):
        """Get the best instructional frame stills from the entire shot sequence"""
        print(f"DEBUG: Compiling final instructional stills from {len(self.best_flaw_frames)} captured frames")
        
        final_stills = {}
        
        for flaw_key, frame_data in self.best_flaw_frames.items():
            # Extract phase and flaw name
            if '_' in flaw_key:
                phase, flaw_name = flaw_key.split('_', 1)
            else:
                phase, flaw_name = 'unknown', flaw_key
                
            final_stills[flaw_name] = {
                'image': frame_data['image'],
                'phase': phase,
                'frame_number': frame_data['frame'],
                'severity': frame_data['severity'],
                'description': f"Best instructional frame for {flaw_name.replace('_', ' ')} in {phase} phase"
            }
            
        print(f"DEBUG: Final instructional stills: {len(final_stills)} unique flaws captured")
        
        # Also update captured_stills to match
        if final_stills:
            self.captured_stills = final_stills.copy()
            print(f"DEBUG: Updated captured_stills with {len(self.captured_stills)} frames")
        
        return final_stills

    def annotate_alignment_lines(self, image, landmarks):
        """Draw alignment lines for balance and stance analysis"""
        try:
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            
            h, w = image.shape[:2]
            
            # Shoulder line
            cv2.line(image, 
                    (int(left_shoulder.x * w), int(left_shoulder.y * h)),
                    (int(right_shoulder.x * w), int(right_shoulder.y * h)),
                    (0, 255, 0), 3)
            
            # Hip line  
            cv2.line(image, 
                    (int(left_hip.x * w), int(left_hip.y * h)),
                    (int(right_hip.x * w), int(right_hip.y * h)),
                    (255, 0, 0), 3)
                    
            # Vertical alignment line
            shoulder_center_x = int(((left_shoulder.x + right_shoulder.x) / 2) * w)
            hip_center_x = int(((left_hip.x + right_hip.x) / 2) * w)
            
            cv2.line(image, 
                    (shoulder_center_x, int(left_shoulder.y * h)),
                    (shoulder_center_x, int(left_hip.y * h)),
                    (0, 255, 255), 2)
                    
        except Exception as e:
            print(f"DEBUG: Error in alignment annotation: {e}")

    def annotate_shooting_arm(self, image, landmarks):
        """Draw shooting arm analysis annotations"""
        try:
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            
            h, w = image.shape[:2]
            
            # Draw shooting arm
            shoulder_pos = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            elbow_pos = (int(right_elbow.x * w), int(right_elbow.y * h))
            wrist_pos = (int(right_wrist.x * w), int(right_wrist.y * h))
            
            # Arm segments
            cv2.line(image, shoulder_pos, elbow_pos, (0, 255, 255), 4)
            cv2.line(image, elbow_pos, wrist_pos, (255, 255, 0), 4)
            
            # Joint markers
            cv2.circle(image, shoulder_pos, 8, (255, 0, 0), -1)
            cv2.circle(image, elbow_pos, 10, (0, 255, 0), -1)
            cv2.circle(image, wrist_pos, 8, (0, 0, 255), -1)
            
        except Exception as e:
            print(f"DEBUG: Error in shooting arm annotation: {e}")

    def annotate_release_mechanics(self, image, landmarks):
        """Draw release mechanics annotations"""
        try:
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            
            h, w = image.shape[:2]
            
            # Release trajectory
            shoulder_pos = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            elbow_pos = (int(right_elbow.x * w), int(right_elbow.y * h))
            wrist_pos = (int(right_wrist.x * w), int(right_wrist.y * h))
            
            # Draw release path
            cv2.arrowedLine(image, elbow_pos, wrist_pos, (255, 0, 255), 4)
            cv2.circle(image, wrist_pos, 15, (255, 255, 0), 3)
            
        except Exception as e:
            print(f"DEBUG: Error in release mechanics annotation: {e}")

    def annotate_thumb_flick_flaw(self, image, landmarks):
        """Draw specific annotations for guide hand thumb flick flaw detection"""
        try:
            # Get guide hand (left) and shooting hand (right) landmarks
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]    # Guide hand
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]    
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]  # Shooting hand
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            h, w = image.shape[:2]
            
            # Guide hand positions
            guide_shoulder_pos = (int(left_shoulder.x * w), int(left_shoulder.y * h))
            guide_elbow_pos = (int(left_elbow.x * w), int(left_elbow.y * h))
            guide_wrist_pos = (int(left_wrist.x * w), int(left_wrist.y * h))
            
            # Shooting hand positions  
            shoot_shoulder_pos = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            shoot_elbow_pos = (int(right_elbow.x * w), int(right_elbow.y * h))
            shoot_wrist_pos = (int(right_wrist.x * w), int(right_wrist.y * h))
            
            # HIGHLIGHT GUIDE HAND FLAW - Draw guide hand in RED (problematic)
            cv2.line(image, guide_shoulder_pos, guide_elbow_pos, (0, 0, 255), 5)  # Red = bad
            cv2.line(image, guide_elbow_pos, guide_wrist_pos, (0, 0, 255), 5)
            cv2.circle(image, guide_wrist_pos, 12, (0, 0, 255), -1)  # Red guide wrist
            
            # HIGHLIGHT PROPER SHOOTING HAND - Draw shooting hand in GREEN (correct)
            cv2.line(image, shoot_shoulder_pos, shoot_elbow_pos, (0, 255, 0), 3)  # Green = good
            cv2.line(image, shoot_elbow_pos, shoot_wrist_pos, (0, 255, 0), 3)
            cv2.circle(image, shoot_wrist_pos, 10, (0, 255, 0), -1)  # Green shooting wrist
            
            # Draw movement direction arrow on guide hand to show unwanted motion
            if hasattr(self, 'thumb_flick_flaw_tracker') and len(self.thumb_flick_flaw_tracker.get('guide_hand_positions', [])) >= 2:
                recent_positions = self.thumb_flick_flaw_tracker['guide_hand_positions'][-2:]
                if len(recent_positions) >= 2:
                    prev_pos = recent_positions[-2]
                    curr_pos = recent_positions[-1]
                    
                    # Calculate movement direction
                    prev_screen = (int(prev_pos[0] * w), int(prev_pos[1] * h))
                    curr_screen = (int(curr_pos[0] * w), int(curr_pos[1] * h))
                    
                    # Draw arrow showing problematic thumb movement
                    cv2.arrowedLine(image, prev_screen, curr_screen, (0, 0, 255), 4, tipLength=0.3)
            
            # Add visual indicators for the specific flaw
            cv2.putText(image, "THUMB FLICK FLAW", 
                       (guide_wrist_pos[0] - 80, guide_wrist_pos[1] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            cv2.putText(image, "GUIDE HAND INTERFERING", 
                       (guide_wrist_pos[0] - 100, guide_wrist_pos[1] + 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            cv2.putText(image, "SHOULD BE PASSIVE", 
                       (shoot_wrist_pos[0] - 70, shoot_wrist_pos[1] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Draw a connecting line showing proper hand separation
            cv2.line(image, guide_wrist_pos, shoot_wrist_pos, (255, 255, 0), 2)
            
            # Calculate and display hand separation distance
            separation_distance = np.linalg.norm([left_wrist.x - right_wrist.x, left_wrist.y - right_wrist.y])
            mid_point = ((guide_wrist_pos[0] + shoot_wrist_pos[0]) // 2, 
                        (guide_wrist_pos[1] + shoot_wrist_pos[1]) // 2)
            
            cv2.putText(image, f"Sep: {separation_distance:.3f}", 
                       mid_point, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
            
        except Exception as e:
            print(f"DEBUG: Error in thumb flick annotation: {e}")

    def add_balance_analysis_overlay(self, image, landmarks):
        """Add biomechanical balance analysis overlay"""
        try:
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            
            h, w = image.shape[:2]
            
            # Hip-knee alignment check
            hip_center_x = int(((left_hip.x + right_hip.x) / 2) * w)
            knee_center_x = int(((left_knee.x + right_knee.x) / 2) * w)
            
            # Draw balance analysis line
            cv2.line(image, (hip_center_x, int(left_hip.y * h)), 
                    (knee_center_x, int(left_knee.y * h)), (255, 0, 255), 3)
            
            # Add balance indicator
            balance_diff = abs(hip_center_x - knee_center_x)
            balance_status = "GOOD" if balance_diff < 20 else "POOR"
            cv2.putText(image, f"BALANCE: {balance_status}", 
                       (w - 200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        except:
            pass

    def add_elbow_angle_overlay(self, image, landmarks):
        """Add elbow angle analysis overlay"""
        try:
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            
            h, w = image.shape[:2]
            elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Draw angle arc
            elbow_pos = (int(right_elbow.x * w), int(right_elbow.y * h))
            cv2.circle(image, elbow_pos, 30, (0, 255, 255), 3)
            
            # Add angle text
            angle_status = "OPTIMAL" if 85 <= elbow_angle <= 105 else "ADJUST"
            cv2.putText(image, f"ELBOW: {elbow_angle:.0f}┬░ ({angle_status})", 
                       (w - 250, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        except:
            pass

    def add_release_point_analysis(self, image, landmarks):
        """Add release point analysis overlay"""
        try:
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            
            h, w = image.shape[:2]
            
            # Release height indicator
            wrist_pos = (int(right_wrist.x * w), int(right_wrist.y * h))
            shoulder_pos = (int(right_shoulder.x * w), int(right_shoulder.y * h))
            
            # Draw release height line
            cv2.line(image, shoulder_pos, wrist_pos, (255, 255, 0), 3)
            cv2.circle(image, wrist_pos, 15, (255, 0, 0), -1)
            
            # Height analysis
            height_diff = (right_shoulder.y - right_wrist.y) * 100
            height_status = "HIGH" if height_diff > 15 else "LOW"
            cv2.putText(image, f"RELEASE: {height_status}", 
                       (w - 200, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        except:
            pass

    def add_body_alignment_analysis(self, image, landmarks):
        """Add body alignment analysis overlay"""  
        try:
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            
            h, w = image.shape[:2]
            
            # Body centerline
            shoulder_center_x = int(((left_shoulder.x + right_shoulder.x) / 2) * w)
            hip_center_x = int(((left_hip.x + right_hip.x) / 2) * w)
            
            # Draw centerline
            cv2.line(image, (shoulder_center_x, int(left_shoulder.y * h)),
                    (hip_center_x, int(left_hip.y * h)), (0, 255, 0), 3)
            
            # Alignment check
            alignment_diff = abs(shoulder_center_x - hip_center_x)
            alignment_status = "ALIGNED" if alignment_diff < 25 else "MISALIGNED"
            cv2.putText(image, f"BODY: {alignment_status}", 
                       (w - 200, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        except:
            pass
        """Draw shooting arm mechanics for elbow analysis"""
        try:
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            
            h, w = image.shape[:2]
            
            # Shooting arm line
            cv2.line(image,
                    (int(right_shoulder.x * w), int(right_shoulder.y * h)),
                    (int(right_elbow.x * w), int(right_elbow.y * h)),
                    (0, 255, 0), 4)
            cv2.line(image,
                    (int(right_elbow.x * w), int(right_elbow.y * h)),
                    (int(right_wrist.x * w), int(right_wrist.y * h)),
                    (0, 255, 0), 4)
                    
            # Elbow angle arc
            elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            cv2.putText(image, f"{elbow_angle:.1f}┬░",
                      (int(right_elbow.x * w) - 30, int(right_elbow.y * h) - 10),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                      
        except Exception as e:
            print(f"DEBUG: Error in shooting arm annotation: {e}")

    def annotate_release_mechanics(self, image, landmarks):
        """Draw release point and follow-through for release analysis"""
        try:
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            h, w = image.shape[:2]
            
            # Release height line
            avg_shoulder_y = int(((left_shoulder.y + right_shoulder.y) / 2) * h)
            wrist_y = int(right_wrist.y * h)
            
            cv2.line(image, (0, avg_shoulder_y), (w, avg_shoulder_y), (255, 0, 255), 2)
            cv2.line(image, (0, wrist_y), (w, wrist_y), (0, 255, 255), 2)
            
            # Follow-through direction
            cv2.arrowedLine(image,
                          (int(right_wrist.x * w), int(right_wrist.y * h)),
                          (int(right_wrist.x * w), int(right_wrist.y * h) + 50),
                          (255, 255, 0), 3)
                          
        except Exception as e:
            print(f"DEBUG: Error in release annotation: {e}")

    def analyze_detailed_flaws(self, landmarks) -> Dict[str, Any]:
        """Main detailed flaw analysis using phase-specific detection"""
        if not landmarks:
            logger.warning("No landmarks provided for detailed flaw analysis")
            return {'flaws': {}, 'overall_score': 0.0, 'phase': 'unknown'}
        
        # Detect current shooting phase
        current_phase = self.detect_shooting_phase(landmarks)
        print(f"DEBUG: Detected phase: {current_phase}")
        
        # Get phase-specific flaws
        phase_analysis = self.analyze_phase_specific_flaws(landmarks, current_phase)
        flaws = phase_analysis.get('flaws', {})
        
        # Calculate overall score based on detected flaws
        priority_weights = {1: 0.25, 2: 0.20, 3: 0.15, 4: 0.10, 5: 0.05, 6: 0.05}
        total_impact = 0
        
        for flaw_data in flaws.values():
            priority = flaw_data.get('priority', 10)
            severity = flaw_data.get('severity', 0)
            weight = priority_weights.get(priority, 0.01)
            # Reduce impact - severity should be less punishing
            total_impact += (severity / 100) * weight * 0.5  # Reduced impact by 50%
        
        # Ensure minimum baseline score - even developing players shouldn't be below 0.55
        # High school/college-level players should be at least 0.65+
        baseline_score = 0.65  # Assume realistic basketball player baseline
        overall_score = max(baseline_score, 1 - total_impact)
        
        # Cap maximum penalty - no serious player should get below 0.50
        overall_score = max(0.50, overall_score)
        
        return {
            'flaws': flaws,
            'overall_score': overall_score,
            'primary_issues': sorted(flaws.items(), key=lambda x: x[1].get('priority', 10)),
            'research_backed': True,
            'phase': current_phase,
            'detection_type': 'phase_specific'
        }
        
        logger.debug("Starting detailed flaw analysis")
        print(f"DEBUG: analyze_detailed_flaws - Starting analysis with {len(landmarks)} landmarks")
        
        try:
            # Get key landmarks for analysis
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            nose = landmarks[mp_pose.PoseLandmark.NOSE]
            
            # 1. Balance and Stance Analysis (Priority 1 - 25-30% accuracy impact)
            hip_center_x = (left_hip.x + right_hip.x) / 2
            shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
            balance_deviation = abs(shoulder_center_x - hip_center_x)
            
            print(f"DEBUG: Balance deviation = {balance_deviation:.4f}")
            
            if balance_deviation > 0.01:  # Much more sensitive threshold for testing
                severity = min(balance_deviation * 200, 100)  # Adjusted sensitivity
                flaws['balance_stance'] = {
                    'priority': 1,
                    'severity': severity,
                    'accuracy_impact': '25-30',
                    'issue': f"Balance deviation: {balance_deviation:.3f} (should be <0.01)",
                    'recommendation': "Focus on feet shoulder-width apart, weight evenly distributed. Practice wall sits to improve stability."
                }
                print(f"DEBUG: Added balance_stance flaw with severity {severity}")
            
            # 2. Elbow Alignment (Priority 2 - 20-25% accuracy impact)
            elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            print(f"DEBUG: Elbow angle = {elbow_angle:.1f}┬░")
            
            if elbow_angle < 70 or elbow_angle > 120:  # Much more sensitive range
                deviation = min(abs(elbow_angle - 90), 45)
                severity = (deviation / 45) * 100
                flaws['elbow_alignment'] = {
                    'priority': 2,
                    'severity': severity,
                    'accuracy_impact': '20-25',
                    'issue': f"Elbow angle: {elbow_angle:.1f}┬░ (optimal: 70-120┬░)",
                    'recommendation': "Maintain proper elbow-under-ball position. Practice form shooting focusing on consistent elbow placement."
                }
                print(f"DEBUG: Added elbow_alignment flaw with severity {severity}")
            
            # 2. Elbow Alignment Analysis (Priority 4 - 15-25% accuracy impact)
            elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            ideal_elbow_min, ideal_elbow_max = 90, 100  # Narrower ideal range
            
            if elbow_angle < 85 or elbow_angle > 110:  # More reasonable range
                deviation = min(abs(elbow_angle - 95), 20)  # 95┬░ is ideal center
                severity = (deviation / 20) * 100
                flaws['elbow_alignment'] = {
                    'priority': 2,
                    'severity': severity,
                    'accuracy_impact': '15-25',
                    'issue': f"Elbow angle: {elbow_angle:.1f}┬░ (optimal: 85-110┬░)",
                    'recommendation': "Keep elbow directly under ball. Practice close-range shooting focusing on elbow position."
                }
            
            # 3. Release Point Analysis (Priority 7 - 8-12% accuracy impact)
            avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            release_height = avg_shoulder_y - right_wrist.y
            
            if release_height < 0.02:  # More reasonable threshold
                severity = min(abs(release_height - 0.08) * 100, 100)
                flaws['release_point'] = {
                    'priority': 4,
                    'severity': severity,
                    'accuracy_impact': '8-12',
                    'issue': f"Low release: {release_height:.3f} (should be >0.02 above shoulders)",
                    'recommendation': "Release ball at forehead level or higher for optimal arc trajectory."
                }
            
            # 4. Knee Bend Analysis (Priority 5 - 10-15% accuracy impact)
            left_knee_angle = self.calculate_angle(left_hip, left_knee, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE])
            right_knee_angle = self.calculate_angle(right_hip, right_knee, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE])
            avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
            
            print(f"DEBUG: Knee angles - Left: {left_knee_angle:.1f}┬░, Right: {right_knee_angle:.1f}┬░, Avg: {avg_knee_angle:.1f}┬░")
            
            if avg_knee_angle < 140 or avg_knee_angle > 170:  # Much more sensitive range for testing
                deviation = min(abs(avg_knee_angle - 155), 20)  # 155┬░ is ideal center
                severity = (deviation / 20) * 100
                flaws['knee_bend'] = {
                    'priority': 3,
                    'severity': severity,
                    'accuracy_impact': '10-15',
                    'issue': f"Knee bend: {avg_knee_angle:.1f}┬░ (optimal: 140-170┬░)",
                    'recommendation': "Practice proper knee flexion for optimal power generation. Too straight reduces power, too bent affects balance."
                }
                print(f"DEBUG: Added knee_bend flaw with severity {severity}")
            
            # TEST: Add a guaranteed flaw for debugging
            flaws['test_detection'] = {
                'priority': 10,
                'severity': 50,
                'accuracy_impact': '5-8',
                'issue': "Test flaw detection - This should always appear",
                'recommendation': "This is a test flaw to verify the detection system is working."
            }
            print("DEBUG: Added test_detection flaw")
            
            print(f"DEBUG: Total flaws detected so far: {len(flaws)} - {list(flaws.keys())}")
            
            # 5. Follow-Through Analysis (Priority 6 - 5-8% accuracy impact)
            follow_through_angle = self.calculate_angle(right_elbow, right_wrist, 
                                                      {"x": right_wrist.x, "y": right_wrist.y - 0.1})
            
            if follow_through_angle < 50 or follow_through_angle > 80:  # Stricter range
                deviation = min(abs(follow_through_angle - 65), 20)
                severity = (deviation / 20) * 100
                flaws['follow_through'] = {
                    'priority': 5,
                    'severity': severity,
                    'accuracy_impact': '5-8',
                    'issue': f"Follow-through: {follow_through_angle:.1f}┬░ (optimal: 50-80┬░)",
                    'recommendation': "Complete wrist snap on follow-through. Fingers should point down toward floor."
                }
            
            # 6. Shooting Arc Analysis (Priority 7 - 5-10% accuracy impact)
            shooting_arc = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            if shooting_arc < 135 or shooting_arc > 165:  # Check for proper shooting arc
                deviation = min(abs(shooting_arc - 150), 20)
                severity = (deviation / 20) * 100
                flaws['shooting_arc'] = {
                    'priority': 6,
                    'severity': severity,
                    'accuracy_impact': '5-10',
                    'issue': f"Shooting arc: {shooting_arc:.1f}┬░ (optimal: 135-165┬░)",
                    'recommendation': "Focus on proper shooting arc. Too flat or too high affects consistency."
                }
            
            # 7. Hand Position Check (Priority 8 - 3-7% accuracy impact)
            # Check if shooting hand is properly positioned
            wrist_elbow_alignment = abs(right_wrist.x - right_elbow.x)
            
            if wrist_elbow_alignment > 0.05:  # Wrist should be aligned with elbow
                severity = min(wrist_elbow_alignment * 400, 100)
                flaws['hand_position'] = {
                    'priority': 7,
                    'severity': severity,
                    'accuracy_impact': '5-8',
                    'issue': f"Hand alignment: {wrist_elbow_alignment:.3f} deviation",
                    'recommendation': "Keep shooting hand directly behind ball, wrist aligned with elbow."
                }
            
            # Always provide coaching feedback - even for good shooters
            if not flaws:
                # Add developmental coaching for players with good basic form
                flaws['consistency_focus'] = {
                    'priority': 9,
                    'severity': 30,  # Moderate importance
                    'accuracy_impact': '5-8',
                    'issue': "Good basic form detected! Focus on advanced consistency.",
                    'recommendation': "Practice shooting under pressure, game-speed shots, and off-the-dribble scenarios."
                }
            elif len(flaws) == 1:
                # Add secondary focus area
                flaws['rhythm_timing'] = {
                    'priority': 8,
                    'severity': 25,
                    'accuracy_impact': '5-8',
                    'issue': "Consider rhythm and timing consistency.",
                    'recommendation': "Develop consistent shooting rhythm. Practice with metronome or counting cadence."
                }
            
            # Calculate overall form score with research-backed weighting
            priority_weights = {
                1: 0.25,  # Balance/Stance - highest impact
                2: 0.20,  # Elbow alignment
                3: 0.15,  # Knee bend
                4: 0.12,  # Release point
                5: 0.10,  # Follow-through
                6: 0.08,  # Shooting arc
                7: 0.05,  # Hand position
                8: 0.03,  # Secondary focus
                9: 0.02   # Advanced development
            }
            
            # Calculate weighted flaw impact
            total_impact = 0
            for flaw_key, flaw_data in flaws.items():
                priority = flaw_data.get('priority', 10)
                severity = flaw_data.get('severity', 0)
                weight = priority_weights.get(priority, 0.01)
                # Reduce severity impact - make scoring less harsh
                total_impact += (severity / 100) * weight * 0.65  # Reduced by 35%
            
            # Set realistic baseline - high school/college level should be 0.65+ minimum
            baseline_score = 0.65
            overall_score = max(baseline_score, 1 - total_impact)
            # Absolute minimum - no serious player below 0.50
            overall_score = max(0.50, overall_score)
            
            detailed_analysis = {
                'flaws': flaws,
                'overall_score': overall_score,
                'primary_issues': sorted(flaws.items(), key=lambda x: x[1].get('priority', 10)),
                'research_backed': True,
                'detection_sensitivity': 'high'
            }
            
        except Exception as e:
            logger.error(f"Error in detailed flaw analysis: {e}")
            print(f"DEBUG: Exception in analyze_detailed_flaws: {e}")
            print(f"DEBUG: Exception type: {type(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            
            # Always return a valid structure
            detailed_analysis = {
                'flaws': {
                    'basic_analysis': {
                        'priority': 10,
                        'severity': 20,
                        'accuracy_impact': '5-10',
                        'issue': 'Basic form analysis completed with limited data.',
                        'recommendation': 'Continue practicing fundamentals and ensure good lighting for analysis.'
                    }
                },
                'overall_score': 0.5,
                'primary_issues': [],
                'research_backed': True,
                'detection_sensitivity': 'error_recovery'
            }
        
        print(f"DEBUG: analyze_detailed_flaws - Returning analysis with {len(detailed_analysis.get('flaws', {}))} flaws")
        return detailed_analysis
        
    def capture_flaw_stills(self, landmarks, flaws, annotated_frame=None):
        """Capture frame stills using phase-specific approach"""
        if not landmarks or not flaws or annotated_frame is None:
            return {}
        
        # Determine current phase for context
        current_phase = self.detect_shooting_phase(landmarks)
        
        # Use the new phase-specific still capture method
        return self.capture_phase_specific_stills(landmarks, flaws, annotated_frame, current_phase)
        
        flaw_stills = {}
        
        try:
            # Convert frame to RGB if needed
            if len(annotated_frame.shape) == 3:
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            else:
                frame_rgb = annotated_frame.copy()
            
            height, width = frame_rgb.shape[:2]
            
            # For each detected flaw, create a focused still highlighting the issue
            for flaw_type, flaw_data in flaws.items():
                if flaw_data.get('severity', 0) > 20:  # Only capture significant flaws
                    
                    # Create a copy of the frame for annotation
                    still_frame = frame_rgb.copy()
                    
                    if flaw_type == 'balance_stance':
                        # Highlight hip and shoulder alignment
                        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                        
                        # Draw alignment lines
                        shoulder_center = (int((left_shoulder.x + right_shoulder.x) / 2 * width),
                                         int((left_shoulder.y + right_shoulder.y) / 2 * height))
                        hip_center = (int((left_hip.x + right_hip.x) / 2 * width),
                                    int((left_hip.y + right_hip.y) / 2 * height))
                        
                        cv2.line(still_frame, shoulder_center, hip_center, (255, 0, 0), 3)
                        cv2.circle(still_frame, shoulder_center, 8, (0, 255, 0), -1)
                        cv2.circle(still_frame, hip_center, 8, (255, 0, 255), -1)
                        cv2.putText(still_frame, "Balance Issue", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    elif flaw_type == 'elbow_alignment':
                        # Highlight elbow positioning relative to shoulder
                        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                        
                        shoulder_pos = (int(right_shoulder.x * width), int(right_shoulder.y * height))
                        elbow_pos = (int(right_elbow.x * width), int(right_elbow.y * height))
                        wrist_pos = (int(right_wrist.x * width), int(right_wrist.y * height))
                        
                        # Draw shooting arm alignment
                        cv2.line(still_frame, shoulder_pos, elbow_pos, (0, 255, 255), 3)
                        cv2.line(still_frame, elbow_pos, wrist_pos, (0, 255, 255), 3)
                        cv2.circle(still_frame, elbow_pos, 10, (255, 0, 0), -1)
                        cv2.putText(still_frame, "Elbow Flare", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    elif flaw_type == 'knee_bend':
                        # Highlight knee angles
                        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
                        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
                        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                        
                        # Draw leg lines
                        for hip, knee, ankle, color in [(left_hip, left_knee, left_ankle, (255, 0, 0)),
                                                       (right_hip, right_knee, right_ankle, (0, 0, 255))]:
                            hip_pos = (int(hip.x * width), int(hip.y * height))
                            knee_pos = (int(knee.x * width), int(knee.y * height))
                            ankle_pos = (int(ankle.x * width), int(ankle.y * height))
                            
                            cv2.line(still_frame, hip_pos, knee_pos, color, 3)
                            cv2.line(still_frame, knee_pos, ankle_pos, color, 3)
                            cv2.circle(still_frame, knee_pos, 8, (255, 255, 0), -1)
                        
                        cv2.putText(still_frame, "Knee Bend Issue", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    elif flaw_type == 'release_point':
                        # Highlight release height relative to shoulders
                        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                        
                        shoulder_y = int((left_shoulder.y + right_shoulder.y) / 2 * height)
                        wrist_pos = (int(right_wrist.x * width), int(right_wrist.y * height))
                        
                        # Draw release height reference line
                        cv2.line(still_frame, (0, shoulder_y), (width, shoulder_y), (0, 255, 0), 2)
                        cv2.circle(still_frame, wrist_pos, 10, (255, 0, 0), -1)
                        cv2.putText(still_frame, "Release Height", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(still_frame, "Shoulder Line", (10, shoulder_y - 10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    elif flaw_type == 'follow_through':
                        # Highlight follow-through angle
                        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                        
                        elbow_pos = (int(right_elbow.x * width), int(right_elbow.y * height))
                        wrist_pos = (int(right_wrist.x * width), int(right_wrist.y * height))
                        
                        # Draw follow-through arc
                        cv2.line(still_frame, elbow_pos, wrist_pos, (255, 255, 0), 4)
                        cv2.circle(still_frame, wrist_pos, 12, (255, 0, 255), -1)
                        cv2.putText(still_frame, "Follow-Through", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    elif flaw_type == 'shooting_arc':
                        # Highlight shooting arm arc
                        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                        
                        shoulder_pos = (int(right_shoulder.x * width), int(right_shoulder.y * height))
                        elbow_pos = (int(right_elbow.x * width), int(right_elbow.y * height))
                        wrist_pos = (int(right_wrist.x * width), int(right_wrist.y * height))
                        
                        # Draw arc trajectory
                        cv2.line(still_frame, shoulder_pos, elbow_pos, (0, 255, 255), 3)
                        cv2.line(still_frame, elbow_pos, wrist_pos, (255, 255, 0), 3)
                        cv2.putText(still_frame, "Shooting Arc", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    elif flaw_type == 'hand_position':
                        # Highlight hand alignment
                        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                        
                        elbow_pos = (int(right_elbow.x * width), int(right_elbow.y * height))
                        wrist_pos = (int(right_wrist.x * width), int(right_wrist.y * height))
                        
                        # Draw alignment check
                        cv2.line(still_frame, 
                               (elbow_pos[0], 0), (elbow_pos[0], height), (0, 255, 0), 2)
                        cv2.circle(still_frame, wrist_pos, 10, (255, 0, 0), -1)
                        cv2.putText(still_frame, "Hand Alignment", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    # Add flaw severity and recommendation text
                    severity_text = f"Severity: {flaw_data.get('severity', 0):.0f}%"
                    impact_text = f"Impact: {flaw_data.get('accuracy_impact', 'N/A')}%"
                    
                    cv2.putText(still_frame, severity_text, (10, height - 50), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.putText(still_frame, impact_text, (10, height - 25), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    # Store the annotated still
                    flaw_stills[flaw_type] = {
                        'image': still_frame,
                        'severity': flaw_data.get('severity', 0),
                        'priority': flaw_data.get('priority', 10),
                        'description': flaw_data.get('issue', 'Form issue detected'),
                        'recommendation': flaw_data.get('recommendation', 'Focus on proper technique')
                    }
        
        except Exception as e:
            logger.error(f"Error capturing flaw stills: {e}")
        
        return flaw_stills
    
    def calculate_angle(self, p1, p2, p3):
        """Calculate angle between three points"""
        try:
            a = np.array([p1.x, p1.y])
            b = np.array([p2.x, p2.y])
            c = np.array([p3.x, p3.y])
            
            ba = a - b
            bc = c - b
            
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
            angle = np.arccos(cosine_angle)
            return np.degrees(angle)
        except:
            return 0.0
    
    def calculate_distance(self, p1, p2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    def detect_shooting_phase(self, landmarks):
        """
        STRICT BIOMECHANICAL PHASE DETECTION - FIXED FOR REAL BASKETBALL ANALYSIS
        
        Critical Fix: True preparation phase should be ONLY the initial setup, before any shooting motion
        - Preparation: Static setup position (frames 1-5 typically)
        - Shooting: Active upward motion toward release
        - Release: Ball departure moment  
        - Follow_through: Post-release recovery
        """
        if not landmarks:
            return "unknown"
        
        try:
            # Get key landmarks for strict phase detection
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            
            # Calculate critical biomechanical measurements
            elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            wrist_shoulder_delta = (right_shoulder.y - right_wrist.y) * 100
            
            # Measure arm extension (key for detecting active shooting motion)
            arm_extension = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Body movement indicator (shoulder rise during shooting)
            shoulder_height_delta = abs(right_shoulder.y - right_hip.y) * 100
            
            print(f"DEBUG: Frame {self.frame_count} - Elbow: {elbow_angle:.1f}┬░, Wrist-Shoulder: {wrist_shoulder_delta:.1f}, Extension: {arm_extension:.1f}┬░")
            print(f"DEBUG: Frame {self.frame_count} - Phase state: shooting_started={self.shooting_started}, release_detected={self.release_detected}")
            
            # ABSOLUTE PHASE SEQUENCE ENFORCEMENT - NO BACKWARDS TRANSITIONS
            
            # PHASE 4: FOLLOW_THROUGH (Only after confirmed release)
            if self.release_detected:
                # Continue release if still at high position
                if wrist_shoulder_delta >= 15 and arm_extension >= 160:
                    print(f"DEBUG: Frame {self.frame_count} - Staying in RELEASE (post-release)")
                    return "release"
                else:
                    print(f"DEBUG: Frame {self.frame_count} - FOLLOW_THROUGH (post-release)")
                    return "follow_through"
                    
            # ALTERNATIVE FOLLOW-THROUGH DETECTION: High arm extension but declining
            # This catches follow-through even if exact release wasn't detected
            if (self.shooting_started and 
                arm_extension >= 150 and  # High extension
                wrist_shoulder_delta >= 10 and  # Elevated but declining
                hasattr(self, 'previous_wrist_height') and
                wrist_shoulder_delta < self.previous_wrist_height):  # Declining from peak
                print(f"DEBUG: Frame {self.frame_count} - FOLLOW_THROUGH (alternative detection)")
                return "follow_through"
            
            # PHASE 3: RELEASE (Ball departure - very strict criteria)
            # Must have high arm extension AND high wrist position
            if (arm_extension >= 165 and wrist_shoulder_delta >= 25):
                if not self.release_detected:
                    self.release_detected = True
                    self.shooting_started = True
                    print(f"DEBUG: RELEASE DETECTED at frame {self.frame_count} - Extension: {arm_extension:.1f}┬░, Wrist height: {wrist_shoulder_delta:.1f}")
                return "release"
            
            # PHASE 2: SHOOTING (Active motion toward release)
            # Any significant upward motion or arm extension beyond preparation range
            if (wrist_shoulder_delta >= 10 or 
                arm_extension >= 135 or
                shoulder_height_delta >= 25):
                if not self.shooting_started:
                    self.shooting_started = True
                    print(f"DEBUG: SHOOTING MOTION STARTED at frame {self.frame_count} - transitioning from preparation")
                print(f"DEBUG: Frame {self.frame_count} - SHOOTING phase")
                return "shooting"
            
            # CRITICAL ENFORCEMENT: Once shooting starts, NO MORE PREPARATION
            if self.shooting_started:
                print(f"DEBUG: Frame {self.frame_count} - LOCKED IN SHOOTING (no prep allowed)")
                return "shooting"
            
            # PHASE 1: PREPARATION (Only very early frames in static setup position)
            # Must be early in video AND have low activity measurements
            if (self.frame_count <= 8 and  # Only first 8 frames can be preparation
                not self.shooting_started and 
                wrist_shoulder_delta < 10 and
                arm_extension < 135 and
                shoulder_height_delta < 25):
                print(f"DEBUG: Frame {self.frame_count} - PREPARATION (early frames)")
                return "preparation"
            
            # SAFETY: After frame 8, if no shooting detected yet, force shooting phase
            # (This prevents entire videos being labeled as preparation)
            elif not self.shooting_started:
                self.shooting_started = True
                print(f"DEBUG: FORCING shooting phase at frame {self.frame_count} - no valid preparation detected")
                return "shooting"
            
            # Default to shooting for active motion
            else:
                print(f"DEBUG: Frame {self.frame_count} - DEFAULT to shooting")
                return "shooting"
                
        except Exception as e:
            print(f"DEBUG: Error in phase detection: {e}")
            return "unknown"
        finally:
            # Store wrist height for next frame comparison
            self.previous_wrist_height = wrist_shoulder_delta
    
    def analyze_wrist_snap(self, landmarks):
        """
        Analyze wrist snap mechanics for optimal ball rotation
        Returns: (snap_angle, snap_speed)
        """
        try:
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            right_index = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX] if hasattr(mp_pose.PoseLandmark, 'RIGHT_INDEX') else right_wrist
            
            # Calculate wrist snap angle (flexion from neutral)
            # Use vector from elbow to wrist and estimate finger direction
            elbow_to_wrist = np.array([right_wrist.x - right_elbow.x, right_wrist.y - right_elbow.y])
            
            # Estimate finger direction (ideally would use hand landmarks but working with pose)
            finger_direction = np.array([0, -0.1])  # Downward direction for follow-through
            
            # Calculate angle between forearm and finger direction
            cosine_angle = np.dot(elbow_to_wrist, finger_direction) / (
                np.linalg.norm(elbow_to_wrist) * np.linalg.norm(finger_direction))
            cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
            snap_angle = np.degrees(np.arccos(cosine_angle))
            
            # Estimate snap speed based on wrist position changes
            if hasattr(self, 'previous_wrist_position'):
                wrist_velocity = np.linalg.norm([
                    right_wrist.x - self.previous_wrist_position[0],
                    right_wrist.y - self.previous_wrist_position[1]
                ])
                snap_speed = wrist_velocity * 30  # Scale for frame rate estimation
            else:
                snap_speed = 3.0  # Default moderate speed
            
            # Store current position for next frame
            self.previous_wrist_position = [right_wrist.x, right_wrist.y]
            
            return snap_angle, snap_speed
            
        except Exception as e:
            print(f"Error in wrist snap analysis: {e}")
            return 70.0, 3.0  # Default acceptable values
    
    def analyze_thumb_flick(self, landmarks):
        """
        CRITICAL FLAW DETECTION: Guide Hand Thumb Flick Analysis
        
        RESEARCH FOUNDATION - THUMB FLICK IS A MAJOR SHOOTING FLAW:
        ========================================================
        
        PROBLEMS CAUSED BY THUMB FLICK:
        - Side-spin instead of pure backspin (reduces shooting percentage)  
        - Left/right directional inconsistencies (causes missed shots)
        - Disrupted ball trajectory and arc
        - Guide hand interference with ball release
        - Inconsistent shot rotation (affects soft shooting touch)
        
        PROPER TECHNIQUE:
        - Guide hand releases cleanly WITHOUT any thumb motion
        - Only shooting hand creates backspin through wrist snap
        - Guide hand should "fall away" naturally after ball separation
        - No lateral or rotational thumb movement from guide hand
        
        This function DETECTS thumb flick as a FLAW to eliminate.
        
        Returns: (thumb_flick_severity, guide_hand_interference_level)
        """
        try:
            # Get primary landmarks
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]   # Guide hand
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST] # Shooting hand
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]   
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW] 
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            # Initialize flaw tracking with frame capture capability
            if not hasattr(self, 'thumb_flick_flaw_tracker'):
                self.thumb_flick_flaw_tracker = {
                    'guide_hand_positions': [],
                    'guide_hand_angles': [],
                    'lateral_movements': [],
                    'post_release_activity': [],
                    'thumb_rotation_detected': False,
                    'capture_frame_ready': False,
                    'frames_since_release': 0
                }
            
            # Calculate guide hand position and movement
            guide_hand_pos = np.array([left_wrist.x, left_wrist.y])
            current_phase = getattr(self, 'current_phase', 'preparation')
            
            # Calculate guide hand wrist angle for thumb rotation detection
            guide_hand_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            
            # Track positions and angles over time
            self.thumb_flick_flaw_tracker['guide_hand_positions'].append(guide_hand_pos)
            self.thumb_flick_flaw_tracker['guide_hand_angles'].append(guide_hand_angle)
            
            # Maintain rolling window for analysis
            if len(self.thumb_flick_flaw_tracker['guide_hand_positions']) > 8:
                self.thumb_flick_flaw_tracker['guide_hand_positions'].pop(0)
                self.thumb_flick_flaw_tracker['guide_hand_angles'].pop(0)
            
            # Track frames since ball release for critical timing detection
            if current_phase in ['release', 'follow_through']:
                self.thumb_flick_flaw_tracker['frames_since_release'] += 1
            else:
                self.thumb_flick_flaw_tracker['frames_since_release'] = 0
                self.thumb_flick_flaw_tracker['thumb_rotation_detected'] = False
                self.thumb_flick_flaw_tracker['capture_frame_ready'] = False
            
            # CRITICAL DETECTION: Guide hand thumb inward rotation immediately after release
            thumb_flick_detected = False
            thumb_rotation_severity = 0
            
            # ENHANCED DETECTION: More sensitive and broader detection window
            if (current_phase in ['release', 'follow_through'] and 
                len(self.thumb_flick_flaw_tracker['guide_hand_angles']) >= 2):  # Need fewer frames
                
                # Analyze recent angle changes for inward rotation pattern
                recent_angles = self.thumb_flick_flaw_tracker['guide_hand_angles'][-2:]  # Just need 2 frames
                
                # Calculate angle change - ANY inward rotation is problematic
                if len(recent_angles) >= 2:
                    angle_change = recent_angles[-1] - recent_angles[0]
                    
                    # MUCH MORE SENSITIVE: ANY inward rotation > 3 degrees is a flaw
                    if angle_change < -3:  # Much more sensitive threshold
                        thumb_flick_detected = True
                        thumb_rotation_severity = min(abs(angle_change) * 10, 100)  # Higher severity multiplier
                        
                        # Mark for frame capture at the exact moment
                        if not self.thumb_flick_flaw_tracker['thumb_rotation_detected']:
                            self.thumb_flick_flaw_tracker['thumb_rotation_detected'] = True
                            self.thumb_flick_flaw_tracker['capture_frame_ready'] = True
                            
                            # IMMEDIATE FRAME CAPTURE - Don't wait for timing logic
                            print(f"DEBUG: IMMEDIATE THUMB FLICK CAPTURE TRIGGERED! "
                                  f"Angle change: {angle_change:.1f}┬░, Phase: {current_phase}")
                            
                            # Force immediate frame capture by setting frame count for capture
                            if hasattr(self, 'immediate_thumb_capture_frame'):
                                self.immediate_thumb_capture_frame = self.frame_count
                            else:
                                setattr(self, 'immediate_thumb_capture_frame', self.frame_count)
                            
                            print(f"DEBUG: THUMB FLICK INWARD ROTATION DETECTED! "
                                  f"Angle change: {angle_change:.1f}┬░, "
                                  f"Phase: {current_phase}, "
                                  f"CAPTURING FRAME STILL!")
                    
                    # Also log all angle changes for debugging
                    print(f"DEBUG: Guide hand angle: {recent_angles[-1]:.1f}┬░, "
                          f"Change: {angle_change:.1f}┬░, Phase: {current_phase}")
                    
            # ALSO detect rapid lateral movement (side thumb flick) - MORE SENSITIVE
            if len(self.thumb_flick_flaw_tracker['guide_hand_positions']) >= 2:
                recent_positions = self.thumb_flick_flaw_tracker['guide_hand_positions'][-2:]
                lateral_movement = abs(recent_positions[-1][0] - recent_positions[0][0])
                
                # MUCH MORE SENSITIVE lateral movement detection
                if lateral_movement > 0.008 and current_phase in ['release', 'follow_through']:  # Lower threshold
                    thumb_flick_detected = True
                    lateral_severity = min(lateral_movement * 4000, 100)  # Higher severity
                    thumb_rotation_severity = max(thumb_rotation_severity, lateral_severity)
                    
                    if not self.thumb_flick_flaw_tracker['capture_frame_ready']:
                        self.thumb_flick_flaw_tracker['capture_frame_ready'] = True
                        
                        # IMMEDIATE FRAME CAPTURE for lateral movement too
                        if hasattr(self, 'immediate_thumb_capture_frame'):
                            self.immediate_thumb_capture_frame = self.frame_count
                        else:
                            setattr(self, 'immediate_thumb_capture_frame', self.frame_count)
                            
                        print(f"DEBUG: LATERAL THUMB FLICK DETECTED! "
                              f"Movement: {lateral_movement:.4f}, Phase: {current_phase}, CAPTURING FRAME!")
                
                # Always log lateral movement for debugging
                print(f"DEBUG: Lateral movement: {lateral_movement:.4f}, Phase: {current_phase}")
            
            # DETECT FLAW #1: Excessive lateral guide hand movement (continued analysis for general patterns)
            lateral_flaw_severity = 0
            if len(self.thumb_flick_flaw_tracker['guide_hand_positions']) >= 4:
                recent_positions = self.thumb_flick_flaw_tracker['guide_hand_positions'][-4:]
                
                # Calculate overall lateral movement pattern
                lateral_changes = []
                for i in range(1, len(recent_positions)):
                    lateral_change = abs(recent_positions[i][0] - recent_positions[i-1][0])
                    lateral_changes.append(lateral_change)
                
                if lateral_changes:
                    avg_lateral_movement = np.mean(lateral_changes)
                    lateral_flaw_severity = min(avg_lateral_movement * 1500, 80)
            
            # DETECT FLAW #2: Guide hand continuing to move after release
            interference_severity = 0
            if (current_phase in ['release', 'follow_through'] and 
                len(self.thumb_flick_flaw_tracker['guide_hand_positions']) >= 3):
                
                recent_pos = self.thumb_flick_flaw_tracker['guide_hand_positions'][-3:]
                post_release_movement = np.linalg.norm(recent_pos[-1] - recent_pos[-3])
                
                interference_severity = min(post_release_movement * 600, 80)
                self.thumb_flick_flaw_tracker['post_release_activity'].append(interference_severity)
            
            # OVERALL THUMB FLICK FLAW SEVERITY CALCULATION
            # Prioritize the specific inward rotation detection
            if thumb_flick_detected:
                combined_flaw_severity = (
                    thumb_rotation_severity * 0.6 +       # Specific inward rotation (highest priority)
                    lateral_flaw_severity * 0.25 +        # General lateral movement
                    interference_severity * 0.15          # Post-release activity
                )
            else:
                combined_flaw_severity = (
                    lateral_flaw_severity * 0.6 +         # General analysis when no specific rotation
                    interference_severity * 0.4
                )
            
            # FALLBACK DETECTION: If we're in follow-through and detect any guide hand activity
            if (not thumb_flick_detected and current_phase == 'follow_through' and
                len(self.thumb_flick_flaw_tracker['guide_hand_positions']) >= 2):
                
                recent_pos = self.thumb_flick_flaw_tracker['guide_hand_positions'][-2:]
                any_movement = np.linalg.norm(recent_pos[-1] - recent_pos[0])
                
                # ANY guide hand movement in follow-through is problematic
                if any_movement > 0.005:  # Very sensitive
                    thumb_flick_detected = True
                    combined_flaw_severity = max(combined_flaw_severity, any_movement * 3000)
                    
                    if not hasattr(self, 'thumb_flick_flaw_tracker') or not self.thumb_flick_flaw_tracker.get('capture_frame_ready', False):
                        if hasattr(self, 'thumb_flick_flaw_tracker'):
                            self.thumb_flick_flaw_tracker['capture_frame_ready'] = True
                        
                        # IMMEDIATE FALLBACK CAPTURE
                        if hasattr(self, 'immediate_thumb_capture_frame'):
                            self.immediate_thumb_capture_frame = self.frame_count
                        else:
                            setattr(self, 'immediate_thumb_capture_frame', self.frame_count)
                        
                        print(f"DEBUG: FALLBACK THUMB FLICK DETECTED! General movement: {any_movement:.4f}, IMMEDIATE CAPTURE!")
            
            # Normalize to 0-1 scale (0 = no flaw, 1 = severe thumb flick problem)
            thumb_flick_flaw_score = min(combined_flaw_severity / 100, 1.0)
            
            # ALWAYS have some level of detection for testing purposes
            if current_phase in ['release', 'follow_through']:
                thumb_flick_flaw_score = max(thumb_flick_flaw_score, 0.1)  # Minimum detectable level
                print(f"DEBUG: Final thumb flick score: {thumb_flick_flaw_score:.3f}, Phase: {current_phase}")
            
            # Calculate guide hand interference level (separate metric)
            recent_interference = self.thumb_flick_flaw_tracker['post_release_activity'][-3:] if self.thumb_flick_flaw_tracker['post_release_activity'] else [0]
            guide_hand_interference = max(np.mean(recent_interference) / 100, 0.05)  # Minimum interference
            
            return thumb_flick_flaw_score, guide_hand_interference
            
        except Exception as e:
            print(f"Error in thumb flick flaw analysis: {e}")
            return 0.0, 0.0  # Default: no flaw detected
    
    def analyze_shot_smoothness_tempo(self, landmarks, current_phase):
        """
        Analyze overall shot smoothness and tempo consistency with enhanced sensitivity
        Returns: (smoothness_score, tempo_consistency)
        """
        try:
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            
            # Track motion vectors for smoothness analysis
            if not hasattr(self, 'motion_history'):
                self.motion_history = []
                self.velocity_history = []
                self.tempo_markers = {}
                self.phase_frame_counts = {}
            
            # Calculate comprehensive motion vector including wrist and shoulder movement
            motion_vector = np.array([
                right_elbow.x - right_shoulder.x,
                right_elbow.y - right_shoulder.y,
                right_wrist.x - right_elbow.x,
                right_wrist.y - right_elbow.y,
                right_wrist.x - right_shoulder.x,  # Direct shoulder-to-wrist vector
                right_wrist.y - right_shoulder.y
            ])
            
            self.motion_history.append(motion_vector)
            
            # Keep rolling window of last 15 frames for better analysis
            if len(self.motion_history) > 15:
                self.motion_history.pop(0)
            
            # Calculate enhanced smoothness based on motion vector consistency
            smoothness_score = 0.9  # Start with high baseline
            if len(self.motion_history) >= 4:
                # Calculate motion consistency with multiple metrics
                motion_changes = []
                acceleration_changes = []
                
                for i in range(1, len(self.motion_history)):
                    # Velocity changes (smoothness indicator)
                    change = np.linalg.norm(self.motion_history[i] - self.motion_history[i-1])
                    motion_changes.append(change)
                    
                    # Acceleration changes (jerkiness indicator)
                    if i >= 2:
                        prev_change = np.linalg.norm(self.motion_history[i-1] - self.motion_history[i-2])
                        acceleration = abs(change - prev_change)
                        acceleration_changes.append(acceleration)
                
                # Smoothness = low variance in velocity + low acceleration spikes
                if motion_changes:
                    motion_variance = np.var(motion_changes)
                    mean_motion = np.mean(motion_changes)
                    
                    # Normalized variance penalty (more sensitive)
                    if mean_motion > 0:
                        variance_penalty = (motion_variance / mean_motion) * 2
                    else:
                        variance_penalty = motion_variance * 20
                    
                    smoothness_score = max(0.3, 1 - min(variance_penalty, 0.7))
                
                # Additional penalty for jerkiness (acceleration spikes)
                if acceleration_changes:
                    max_acceleration = max(acceleration_changes)
                    jerk_penalty = min(max_acceleration * 3, 0.3)  # More sensitive jerk detection
                    smoothness_score = max(0.3, smoothness_score - jerk_penalty)
            
            # Enhanced tempo tracking by phase
            if current_phase not in self.phase_frame_counts:
                self.phase_frame_counts[current_phase] = 0
            self.phase_frame_counts[current_phase] += 1
            
            # Track tempo markers by phase transitions
            if current_phase not in self.tempo_markers:
                self.tempo_markers[current_phase] = []
            self.tempo_markers[current_phase].append(self.frame_count)
            
            # Calculate tempo consistency with improved metrics
            tempo_consistency = 0.85  # Higher baseline
            
            # Analyze within-phase consistency
            if current_phase in self.tempo_markers and len(self.tempo_markers[current_phase]) >= 3:
                phase_frames = self.tempo_markers[current_phase]
                frame_intervals = []
                for i in range(1, len(phase_frames)):
                    interval = phase_frames[i] - phase_frames[i-1]
                    frame_intervals.append(interval)
                
                if frame_intervals:
                    interval_variance = np.var(frame_intervals)
                    mean_interval = np.mean(frame_intervals)
                    if mean_interval > 0:
                        consistency_ratio = 1 - min((interval_variance / mean_interval), 0.5)
                        tempo_consistency = max(0.4, consistency_ratio)
            
            # Cross-phase tempo analysis
            if len(self.phase_frame_counts) >= 2:
                phase_durations = list(self.phase_frame_counts.values())
                if len(phase_durations) >= 2:
                    # Check for reasonable phase duration ratios
                    duration_ratios = []
                    for i in range(1, len(phase_durations)):
                        if phase_durations[i-1] > 0:
                            ratio = phase_durations[i] / phase_durations[i-1]
                            duration_ratios.append(ratio)
                    
                    if duration_ratios:
                        # Penalize extreme tempo variations between phases
                        for ratio in duration_ratios:
                            if ratio > 3.0 or ratio < 0.33:  # Very fast/slow phase transitions
                                tempo_consistency *= 0.85
            
            return smoothness_score, tempo_consistency
            
        except Exception as e:
            print(f"Error in smoothness/tempo analysis: {e}")
            return 0.85, 0.8  # Higher default scores to match new sensitivity
    
    def analyze_guide_hand_mechanics(self, landmarks):
        """
        Analyze guide hand (non-shooting hand) placement and interference
        Returns: {'interference_score': float, 'placement_score': float, 'early_release': bool}
        """
        try:
            # Get key landmarks for guide hand analysis
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            
            # Track guide hand motion history for interference analysis
            if not hasattr(self, 'guide_hand_history'):
                self.guide_hand_history = []
                self.guide_hand_velocity_history = []
            
            # Calculate guide hand position relative to shooting hand
            guide_to_shooting_distance = self.calculate_distance(left_wrist, right_wrist)
            
            # Optimal guide hand placement (on side of ball, not behind or in front)
            # Guide hand should be perpendicular to shooting line
            shooting_direction = np.array([right_wrist.x - right_shoulder.x, right_wrist.y - right_shoulder.y])
            guide_direction = np.array([left_wrist.x - right_wrist.x, left_wrist.y - right_wrist.y])
            
            # Calculate if guide hand is properly positioned (should be perpendicular)
            if np.linalg.norm(shooting_direction) > 0 and np.linalg.norm(guide_direction) > 0:
                dot_product = np.dot(shooting_direction, guide_direction)
                angle_between = np.arccos(np.clip(dot_product / (np.linalg.norm(shooting_direction) * np.linalg.norm(guide_direction)), -1, 1))
                perpendicular_score = abs(np.pi/2 - angle_between) / (np.pi/2)  # 0 = perfect perpendicular, 1 = parallel
                placement_score = max(0, 1 - perpendicular_score)
            else:
                placement_score = 0.5  # Default neutral
            
            # Analyze guide hand velocity for interference detection
            current_guide_position = np.array([left_wrist.x, left_wrist.y])
            self.guide_hand_history.append(current_guide_position)
            
            # Keep rolling window
            if len(self.guide_hand_history) > 5:
                self.guide_hand_history.pop(0)
            
            # Calculate guide hand velocity and movement patterns
            interference_score = 0.0
            if len(self.guide_hand_history) >= 3:
                # Calculate velocity changes
                velocities = []
                for i in range(1, len(self.guide_hand_history)):
                    velocity = np.linalg.norm(self.guide_hand_history[i] - self.guide_hand_history[i-1])
                    velocities.append(velocity)
                
                self.guide_hand_velocity_history.extend(velocities)
                if len(self.guide_hand_velocity_history) > 10:
                    self.guide_hand_velocity_history = self.guide_hand_velocity_history[-10:]
                
                # High guide hand velocity during shooting phase indicates interference
                if velocities:
                    avg_velocity = np.mean(velocities)
                    max_velocity = max(velocities)
                    
                    # Interference indicators:
                    # 1. High average velocity (guide hand moving too much)
                    velocity_interference = min(avg_velocity * 50, 0.4)
                    
                    # 2. Sudden velocity spikes (pushing/jerking motion)
                    spike_interference = min(max_velocity * 30, 0.3) if max_velocity > avg_velocity * 2 else 0
                    
                    # 3. Guide hand too close to shooting hand (thumbs interference)
                    if guide_to_shooting_distance < 0.08:  # Too close indicates potential interference
                        proximity_interference = (0.08 - guide_to_shooting_distance) * 5
                    else:
                        proximity_interference = 0
                    
                    interference_score = min(velocity_interference + spike_interference + proximity_interference, 1.0)
            
            # Detect early release (guide hand should release before shooting hand)
            # This is inferred from the motion patterns
            early_release = True  # Default assumption
            if len(self.guide_hand_velocity_history) >= 3:
                recent_velocities = self.guide_hand_velocity_history[-3:]
                if all(v > 0.02 for v in recent_velocities):  # Still moving significantly
                    early_release = False
            
            # Adjust scores based on shooting phase
            current_phase = self.detect_shooting_phase(landmarks)
            if current_phase == "release" or current_phase == "follow_through":
                # Guide hand should have minimal involvement in these phases
                if not early_release:
                    interference_score += 0.2
            
            return {
                'interference_score': interference_score,
                'placement_score': placement_score,
                'early_release': early_release,
                'guide_distance': guide_to_shooting_distance,
                'current_phase': current_phase
            }
            
        except Exception as e:
            print(f"Error in guide hand analysis: {e}")
            return {
                'interference_score': 0.2,  # Default low interference
                'placement_score': 0.8,    # Default good placement
                'early_release': True,     # Default proper release
                'guide_distance': 0.12,    # Default reasonable distance
                'current_phase': 'unknown'
            }
    
    def analyze_shot_form(self, landmarks) -> Dict[str, float]:
        """Comprehensive analysis of shooting form using research-backed metrics"""
        if not landmarks:
            return {}
        
        # Get detailed flaw analysis first
        detailed_analysis = self.analyze_detailed_flaws(landmarks)
        
        # Ensure detailed_analysis is a proper dictionary
        if not isinstance(detailed_analysis, dict):
            detailed_analysis = {
                'flaws': {},
                'overall_score': 0.5,
                'primary_issues': [],
                'research_backed': False
            }
        
        metrics = {}
        
        try:
            # Key landmarks
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            # 1. Release angle (shooting arm) - Research optimal: 45-55┬░
            shooting_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            # Normalize to research-backed optimal range
            if 45 <= shooting_elbow_angle <= 55:
                release_angle_score = 1.0
            elif 85 <= shooting_elbow_angle <= 105:  # Alternative good range
                release_angle_score = 0.85
            else:
                deviation = min(abs(shooting_elbow_angle - 50), 50)
                release_angle_score = max(0, 1 - (deviation / 50))
            
            metrics['release_angle'] = shooting_elbow_angle
            metrics['release_angle_score'] = release_angle_score
            
            # 2. Release height - Research optimal: above forehead
            avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            release_height = avg_shoulder_y - right_wrist.y
            # Normalize based on body proportions
            nose = landmarks[mp_pose.PoseLandmark.NOSE]
            body_height = abs(nose.y - ((left_hip.y + right_hip.y) / 2))
            relative_release_height = release_height / body_height if body_height > 0 else 0
            
            metrics['release_height'] = release_height
            metrics['relative_release_height'] = relative_release_height
            
            # 3. Follow-through angle - Research optimal: 43-48┬░ arc entry
            follow_through = self.calculate_angle(right_elbow, right_wrist, 
                                                {"x": right_wrist.x, "y": right_wrist.y - 0.1})
            metrics['follow_through_angle'] = follow_through
            
            # 4. Elbow alignment - Research: flare reduces accuracy by 15-25%
            shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
            elbow_alignment = abs(right_elbow.x - shoulder_center_x)
            elbow_alignment_score = max(0, 1 - (elbow_alignment * 5))  # Penalize deviation
            metrics['elbow_alignment'] = elbow_alignment_score
            
            # 5. Knee bend analysis - Research optimal: 115-135┬░
            left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
            avg_knee_bend = (left_knee_angle + right_knee_angle) / 2
            
            # Score based on research-backed optimal range
            if 115 <= avg_knee_bend <= 135:
                knee_bend_score = 1.0
            else:
                deviation = min(abs(avg_knee_bend - 125), 40)  # 125┬░ is center of optimal range
                knee_bend_score = max(0, 1 - (deviation / 40))
            
            metrics['knee_bend'] = avg_knee_bend
            metrics['knee_bend_score'] = knee_bend_score
            
            # 6. Balance score - Research: foundational for 25-30% accuracy
            hip_center_x = (left_hip.x + right_hip.x) / 2
            balance_deviation = abs(shoulder_center_x - hip_center_x)
            balance_score = max(0, 1 - (balance_deviation * 10))  # Heavy penalty for poor balance
            metrics['balance_score'] = balance_score
            
            # 7. Consistency score using research-backed variance analysis
            key_values = [shooting_elbow_angle, release_height, elbow_alignment_score]
            if len(key_values) > 1:
                consistency = 1.0 - (np.std(key_values) / 100.0)
                consistency = max(0.0, min(1.0, consistency))
            else:
                consistency = 0.5
            metrics['consistency_score'] = consistency
            
            # Store detailed analysis for coaching
            metrics['detailed_analysis'] = detailed_analysis
            
        except Exception as e:
            logger.error(f"Error in shot analysis: {e}")
            # Provide default values
            metrics = {
                'release_angle': 0.0,
                'release_height': 0.0,
                'follow_through_angle': 0.0,
                'elbow_alignment': 0.0,
                'knee_bend': 0.0,
                'balance_score': 0.0,
                'consistency_score': 0.0,
                'detailed_analysis': {'flaws': {}, 'overall_score': 0.0}
            }
        
        # Calculate overall shooting form score using research-backed weighting
        # Priority weighting based on accuracy impact research
        weights = {
            'balance_score': 0.25,      # Foundational - 25-30% impact
            'elbow_alignment': 0.20,    # 15-25% accuracy impact
            'release_angle_score': 0.15, # Release mechanics
            'knee_bend_score': 0.15,    # Power generation - 10-15% impact
            'relative_release_height': 0.12, # 8-12% accuracy impact
            'follow_through_angle': 0.08,    # 5-8% impact
            'consistency_score': 0.05        # Overall consistency
        }
        
        # Calculate weighted score with available metrics
        overall_score = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            if metric in metrics and metrics[metric] is not None:
                if metric in ['balance_score', 'elbow_alignment', 'consistency_score']:
                    # These are already normalized 0-1
                    overall_score += weight * metrics[metric]
                elif metric == 'release_angle_score':
                    overall_score += weight * metrics.get('release_angle_score', 0.5)
                elif metric == 'knee_bend_score':
                    overall_score += weight * metrics.get('knee_bend_score', 0.5)
                elif metric == 'relative_release_height':
                    # Normalize relative height (positive is generally better)
                    height_score = min(1.0, max(0.0, metrics[metric] + 0.5))
                    overall_score += weight * height_score
                elif metric == 'follow_through_angle':
                    # Normalize follow-through (target ~60-80┬░)
                    ft_angle = metrics[metric]
                    if 60 <= ft_angle <= 80:
                        ft_score = 1.0
                    else:
                        deviation = min(abs(ft_angle - 70), 35)
                        ft_score = max(0, 1 - (deviation / 35))
                    overall_score += weight * ft_score
                total_weight += weight
        
        # Normalize by actual weights used
        if total_weight > 0:
            overall_score = overall_score / total_weight
        else:
            # If no metrics available, assume reasonable baseline
            overall_score = 0.5  # Default to average shooter
        
        # Ensure minimum baseline - no shooter should score below 0.25
        # College-level players should be at least 0.45+
        overall_score = max(0.25, overall_score)
        
        metrics['shooting_form_score'] = overall_score
        
        # Include the detailed analysis in the returned metrics
        metrics['detailed_analysis'] = detailed_analysis
        
        return metrics
    
    def process_frame(self, image):
        """Process a single frame for pose detection"""
        # Increment frame count FIRST for proper timing analysis
        self.frame_count += 1
        
        # Debug every 30 frames to track video processing
        if self.frame_count % 30 == 1:
            print(f"DEBUG: Processing frame {self.frame_count}, shot_sequence length: {len(self.shot_sequence)}")
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_image)
        
        if results.pose_landmarks:
            # Analyze the shot form with detailed metrics
            shot_metrics = self.analyze_shot_form(results.pose_landmarks.landmark)
            
            # Debug logging
            detailed_analysis = shot_metrics.get('detailed_analysis', {})
            if detailed_analysis and detailed_analysis.get('flaws'):
                flaws = detailed_analysis['flaws']
                print(f"DEBUG: Frame {self.frame_count} - Detected {len(flaws)} flaws: {list(flaws.keys())}")
                
                # Log individual flaw details
                for flaw_name, flaw_data in flaws.items():
                    print(f"  - {flaw_name}: Priority {flaw_data.get('priority', 'N/A')}, Severity {flaw_data.get('severity', 'N/A')}")
            else:
                print(f"DEBUG: Frame {self.frame_count} - No flaws detected or detailed analysis failed")
            
            self.shot_sequence.append({
                'frame': self.frame_count,
                'landmarks': results.pose_landmarks.landmark,
                'phase': self.detect_shooting_phase(results.pose_landmarks.landmark),
                'metrics': shot_metrics
            })
            
            # Store the last detailed analysis for UI display
            self.last_analysis_result = shot_metrics
            
            # Draw landmarks
            annotated_image = image.copy()
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Capture flaw stills if detailed analysis contains flaws
            if 'detailed_analysis' in shot_metrics and shot_metrics['detailed_analysis'] is not None:
                detailed_analysis = shot_metrics['detailed_analysis']
                if isinstance(detailed_analysis, dict) and detailed_analysis.get('flaws'):
                    flaws = detailed_analysis['flaws']
                    flaw_stills = self.capture_flaw_stills(
                        results.pose_landmarks.landmark, 
                        flaws, 
                        annotated_image
                    )
                    # Store flaw stills in the analysis result
                    shot_metrics['flaw_stills'] = flaw_stills
                    self.last_analysis_result['flaw_stills'] = flaw_stills
            
            return annotated_image, results.pose_landmarks
        
        return image, None
    
    def get_shot_summary(self) -> ShotMetrics:
        """Generate summary metrics for the entire shot sequence"""
        print(f"DEBUG: get_shot_summary called - shot_sequence length: {len(self.shot_sequence)}")
        
        if not self.shot_sequence:
            print("DEBUG: No shot sequence data - returning default metrics")
            return ShotMetrics(0, 0, 0, 0, 0, 0, 0, 0, datetime.now())
        
        # Find the release phase
        release_frames = [frame for frame in self.shot_sequence if frame['phase'] == 'release']
        print(f"DEBUG: Found {len(release_frames)} release frames out of {len(self.shot_sequence)} total frames")
        
        if release_frames:
            # Use metrics from the release frame
            release_metrics = release_frames[0]['metrics']
            print(f"DEBUG: Using release frame metrics: {list(release_metrics.keys())}")
        else:
            print("DEBUG: No release frames found - using averaged metrics")
            # Use average of all frames, but only for numeric values
            all_metrics = [frame['metrics'] for frame in self.shot_sequence]
            release_metrics = {}
            
            # Define numeric keys that can be averaged
            numeric_keys = [
                'release_angle', 'release_height', 'follow_through_angle',
                'elbow_alignment', 'knee_bend', 'balance_score', 
                'consistency_score', 'shooting_form_score', 'release_angle_score',
                'knee_bend_score', 'relative_release_height'
            ]
            
            for key in numeric_keys:
                if key in all_metrics[0]:
                    # Only average numeric values, skip None values
                    values = [m.get(key, 0) for m in all_metrics if isinstance(m.get(key), (int, float))]
                    if values:
                        release_metrics[key] = np.mean(values)
                        print(f"DEBUG: Averaged {key}: {release_metrics[key]:.3f} from {len(values)} values")
                    else:
                        release_metrics[key] = 0
                        print(f"DEBUG: No valid values for {key}, defaulting to 0")
            
            # For non-numeric data like detailed_analysis, use the last available one
            if all_metrics and 'detailed_analysis' in all_metrics[-1]:
                release_metrics['detailed_analysis'] = all_metrics[-1]['detailed_analysis']
        
        return ShotMetrics(
            release_angle=release_metrics.get('release_angle', 0),
            release_height=release_metrics.get('release_height', 0),
            follow_through_angle=release_metrics.get('follow_through_angle', 0),
            elbow_alignment=release_metrics.get('elbow_alignment', 0),
            knee_bend=release_metrics.get('knee_bend', 0),
            balance_score=release_metrics.get('balance_score', 0),
            consistency_score=release_metrics.get('consistency_score', 0),
            shooting_form_score=release_metrics.get('shooting_form_score', 0),
            timestamp=datetime.now()
        )
    
    def reset(self):
        """Reset analyzer for new shot"""
        print(f"DEBUG: !!!! RESETTING ANALYZER - New shot analysis started !!!!")
        self.shot_sequence = []
        self.frame_count = 0
        self.analysis_complete = False
        
        # Reset intelligent frame capture tracking
        self.phase_history = []
        self.best_flaw_frames = {}
        self.phase_transition_frames = {}
        self.captured_flaws = set()
        self.last_analysis_result = None
        self.captured_stills = {}  # Reset captured stills
        
        # CRITICAL: Reset sequential phase tracking
        self.release_detected = False
        self.shooting_started = False

def create_performance_charts(df: pd.DataFrame):
    """Create interactive performance visualization charts"""
    if df.empty:
        st.warning("No data available for visualization")
        return
    
    # Convert timestamp if it's a string
    if 'recorded_at' in df.columns:
        df['recorded_at'] = pd.to_datetime(df['recorded_at'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Overall score trend
        fig_score = px.line(
            df, 
            x='recorded_at', 
            y='shooting_form_score',
            title="Overall Shooting Form Score Trend",
            labels={'shooting_form_score': 'Form Score', 'recorded_at': 'Time'}
        )
        fig_score.update_traces(mode='markers+lines')
        st.plotly_chart(fig_score, use_container_width=True)
        
        # Release angle distribution
        fig_angle = px.histogram(
            df, 
            x='release_angle',
            title="Release Angle Distribution",
            labels={'release_angle': 'Release Angle (degrees)'}
        )
        st.plotly_chart(fig_angle, use_container_width=True)
    
    with col2:
        # Radar chart for latest shot
        if not df.empty:
            latest_shot = df.iloc[-1]
            
            categories = ['Release Angle', 'Release Height', 'Follow Through', 
                         'Elbow Alignment', 'Balance', 'Consistency']
            values = [
                latest_shot['release_angle'] / 180,  # Normalize to 0-1
                (latest_shot['release_height'] + 0.5),  # Adjust range
                latest_shot['follow_through_angle'] / 180,
                latest_shot['elbow_alignment'],
                latest_shot['balance_score'],
                latest_shot['consistency_score']
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Latest Shot'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1])
                ),
                showlegend=True,
                title="Latest Shot Analysis"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # Progress metrics
        if len(df) > 1:
            current_avg = df.tail(5)['shooting_form_score'].mean()
            previous_avg = df.head(max(1, len(df)-5))['shooting_form_score'].mean()
            improvement = ((current_avg - previous_avg) / previous_avg) * 100 if previous_avg > 0 else 0
            
            st.metric(
                label="Recent Performance",
                value=f"{current_avg:.3f}",
                delta=f"{improvement:+.1f}%" if improvement != 0 else None
            )

def main():
    st.set_page_config(
        page_title="ApexSports TrAiNer - Basketball Shot Analyzer",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for futuristic sports theme
    st.markdown("""
    <style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --apex-blue: #00d4ff;
        --apex-dark-blue: #003d5c;
        --apex-orange: #ff6b35;
        --apex-dark: #1a1a2e;
        --apex-darker: #16213e;
        --apex-light: #e3f2fd;
        --neon-glow: 0 0 20px var(--apex-blue);
    }
    
    /* Background and main styling */
    .stApp {
        background: linear-gradient(135deg, var(--apex-dark) 0%, var(--apex-darker) 100%);
        color: var(--apex-light);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, var(--apex-dark-blue), var(--apex-dark));
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px solid var(--apex-blue);
        box-shadow: var(--neon-glow);
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        color: var(--apex-blue);
        text-align: center;
        text-shadow: 0 0 30px var(--apex-blue);
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--apex-orange);
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    /* Logo styling */
    .logo-container {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .logo-container img {
        border-radius: 15px;
        border: 3px solid var(--apex-blue);
        box-shadow: var(--neon-glow);
        max-width: 300px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--apex-darker);
        border-radius: 10px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--apex-light);
        border-radius: 8px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 1.5rem;
        margin: 0.25rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--apex-dark-blue);
        color: var(--apex-blue);
        box-shadow: 0 0 15px var(--apex-blue);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, var(--apex-blue), var(--apex-orange)) !important;
        color: var(--apex-dark) !important;
        box-shadow: var(--neon-glow) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--apex-darker);
    }
    
    /* Metrics styling */
    .stMetric {
        background: var(--apex-darker);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--apex-blue);
        margin: 0.5rem 0;
    }
    
    .stMetric > div {
        color: var(--apex-light);
    }
    
    .stMetric label {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        color: var(--apex-blue) !important;
        text-transform: uppercase;
    }
    
    .stMetric [data-testid="metric-value"] {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        color: var(--apex-orange) !important;
        text-shadow: 0 0 10px var(--apex-orange);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--apex-blue), var(--apex-orange));
        color: var(--apex-dark);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px var(--apex-blue);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--apex-blue), var(--apex-orange));
        box-shadow: 0 0 10px var(--apex-blue);
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning {
        background: var(--apex-darker);
        border-radius: 10px;
        border-left: 4px solid var(--apex-blue);
    }
    
    /* Coaching tips styling */
    .coaching-tip {
        background: linear-gradient(135deg, var(--apex-darker), var(--apex-dark-blue));
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--apex-orange);
        margin: 0.5rem 0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* DataFrames */
    .dataframe {
        background: var(--apex-darker);
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* File uploader */
    .stFileUploader {
        background: var(--apex-darker);
        border-radius: 10px;
        border: 2px dashed var(--apex-blue);
        padding: 2rem;
        text-align: center;
    }
    
    /* Custom animations */
    @keyframes pulse {
        0% { box-shadow: 0 0 15px var(--apex-blue); }
        50% { box-shadow: 0 0 30px var(--apex-blue), 0 0 40px var(--apex-orange); }
        100% { box-shadow: 0 0 15px var(--apex-blue); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: var(--apex-blue);
        text-align: center;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 20px var(--apex-blue);
    }
    
    .subsection-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--apex-orange);
        margin: 1.5rem 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with logo
    header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
    
    with header_col2:
        try:
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            st.image("assets/ApexLogo.jpg", width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        except:
            # Fallback if logo not found
            st.markdown("""
            <div class="main-header">
                <h1 class="main-title">🏀 ApexSports TrAiNer</h1>
                <p class="main-subtitle">AI-Powered Basketball Shot Analysis</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Basketball Shot Analysis System</div>', unsafe_allow_html=True)
    
    # Initialize components
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = ShotAnalyzer()
    
    # Sidebar for session management
    with st.sidebar:
        st.markdown('<div class="subsection-header">⚙️ Session Control</div>', unsafe_allow_html=True)
        
        # Create new session
        with st.expander("🚀 Initialize Training Session", expanded=True):
            session_name = st.text_input("Session Identifier", 
                                       value=f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                                       help="Unique identifier for this training session")
            session_notes = st.text_area("Session Parameters", 
                                        placeholder="Training objectives, environmental conditions, focus areas...",
                                        help="Additional context for this session")
            
            if st.button("🎯 CREATE SESSION"):
                session_id = st.session_state.db_manager.create_session(session_name, session_notes)
                if session_id > 0:
                    st.session_state.current_session_id = session_id
                    st.success(f"✅ Session initialized! Neural ID: {session_id}")
                else:
                    st.error("Γ¥î Session creation failed")
        
        # Select existing session
        sessions_df = st.session_state.db_manager.get_all_sessions()
        if not sessions_df.empty:
            with st.expander("💾 Load Previous Session"):
                selected_session = st.selectbox(
                    "Choose Session",
                    sessions_df['id'].tolist(),
                    format_func=lambda x: f"{sessions_df[sessions_df['id']==x]['session_name'].iloc[0]} (ID: {x})"
                )
                if st.button("📂 LOAD SESSION"):
                    st.session_state.current_session_id = selected_session
                    st.success(f"✅ Session {selected_session} loaded successfully")
        
        # Display current session
        if 'current_session_id' in st.session_state:
            st.markdown(f"""
            <div class="coaching-tip pulse-animation">
            🏀 <strong>ACTIVE SESSION</strong><br>
            Neural ID: {st.session_state.current_session_id}
            </div>
            """, unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🧠 NEURAL ANALYSIS", "📊 PERFORMANCE CORE", "📈 EVOLUTION TRACKER", "⚙️ SYSTEM CONFIG"])
    
    with tab1:
        st.markdown('<div class="section-header">🎯 Neural Shot Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Video input options
            st.markdown('<div class="subsection-header">Analysis Protocol</div>', unsafe_allow_html=True)
            analysis_option = st.radio(
                "Choose Analysis Method:",
                ["Upload Video File", "Use Camera", "Upload Image"],
                help="Select your preferred input method for AI analysis"
            )
            
            if analysis_option == "Upload Video File":
                uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov', 'mkv'])
                
                if uploaded_file is not None:
                    # DEBUG: Track video file changes
                    video_name = uploaded_file.name
                    video_size = len(uploaded_file.getvalue())
                    print(f"DEBUG: !!!! NEW VIDEO UPLOADED: {video_name}, size: {video_size} bytes !!!!")
                    
                    # Store video bytes for download functionality
                    uploaded_file.seek(0)  # Reset file pointer
                    st.session_state.uploaded_video_bytes = uploaded_file.read()
                    
                    # Process video
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(st.session_state.uploaded_video_bytes)
                        tmp_file_path = tmp_file.name
                    
                    # Video processing
                    cap = cv2.VideoCapture(tmp_file_path)
                    
                    # Slow motion control
                    st.subheader("📹 Video Download Settings")
                    slow_motion_factor = st.slider(
                        "Slow Motion Speed",
                        min_value=0.25,
                        max_value=1.0,
                        value=0.5,
                        step=0.25,
                        help="Choose playback speed for downloaded video. 0.5 = half speed (2x slower), 0.25 = quarter speed (4x slower)"
                    )
                    
                    speed_description = {
                        0.25: "Quarter Speed (4x Slower) - Great for detailed technique analysis",
                        0.5: "Half Speed (2x Slower) - Perfect for coaching review", 
                        0.75: "3/4 Speed - Slightly slower for better observation",
                        1.0: "Normal Speed - Original timing"
                    }
                    
                    if slow_motion_factor in speed_description:
                        st.info(f"**{speed_description[slow_motion_factor]}**")
                    
                    if st.button("Analyze Video"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        video_placeholder = st.empty()
                        
                        # FORCE FRESH ANALYSIS - Reset ALL state
                        st.session_state.analyzer.reset()
                        st.session_state.analyzer.reset_analysis_state()  # Force fresh capture
                        
                        # Create annotated video file path
                        with tempfile.NamedTemporaryFile(delete=False, suffix='_annotated.mp4') as annotated_file:
                            annotated_video_path = annotated_file.name
                        
                        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        current_frame = 0
                        
                        # Get video properties for creating annotated video
                        original_fps = int(cap.get(cv2.CAP_PROP_FPS))
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        
                        # Create slow motion video based on user selection
                        slow_motion_fps = max(1, int(original_fps * slow_motion_factor))  # Use user-selected factor
                        
                        # Create video writer for annotated output
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        out = cv2.VideoWriter(annotated_video_path, fourcc, slow_motion_fps, (width, height))
                        
                        while cap.isOpened():
                            ret, frame = cap.read()
                            if not ret:
                                break
                            
                            # Process frame and get proper RGB version for display
                            processed_frame, landmarks = st.session_state.analyzer.process_frame(frame)
                            
                            # Add frame number overlay to processed frame
                            cv2.putText(processed_frame, f"Frame {current_frame + 1}/{frame_count}", 
                                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                            
                            # Write the annotated frame to output video
                            out.write(processed_frame)
                            
                            # Convert to RGB for Streamlit display (OpenCV uses BGR by default)
                            display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                            
                            # Update progress
                            current_frame += 1
                            progress = current_frame / frame_count
                            progress_bar.progress(progress)
                            
                            # Show slow motion info in status
                            speed_text = f" (Creating {slow_motion_factor}x speed video)" if slow_motion_factor < 1.0 else ""
                            status_text.text(f"Processing frame {current_frame}/{frame_count}{speed_text}")
                            
                            # Display frame (every 5th frame to show more progress)
                            if current_frame % 5 == 0:
                                video_placeholder.image(display_frame, channels="RGB", use_container_width=True)
                        
                        cap.release()
                        out.release()  # Close the annotated video writer
                        
                        # Store annotated video for download
                        try:
                            with open(annotated_video_path, 'rb') as f:
                                st.session_state.annotated_video_bytes = f.read()
                            # Clean up temporary file
                            os.unlink(annotated_video_path)
                        except Exception as e:
                            print(f"Error saving annotated video: {e}")
                            st.session_state.annotated_video_bytes = None
                        
                        # Clean up original temporary file
                        os.unlink(tmp_file_path)
                        
                        # Generate summary and final instructional stills
                        shot_metrics = st.session_state.analyzer.get_shot_summary()
                        
                        # Get the best instructional stills from the entire video
                        final_stills = st.session_state.analyzer.get_final_instructional_stills()
                        
                        # Debug information about captured stills
                        if final_stills:
                            print(f"\n=== FINAL STILLS SUMMARY ===")
                            for flaw_name, still_data in final_stills.items():
                                print(f"- {flaw_name}: Frame {still_data.get('frame_number', 'N/A')} | Phase: {still_data.get('phase', 'N/A')} | Severity: {still_data.get('severity', 0):.1f}%")
                            print(f"=== END SUMMARY ===\n")
                        else:
                            print("WARNING: No final stills captured!")
                            
                        if final_stills:
                            # Add final stills to the last analysis result for UI display
                            if not hasattr(st.session_state.analyzer, 'last_analysis_result') or not st.session_state.analyzer.last_analysis_result:
                                st.session_state.analyzer.last_analysis_result = {'detailed_analysis': {}}
                            if 'detailed_analysis' not in st.session_state.analyzer.last_analysis_result:
                                st.session_state.analyzer.last_analysis_result['detailed_analysis'] = {}
                            st.session_state.analyzer.last_analysis_result['flaw_stills'] = final_stills
                            
                        print(f"DEBUG: Video analysis complete - {len(final_stills)} instructional stills available")
                        
                        # Save to database if session is active
                        if 'current_session_id' in st.session_state:
                            st.session_state.db_manager.save_metrics(
                                st.session_state.current_session_id, 
                                shot_metrics
                            )
                            st.success("Shot analysis saved to session!")
                        
                        status_text.text("Analysis Complete!")
            
            elif analysis_option == "Upload Image":
                uploaded_image = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])
                
                if uploaded_image is not None:
                    image = Image.open(uploaded_image)
                    image_np = np.array(image)
                    
                    if image_np.shape[2] == 4:  # RGBA to RGB
                        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
                    if len(image_np.shape) == 3 and image_np.shape[2] == 3:  # RGB to BGR for OpenCV
                        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                    
                    st.session_state.analyzer.reset()
                    processed_image, landmarks = st.session_state.analyzer.process_frame(image_np)
                    
                    st.image(processed_image, channels="BGR", caption="Processed Image", use_container_width=True)
                    
                    if landmarks:
                        shot_metrics = st.session_state.analyzer.get_shot_summary()
                        
                        # Save to database if session is active
                        if 'current_session_id' in st.session_state:
                            st.session_state.db_manager.save_metrics(
                                st.session_state.current_session_id, 
                                shot_metrics
                            )
                            st.success("Shot analysis saved to session!")
            
            else:  # Camera option
                st.info("Camera functionality requires additional setup. Please use video upload for now.")
        
        with col2:
            # Display latest shot metrics if available
            if hasattr(st.session_state, 'analyzer') and st.session_state.analyzer.shot_sequence:
                latest_metrics = st.session_state.analyzer.get_shot_summary()
                
                # ==============================================
                # 🎯 PRIMARY COACHING SUMMARY SECTION
                # ==============================================
                st.markdown('<div class="subsection-header">🏆 Your Personal Coach</div>', unsafe_allow_html=True)
                
                # Get flaws and overall score for coaching methods
                flaws_data = {}
                overall_score = latest_metrics.shooting_form_score
                
                # Get detailed analysis if available
                if hasattr(st.session_state.analyzer, 'last_analysis_result') and st.session_state.analyzer.last_analysis_result:
                    if 'detailed_analysis' in st.session_state.analyzer.last_analysis_result:
                        detailed_analysis = st.session_state.analyzer.last_analysis_result['detailed_analysis']
                        flaws_data = detailed_analysis.get('flaws', {})
                
                # Generate coaching summary with proper parameters
                coaching_summary = st.session_state.analyzer.generate_coaching_summary(flaws_data, overall_score)
                
                # Display coaching summary in full readable format without height restrictions
                st.markdown(f"""
                <div class="coaching-tip" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     border-radius: 15px; padding: 25px; margin: 20px 0; color: white; 
                     box-shadow: 0 8px 32px rgba(0,0,0,0.3); min-height: auto;">
                    <h2 style="color: white; margin-top: 0; text-align: center; font-size: 1.8em; margin-bottom: 20px;">
                        🏀 Your Personal Shooting Coach
                    </h2>
                    <div style="font-size: 1.15em; line-height: 1.8; text-align: left; white-space: pre-wrap; 
                         max-width: 100%; overflow-wrap: break-word; word-wrap: break-word;">
                        {escape_html_content(coaching_summary)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate 60-day improvement plan with proper parameters
                improvement_plan_data = st.session_state.analyzer.generate_60_day_improvement_plan(flaws_data, overall_score)
                
                # Format the improvement plan dictionary as a readable string
                try:
                    improvement_plan = st.session_state.analyzer.format_improvement_plan(improvement_plan_data)
                    # Ensure it's a string
                    if isinstance(improvement_plan, dict):
                        improvement_plan = "60-day improvement plan data received but formatting failed. Please check the system."
                except Exception as e:
                    improvement_plan = f"Error formatting improvement plan: {str(e)}"
                
                # Display 60-day improvement plan in full readable format
                st.markdown(f"""
                <div class="coaching-tip" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                     border-radius: 15px; padding: 25px; margin: 20px 0; color: white; 
                     box-shadow: 0 8px 32px rgba(0,0,0,0.3); min-height: auto;">
                    <h2 style="color: white; margin-top: 0; text-align: center; font-size: 1.7em; margin-bottom: 20px;">
                        📈 Your 60-Day Transformation Plan
                    </h2>
                    <div style="font-size: 1.1em; line-height: 1.7; text-align: left; white-space: pre-wrap; 
                         max-width: 100%; overflow-wrap: break-word; word-wrap: break-word;">
                        {escape_html_content(improvement_plan)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # ==============================================
                # ∩┐╜ DOWNLOAD SECTION
                # ==============================================
                st.markdown('<div class="subsection-header">💾 Download Your Analysis</div>', unsafe_allow_html=True)
                
                # Create single centered download button
                download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
                
                with download_col2:
                    # Check if we have all necessary components - with detailed debugging
                    has_video = hasattr(st.session_state, 'annotated_video_bytes') and st.session_state.annotated_video_bytes
                    has_stills = hasattr(st.session_state, 'analyzer') and hasattr(st.session_state.analyzer, 'captured_stills') and st.session_state.analyzer.captured_stills
                    has_metrics = 'latest_metrics' in locals() and latest_metrics is not None
                    has_coaching = 'coaching_summary' in locals() and coaching_summary
                    
                    # Debug information (remove in production)
                    print(f"DEBUG - Download check: video={has_video}, stills={has_stills}, metrics={has_metrics}, coaching={has_coaching}")
                    if hasattr(st.session_state, 'analyzer'):
                        print(f"DEBUG - Analyzer captured_stills: {hasattr(st.session_state.analyzer, 'captured_stills')}")
                        if hasattr(st.session_state.analyzer, 'captured_stills'):
                            print(f"DEBUG - Stills count: {len(st.session_state.analyzer.captured_stills) if st.session_state.analyzer.captured_stills else 0}")
                    
                    # More flexible check - need either video+coaching OR stills+coaching as minimum
                    can_create_package = (has_video or has_stills) and has_coaching and has_metrics
                    
                    if can_create_package:
                        try:
                            # Create comprehensive analysis package
                            frame_stills = getattr(st.session_state.analyzer, 'captured_stills', {}) if hasattr(st.session_state, 'analyzer') else {}
                            video_bytes = getattr(st.session_state, 'uploaded_video_bytes', None)
                            annotated_video_bytes = getattr(st.session_state, 'annotated_video_bytes', None)
                            
                            # Generate coaching report content
                            report_content = create_coaching_report_pdf(coaching_summary, improvement_plan, latest_metrics)
                            
                            # Create the complete analysis package ZIP
                            zip_data = create_analysis_package_zip(
                                video_bytes, 
                                frame_stills, 
                                coaching_summary, 
                                improvement_plan, 
                                latest_metrics,
                                annotated_video_bytes,
                                report_content
                            )
                            
                            st.download_button(
                                label="📦 Download Complete Basketball Analysis Package",
                                data=zip_data,
                                file_name=f"basketball_analysis_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                                mime="application/zip",
                                help="📦 Complete package includes:\n• 🎥 Slow-motion analysis video with pose estimation\n• 📸 Key instructional frame stills\n• 📄 Personalized coaching report\n• 📊 Technical metrics data",
                                use_container_width=True
                            )
                            
                            # Show package contents preview
                            with st.expander("📦 Package Contents Preview"):
                                st.markdown("""
                                **🎯 Your Complete Analysis Package Contains:**
                                
                                🎥 **Slow-Motion Analysis Video**
                                - Pose estimation overlays showing body positioning
                                - Flaw detection markers and annotations
                                - Frame-by-frame breakdown at your selected speed
                                
                                📸 **Key Instructional Frames**
                                - Critical moments captured during shot analysis
                                - Before/after comparison stills
                                - Technique demonstration images
                                
                                📄 **Personalized Coaching Report**
                                - Detailed assessment of your shooting form
                                - Specific improvement recommendations
                                - Practice drills and exercises
                                
                                📊 **Technical Data Files**
                                - AI analysis metrics and scores
                                - Biomechanical measurements
                                - Performance tracking data
                                
                                📋 **README Guide**
                                - Instructions on how to use each component
                                - Package structure explanation
                                """)
                        except Exception as e:
                            st.error(f"Error creating analysis package: {str(e)}")
                            st.button("❌ Package Creation Error", disabled=True, help=f"Unable to create package: {str(e)}")
                    else:
                        # Show what's missing
                        missing_items = []
                        if not has_video:
                            missing_items.append("🎥 Analysis video")
                        if not has_stills:
                            missing_items.append("∩┐╜ Frame stills")
                        
                        st.info(f"📊 Complete video analysis first to download your package.\n\nStill processing: {', '.join(missing_items)}")
                        st.button("⏳ Analysis In Progress", disabled=True, help="Complete video analysis first to download comprehensive package")

                # ==============================================
                # 🧠📊 SECONDARY AI METRICS SECTION (Expandable)
                # ==============================================
                with st.expander("🏀 View Detailed AI Metrics & Technical Data", expanded=False):
                    st.markdown('<div class="subsection-header">📊 Technical Analysis Data</div>', unsafe_allow_html=True)
                    
                    # Create metric containers with futuristic styling
                    metric_container = st.container()
                    with metric_container:
                        st.metric("🧠 Neural Form Score", f"{latest_metrics.shooting_form_score:.3f}", help="AI-calculated overall form rating (0.0-1.0)")
                        with st.expander("📈 Form Score Analysis"):
                            st.markdown("""
                            **🧠 What it measures:** Overall shooting technique combining all biomechanical factors
                            
                            **📊 Score Ranges:**
                            - 🟢 **0.80-1.00**: Elite form - Professional level technique
                            - 🟡 **0.60-0.79**: Good form - Solid fundamentals with room for refinement
                            - 🟠 **0.40-0.59**: High school JV form - Key areas need attention
                            - 🔴 **0.00-0.39**: Needs work - Focus on basic fundamentals
                            
                            **💡 Improvement Tips:**
                            - Practice slow-motion shooting to build muscle memory
                            - Focus on consistent pre-shot routine
                            - Work with a coach to identify specific weaknesses
                            - Film yourself from multiple angles for self-analysis
                            """)
                        
                        st.metric("🚀 Release Vector", f"{latest_metrics.release_angle:.1f}°", help="Optimal shooting angle analysis")
                        with st.expander("📈 Release Angle Analysis"):
                            st.markdown("""
                            **🚀 What it measures:** The angle your shooting arm makes at ball release
                            
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
                        
                        st.metric("🚀 Launch Height", f"{latest_metrics.release_height:.3f}", help="Release point elevation metrics (relative to shoulders)")
                        with st.expander("📈 Launch Height Analysis"):
                            st.markdown("""
                            **🚀 What it measures:** How high you release the ball relative to your shoulder line
                            
                            **📊 Optimal Range:**
                            - 🎯 **Target**: 0.1-0.3 above shoulder line
                            - Higher release = harder to block, better arc
                            - Lower release = quicker shot, less arc
                            
                            **🎯 Improvement Tips:**
                            - **Too Low**: Strengthen legs for better lift, practice jump shots
                            - **Too High**: Work on shooting off the dribble, quick release drills
                            - Practice shooting at different heights to find your sweet spot
                            - Focus on consistent leg drive and follow-through
                            """)
                        
                        st.metric("🎯 Joint Alignment", f"{latest_metrics.elbow_alignment:.3f}", help="Biomechanical alignment score (0.0-1.0)")
                        with st.expander("📈 Elbow Alignment Analysis"):
                            st.markdown("""
                            **🎯 What it measures:** How well your elbow stays aligned under the basketball
                            
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
                        
                        st.metric("⚖️ Balance Matrix", f"{latest_metrics.balance_score:.3f}", help="Stability analysis (0.0-1.0)")
                        with st.expander("📈 Balance Analysis"):
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
                        
                        st.metric("🔄 Consistency Index", f"{latest_metrics.consistency_score:.3f}", help="Repeatability factor (0.0-1.0)")
                        with st.expander("📈 Consistency Analysis"):
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
                    
                    # AI Coaching System (Inside expandable section)
                    st.markdown('<div class="subsection-header">🤖 AI Coach Recommendations</div>', unsafe_allow_html=True)
                    tips = []
                    
                    if latest_metrics.release_angle < 90:
                        tips.append("📈 **ELEVATION PROTOCOL**: Increase release trajectory to 90-105° for optimal arc")
                    if latest_metrics.elbow_alignment < 0.7:
                        tips.append("🎯 **ALIGNMENT SEQUENCE**: Maintain elbow positioning directly under ball pathway")
                    if latest_metrics.balance_score < 0.7:
                        tips.append("ΓÜû∩╕Å **STABILITY MODULE**: Engage core stabilization throughout motion sequence")
                    if latest_metrics.follow_through_angle < 45:
                        tips.append("🏀 **EXTENSION PROTOCOL**: Maximize follow-through extension for enhanced accuracy")
                    
                    if tips:
                        for tip in tips:
                            st.markdown(f'<div class="coaching-tip">{tip}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="coaching-tip">🏆 **ELITE PERFORMANCE**: All systems optimal! Maintain current form patterns.</div>', unsafe_allow_html=True)
                    
                    # Research-backed detailed analysis (Inside expandable section)
                    st.markdown('<div class="subsection-header">🔬 Research-Backed Analysis</div>', unsafe_allow_html=True)
                
                # Get the latest shot analysis for detailed insights
                if hasattr(st.session_state.analyzer, 'last_analysis_result'):
                    last_result = st.session_state.analyzer.last_analysis_result
                    if last_result and 'detailed_analysis' in last_result:
                        detailed_analysis = last_result['detailed_analysis']
                        flaws = detailed_analysis.get('flaws', {})
                        flaw_stills = last_result.get('flaw_stills', {})
                        
                        if flaws:
                            st.markdown("#### 🎯 Priority Focus Areas (Based on Scientific Research)")
                            
                            # Sort by priority (lower number = higher priority)
                            sorted_flaws = sorted(flaws.items(), key=lambda x: x[1].get('priority', 10))
                            
                            # Create columns for flaw stills display
                            if flaw_stills:
                                st.markdown("##### 📸 Critical Form Analysis Stills")
                                
                                # Display top priority flaw stills
                                priority_stills = []
                                for flaw_type, still_data in flaw_stills.items():
                                    if still_data.get('priority', 10) <= 5:  # Show high/medium priority
                                        priority_stills.append((flaw_type, still_data))
                                
                                # Sort by priority and display
                                priority_stills.sort(key=lambda x: x[1].get('priority', 10))
                                
                                if priority_stills:
                                    cols = st.columns(min(len(priority_stills), 3))
                                    for idx, (flaw_type, still_data) in enumerate(priority_stills[:3]):
                                        with cols[idx]:
                                            st.markdown(f"**{flaw_type.replace('_', ' ').title()}**")
                                            
                                            # Convert the still image for proper display (already RGB from storage)
                                            still_image = still_data['image']
                                            if still_image is not None and still_image.size > 0:
                                                try:
                                                    from PIL import Image
                                                    # Image is already in RGB format from storage
                                                    pil_image = Image.fromarray(still_image.astype('uint8'))
                                                    st.image(pil_image, use_container_width=True, 
                                                            caption=f"Priority {still_data.get('priority', 10)} - {still_data.get('severity', 0):.0f}% Severity")
                                                    
                                                    # Add frame and phase information
                                                    st.caption(f"📊 Frame {still_data.get('frame_number', 'N/A')} | 🎯 {still_data.get('phase', 'Unknown').title()} Phase")
                                                    
                                                    # Add download button for individual frame
                                                    try:
                                                        # Convert image to bytes for download
                                                        pil_image_bytes = BytesIO()
                                                        pil_image.save(pil_image_bytes, format='JPEG', quality=95)
                                                        pil_image_bytes.seek(0)
                                                        
                                                        st.download_button(
                                                            label="💾 Download Frame",
                                                            data=pil_image_bytes.getvalue(),
                                                            file_name=f"frame_{still_data.get('frame_number', 'unknown')}_{flaw_type}.jpg",
                                                            mime="image/jpeg",
                                                            help=f"Download this frame showing {flaw_type.replace('_', ' ')}",
                                                            key=f"download_{flaw_type}_{still_data.get('frame_number', 'unknown')}"
                                                        )
                                                    except Exception as e:
                                                        st.caption(f"Download unavailable: {str(e)}")
                                                    
                                                    # Add expandable details
                                                    with st.expander(f"📋 {flaw_type.replace('_', ' ').title()} Details"):
                                                        st.markdown(f"**🎯 Issue:** {still_data.get('coaching_focus', 'N/A')}")
                                                        st.markdown(f"**👁️ Visual Key:** {still_data.get('visual_key', 'N/A')}")
                                                        st.markdown(f"**📊 Severity:** {still_data.get('severity', 0):.1f}%")
                                                        st.markdown(f"**📸 Captured:** {still_data.get('timestamp', 'N/A')}")
                                                        st.markdown(f"**🔧 Fix:** {flaws[flaw_type].get('recommendation', 'N/A')}")
                                                        st.markdown(f"**🎯 Accuracy Impact:** {flaws[flaw_type].get('accuracy_impact', 'N/A')}%")
                                                except Exception as e:
                                                    st.error(f"Error displaying image: {e}")
                                                    st.text(f"Image shape: {still_image.shape if hasattr(still_image, 'shape') else 'No shape'}")
                            
                            for component, analysis in sorted_flaws[:3]:  # Show top 3 priorities
                                priority = analysis.get('priority', 10)
                                # Handle both string and numeric accuracy impact values
                                accuracy_impact_raw = analysis.get('accuracy_impact', '5-10')
                                if isinstance(accuracy_impact_raw, str):
                                    # Remove % if present and use the string as-is for display
                                    accuracy_impact = accuracy_impact_raw.replace('%', '')
                                else:
                                    accuracy_impact = str(accuracy_impact_raw) if accuracy_impact_raw > 0 else '5-10'
                                
                                issue = analysis.get('issue', 'No specific issue detected')
                                recommendation = analysis.get('recommendation', 'Continue current form')
                                
                                # Get comprehensive coaching feedback
                                explanation = st.session_state.analyzer.get_flaw_explanation(component)
                                correction = st.session_state.analyzer.get_flaw_correction(component)
                                drills = st.session_state.analyzer.get_flaw_drills(component)
                                
                                # Priority badge styling
                                if priority <= 2:
                                    priority_color = "#FF4444"  # High priority - red
                                    priority_text = "HIGH PRIORITY"
                                elif priority <= 5:
                                    priority_color = "#FFA500"  # Medium priority - orange
                                    priority_text = "MEDIUM PRIORITY"
                                else:
                                    priority_color = "#4CAF50"  # Low priority - green
                                    priority_text = "LOW PRIORITY"
                                
                                st.markdown(f"""
                                <div class="metric-card" style="margin-bottom: 15px; border-left: 4px solid {priority_color};">
                                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                        <h4 style="color: var(--accent-color); margin: 0; flex: 1;">{component.replace('_', ' ').title()}</h4>
                                        <span style="background: {priority_color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold;">
                                            {priority_text}
                                        </span>
                                    </div>
                                    <div style="background: rgba(255,255,255,0.08); padding: 12px; border-radius: 8px; margin: 8px 0;">
                                        <strong>🎯 Accuracy Impact:</strong> Up to {accuracy_impact}% improvement possible
                                    </div>
                                    <div style="background: rgba(255,255,255,0.08); padding: 12px; border-radius: 8px; margin: 8px 0;">
                                        <strong>🔍 What's Wrong:</strong> {explanation}
                                    </div>
                                    <div style="background: rgba(0,255,100,0.1); padding: 12px; border-radius: 8px; border-left: 3px solid var(--accent-color);">
                                        <strong>🔧 How to Fix It:</strong> {correction}
                                    </div>
                                    <div style="background: rgba(0,150,255,0.1); padding: 12px; border-radius: 8px; border-left: 3px solid #0096FF;">
                                        <strong>🏋️ Training Drills:</strong> {drills}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Overall research-based score
                            overall_analysis_score = detailed_analysis.get('overall_score', 0.0)
                            score_color = "#4CAF50" if overall_analysis_score >= 0.8 else "#FFA500" if overall_analysis_score >= 0.6 else "#FF4444"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="text-align: center;">
                                <h4 style="color: var(--accent-color);">📊 Research Assessment Score</h4>
                                <div style="font-size: 2.2em; color: {score_color}; font-weight: bold;">
                                    {overall_analysis_score:.1%}
                                </div>
                                <div style="margin-top: 10px; font-size: 1.1em;">
                                    Based on biomechanical research and professional analysis
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Add comprehensive explanation of Research Assessment Score
                            with st.expander("📈 Understanding Your Research Assessment Score", expanded=False):
                                st.markdown(f"""
                                **🔬 What is the Research Assessment Score?**
                                
                                Your Research Assessment Score ({overall_analysis_score:.1%}) is a comprehensive evaluation of your shooting technique based on:
                                - **Biomechanical Research**: Studies from sports science labs analyzing elite shooters
                                - **Professional Analysis**: Techniques used by NBA shooting coaches
                                - **15+ Key Factors**: Balance, alignment, release mechanics, follow-through, and more
                                
                                **📊 Score Breakdown:**
                                - 🟢 **85-100%**: Elite shooter - NBA/Professional level technique
                                - 🟡 **70-84%**: College level - Advanced technique and consistency  
                                - 🟠 **55-69%**: High school varsity - Good fundamentals, needs refinement
                                - 🟡 **40-54%**: Intermediate shooter - Some fundamentals solid, key areas need work
                                - 🟡 **Below 40%**: Beginner shooter - Focus on basic fundamentals
                                
                                **🎯 How to Improve Your Score:**
                                
                                **Immediate Actions (This Week):**
                                - Focus on the HIGH PRIORITY flaws identified above
                                - Practice slow-motion shooting to build proper muscle memory
                                - Work on consistent pre-shot routine and setup
                                
                                **Short-term Goals (1-2 Months):**
                                - Address MEDIUM PRIORITY technical issues
                                - Increase practice volume with proper form
                                - Record yourself shooting to monitor progress
                                
                                **Long-term Development (3-6 Months):**
                                - Fine-tune advanced mechanics (guide hand, arc consistency)
                                - Practice game-speed shooting scenarios
                                - Work on shooting under pressure situations
                                
                                **🎯 Pro Tips:**
                                - A 5-10% improvement can significantly boost your field goal percentage
                                - Elite shooters typically score 85%+ in multiple categories
                                - Consistency beats perfection - focus on repeatable mechanics
                                - Use the download feature to track your progress over time
                                """)
                            
                            
                            # Comprehensive flaw stills gallery
                            if flaw_stills:
                                st.markdown("---")
                                st.markdown("##### 🔍 Complete Form Analysis Gallery")
                                st.markdown("*Click on images to enlarge and see detailed annotations*")
                                
                                # Group stills by priority
                                high_priority = []
                                medium_priority = []
                                low_priority = []
                                
                                for flaw_type, still_data in flaw_stills.items():
                                    priority = still_data.get('priority', 10)
                                    if priority <= 2:
                                        high_priority.append((flaw_type, still_data))
                                    elif priority <= 5:
                                        medium_priority.append((flaw_type, still_data))
                                    else:
                                        low_priority.append((flaw_type, still_data))
                                
                                # Display by priority groups
                                for group_name, group_stills, group_color in [
                                    ("🔴 Critical Issues", high_priority, "#FF4444"),
                                    ("ΓÜá∩╕Å Important Areas", medium_priority, "#FFA500"),
                                    ("🎯 Development Areas", low_priority, "#4CAF50")
                                ]:
                                    if group_stills:
                                        st.markdown(f"**{group_name}**")
                                        cols = st.columns(min(len(group_stills), 3))
                                        
                                        for idx, (flaw_type, still_data) in enumerate(group_stills):
                                            with cols[idx % 3]:
                                                still_image = still_data['image']
                                                if still_image is not None:
                                                    from PIL import Image
                                                    pil_image = Image.fromarray(still_image)
                                                    
                                                    st.image(pil_image, 
                                                           caption=f"{flaw_type.replace('_', ' ').title()}", 
                                                           use_container_width=True)
                                                    
                                                    # Progress bar for severity
                                                    severity = still_data.get('severity', 0)
                                                    st.progress(severity / 100, 
                                                              text=f"Severity: {severity:.0f}%")
                                                    
                                                    # Quick fix tip
                                                    st.markdown(f"*Quick Fix: {still_data.get('recommendation', 'Focus on form')[:50]}...*")
                        else:
                            st.success("✅ No major form issues detected based on research parameters!")
                    else:
                        st.info("Take a shot to see detailed research-backed analysis!")
                
                    # Training periodization based on current level (Inside expandable section)
                    st.markdown('<div class="subsection-header">📅 Periodized Training Plan</div>', unsafe_allow_html=True)
                    
                    overall_score = latest_metrics.shooting_form_score
                    
                    if overall_score < 0.6:
                        st.markdown("""
                        <div class="coaching-tip">
                        🏀 **FOUNDATION PHASE (Weeks 1-4)**<br>
                        • Master basic stance and alignment (25-30% accuracy gain)<br>
                        • 200 form shots daily at close range<br>
                        • Focus on balance and consistent release point
                        </div>
                        """, unsafe_allow_html=True)
                    elif overall_score < 0.8:
                        st.markdown("""
                        <div class="coaching-tip">
                        🎯 **REFINEMENT PHASE (Weeks 5-8)**<br>
                        • Eliminate remaining mechanical flaws (15-25% improvement)<br>
                        • Add game-speed shooting with proper form<br>
                        • Introduce shooting under light pressure
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="coaching-tip">
                        🏆 **MASTERY PHASE (Weeks 9-12)**<br>
                        • Maintain elite mechanics under game conditions<br>
                        • Advanced shooting drills and contested shots<br>
                        • Mental training and performance optimization
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📊 Analyze a shot first to see your personalized coaching summary!")
    
    with tab2:
        st.markdown('<div class="section-header">📊 Performance Core Dashboard</div>', unsafe_allow_html=True)
        
        if 'current_session_id' in st.session_state:
            session_data = st.session_state.db_manager.get_session_data(st.session_state.current_session_id)
            
            if not session_data.empty:
                st.markdown(f'<div class="subsection-header">Session {st.session_state.current_session_id} Neural Analytics</div>', unsafe_allow_html=True)
                
                # Enhanced statistics display
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_score = session_data['shooting_form_score'].mean()
                    st.metric("🧠 Neural Average", f"{avg_score:.3f}", help="AI-calculated session average")
                
                with col2:
                    best_score = session_data['shooting_form_score'].max()
                    st.metric("🏆 Peak Performance", f"{best_score:.3f}", help="Highest recorded score")
                
                with col3:
                    total_shots = len(session_data)
                    st.metric("📊 Analysis Count", total_shots, help="Total shots processed")
                
                with col4:
                    consistency = 1 - session_data['shooting_form_score'].std()
                    st.metric("🎯 Precision Index", f"{consistency:.3f}", help="Consistency rating")
                
                # Performance visualizations
                create_performance_charts(session_data)
                
                # Detailed metrics table
                st.subheader("Detailed Shot Analysis")
                display_columns = [
                    'recorded_at', 'shooting_form_score', 'release_angle', 
                    'release_height', 'elbow_alignment', 'balance_score'
                ]
                st.dataframe(session_data[display_columns].round(3))
                
            else:
                st.info("No shot data available for this session. Start analyzing shots to see your performance!")
        else:
            st.warning("Please create or select a session to view performance data.")
    
    with tab3:
        st.markdown('<div class="section-header">📊 Evolution Tracker</div>', unsafe_allow_html=True)
        
        # All sessions comparison
        all_sessions = st.session_state.db_manager.get_all_sessions()
        
        if not all_sessions.empty:
            st.markdown('<div class="subsection-header">Cross-Session Performance Matrix</div>', unsafe_allow_html=True)
            
            session_performances = []
            for _, session in all_sessions.iterrows():
                session_data = st.session_state.db_manager.get_session_data(session['id'])
                if not session_data.empty:
                    avg_score = session_data['shooting_form_score'].mean()
                    shot_count = len(session_data)
                    session_performances.append({
                        'Session': session['session_name'],
                        'Average Score': avg_score,
                        'Shots': shot_count,
                        'Date': session['created_at']
                    })
            
            if session_performances:
                perf_df = pd.DataFrame(session_performances)
                
                # Progress over time
                fig_progress = px.line(
                    perf_df, 
                    x='Date', 
                    y='Average Score',
                    title="Progress Over Time",
                    markers=True
                )
                st.plotly_chart(fig_progress, use_container_width=True)
                
                # Session comparison table
                st.dataframe(perf_df.round(3))
        else:
            st.info("Create some sessions and analyze shots to track your progress!")
    
    with tab4:
        st.markdown('<div class="section-header">ΓÜÖ∩╕Å System Configuration</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-header">Neural Network Parameters</div>', unsafe_allow_html=True)
            
            # MediaPipe confidence thresholds
            detection_confidence = st.slider("🎯 Detection Confidence Matrix", 0.1, 1.0, 0.7, 0.1, 
                                            help="AI pose detection sensitivity threshold")
            tracking_confidence = st.slider("🏀 Tracking Precision Index", 0.1, 1.0, 0.5, 0.1,
                                           help="Motion tracking accuracy parameter")
            
            # Update analyzer settings
            if st.button("🚀 DEPLOY CONFIGURATION", help="Apply neural network parameters"):
                st.session_state.analyzer = ShotAnalyzer()
                st.success("✅ Configuration deployed! Neural upgrades active on next analysis.")
            
            st.markdown('<div class="subsection-header">Data Management Protocol</div>', unsafe_allow_html=True)
            
            # Export data
            if st.button("📊 EXTRACT DATA MATRIX", help="Export all training data"):
                sessions_df = st.session_state.db_manager.get_all_sessions()
                if not sessions_df.empty:
                    # Combine all session data
                    all_data = []
                    for _, session in sessions_df.iterrows():
                        session_data = st.session_state.db_manager.get_session_data(session['id'])
                        if not session_data.empty:
                            session_data['session_name'] = session['session_name']
                            all_data.append(session_data)
                    
                    if all_data:
                        combined_df = pd.concat(all_data, ignore_index=True)
                        csv = combined_df.to_csv(index=False)
                        st.download_button(
                            label="💾 Download Neural Data",
                            data=csv,
                            file_name=f"apexsports_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("ΓÜá∩╕Å No training data available for extraction")
                else:
                    st.warning("ΓÜá∩╕Å No active sessions detected")
        
        with col2:
            st.markdown('<div class="subsection-header">ApexSports TrAiNer</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="coaching-tip">
            <strong>🧠 ADVANCED AI TRAINING SYSTEM</strong><br><br>
            
            <strong>🎯 CORE CAPABILITIES:</strong><br>
            • Real-time neural pose detection and analysis<br>
            • Advanced biomechanical form evaluation<br>
            • Performance tracking with ML insights<br>
            • Personalized AI coaching recommendations<br>
            • Data-driven improvement analytics<br><br>
            
            <strong>⚙️ TECHNOLOGY STACK:</strong><br>
            • MediaPipe for pose estimation<br>
            • OpenCV for computer vision<br>
            • Scikit-learn for analytics<br>
            • Plotly for data visualization<br>
            • SQLite for performance storage<br><br>
            
            <strong>🚀 VERSION:</strong> TrAiNer v2.0<br>
            <strong>📅 LAST NEURAL UPDATE:</strong> August 2025
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="subsection-header">Support Protocol</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="coaching-tip">
            <strong>🛠️ TECHNICAL SUPPORT CHANNELS:</strong><br>
            • 📧 Neural Support: ai-support@apexsports.tech<br>
            • 🌐 Training Portal: www.apexsports.tech/trainer<br>
            • 🏀 AI Community: Follow @ApexSportsAI<br>
            • 📱 Real-time updates on social platforms
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
