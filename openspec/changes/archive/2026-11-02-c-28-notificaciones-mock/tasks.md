# Tasks

## 1. Setup

- [x] 1.1 Crear la interfaz `NotificationService` en `backend/app/notifications/interface.py` y verificar su presencia.
- [x] 1.2 Implementar `MockNotificationService` en `backend/app/notifications/mock.py` con almacenamiento en memoria y registro de errores.
- [x] 1.3 Añadir la variable de entorno `NOTIF_BACKEND=mock` en `backend/app/core/config.py` y actualizar `.env.example`.

## 2. Implementación

- [x] 2.1 Inyectar el servicio de notificaciones en `backend/app/application/bookings.py` después de persistir un turno.
- [x] 2.2 Asegurar que cualquier excepción del mock se loguea y la transacción del turno sigue commit.

## 3. Pruebas

- [x] 3.1 Escribir pruebas unitarias para `MockNotificationService` verificando el almacenamiento de eventos y manejo de excepciones.
- [x] 3.2 Escribir prueba de integración que cree un turno y compruebe que se registra una notificación en el mock.

## 4. Documentación

- [x] 4.1 Actualizar `knowledge-base/05_reglas_de_negocio.md` con la descripción del mecanismo de notificaciones mock.
- [x] 4.2 Documentar la configuración y uso del mock en el README del proyecto.
