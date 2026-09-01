

class NarrAIError(Exception):
    """Base exceptions for  NarrrAI ."""
    
class AudioMergerError(NarrAIError):
    """Raised when  audio merging fails."""

class PDFProcessingError(NarrAIError):
    """Raised when PDF processing fails."""

class TTSGenerationError(NarrAIError):
    """Raised when TTS generation fails."""