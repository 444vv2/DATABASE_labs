from .artist_controller import router as artist_router
from .event_controller import router as event_router
from .insurance_controller import router as insurance_router
from .ticket_controller import router as ticket_router
from .user_controller import router as user_router
from .order_controller import router as order_router
from .payment_controller import router as payment_router
from .delivery_controller import router as delivery_router
from .transport_controller import router as transport_router
from .location_controller import router as location_router
from .comment_controller import router as comment_router
from .artist_has_event_controller import router as artist_has_event_router
from .procedure_controller import router as procedure_router

__all__ = [
    "artist_router",
    "event_router",
    "insurance_router",
    "ticket_router",
    "user_router",
    "order_router",
    "payment_router",
    "delivery_router",
    "transport_router",
    "location_router",
    "comment_router",
    "artist_has_event_router",
    "procedure_router",
]
