"""
Component 1: Multimodal Behavioral Analysis
Extracts behavioral signals from video and audio streams.
"""

import numpy as np
import cv2
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Try to import mediapipe, fallback to mock if not available
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("MediaPipe not available - using mock detection")


class BehavioralAnalyzer:
    """
    Analyzes student behavior from video and audio inputs.
    
    Extracts:
    - Visual features: face landmarks, pose, gaze, expressions
    - Audio features: speech transcription, prosody (rate, pitch, energy)
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize behavioral analyzer.
        
        Args:
            model_path: Path to fine-tuned expression classification model (future)
        """
        self.model_path = model_path
        self.mediapipe_available = MEDIAPIPE_AVAILABLE
        
        # Initialize MediaPipe components (optional)
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_face = mp.solutions.face_detection
                self.mp_pose = mp.solutions.pose
                self.mp_hands = mp.solutions.hands
                
                self.face_detector = self.mp_face.FaceDetection()
                self.pose_detector = self.mp_pose.Pose()
                self.hand_detector = self.mp_hands.Hands()
                
                logger.info("BehavioralAnalyzer initialized with MediaPipe components")
            except Exception as e:
                logger.warning(f"MediaPipe initialization failed: {e} - using mock mode")
                self.mediapipe_available = False
        else:
            logger.info("BehavioralAnalyzer initialized in mock mode (no MediaPipe)")
    
    def extract_visual_features(self, frame: np.ndarray) -> Dict:
        """
        Extract visual features from a video frame.
        
        Args:
            frame: RGB video frame (H, W, 3)
            
        Returns:
            Dictionary containing:
            - face_landmarks: Facial keypoints
            - face_detected: Boolean if face found
            - pose_landmarks: Body keypoints
            - gaze_direction: Estimated gaze vector
            - expression_signals: Encoded facial expression features
        """
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]
        
        features = {
            'frame_shape': (h, w),
            'timestamp': None,  # Should be set by caller
            'visual_present': True,
        }
        
        # If MediaPipe not available, use mock detection
        if not self.mediapipe_available:
            return self._extract_visual_features_mock(frame, features)
        
        # Real MediaPipe processing
        try:
            # Face detection and landmarks
            face_results = self.face_detector.process(frame_rgb)
            if face_results.detections:
                features['face_detected'] = True
                features['num_faces'] = len(face_results.detections)
                
                face_data = []
                for detection in face_results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    face_data.append({
                        'x': bbox.xmin,
                        'y': bbox.ymin,
                        'width': bbox.width,
                        'height': bbox.height,
                        'confidence': detection.score[0]
                    })
                features['face_data'] = face_data
            else:
                features['face_detected'] = False
                features['num_faces'] = 0
            
            # Pose detection
            pose_results = self.pose_detector.process(frame_rgb)
            if pose_results.pose_landmarks:
                features['pose_detected'] = True
                
                # Extract key poses
                landmarks = pose_results.pose_landmarks.landmark
                pose_data = {
                    'nose': (landmarks[0].x, landmarks[0].y),
                    'shoulders': (
                        (landmarks[11].x + landmarks[12].x) / 2,
                        (landmarks[11].y + landmarks[12].y) / 2
                    ),
                    'hips': (
                        (landmarks[23].x + landmarks[24].x) / 2,
                        (landmarks[23].y + landmarks[24].y) / 2
                    ),
                    'all_landmarks': [(l.x, l.y, l.z) for l in landmarks]
                }
                features['pose_data'] = pose_data
                
                # Estimate body orientation
                features['body_lean'] = self._estimate_body_lean(landmarks)
            
            # Hand detection
            hand_results = self.hand_detector.process(frame_rgb)
            if hand_results.multi_hand_landmarks:
                features['hands_detected'] = True
                features['num_hands'] = len(hand_results.multi_hand_landmarks)
            else:
                features['hands_detected'] = False
                features['num_hands'] = 0
            
            # Expression signals (placeholder - would use fine-tuned model)
            features['expression_signals'] = self._extract_expression_signals(
                frame, face_results
            )
            
        except Exception as e:
            logger.warning(f"MediaPipe processing error: {e} - using mock data")
            return self._extract_visual_features_mock(frame, features)
        
        return features
    
    def _extract_visual_features_mock(self, frame: np.ndarray, features: Dict) -> Dict:
        """
        Extract mock visual features when MediaPipe is not available.
        Generates realistic-looking default values for demo purposes.
        """
        h, w = frame.shape[:2]
        
        # Simulate face detection in center of frame
        features['face_detected'] = True
        features['num_faces'] = 1
        features['face_data'] = [{
            'x': 0.2,  # 20% from left
            'y': 0.1,  # 10% from top
            'width': 0.6,  # 60% width
            'height': 0.8,  # 80% height
            'confidence': 0.95
        }]
        
        # Simulate body/pose
        features['pose_detected'] = True
        features['pose_data'] = {
            'nose': (0.5, 0.2),
            'shoulders': (0.5, 0.4),
            'hips': (0.5, 0.7),
            'all_landmarks': (np.random.rand(33, 3) * 0.1 + np.array([0.5, 0.5, 0.0])).tolist()
        }
        features['body_lean'] = 'neutral'
        
        # Simulate hands
        features['hands_detected'] = np.random.rand() > 0.5
        features['num_hands'] = 2 if features['hands_detected'] else 0
        
        # Expression signals with random variation
        features['expression_signals'] = {
            'smile': np.random.rand() * 0.5,  # 0-50% smile
            'frown': np.random.rand() * 0.3,
            'furrowed_brow': np.random.rand() * 0.4,
            'head_tilt': np.random.rand() * 0.5,
            'gaze_forward': 0.8 + np.random.rand() * 0.2
        }
        
        logger.debug("Using mock visual features (MediaPipe not available)")
        return features
    
    def _estimate_body_lean(self, landmarks) -> str:
        """
        Estimate if body is leaning forward or back based on pose landmarks.
        
        Returns one of: 'forward', 'back', 'neutral'
        """
        # Simple heuristic: compare shoulder and hip positions
        shoulder_y = (landmarks[11].y + landmarks[12].y) / 2
        hip_y = (landmarks[23].y + landmarks[24].y) / 2
        
        nose_y = landmarks[0].y
        
        # If nose is significantly forward of shoulders, lean is forward
        if nose_y < shoulder_y * 0.95:
            return 'forward'
        elif nose_y > shoulder_y * 1.05:
            return 'back'
        else:
            return 'neutral'
    
    def _extract_expression_signals(self, frame: np.ndarray, 
                                    face_results: Optional[np.ndarray] = None) -> Dict:
        """
        Extract raw expression signal features from face region.
        
        Placeholder for fine-tuned LLaVA/LlaMA-based expression classification.
        Currently returns simple heuristics.
        
        Future: Use LLaVA or Qwen-VL for more sophisticated analysis
        """
        signals = {
            'has_face': face_results is not None,
            'brightness_mean': np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) / 255.0,
            # These would come from a fine-tuned expression model:
            'furrowed_brows_score': np.random.rand() * 0.5,  # 0-1 scale
            'smile_intensity': np.random.rand() * 0.7,  # 0-1 scale
            'eye_contact': np.random.rand() * 0.8,  # 0-1 scale (looking at camera/task)
        }
        return signals
    
    def extract_audio_features(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Dict:
        """
        Extract audio features from audio stream.
        
        Args:
            audio_data: Audio samples (mono or stereo)
            sample_rate: Sample rate in Hz
            
        Returns:
            Dictionary containing:
            - transcription: Speech-to-text via Whisper (requires API call)
            - speech_rate: Words per second
            - pitch_mean: Average fundamental frequency
            - energy: RMS energy
            - silence_ratio: Proportion of silence
        """
        
        features = {
            'sample_rate': sample_rate,
            'audio_length_seconds': len(audio_data) / sample_rate,
        }
        
        # Simple audio analysis (without external APIs for now)
        if len(audio_data) == 0:
            features['has_speech'] = False
            return features
        
        # Normalize audio
        audio_normalized = audio_data / np.max(np.abs(audio_data) + 1e-8)
        
        # Energy-based speech activity detection
        frame_size = 512
        frames = [
            audio_normalized[i:i+frame_size] 
            for i in range(0, len(audio_normalized), frame_size)
        ]
        
        energies = [np.sqrt(np.mean(f**2)) for f in frames]
        energy_threshold = np.mean(energies) * 0.1  # Adaptive threshold
        
        speech_frames = [e > energy_threshold for e in energies]
        features['has_speech'] = any(speech_frames)
        features['speech_duration_ratio'] = sum(speech_frames) / len(speech_frames) if speech_frames else 0
        
        # Fundamental frequency estimation (simple autocorrelation)
        features['pitch_mean'] = self._estimate_pitch(audio_normalized, sample_rate)
        features['energy_mean'] = np.mean(energies)
        
        # Speech rate placeholder (would use Whisper API)
        features['speech_rate_wps'] = None  # Words per second - requires transcription
        
        # Placeholder: transcription would come from Whisper
        features['transcription'] = None
        
        return features
    
    def _estimate_pitch(self, audio: np.ndarray, sample_rate: int) -> float:
        """
        Estimate fundamental frequency using autocorrelation.
        
        Returns frequency in Hz, or 0 if no clear pitch detected.
        """
        # Simple autocorrelation-based pitch estimation
        if len(audio) < sample_rate // 50:  # Min 20ms
            return 0.0
        
        # Work with frame of audio
        frame = audio[:sample_rate // 10]  # 100ms frame
        
        # Compute autocorrelation
        acf = np.correlate(frame, frame, mode='full')
        acf = acf[len(acf) // 2:]
        
        # Look for periodicity in range 50-500 Hz
        min_lag = sample_rate // 500
        max_lag = sample_rate // 50
        
        if max_lag >= len(acf):
            return 0.0
        
        peaks = np.argmax(acf[min_lag:max_lag]) + min_lag
        estimated_freq = sample_rate / peaks if peaks > 0 else 0.0
        
        return float(estimated_freq)
    
    def fuse_modalities(self, visual_features: Dict, audio_features: Dict) -> Dict:
        """
        Combine visual and audio features into unified representation.
        
        Returns multimodal feature vector for state inference.
        """
        
        fused = {
            'timestamp': None,
            'visual_features': visual_features,
            'audio_features': audio_features,
        }
        
        # Create composite features
        fused['has_visual'] = visual_features.get('visual_present', False)
        fused['has_audio'] = audio_features.get('has_speech', False)
        fused['multimodal_quality'] = float(
            fused['has_visual'] and fused['has_audio']
        )
        
        return fused
    
    def close(self):
        """Clean up MediaPipe resources."""
        if self.mediapipe_available:
            try:
                self.face_detector.close()
                self.pose_detector.close()
                self.hand_detector.close()
            except Exception as e:
                logger.warning(f"Error closing MediaPipe resources: {e}")
