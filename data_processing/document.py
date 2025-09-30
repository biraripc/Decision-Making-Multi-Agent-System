from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

@dataclass
class Document:
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None
