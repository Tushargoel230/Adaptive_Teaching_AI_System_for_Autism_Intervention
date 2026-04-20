"""
Adaptive Multimodal AI Teaching System for Autism Intervention
A system that combines visual and audio analysis with adaptive teaching strategies.
"""

__version__ = "0.1.0"
__author__ = "Research Team"

from .behavioral_analysis import BehavioralAnalyzer
from .state_inference import StateInferenceEngine
from .strategy_selector import StrategySelector
from .dialogue_generator import DialogueGenerator
from .teaching_ai import AdaptiveTeachingAI

__all__ = [
    "BehavioralAnalyzer",
    "StateInferenceEngine",
    "StrategySelector",
    "DialogueGenerator",
    "AdaptiveTeachingAI",
]
