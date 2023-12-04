from enum import Enum


class Status(Enum):
    
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    IN_PROGRESS = 'in_progress'
