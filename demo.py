#!/usr/bin/env python3
"""
Demo script: Adaptive Teaching AI System

This script demonstrates the system on mock data (without real camera/mic).
For real deployment, replace mock data with actual video/audio streams.
"""

import numpy as np
import logging
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from autism_teaching_ai import AdaptiveTeachingAI

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_mock_video_frame(width=640, height=480, face_visible=True):
    """Create mock video frame for demo."""
    frame = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)
    
    if face_visible:
        # Add a light region to simulate face
        frame[100:300, 150:350] = 200
    
    return frame


def create_mock_audio(sample_rate=16000, duration_seconds=1.0):
    """Create mock audio for demo."""
    # Simple sine wave at 440 Hz (A note)
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    audio = 0.2 * np.sin(2 * np.pi * 440 * t)
    return audio.astype(np.float32)


def demo_basic_interaction():
    """Demo: Single teaching interaction."""
    
    print("\n" + "="*60)
    print("DEMO 1: Single Teaching Interaction")
    print("="*60 + "\n")
    
    # Initialize system
    ai = AdaptiveTeachingAI()
    
    # Create mock inputs
    video_frame = create_mock_video_frame(face_visible=True)
    audio_data = create_mock_audio()
    
    # Process single interaction
    print("Processing teaching interaction...")
    response = ai.process_interaction(
        video_frame=video_frame,
        audio_data=audio_data,
        topic="math/counting",
        student_previous_input="I don't know"
    )
    
    # Display results
    print(f"\n[SYSTEM ANALYSIS]")
    print(f"Student State: {response['student_state']} (confidence: {response['state_confidence']:.1%})")
    print(f"Contributing Signals: {', '.join(response['contributing_signals'])}")
    print(f"Teaching Strategy: {response['strategy_used']}")
    print(f"Strategy Description: {response['strategy_description']}")
    
    print(f"\n[SYSTEM RESPONSE]")
    print(f"AI Teacher: {response['response_text']}")
    print(f"Visual Actions: {response['visual_actions']}")
    print(f"Tone: {response['tone']}")
    print(f"Pacing: {response['pacing']}")
    
    print(f"\n[STATE ANALYSIS]")
    for key, value in response['explanation']['state_info'].items():
        print(f"  {key}: {value}")
    
    ai.close()


def demo_session_with_state_progression():
    """Demo: Teaching session with student state changes."""
    
    print("\n" + "="*60)
    print("DEMO 2: Teaching Session with State Progression")
    print("="*60 + "\n")
    
    ai = AdaptiveTeachingAI()
    
    # Simulate 5 turns with different states
    scenarios = [
        {
            'name': 'Initially Engaged',
            'face_visible': True,
            'student_input': None,
        },
        {
            'name': 'Student Shows Confusion',
            'face_visible': True,
            'student_input': "I don't understand",
        },
        {
            'name': 'Still Confused - Using Concrete',
            'face_visible': True,
            'student_input': "What do you mean?",
        },
        {
            'name': 'Starting to Engage',
            'face_visible': True,
            'student_input': "Oh, I see",
        },
        {
            'name': 'Successfully Learning',
            'face_visible': True,
            'student_input': "I got it!",
        },
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- TURN {i}: {scenario['name']} ---")
        
        video_frame = create_mock_video_frame(face_visible=scenario['face_visible'])
        audio_data = create_mock_audio()
        
        response = ai.process_interaction(
            video_frame=video_frame,
            audio_data=audio_data,
            topic="social/sharing",
            student_previous_input=scenario['student_input']
        )
        
        print(f"State: {response['student_state']} ({response['state_confidence']:.0%})")
        print(f"Strategy: {response['strategy_used']}")
        print(f"Response: {response['response_text'][:100]}...")
    
    # Print session summary
    summary = ai.get_session_summary()
    
    print(f"\n\n[SESSION SUMMARY]")
    print(f"Duration: {summary['session_duration_seconds']:.1f} seconds")
    print(f"Number of turns: {summary['num_turns']}")
    print(f"Topic: {summary['topic']}")
    print(f"State Distribution: {summary['state_distribution']}")
    print(f"Strategies Used: {summary['strategies_used']}")
    print(f"Average State Confidence: {summary['average_state_confidence']:.1%}")
    
    ai.close()


def demo_batch_teaching_session():
    """Demo: Process complete session as batch."""
    
    print("\n" + "="*60)
    print("DEMO 3: Batch Processing Teaching Session")
    print("="*60 + "\n")
    
    ai = AdaptiveTeachingAI()
    
    # Create mock batch data
    num_turns = 3
    video_frames = [create_mock_video_frame() for _ in range(num_turns)]
    audio_chunks = [create_mock_audio() for _ in range(num_turns)]
    student_inputs = [
        "What's that?",
        "I'm confused",
        "Oh I see!"
    ]
    
    # Process batch
    print(f"Processing batch session with {num_turns} turns...")
    responses = ai.process_batch_session(
        video_frames=video_frames,
        audio_chunks=audio_chunks,
        topic="science/colors",
        student_inputs=student_inputs
    )
    
    # Display results
    print(f"\nBatch processed {len(responses)} interactions:\n")
    
    for i, (response, student_input) in enumerate(zip(responses, student_inputs), 1):
        print(f"Turn {i}:")
        print(f"  Student: {student_input}")
        print(f"  AI State Assessment: {response['student_state']}")
        print(f"  Teaching Strategy: {response['strategy_used']}")
        print(f"  AI Response: {response['response_text'][:80]}...")
        print()
    
    ai.close()


def main():
    """Run all demos."""
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Adaptive Teaching AI System for Autism Intervention       ║")
    print("║  Demo Script                                               ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    try:
        # Run demos
        demo_basic_interaction()
        demo_session_with_state_progression()
        demo_batch_teaching_session()
        
        print("\n" + "="*60)
        print("All demos completed successfully!")
        print("="*60 + "\n")
        
        print("NEXT STEPS:")
        print("1. Integrate with real camera/microphone input")
        print("2. Add OpenAI/Ollama API integration for dialogue generation")
        print("3. Fine-tune models on MMASD autism behavior dataset")
        print("4. Deploy to robot platform (TurtleBot3, Pepper, etc.)")
        print("5. Test with real therapy sessions\n")
        
    except Exception as e:
        logger.error(f"Demo failed with error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
