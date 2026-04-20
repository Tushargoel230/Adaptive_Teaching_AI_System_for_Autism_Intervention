"""Configuration and constants for Adaptive Teaching AI System"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# LLM Configuration
# ============================================================================

# LLM Provider: "openai" or "ollama" or "mock"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "256"))

# Ollama Configuration (for local deployment)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mixtral:8x7b")

# ============================================================================
# Behavioral Analysis Configuration
# ============================================================================

# Confidence thresholds for feature detection
CONFIDENCE_FACE_DETECTION = float(os.getenv("CONFIDENCE_FACE_DETECTION", "0.5"))
CONFIDENCE_POSE_DETECTION = float(os.getenv("CONFIDENCE_POSE_DETECTION", "0.5"))
CONFIDENCE_HAND_DETECTION = float(os.getenv("CONFIDENCE_HAND_DETECTION", "0.5"))

# Expression thresholds
SMILE_THRESHOLD = float(os.getenv("SMILE_THRESHOLD", "0.3"))
FROWN_THRESHOLD = float(os.getenv("FROWN_THRESHOLD", "0.3"))
FURROWED_BROW_THRESHOLD = float(os.getenv("FURROWED_BROW_THRESHOLD", "0.4"))

# Posture analysis
LEAN_THRESHOLD = float(os.getenv("LEAN_THRESHOLD", "0.15"))  # Forward/backward lean
TENSION_THRESHOLD = float(os.getenv("TENSION_THRESHOLD", "0.7"))  # Shoulder tension

# Audio analysis
PITCH_THRESHOLD_LOW = float(os.getenv("PITCH_THRESHOLD_LOW", "80"))  # Hz
PITCH_THRESHOLD_HIGH = float(os.getenv("PITCH_THRESHOLD_HIGH", "250"))  # Hz
ENERGY_THRESHOLD = float(os.getenv("ENERGY_THRESHOLD", "0.6"))
SPEECH_RATE_NORMAL = float(os.getenv("SPEECH_RATE_NORMAL", "150"))  # words per minute

# ============================================================================
# State Inference Configuration
# ============================================================================

# State classification thresholds
STATE_CONFIDENCE_THRESHOLD = float(os.getenv("STATE_CONFIDENCE_THRESHOLD", "0.60"))
STATE_UNCERTAINTY_THRESHOLD = float(os.getenv("STATE_UNCERTAINTY_THRESHOLD", "0.15"))

# State weights for multimodal fusion
WEIGHT_VISUAL = float(os.getenv("WEIGHT_VISUAL", "0.6"))
WEIGHT_AUDIO = float(os.getenv("WEIGHT_AUDIO", "0.4"))

# Time-based state memory (seconds)
STATE_MEMORY_WINDOW = int(os.getenv("STATE_MEMORY_WINDOW", "30"))

# ============================================================================
# Strategy Selection Configuration
# ============================================================================

# Anti-repetition penalty
STRATEGY_REPETITION_PENALTY = float(os.getenv("STRATEGY_REPETITION_PENALTY", "0.1"))

# Time-on-task thresholds
TIME_ON_TASK_THRESHOLD = int(os.getenv("TIME_ON_TASK_THRESHOLD", "600"))  # seconds

# Strategy parameter defaults
SLOWDOWN_RATE_MULTIPLIER = float(os.getenv("SLOWDOWN_RATE_MULTIPLIER", "0.7"))
SIMPLIFY_LANGUAGE_REDUCTION = float(os.getenv("SIMPLIFY_LANGUAGE_REDUCTION", "0.5"))

# ============================================================================
# Dialogue Generation Configuration
# ============================================================================

# Dialogue parameters
MAX_DIALOGUE_LENGTH = int(os.getenv("MAX_DIALOGUE_LENGTH", "256"))
DIALOGUE_TEMPERATURE = float(os.getenv("DIALOGUE_TEMPERATURE", "0.7"))

# Tone options: 'encouraging', 'neutral', 'playful', 'supportive'
DEFAULT_TONE = os.getenv("DEFAULT_TONE", "encouraging")

# Speaking rate (words per minute)
DEFAULT_SPEAKING_RATE = int(os.getenv("DEFAULT_SPEAKING_RATE", "120"))

# ============================================================================
# Dataset Configuration
# ============================================================================

# MMASD Dataset paths
MMASD_DATA_PATH = os.getenv("MMASD_DATA_PATH", "./data/MMASD")
MMASD_SPLIT_RATIO = float(os.getenv("MMASD_SPLIT_RATIO", "0.8"))  # Train/val split

# Behavioral annotation paths
ANNOTATION_PATH = os.getenv("ANNOTATION_PATH", "./data/annotations")

# ============================================================================
# Fine-tuning Configuration
# ============================================================================

# VLA Model
VLA_MODEL_NAME = os.getenv("VLA_MODEL_NAME", "openvla-7b")

# Fine-tuning parameters
FINETUNING_LEARNING_RATE = float(os.getenv("FINETUNING_LEARNING_RATE", "1e-4"))
FINETUNING_BATCH_SIZE = int(os.getenv("FINETUNING_BATCH_SIZE", "16"))
FINETUNING_EPOCHS = int(os.getenv("FINETUNING_EPOCHS", "3"))
FINETUNING_SAVE_STEPS = int(os.getenv("FINETUNING_SAVE_STEPS", "100"))

# LoRA parameters
LORA_R = int(os.getenv("LORA_R", "16"))
LORA_ALPHA = int(os.getenv("LORA_ALPHA", "32"))
LORA_DROPOUT = float(os.getenv("LORA_DROPOUT", "0.1"))

# ============================================================================
# Logging Configuration
# ============================================================================

# Logging level: "DEBUG", "INFO", "WARNING", "ERROR"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "./logs/teaching_ai.log")

# Session logging
LOG_SESSION_INTERACTIONS = os.getenv("LOG_SESSION_INTERACTIONS", "True").lower() == "true"
SESSION_LOG_PATH = os.getenv("SESSION_LOG_PATH", "./logs/sessions")

# ============================================================================
# System Configuration
# ============================================================================

# Device: "cpu" or "cuda"
DEVICE = os.getenv("DEVICE", "cuda")

# Video/Audio processing
VIDEO_FRAME_RATE = int(os.getenv("VIDEO_FRAME_RATE", "30"))
AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))

# Session defaults
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # seconds
MAX_INTERACTIONS_PER_SESSION = int(os.getenv("MAX_INTERACTIONS_PER_SESSION", "50"))

# ============================================================================
# Debugging & Mock Configuration
# ============================================================================

# Use mock LLM instead of real API (for development)
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "False").lower() == "true"

# Use mock video/audio input (for testing)
USE_MOCK_INPUT = os.getenv("USE_MOCK_INPUT", "False").lower() == "true"

# Verbose logging
VERBOSE = os.getenv("VERBOSE", "False").lower() == "true"

# ============================================================================
# Validation & Safety
# ============================================================================

# Confidence thresholds for output validation
MIN_RESPONSE_CONFIDENCE = float(os.getenv("MIN_RESPONSE_CONFIDENCE", "0.5"))

# Fallback behavior for low confidence predictions
ENABLE_FALLBACK_RESPONSES = os.getenv("ENABLE_FALLBACK_RESPONSES", "True").lower() == "true"

# Safety check: reject responses with negative sentiment
SAFETY_CHECK_ENABLED = os.getenv("SAFETY_CHECK_ENABLED", "True").lower() == "true"


def validate_config():
    """Validate configuration for required parameters"""
    warnings = []
    
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        warnings.append("WARNING: OpenAI API key not set. LLM functionality will be limited.")
    
    if not os.path.exists(ANNOTATION_PATH):
        warnings.append(f"WARNING: Annotation path does not exist: {ANNOTATION_PATH}")
    
    if USE_MOCK_INPUT:
        warnings.append("NOTE: Using mock input data (development mode)")
    
    if USE_MOCK_LLM:
        warnings.append("NOTE: Using mock LLM responses (development mode)")
    
    return warnings


if __name__ == "__main__":
    print("Configuration loaded successfully!")
    print(f"LLM Provider: {LLM_PROVIDER}")
    print(f"Device: {DEVICE}")
    print(f"Log Level: {LOG_LEVEL}")
    
    for msg in validate_config():
        print(msg)
