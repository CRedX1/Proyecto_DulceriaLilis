# Dulcería Lilis - Sistema de Gestión

## Motor de BD y ejecución
- Motor: SQLite
- Archivo: db.sqlite3

```bash
python manage.py migrate
python manage.py runserver
```

## Cómo cargar semillas
```bash
python manage.py shell
# Ejecutar comandos para crear roles, proveedores, usuarios
```

## Usuario admin de prueba
- Usuario: admin
- Contraseña: admin123

## Apps del proyecto
- cuentas_usuario: Gestión de usuarios y roles
- proveedores: Gestión de proveedores y órdenes
- produccion: Gestión de producción  
- ventas: Gestión de ventas