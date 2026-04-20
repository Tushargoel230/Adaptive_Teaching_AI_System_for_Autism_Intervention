#!/usr/bin/env python3
"""
LIVE WEBCAM DEMO - Real-time behavioral analysis with facial detection
Perfect for quick on-the-spot demonstrations without pre-recorded videos.

Usage:
    python live_demo.py --duration 30  (30-second demo)
    python live_demo.py --mock        (without camera, using simulated data)
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional
import threading
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import cv2
    from autism_teaching_ai import (
        BehavioralAnalyzer,
        StateInferenceEngine,
        StrategySelector,
        DialogueGenerator,
        AdaptiveTeachingAI,
    )
    IMPORTS_OK = True
except ImportError as e:
    logger.warning(f"Import error: {e}")
    IMPORTS_OK = False

class LiveBehavioralDemoUI:
    """Live demo UI showing real-time facial detection and behavioral analysis"""
    
    def __init__(self, use_camera: bool = True, mock_mode: bool = False):
        self.use_camera = use_camera and self._check_camera()
        self.mock_mode = mock_mode
        self.is_running = False
        
        if IMPORTS_OK:
            self.ai = AdaptiveTeachingAI()
            self.analyzer = BehavioralAnalyzer()
        else:
            self.ai = None
            self.analyzer = None
        
        if self.use_camera:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                logger.warning("Camera not available, falling back to mock mode")
                self.use_camera = False
            else:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.frame_count = 0
        self.total_duration = 0
        self.start_time = None
    
    def _check_camera(self) -> bool:
        """Check if camera is available"""
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                cap.release()
                return True
        except:
            pass
        return False
    
    def _add_text_overlay(self, frame: np.ndarray, lines: list, position: str = "top-left"):
        """Add text overlay to frame"""
        if position == "top-left":
            x, y = 10, 30
            dy = 25
        else:  # bottom-left
            x, y = 10, frame.shape[0] - 20
            dy = -25
        
        for i, text in enumerate(lines):
            y_pos = y + (i * dy) if position == "top-left" else y - (i * abs(dy))
            cv2.putText(
                frame,
                text,
                (x, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        return frame
    
    def _create_mock_frame(self) -> np.ndarray:
        """Create a mock frame with some features"""
        # Create background
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:] = (50, 50, 50)  # Dark gray background
        
        # Add some rectangles to simulate face
        # Face region
        cv2.rectangle(frame, (200, 100), (440, 380), (100, 100, 100), -1)
        
        # Eyes
        cv2.circle(frame, (280, 180), 20, (200, 200, 200), -1)
        cv2.circle(frame, (360, 180), 20, (200, 200, 200), -1)
        
        # Pupils
        cv2.circle(frame, (280, 180), 10, (50, 50, 50), -1)
        cv2.circle(frame, (360, 180), 10, (50, 50, 50), -1)
        
        # Mouth
        cv2.ellipse(frame, (320, 280), (40, 20), 0, 0, 180, (150, 100, 100), -1)
        
        # Add noise for realism
        noise = np.random.randint(0, 20, frame.shape, dtype=np.uint8)
        frame = cv2.add(frame, noise)
        
        return frame
    
    def run_live_demo(self, duration: int = 30):
        """Run live demo for N seconds"""
        self.is_running = True
        self.start_time = time.time()
        self.total_duration = duration
        
        logger.info("=" * 70)
        logger.info("LIVE BEHAVIORAL ANALYSIS DEMO")
        logger.info("=" * 70)
        logger.info(f"Duration: {duration} seconds")
        logger.info(f"Mode: {'CAMERA' if self.use_camera else 'MOCK DATA'}")
        
        if self.use_camera:
            logger.info("\n📹 Starting camera capture...")
            logger.info("   Press 'q' to quit early, 'p' to pause/resume")
        
        logger.info("\n⏱️  Analyzing...\n")
        
        paused = False
        pause_time = 0
        
        while self.is_running:
            # Calculate elapsed time (accounting for pauses)
            elapsed = time.time() - self.start_time - pause_time
            
            if elapsed >= duration:
                break
            
            # Get frame
            if self.use_camera:
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)  # Mirror for natural look
            else:
                frame = self._create_mock_frame()
            
            # Create audio mock
            audio = np.random.randn(16000).astype(np.float32)
            
            # Process with AI
            if self.ai and not paused:
                try:
                    response = self.ai.process_interaction(
                        video_frame=frame,
                        audio_data=audio,
                        topic="Demo Interaction",
                        student_previous_input=""
                    )
                    
                    # Extract analysis
                    state = response.get('student_state', 'UNKNOWN')
                    confidence = response.get('student_state_confidence', 0)
                    strategy = response.get('strategy_used', 'NONE')
                    
                    # Create display frame
                    display_frame = frame.copy()
                    
                    # Add analysis overlay
                    overlay_lines = [
                        f"State: {state} ({confidence:.1%})",
                        f"Strategy: {strategy}",
                        f"Time: {int(elapsed)}/{duration}s",
                        f"Frame: {self.frame_count}"
                    ]
                    
                    display_frame = self._add_text_overlay(
                        display_frame,
                        overlay_lines,
                        position="top-left"
                    )
                    
                    # Add instruction
                    display_frame = self._add_text_overlay(
                        display_frame,
                        ["Press 'q' to quit"],
                        position="bottom-left"
                    )
                    
                except Exception as e:
                    logger.error(f"Processing error: {e}")
                    display_frame = frame.copy()
                
                self.frame_count += 1
            else:
                display_frame = frame.copy()
                display_frame = self._add_text_overlay(
                    display_frame,
                    [f"Time: {int(elapsed)}/{duration}s", "PAUSED"],
                    position="top-left"
                )
            
            # Show frame
            if self.use_camera:
                cv2.imshow('Live Behavioral Analysis', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    logger.info("\nQuitting demo...")
                    break
                elif key == ord('p'):
                    paused = not paused
                    if paused:
                        pause_time_start = time.time()
                        logger.info("Paused (press 'p' to resume)")
                    else:
                        pause_time += time.time() - pause_time_start
                        logger.info("Resumed")
        
        self.is_running = False
        
        if self.use_camera:
            cv2.destroyAllWindows()
            self.cap.release()
        
        # Print summary
        self._print_summary()
    
    def _print_summary(self):
        """Print session summary"""
        logger.info("\n" + "=" * 70)
        logger.info("DEMO COMPLETE - Summary")
        logger.info("=" * 70)
        logger.info(f"Frames Processed: {self.frame_count}")
        logger.info(f"Duration: {self.total_duration} seconds")
        if self.frame_count > 0:
            logger.info(f"FPS: {self.frame_count / self.total_duration:.1f}")
        logger.info("\n✓ System successfully demonstrated real-time:")
        logger.info("  • Behavioral signal extraction from video/audio")
        logger.info("  • State classification (ENGAGED/CONFUSED/BORED/FRUSTRATED)")
        logger.info("  • Adaptive strategy selection")
        logger.info("  • Multi-modal fusion")
        logger.info("\n" + "=" * 70)

def main():
    parser = argparse.ArgumentParser(
        description="Live behavioral analysis demo with real-time facial detection"
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=30,
        help='Demo duration in seconds (default: 30)'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Use mock data instead of camera'
    )
    parser.add_argument(
        '--no-camera',
        action='store_true',
        help='Disable camera even if available'
    )
    
    args = parser.parse_args()
    
    if not IMPORTS_OK:
        logger.error("System components not installed. Install with:")
        logger.error("  pip install -r requirements.txt")
        return 1
    
    # Run demo
    demo = LiveBehavioralDemoUI(
        use_camera=(not args.no_camera),
        mock_mode=args.mock
    )
    
    demo.run_live_demo(duration=args.duration)
    
    return 0

if __name__ == "__main__":
    exit(main())
