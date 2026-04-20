# Adaptive Teaching AI System for Autism Intervention

An intelligent, real-time adaptive teaching system that uses Vision-Language Models (VLMs) to provide personalized instruction for children with autism. The system analyzes behavioral signals in real-time and adjusts its teaching strategy accordingly.

## 🎯 Project Overview

This system implements a proof-of-concept for adaptive AI-based teaching that:

- **Observes** student behavior through computer vision (face, pose, hand tracking) and audio analysis
- **Infers** cognitive and emotional states (engaged, confused, bored, frustrated)
- **Decides** which teaching strategy is most appropriate (concrete examples, slow down, simplify, etc.)
- **Responds** with natural language dialogue tailored to the student's current needs

### Key Innovation

Unlike static educational software, this system **continuously adapts** based on real-time behavioral feedback, enabling truly personalized learning experiences.

## 📋 System Architecture

```
Video/Audio Input
       ↓
┌──────────────────────────────┐
│  Component 1: Behavioral     │ ← Extracts visual & audio features
│  Analysis                    │   (MediaPipe, Librosa)
└────────────┬─────────────────┘
             ↓
      Feature Vector
             ↓
┌──────────────────────────────┐
│  Component 2: State          │ ← Classifies student state
│  Inference                   │   (Rule-based + ML)
└────────────┬─────────────────┘
             ↓
      Student State
      (ENGAGED/CONFUSED/BORED/FRUSTRATED)
             ↓
┌──────────────────────────────┐
│  Component 3: Strategy       │ ← Selects optimal teaching
│  Selection                   │   strategy (scoring + ranking)
└────────────┬─────────────────┘
             ↓
      Teaching Strategy
      (with parameters)
             ↓
┌──────────────────────────────┐
│  Component 4: Dialogue       │ ← Generates response via LLM
│  Generation                  │   (OpenAI/Ollama)
└────────────┬─────────────────┘
             ↓
   Natural Language Response
   + Visual Actions + Pacing
```

## 📦 Components

### 1. Behavioral Analysis (`behavioral_analysis.py`)

Extracts multi-modal behavioral features:
- Face detection and expression analysis (smile, frown, furrowed brow)
- Pose estimation (body lean, shoulder tension)
- Hand tracking and gesture recognition
- Speech activity, pitch, energy, speech rate analysis
- Fused multimodal feature vector

### 2. State Inference (`state_inference.py`)

Classifies student cognitive/emotional states:
- **ENGAGED** 🟢: Focused, responsive, participating
- **CONFUSED** 🔵: Shows confusion signals (furrowed brow, slow response)
- **BORED** 🟡: Disengaged (gaze away, minimal participation)
- **FRUSTRATED** 🔴: Showing frustration (high tension, elevated pitch)

Confidence-based threshold (60%) with fallback to safe responses.

### 3. Strategy Selection (`strategy_selector.py`)

Selects optimal teaching strategy:
- USE_CONCRETE_EXAMPLES
- SLOW_DOWN
- SIMPLIFY_LANGUAGE
- CHANGE_MODALITY
- TAKE_BREAK
- ENCOURAGE
- ASK_GUIDING_QUESTIONS
- REPEAT_WITH_VARIATION
- CONTINUE_CURRENT

Scoring considers: state fit, interaction history, time-on-task.

### 4. Dialogue Generation (`dialogue_generator.py`)

Generates natural language responses:
- Constructs context-aware prompts
- Calls LLM (OpenAI GPT-3.5/4 or Ollama Mixtral)
- Parses response for tone, pacing, visual actions
- Records interactions for learning

## 🚀 Quick Start

### Installation

```bash
# Inside the project directory
pip install -r requirements.txt

# Or with setup.py
pip install -e .
```

### Configuration

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Run Demo

```bash
python demo.py
```

## 💻 Usage

### Single Interaction

```python
from autism_teaching_ai import AdaptiveTeachingAI
import cv2
import numpy as np

ai = AdaptiveTeachingAI()

# Get video and audio
video_frame = cv2.imread("student.jpg")
audio_data = np.random.randn(16000)  # 1 second at 16kHz

# Process
response = ai.process_interaction(
    video=video_frame,
    audio=audio_data,
    topic="Counting Numbers",
    student_previous_input="I don't understand"
)

print(f"State: {response['student_state']}")
print(f"Strategy: {response['strategy_used']}")
print(f"Response: {response['response_text']}")
```

### Multi-Turn Session

```python
ai = AdaptiveTeachingAI()

for turn in range(5):
    response = ai.process_interaction(
        video=get_frame(),
        audio=get_audio(),
        topic="Sorting by Color",
        student_previous_input=get_student_input()
    )

summary = ai.get_session_summary()
print(f"Duration: {summary['duration_seconds']}s")
print(f"State distribution: {summary['state_distribution']}")
```

## ⚙️ Configuration

Key parameters in `.env`:

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `LLM_PROVIDER` | openai | LLM backend |
| `OPENAI_API_KEY` | (blank) | OpenAI API key |
| `STATE_CONFIDENCE_THRESHOLD` | 0.60 | State classification threshold |
| `STRATEGY_REPETITION_PENALTY` | 0.10 | Penalty for same strategy twice |
| `DEVICE` | cuda | GPU/CPU for models |
| `USE_MOCK_LLM` | False | Mock LLM (for testing) |

See `config.py` for all parameters.

## 🧠 For Researchers

### Phase 2: LLM Integration

```python
# Replace mock LLM in dialogue_generator.py
import openai
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

### Phase 3: MMASD Fine-tuning

```bash
# Download MMASD dataset and fine-tune behavioral model
python scripts/finetune_vla.py \
    --dataset_path ./data/MMASD \
    --output_dir ./models/vla_finetuned \
    --epochs 3
```

### Phase 4: Real Input Integration

```python
# Connect to actual camera
import cv2
cap = cv2.VideoCapture(0)
frame = cap.read()[1]

# Connect to microphone
import pyaudio
audio_stream = pyaudio.PyAudio().open(...)
```

## ⚠️ Important Notes

1. ⚠️ **Not a Medical Device**: This is a research prototype, not a medical device.
2. 🔒 **Privacy**: Handle video/audio carefully per IRB requirements.
3. 👤 **Not Human Replacement**: Cannot replace human therapists.
4. ✔️ **Always Review**: Verify AI-generated responses before use with children.
5. 📊 **Validation Needed**: Accuracy must be validated on actual users.

## 📚 API Reference

### AdaptiveTeachingAI

```python
class AdaptiveTeachingAI:
    def __init__(self):
        """Initialize all 4 components"""
    
    def process_interaction(
        self, 
        video: np.ndarray,
        audio: np.ndarray,
        topic: str,
        student_previous_input: str
    ) -> dict:
        """Process single teaching turn.
        
        Returns: {
            'student_state': 'ENGAGED/CONFUSED/BORED/FRUSTRATED',
            'student_state_confidence': float,
            'contributing_signals': list,
            'strategy_used': str,
            'response_text': str,
            'visual_actions': str,
            'tone': str,
            'pacing': str,
            'session_debug': dict
        }
        """
    
    def process_batch_session(
        self,
        videos: list,
        audios: list,
        topic: str,
        inputs: list
    ) -> list:
        """Process multiple turns."""
    
    def get_session_summary(self) -> dict:
        """Get session statistics."""
```

### BehavioralAnalyzer

```python
class BehavioralAnalyzer:
    def extract_visual_features(self, frame: np.ndarray) -> dict:
        """Extract face, pose, hand features"""
    
    def extract_audio_features(self, audio: np.ndarray) -> dict:
        """Extract prosody and speech features"""
    
    def fuse_modalities(self, visual: dict, audio: dict) -> np.ndarray:
        """Combine visual + audio into feature vector"""
```

### StateInferenceEngine

```python
class StateInferenceEngine:
    def infer_state(self, fused_features: np.ndarray) -> StudentState:
        """Classify student state with confidence"""
```

### StrategySelector

```python
class StrategySelector:
    def select_strategy(
        self,
        state: str,
        topic: str,
        context: dict
    ) -> TeachingStrategy:
        """Select best teaching strategy"""
```

### DialogueGenerator

```python
class DialogueGenerator:
    def generate_response(
        self,
        strategy_description: str,
        state: str,
        topic: str,
        student_input: str,
        history: list
    ) -> dict:
        """Generate LLM-based response"""
```

## 📈 Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| State classification accuracy | >0.80 | Development |
| Response generation latency | <2s | Development |
| Strategy selection accuracy | >0.75 | Development |
| Multimodal fusion | >0.70 | ✅ Complete |

## 🗂️ Project Structure

```
autism_teaching_ai/
├── __init__.py                 # Package exports
├── behavioral_analysis.py      # Component 1
├── state_inference.py          # Component 2
├── strategy_selector.py        # Component 3
├── dialogue_generator.py       # Component 4
└── teaching_ai.py             # Orchestration

demo.py                        # Demo scenarios
config.py                      # Configuration
requirements.txt               # Dependencies
```

## 📖 Documentation

- See parent `README.md` for project-wide setup
- See `config.py` for all available parameters
- See `demo.py` for usage examples

## 🤝 Contributing

Contributions welcome! Areas to contribute:

- [ ] Real camera/microphone integration
- [ ] MMASD dataset loader
- [ ] VLA fine-tuning pipeline
- [ ] Evaluation metrics framework
- [ ] Robot platform integration
- [ ] IRB approval documentation

## 📝 License

MIT License

## 🙏 Acknowledgments

- MMASD dataset creators
- MediaPipe developers
- OpenAI for GPT API
- TU Dortmund University

---

**Version**: 0.1.0 (Alpha)
**Last Updated**: April 13, 2026
**Status**: ✅ Demo working | 🔄 LLM integration pending
