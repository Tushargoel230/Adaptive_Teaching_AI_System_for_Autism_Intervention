"""
Main integration: Adaptive Teaching AI System
Orchestrates all four components into a complete adaptive teaching loop.
"""

from typing import Dict, Optional
import logging
from datetime import datetime

from .behavioral_analysis import BehavioralAnalyzer
from .state_inference import StateInferenceEngine
from .strategy_selector import StrategySelector
from .dialogue_generator import DialogueGenerator

logger = logging.getLogger(__name__)


class AdaptiveTeachingAI:
    """
    Main teaching AI orchestrator.
    
    Implements the complete loop:
    INPUT (Video+Audio) → BEHAVIOR ANALYSIS → STATE INFERENCE → STRATEGY SELECTION → DIALOGUE GENERATION → OUTPUT
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the complete system.
        
        Args:
            config: Configuration dictionary with optional settings
        """
        
        self.config = config or {}
        
        # Initialize components
        self.behavioral_analyzer = BehavioralAnalyzer()
        self.state_inference = StateInferenceEngine()
        self.strategy_selector = StrategySelector()
        self.dialogue_generator = DialogueGenerator()
        
        # Interaction state
        self.interaction_history = []
        self.current_topic = None
        self.session_start = datetime.now()
        
        logger.info("AdaptiveTeachingAI system initialized successfully")
    
    def process_interaction(self,
                           video_frame: 'np.ndarray',
                           audio_data: 'np.ndarray',
                           topic: str,
                           student_previous_input: Optional[str] = None) -> Dict:
        """
        Process a single teaching interaction.
        
        Args:
            video_frame: Video frame from camera (H, W, 3)
            audio_data: Audio samples from microphone
            topic: Current teaching topic
            student_previous_input: What student said/did last turn
            
        Returns:
            Dictionary with:
            - response_text: What to say
            - visual_actions: What to display/do
            - student_state: Inferred student state
            - strategy_used: Teaching strategy used
            - explanation: Debug info for interview
        """
        
        self.current_topic = topic
        
        # STEP 1: Behavioral Analysis
        logger.info("Step 1: Analyzing behavior...")
        visual_features = self.behavioral_analyzer.extract_visual_features(video_frame)
        audio_features = self.behavioral_analyzer.extract_audio_features(audio_data)
        fused_features = self.behavioral_analyzer.fuse_modalities(visual_features, audio_features)
        
        # STEP 2: State Inference
        logger.info("Step 2: Inferring student state...")
        student_state = self.state_inference.infer_state(fused_features)
        state_info = self.state_inference.get_state_info(student_state)
        
        # STEP 3: Strategy Selection
        logger.info("Step 3: Selecting teaching strategy...")
        interaction_context = {
            'time_on_task_seconds': self._get_time_on_task(),
            'recent_strategies': [h.get('strategy') for h in self.interaction_history[-5:]],
        }
        
        teaching_strategy = self.strategy_selector.select_strategy(
            student_state.state,
            topic,
            interaction_context
        )
        
        strategy_desc = self.strategy_selector.get_strategy_description_for_llm(teaching_strategy)
        
        # STEP 4: Dialogue Generation
        logger.info("Step 4: Generating response...")
        response = self.dialogue_generator.generate_response(
            strategy_description=strategy_desc,
            student_state=student_state.state,
            topic=topic,
            student_input=student_previous_input,
            interaction_history=self.interaction_history
        )
        
        # Record this interaction
        interaction_record = {
            'timestamp': datetime.now(),
            'topic': topic,
            'student_state': student_state.state,
            'student_state_confidence': student_state.confidence,
            'strategy': teaching_strategy.name,
            'student_input': student_previous_input,
            'teacher_response': response['response_text'],
            'visual_features_summary': {
                'face_detected': visual_features.get('face_detected'),
                'pose_detected': visual_features.get('pose_detected'),
                'hands_detected': visual_features.get('hands_detected'),
            },
            'audio_features_summary': {
                'has_speech': audio_features.get('has_speech'),
                'speech_duration_ratio': audio_features.get('speech_duration_ratio'),
            },
        }
        
        self.interaction_history.append(interaction_record)
        
        # Return complete response
        return {
            'response_text': response['response_text'],
            'visual_actions': response['visual_actions'],
            'tone': response['tone'],
            'pacing': response['pacing'],
            'student_state': student_state.state,
            'state_confidence': student_state.confidence,
            'contributing_signals': student_state.contributing_signals,
            'strategy_used': teaching_strategy.name,
            'strategy_description': teaching_strategy.description,
            # Debug/explanation info
            'explanation': {
                'state_info': state_info,
                'strategy_parameters': teaching_strategy.parameters,
                'behavioral_summary': {
                    'visual': f"Face: {visual_features.get('face_detected')}, Pose: {visual_features.get('pose_detected')}",
                    'audio': f"Speech: {audio_features.get('has_speech')}, Duration: {audio_features.get('speech_duration_ratio', 0):.1%}",
                },
            },
        }
    
    def process_batch_session(self,
                             video_frames: list,
                             audio_chunks: list,
                             topic: str,
                             student_inputs: Optional[list] = None) -> list:
        """
        Process a complete teaching session with multiple turns.
        
        Args:
            video_frames: List of video frames
            audio_chunks: List of audio chunks
            topic: Teaching topic
            student_inputs: Optional list of what student said each turn
            
        Returns:
            List of responses, one for each turn
        """
        
        responses = []
        
        for i, (frame, audio) in enumerate(zip(video_frames, audio_chunks)):
            student_input = student_inputs[i] if student_inputs else None
            
            response = self.process_interaction(
                video_frame=frame,
                audio_data=audio,
                topic=topic,
                student_previous_input=student_input
            )
            
            responses.append(response)
        
        return responses
    
    def get_session_summary(self) -> Dict:
        """
        Get summary of current teaching session.
        
        Returns statistics about the session for analysis.
        """
        
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        # Count strategy usage
        strategy_counts = {}
        for record in self.interaction_history:
            strategy = record.get('strategy', 'unknown')
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        # Average state confidence
        confidences = [r['student_state_confidence'] for r in self.interaction_history]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # State distribution
        state_counts = {}
        for record in self.interaction_history:
            state = record.get('student_state', 'unknown')
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            'session_duration_seconds': session_duration,
            'num_turns': len(self.interaction_history),
            'strategies_used': strategy_counts,
            'state_distribution': state_counts,
            'average_state_confidence': avg_confidence,
            'topic': self.current_topic,
            'timestamp': self.session_start.isoformat(),
        }
    
    def _get_time_on_task(self) -> float:
        """Get time spent on current topic in seconds."""
        if not self.interaction_history:
            return 0.0
        
        first_time = self.interaction_history[0]['timestamp']
        last_time = datetime.now()
        
        return (last_time - first_time).total_seconds()
    
    def close(self):
        """Clean up resources."""
        self.behavioral_analyzer.close()
        logger.info("AdaptiveTeachingAI system closed")
