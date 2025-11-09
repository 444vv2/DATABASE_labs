from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Імпортуємо роутери з контролерів
from Controler.user_controller import router as user_router
from Controler.event_controller import router as event_router
from Controler.ticket_controller import router as ticket_router
from Controler.order_controller import router as order_router
from Controler.location_controller import router as location_router
from Controler.transport_controller import router as transport_router
from Controler.payment_controller import router as payment_router
from Controler.insurance_controller import router as insurance_router
from Controler.delivery_controller import router as delivery_router
from Controler.artist_controller import router as artist_router

app = FastAPI(
    title="Ticket UA API",
    description="API для Квитки UA з бронюванням квитків та подій",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(event_router)
app.include_router(ticket_router)
app.include_router(order_router)
app.include_router(location_router)
app.include_router(transport_router)
app.include_router(payment_router)
app.include_router(insurance_router)
app.include_router(delivery_router)
app.include_router(artist_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tickets-ua-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
