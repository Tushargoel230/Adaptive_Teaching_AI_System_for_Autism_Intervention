"""
Component 3: Teaching Strategy Selector
Selects appropriate teaching strategy based on student state and topic.
"""

from typing import Dict, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TeachingStrategy:
    """Represents a selected teaching strategy."""
    name: str
    description: str
    parameters: Dict
    estimated_effectiveness: float  # 0-1


class StrategySelector:
    """
    Selects optimal teaching strategy based on:
    - Student state (engaged, confused, bored, frustrated)
    - Current topic/content
    - Interaction history
    - Learned patterns from therapy data
    """
    
    STRATEGIES = {
        'USE_CONCRETE_EXAMPLES': {
            'description': 'Show physical objects or examples instead of abstract concepts',
            'modality': 'visual+tactile',
            'best_for': ['confused'],
            'effectiveness': 0.85,
        },
        'SLOW_DOWN': {
            'description': 'Reduce speech rate, allow more time for processing',
            'modality': 'verbal',
            'best_for': ['confused', 'frustrated'],
            'effectiveness': 0.80,
        },
        'SIMPLIFY_LANGUAGE': {
            'description': 'Use shorter sentences, simpler vocabulary',
            'modality': 'verbal',
            'best_for': ['confused', 'bored'],
            'effectiveness': 0.82,
        },
        'CHANGE_MODALITY': {
            'description': 'Switch between visual, auditory, tactile presentation',
            'modality': 'multi',
            'best_for': ['bored', 'disengaged'],
            'effectiveness': 0.75,
        },
        'TAKE_BREAK': {
            'description': 'Pause teaching, reduce stimulation, give time to reset',
            'modality': 'none',
            'best_for': ['frustrated', 'bored'],
            'effectiveness': 0.70,
        },
        'ENCOURAGE': {
            'description': 'Provide positive reinforcement and build confidence',
            'modality': 'verbal',
            'best_for': ['confused', 'frustrated'],
            'effectiveness': 0.78,
        },
        'ASK_GUIDING_QUESTIONS': {
            'description': 'Lead student to discovery with questions instead of direct answers',
            'modality': 'verbal',
            'best_for': ['engaged'],
            'effectiveness': 0.81,
        },
        'REPEAT_WITH_VARIATION': {
            'description': 'Reiterate concept using different examples or wording',
            'modality': 'verbal+visual',
            'best_for': ['confused', 'bored'],
            'effectiveness': 0.79,
        },
        'CONTINUE_CURRENT': {
            'description': 'Maintain current teaching approach - it is working',
            'modality': 'current',
            'best_for': ['engaged'],
            'effectiveness': 0.90,
        },
    }
    
    def __init__(self):
        """Initialize strategy selector with learned policies."""
        self.history = []
        logger.info(f"StrategySelector initialized with {len(self.STRATEGIES)} strategies")
    
    def select_strategy(self, 
                       student_state: str,
                       topic: str,
                       interaction_context: Dict = None) -> TeachingStrategy:
        """
        Select best teaching strategy given context.
        
        Args:
            student_state: Current state ('engaged', 'confused', 'bored', 'frustrated')
            topic: Topic being taught (e.g., 'math/counting', 'social/sharing')
            interaction_context: Dict with history, time_on_task, previous_effectiveness, etc.
            
        Returns:
            TeachingStrategy object with selected strategy and parameters
        """
        
        if interaction_context is None:
            interaction_context = {}
        
        # Get candidates for this state
        candidates = self._get_strategy_candidates(student_state)
        
        # Score each candidate
        scores = {}
        for strategy_name in candidates:
            score = self._score_strategy(
                strategy_name,
                student_state,
                topic,
                interaction_context
            )
            scores[strategy_name] = score
        
        # Select highest-scoring strategy
        best_strategy = max(scores.items(), key=lambda x: x[1])
        strategy_name = best_strategy[0]
        
        # Build strategy object with parameters
        strategy_def = self.STRATEGIES[strategy_name]
        
        strategy = TeachingStrategy(
            name=strategy_name,
            description=strategy_def['description'],
            parameters=self._get_strategy_parameters(strategy_name, topic, interaction_context),
            estimated_effectiveness=strategy_def['effectiveness'],
        )
        
        # Log strategy selection
        self.history.append({
            'state': student_state,
            'topic': topic,
            'selected_strategy': strategy_name,
            'scores': scores,
        })
        
        logger.info(f"Selected strategy: {strategy_name} (score: {best_strategy[1]:.2f}) for state: {student_state}")
        
        return strategy
    
    def _get_strategy_candidates(self, state: str) -> List[str]:
        """Get list of strategies suitable for given state."""
        if state == 'engaged':
            return [
                'CONTINUE_CURRENT',
                'ASK_GUIDING_QUESTIONS',
                'CHANGE_MODALITY',
            ]
        elif state == 'confused':
            return [
                'USE_CONCRETE_EXAMPLES',
                'SLOW_DOWN',
                'SIMPLIFY_LANGUAGE',
                'ENCOURAGE',
                'REPEAT_WITH_VARIATION',
            ]
        elif state == 'bored':
            return [
                'CHANGE_MODALITY',
                'TAKE_BREAK',
                'USE_CONCRETE_EXAMPLES',
                'SIMPLIFY_LANGUAGE',
            ]
        elif state == 'frustrated':
            return [
                'TAKE_BREAK',
                'ENCOURAGE',
                'SLOW_DOWN',
                'SIMPLIFY_LANGUAGE',
            ]
        else:
            # Default: all strategies available
            return list(self.STRATEGIES.keys())
    
    def _score_strategy(self, 
                       strategy: str,
                       state: str,
                       topic: str,
                       context: Dict) -> float:
        """
        Score strategy based on suitability for context.
        
        Higher score = better strategy for this situation.
        """
        
        strategy_def = self.STRATEGIES[strategy]
        base_score = strategy_def['effectiveness']
        
        # Boost if explicitly best for this state
        if state in strategy_def['best_for']:
            base_score += 0.15
        
        # Consider interaction history
        time_on_task = context.get('time_on_task_seconds', 0)
        
        # If been on same task too long, boost CHANGE_MODALITY
        if time_on_task > 600 and strategy == 'CHANGE_MODALITY':  # 10+ minutes
            base_score += 0.10
        
        # If just took break, down-vote TAKE_BREAK
        if context.get('just_took_break') and strategy == 'TAKE_BREAK':
            base_score -= 0.30
        
        # Previous strategy history
        recent_strategies = context.get('recent_strategies', [])
        if strategy in recent_strategies[-2:]:  # Used in last 2 teaching turns
            base_score -= 0.10  # Avoid repetition
        
        return max(base_score, 0.0)  # Clamp to [0, 1]
    
    def _get_strategy_parameters(self, strategy: str, topic: str, context: Dict) -> Dict:
        """
        Get specific parameters for executing this strategy.
        
        Returns dict with strategy-specific parameters.
        """
        
        params = {
            'strategy': strategy,
            'topic': topic,
        }
        
        # Strategy-specific parameters
        if strategy == 'USE_CONCRETE_EXAMPLES':
            params['use_physical_objects'] = True
            params['num_examples'] = 3
            params['allow_touch'] = True
            
        elif strategy == 'SLOW_DOWN':
            params['speech_rate_multiplier'] = 0.7  # 70% of normal speed
            params['pause_duration_seconds'] = 2.0
            
        elif strategy == 'SIMPLIFY_LANGUAGE':
            params['max_sentence_length'] = 8
            params['vocabulary_level'] = 'elementary'
            params['avoid_abstract'] = True
            
        elif strategy == 'CHANGE_MODALITY':
            current_modality = context.get('current_modality', 'verbal')
            if current_modality == 'verbal':
                params['target_modality'] = 'visual'
            elif current_modality == 'visual':
                params['target_modality'] = 'tactile'
            else:
                params['target_modality'] = 'verbal'
            
        elif strategy == 'TAKE_BREAK':
            params['break_duration_seconds'] = 120
            params['activity_type'] = 'free_movement'
            
        elif strategy == 'ENCOURAGE':
            params['positive_reinforcement'] = True
            params['effort_focused'] = True
            
        elif strategy == 'ASK_GUIDING_QUESTIONS':
            params['questions_first'] = True
            params['scaffold_complexity'] = True
            
        elif strategy == 'REPEAT_WITH_VARIATION':
            params['num_repetitions'] = 2
            params['vary_examples'] = True
        
        return params
    
    def get_strategy_description_for_llm(self, strategy: TeachingStrategy) -> str:
        """
        Format strategy for LLM prompt in dialogue generation.
        
        Returns a clear description of what the LLM should do.
        """
        
        description = f"Teaching Strategy: {strategy.name}\n"
        description += f"Goal: {strategy.description}\n"
        description += f"Parameters:\n"
        
        for key, value in strategy.parameters.items():
            if key != 'strategy' and key != 'topic':
                description += f"  - {key}: {value}\n"
        
        return description
