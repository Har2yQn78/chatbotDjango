import threading
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class RAGInitializer:
    _initialized = False
    _lock = threading.Lock()

    @classmethod
    def initialize_once(cls, with_sync=False):
        if not cls._initialized:
            with cls._lock:
                if not cls._initialized:
                    try:
                        from rag import (
                            db as rag_db,
                            settings as rag_settings,
                            sync as rag_sync
                        )
                        logger.info("Starting RAG initialization...")
                        rag_settings.init()
                        logger.info("RAG settings initialized")
                        rag_db.init_vector_db()
                        logger.info("Vector DB initialized")
                        
                        if with_sync:
                            cls.perform_sync()
                            
                        cls._initialized = True
                        logger.info("RAG initialized successfully")
                    except Exception as e:
                        logger.error(f"RAG initialization failed: {e}")
                        cls._initialized = False
        return cls._initialized
    
    @classmethod
    def perform_sync(cls):
        try:
            from rag import sync as rag_sync
            logger.info("Starting RAG sync...")
            rag_sync.full_sync()
            logger.info("Full sync completed")
            return True
        except Exception as e:
            logger.error(f"RAG sync failed: {e}")
            return False

def ensure_rag_initialized(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        RAGInitializer.initialize_once(with_sync=False)
        return view_func(request, *args, **kwargs)
    return wrapper