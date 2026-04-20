#!/usr/bin/env python3
"""
Test script to validate all components of the Adaptive Teaching AI System.
Run this to verify the system is working correctly before deployment.
"""

import sys
import os
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all components can be imported"""
    logger.info("Testing imports...")
    try:
        from autism_teaching_ai import (
            BehavioralAnalyzer,
            StateInferenceEngine,
            StrategySelector,
            DialogueGenerator,
            AdaptiveTeachingAI,
        )
        logger.info("✓ All components imported successfully")
        return True
    except ImportError as e:
        logger.error(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test that configuration loads correctly"""
    logger.info("Testing configuration...")
    try:
        import config
        logger.info(f"  LLM Provider: {config.LLM_PROVIDER}")
        logger.info(f"  Device: {config.DEVICE}")
        logger.info(f"  State threshold: {config.STATE_CONFIDENCE_THRESHOLD}")
        logger.info("✓ Configuration loaded successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Configuration failed: {e}")
        return False

def test_components():
    """Test basic component functionality"""
    logger.info("Testing components...")
    try:
        import numpy as np
        from autism_teaching_ai import AdaptiveTeachingAI
        
        logger.info("  Initializing AdaptiveTeachingAI...")
        ai = AdaptiveTeachingAI()
        logger.info("  ✓ Initialization successful")
        
        # Create mock data
        logger.info("  Creating mock data...")
        mock_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        mock_audio = np.random.randn(16000).astype(np.float32)
        
        logger.info("  Processing test interaction...")
        response = ai.process_interaction(
            video=mock_frame,
            audio=mock_audio,
            topic="Test Topic",
            student_previous_input="test"
        )
        
        # Validate response
        required_keys = [
            'student_state',
            'student_state_confidence',
            'strategy_used',
            'response_text'
        ]
        
        for key in required_keys:
            if key not in response:
                raise ValueError(f"Missing key in response: {key}")
        
        logger.info(f"  Student State: {response['student_state']}")
        logger.info(f"  Strategy: {response['strategy_used']}")
        logger.info("✓ Components working correctly")
        return True
        
    except Exception as e:
        logger.error(f"✗ Component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session():
    """Test multi-turn session"""
    logger.info("Testing multi-turn session...")
    try:
        import numpy as np
        from autism_teaching_ai import AdaptiveTeachingAI
        
        ai = AdaptiveTeachingAI()
        
        logger.info("  Running 3-turn session...")
        for turn in range(3):
            mock_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            mock_audio = np.random.randn(16000).astype(np.float32)
            
            response = ai.process_interaction(
                video=mock_frame,
                audio=mock_audio,
                topic="Learning Test",
                student_previous_input=f"turn {turn}"
            )
            logger.info(f"    Turn {turn+1}: {response['student_state']}")
        
        summary = ai.get_session_summary()
        logger.info(f"  Session Duration: {summary['duration_seconds']:.1f}s")
        logger.info(f"  Total Interactions: {summary['total_interactions']}")
        logger.info("✓ Multi-turn session successful")
        return True
        
    except Exception as e:
        logger.error(f"✗ Session test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_directories():
    """Test that required directories exist or can be created"""
    logger.info("Testing directories...")
    try:
        directories = ['./logs', './logs/sessions', './data']
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"  ✓ {directory}")
        logger.info("✓ Directories ready")
        return True
    except Exception as e:
        logger.error(f"✗ Directory setup failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Adaptive Teaching AI System - Test Suite")
    logger.info("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Directory Test", test_directories),
        ("Component Test", test_components),
        ("Session Test", test_session),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info("")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"✗ {test_name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info("")
    logger.info(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✓ All tests passed! System is ready to use.")
        return 0
    else:
        logger.error("✗ Some tests failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
