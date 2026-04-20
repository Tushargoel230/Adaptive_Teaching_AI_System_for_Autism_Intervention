"""
Component 2: State Inference Engine
Maps behavioral signals to student states (ENGAGED, CONFUSED, BORED, FRUSTRATED).
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class StudentState:
    """Represents inferred student state with confidence."""
    state: str  # 'engaged', 'confused', 'bored', 'frustrated'
    confidence: float  # 0-1
    contributing_signals: List[str]
    uncertainty: float  # 1 - confidence


class StateInferenceEngine:
    """
    Infers student state from multimodal behavioral signals.
    
    States:
    - ENGAGED: Focused, responsive, positive body language
    - CONFUSED: Uncertain, hesitant, averted gaze, furrowed brows
    - BORED: Disinterested, minimal engagement, restless
    - FRUSTRATED: Agitated, negative affect, high tension
    """
    
    def __init__(self):
        """Initialize state inference rules."""
        self.states = ['engaged', 'confused', 'bored', 'frustrated']
        self.state_confidence_threshold = 0.60  # Min confidence to act on prediction
        
        logger.info(f"StateInferenceEngine initialized with states: {self.states}")
    
    def infer_state(self, fused_features: Dict) -> StudentState:
        """
        Infer student state from multimodal features.
        
        Args:
            fused_features: Output from BehavioralAnalyzer.fuse_modalities()
            
        Returns:
            StudentState object with predicted state and confidence
        """
        
        state_scores = {state: 0.0 for state in self.states}
        contributing_signals = []
        
        visual_features = fused_features.get('visual_features', {})
        audio_features = fused_features.get('audio_features', {})
        
        # Rule 1: ENGAGED signals
        if self._check_engaged_signals(visual_features, audio_features):
            state_scores['engaged'] += 0.4
            contributing_signals.append('positive_body_language')
        
        # Rule 2: CONFUSED signals
        if self._check_confused_signals(visual_features, audio_features):
            state_scores['confused'] += 0.35
            contributing_signals.append('averted_gaze')
            contributing_signals.append('hesitant_speech')
        
        # Rule 3: BORED signals
        if self._check_bored_signals(visual_features, audio_features):
            state_scores['bored'] += 0.3
            contributing_signals.append('gaze_avoidance')
            contributing_signals.append('minimal_response')
        
        # Rule 4: FRUSTRATED signals
        if self._check_frustrated_signals(visual_features, audio_features):
            state_scores['frustrated'] += 0.35
            contributing_signals.append('high_tension')
            contributing_signals.append('negative_affect')
        
        # Normalize scores to probability distribution
        total_score = sum(state_scores.values())
        if total_score > 0:
            state_probs = {s: state_scores[s] / total_score for s in self.states}
        else:
            # Default to uniform if no signals matched
            state_probs = {s: 1.0 / len(self.states) for s in self.states}
        
        # Get highest confidence state
        best_state = max(state_probs.items(), key=lambda x: x[1])
        state_name, confidence = best_state
        
        return StudentState(
            state=state_name,
            confidence=confidence,
            contributing_signals=contributing_signals[:5],  # Top 5 signals
            uncertainty=1.0 - confidence
        )
    
    def _check_engaged_signals(self, visual: Dict, audio: Dict) -> bool:
        """Check if signals indicate ENGAGED state."""
        signals = []
        
        # Visual: eyes on task, forward lean, smile
        if visual.get('pose_detected'):
            body_lean = visual.get('body_data', {}).get('body_lean')
            if body_lean == 'forward':
                signals.append(True)
        
        # Audio: speech present, normal rate
        if audio.get('has_speech'):
            signals.append(True)
        
        # Expression: smile, eye contact (placeholders)
        expr = visual.get('expression_signals', {})
        if expr.get('smile_intensity', 0) > 0.3:
            signals.append(True)
        
        # At least 2 engagement signals
        return sum(signals) >= 2
    
    def _check_confused_signals(self, visual: Dict, audio: Dict) -> bool:
        """Check if signals indicate CONFUSED state."""
        signals = []
        
        # Visual: furrowed brows, gaze away
        expr = visual.get('expression_signals', {})
        if expr.get('furrowed_brows_score', 0) > 0.4:
            signals.append(True)
        
        # Audio: slow response, long silence
        if audio.get('audio_length_seconds', 0) > 3 and not audio.get('has_speech'):
            signals.append(True)
        
        # Body: leaning back
        if visual.get('pose_data', {}).get('body_lean') == 'back':
            signals.append(True)
        
        # Requires at least 2 confusion signals
        return sum(signals) >= 2
    
    def _check_bored_signals(self, visual: Dict, audio: Dict) -> bool:
        """Check if signals indicate BORED state."""
        signals = []
        
        # Visual: gaze away, neutral expression, hand stimming
        expr = visual.get('expression_signals', {})
        if expr.get('smile_intensity', 0) < 0.2:
            signals.append(True)
        
        if expr.get('eye_contact', 0) < 0.3:
            signals.append(True)
        
        # Audio: monotone, minimal speech
        if audio.get('has_speech') and audio.get('speech_duration_ratio', 0) < 0.2:
            signals.append(True)
        
        # Hand movement (fidgeting)
        if visual.get('hands_detected'):
            signals.append(True)
        
        return sum(signals) >= 2
    
    def _check_frustrated_signals(self, visual: Dict, audio: Dict) -> bool:
        """Check if signals indicate FRUSTRATED state."""
        signals = []
        
        # Visual: tense posture, furrowed brows
        expr = visual.get('expression_signals', {})
        if expr.get('furrowed_brows_score', 0) > 0.5:
            signals.append(True)
        
        # Audio: high pitch, loud/agitated speech
        if audio.get('pitch_mean', 0) > 250:  # Higher pitch (Hz)
            signals.append(True)
        
        if audio.get('energy_mean', 0) > 0.6:  # High energy
            signals.append(True)
        
        # Body: rapid movements, tension
        if visual.get('pose_detected'):
            signals.append(True)  # Placeholder for tension detection
        
        return sum(signals) >= 2
    
    def get_state_info(self, state: StudentState) -> Dict:
        """
        Get interpretable information about the state for debugging.
        
        Returns:
            Dictionary with state details
        """
        return {
            'primary_state': state.state,
            'confidence_percent': f"{state.confidence*100:.1f}%",
            'uncertainty_percent': f"{state.uncertainty*100:.1f}%",
            'contributing_signals': state.contributing_signals,
            'can_act_on': state.confidence >= self.state_confidence_threshold,
            'recommendation': self._get_recommendation(state),
        }
    
    def _get_recommendation(self, state: StudentState) -> str:
        """Get action recommendation based on state."""
        if state.confidence < self.state_confidence_threshold:
            return "Confidence too low - wait for clearer signals"
        
        if state.state == 'engaged':
            return "Continue current approach, slightly increase complexity"
        elif state.state == 'confused':
            return "Switch to simplified explanation or concrete examples"
        elif state.state == 'bored':
            return "Change activity or modality to re-engage"
        elif state.state == 'frustrated':
            return "Take a break, reduce complexity, provide encouragement"
        
        return "No specific recommendation"
