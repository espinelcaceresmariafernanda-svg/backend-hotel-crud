from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="API Sistema de Hotel y Reserva de Habitaciones",
    description="API RESTful CRUD completa para la gestión de habitaciones de hotel",
    version="1.0.0"
)

# Modelo Pydantic para la entidad Habitacion
class Habitacion(BaseModel):
    id: int
    tipo_habitacion: str
    tarifa_noche: float
    capacidad_personas: int
    disponible_reserva: bool

# Modelo para actualización parcial/total
class HabitacionUpdate(BaseModel):
    tipo_habitacion: str
    tarifa_noche: float
    capacidad_personas: int
    disponible_reserva: bool

# Base de datos simulada en memoria con 2 registros iniciales
db_habitaciones: List[Habitacion] = [
    Habitacion(id=1, tipo_habitacion="Sencilla", tarifa_noche=120000.0, capacidad_personas=1, disponible_reserva=True),
    Habitacion(id=2, tipo_habitacion="Suite", tarifa_noche=350000.0, capacidad_personas=2, disponible_reserva=False)
]

# --- ENDPOINTS CRUD ---

# 1. READ: Obtener todas las habitaciones
@app.get("/api/v1/habitaciones", response_model=List[Habitacion], status_code=status.HTTP_200_OK)
def obtener_todas_las_habitaciones():
    return db_habitaciones

# 2. READ: Obtener una habitacion por ID
@app.get("/api/v1/habitaciones/{habitacion_id}", response_model=Habitacion, status_code=status.HTTP_200_OK)
def obtener_habitacion_por_id(habitacion_id: int):
    for hab in db_habitaciones:
        if hab.id == habitacion_id:
            return hab
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"La habitación con ID {habitacion_id} no existe en el sistema del hotel."
    )

# 3. CREATE: Registrar una nueva habitacion
@app.post("/api/v1/habitaciones", response_model=Habitacion, status_code=status.HTTP_201_CREATED)
def crear_nueva_habitacion(habitacion: Habitacion):
    for hab in db_habitaciones:
        if hab.id == habitacion.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de registro: Ya existe una habitación con el ID {habitacion.id}."
            )
    db_habitaciones.append(habitacion)
    return habitacion

# 4. UPDATE: Actualizar una habitacion
@app.put("/api/v1/habitaciones/{habitacion_id}", response_model=Habitacion, status_code=status.HTTP_200_OK)
def actualizar_habitacion(habitacion_id: int, datos_actualizados: HabitacionUpdate):
    for index, hab in enumerate(db_habitaciones):
        if hab.id == habitacion_id:
            habitacion_modificada = Habitacion(
                id=habitacion_id,
                tipo_habitacion=datos_actualizados.tipo_habitacion,
                tarifa_noche=datos_actualizados.tarifa_noche,
                capacidad_personas=datos_actualizados.capacidad_personas,
                disponible_reserva=datos_actualizados.disponible_reserva
            )
            db_habitaciones[index] = habitacion_modificada
            return habitacion_modificada
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. La habitación con ID {habitacion_id} no fue encontrada."
    )

# 5. DELETE: Eliminar una habitacion
@app.delete("/api/v1/habitaciones/{habitacion_id}", status_code=status.HTTP_200_OK)
def eliminar_habitacion(habitacion_id: int):
    for index, hab in enumerate(db_habitaciones):
        if hab.id == habitacion_id:
            db_habitaciones.pop(index)
            return {"mensaje": f"La habitación con ID {habitacion_id} fue eliminada exitosamente."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. La habitación con ID {habitacion_id} no existe."
    )