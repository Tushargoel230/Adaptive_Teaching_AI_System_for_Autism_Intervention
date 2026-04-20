# Installation & Deployment Guide

Complete guide for setting up and deploying the Adaptive Teaching AI System.

## Prerequisites

- **Python**: 3.10 or higher
- **GPU** (optional): NVIDIA GPU with CUDA 11.8+ (for real-time performance)
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 20GB minimum (more if downloading MMASD dataset)
- **OS**: Linux (tested on Ubuntu 22.04), macOS, or Windows with WSL2

## Method 1: Quick Start (5 minutes)

### 1. Clone/Setup Repository

```bash
# Navigate to the project directory
cd /home/tushar/ros2_fp_ws/src/final_project
```

### 2. Run Setup Script

```bash
python scripts/setup.py
```

This will:
- Create necessary directories
- Set up .env file
- Check dependencies
- Test installation

### 3. Configure Environment

Edit `.env` file and add your OpenAI API key:

```bash
nano .env
# Add line: OPENAI_API_KEY=sk-your-key-here
```

### 4. Test Installation

```bash
python scripts/test_system.py
```

### 5. Run Demo

```bash
python demo.py
```

## Method 2: Manual Installation (Detailed)

### Step 1: Install Python Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using conda
conda create -n autism-ai python=3.10
conda activate autism-ai
pip install -r requirements.txt

# Or install from setup.py
pip install -e .
```

### Step 2: Create Project Structure

```bash
mkdir -p data/annotations
mkdir -p data/MMASD
mkdir -p logs/sessions
mkdir -p models/checkpoints
```

### Step 3: Setup Environment Configuration

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
export OPENAI_API_KEY="your-key"
export LLM_PROVIDER="openai"
export DEVICE="cuda"  # or "cpu"
```

### Step 4: Verify Installation

```bash
python -c "from autism_teaching_ai import AdaptiveTeachingAI; print('✓ Ready')"
```

## Using with Virtual Environment

### venv (Standard Python)

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### conda (Recommended for ML)

```bash
# Create environment
conda create -n autism-ai python=3.10

# Activate
conda activate autism-ai

# Install dependencies
pip install -r requirements.txt

# Add CUDA support (optional)
conda install pytorch::pytorch pytorch::torchvision torchvision torchaudio -c pytorch -c nvidia
```

### Poetry

```bash
# If you have poetry installed
poetry install

# Or create poetry environment
poetry env use python3.10
poetry install
```

## GPU Setup (Optional but Recommended)

### NVIDIA GPU with CUDA

```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Install NVIDIA PyTorch with CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU
python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

### Set in Configuration

```bash
# In .env
DEVICE=cuda
```

## Troubleshooting Installation

### Issue: "No module named 'mediapipe'"

```bash
pip install --upgrade mediapipe
```

### Issue: "No module named 'openai'"

```bash
pip install --upgrade openai
```

### Issue: CUDA/GPU not detected

```bash
# Check PyTorch installation
python -c "import torch; print(torch.__version__)"

# If CUDA not available, reinstall
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Or fall back to CPU
# Edit .env: DEVICE=cpu
```

### Issue: "Permission denied" on scripts

```bash
chmod +x scripts/test_system.py
chmod +x scripts/setup.py
```

### Issue: OpenAI API key not working

```bash
# Verify key format (should start with 'sk-')
# Check environment variable
echo $OPENAI_API_KEY

# Or set directly in code
import os
os.environ['OPENAI_API_KEY'] = 'sk-your-key'
```

## Configuration Options

### Minimal Configuration (Mock Mode)

Run without LLM API (for testing):

```bash
# .env
LLM_PROVIDER=mock
USE_MOCK_LLM=True
USE_MOCK_INPUT=True
DEVICE=cpu
```

Then run:
```bash
python demo.py
```

### Production Configuration

For real deployment:

```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
DEVICE=cuda
STATE_CONFIDENCE_THRESHOLD=0.70
SAFETY_CHECK_ENABLED=True
LOG_LEVEL=INFO
```

### Development Configuration

For development and debugging:

```bash
# .env
LLM_PROVIDER=openai
DEVICE=cuda
USE_MOCK_INPUT=False
LOG_LEVEL=DEBUG
VERBOSE=True
```

## Running the System

### 1. Run Demo

```bash
python demo.py
```

Shows 3 complete scenarios with system output.

### 2. Test Components

```bash
python scripts/test_system.py
```

Validates all components are working.

### 3. Run Your Own Code

```python
from autism_teaching_ai import AdaptiveTeachingAI
import cv2
import numpy as np

ai = AdaptiveTeachingAI()

# Get video and audio
frame = cv2.imread("student.jpg")
audio = np.random.randn(16000)

# Process
response = ai.process_interaction(
    video=frame,
    audio=audio,
    topic="Math Lesson",
    student_previous_input="test"
)

print(response['response_text'])
```

### 4. Integration with ROS2

```python
# In ROS2 node
import rclpy
from sensor_msgs.msg import Image
from autism_teaching_ai import AdaptiveTeachingAI

class TeachingAINode(rclpy.Node):
    def __init__(self):
        super().__init__('teaching_ai')
        self.ai = AdaptiveTeachingAI()
        
        # Subscribe to camera
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
    
    def image_callback(self, msg):
        # Convert ROS Image to numpy array
        # Process with AI
        # Publish response
        pass
```

## Docker Deployment (Optional)

### Create Dockerfile

```dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "demo.py"]
```

### Build and Run

```bash
docker build -t autism-teaching-ai .
docker run --gpus all autism-teaching-ai
```

## Environment Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OPENAI_API_KEY` | string | (blank) | Your OpenAI API key |
| `LLM_PROVIDER` | string | openai | LLM backend (openai/ollama/mock) |
| `DEVICE` | string | cuda | Compute device (cuda/cpu) |
| `USE_MOCK_LLM` | bool | False | Use mock LLM responses |
| `USE_MOCK_INPUT` | bool | False | Use mock video/audio input |
| `LOG_LEVEL` | string | INFO | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `STATE_CONFIDENCE_THRESHOLD` | float | 0.60 | Minimum state classification confidence |
| `STRATEGY_REPETITION_PENALTY` | float | 0.10 | Penalty for repeated strategy |

See `config.py` for complete reference.

## Next Steps

1. ✅ Installation complete
2. Run `python demo.py` to see system in action
3. Run `python scripts/test_system.py` to validate components
4. Integrate LLM API in `dialogue_generator.py`
5. Download MMASD dataset for fine-tuning
6. Deploy with real camera/microphone input

## Deployment Checklist

- [ ] Python 3.10+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenAI API key configured in `.env`
- [ ] Test script passes (`python scripts/test_system.py`)
- [ ] Demo runs successfully (`python demo.py`)
- [ ] Camera and microphone tested (if using real input)
- [ ] IRB approval obtained (if deploying with real users)

## Support

For issues:
1. Check Troubleshooting section above
2. Review logs in `./logs/` directory
3. Enable debug logging: `LOG_LEVEL=DEBUG` in .env
4. Run test suite: `python scripts/test_system.py`

## Documentation Links

- [Project README](../README.md) - Project overview
- [Component README](../autism_teaching_ai/README.md) - Component documentation
- [Configuration](../config.py) - All available parameters
- [Demo Script](../demo.py) - Usage examples

---

**Last Updated**: April 13, 2026
**Version**: 0.1.0 (Alpha)
