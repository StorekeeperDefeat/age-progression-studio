"""AI Age Progression Studio.

Desktop toolkit for generating age-progressed and age-regressed renders
of a source face using a modular pipeline of face detection, landmark
alignment, identity embedding, and conditional aging synthesis.
"""

__version__ = "0.6.3"
__build__ = "2026.02.14"

from age_progression_studio.core.pipeline import AgeProgressionPipeline

__all__ = ["AgeProgressionPipeline", "__version__", "__build__"]