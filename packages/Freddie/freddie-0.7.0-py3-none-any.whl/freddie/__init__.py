"""FastAPI tools library for building DRF-like viewsets"""

__version__ = '0.7.0'

from .schemas import Schema
from .viewsets import ViewSet

__all__ = ('Schema', 'ViewSet')
