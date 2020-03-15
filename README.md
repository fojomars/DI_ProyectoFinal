# AppTienda
Proyecto Desarrollo de Interfaces. Esto es una pequeña guía.

1. Cuando inicias la aplicación se abre la ventana Login

Al abrirse puedes acceder:

- Administrador -> Usuario para acceder a la parte de administración

- numc -> Es el número del cliente para acceder a la ventana cliente

También puedes crear un nuevo cliente en el boton "Registrar Usuario"

2. Ventanas de Administración / Compras:

- En la ventana compras seleccionas un producto del TreeView, el apartado de cantidad es un SpinButton editable.
Una vez terminas de seleccionar los productos si pulsas en "finalizar pedido" generas una factura simple.

- En la ventana del Administrador hay 3 botones:
  - Gestionar usuarios permite crear usuarios, y mostrar los que hay en la base de datos.
  - Gestionar productos permite crear productos, y mostrar los que hay en la base de datos.
  (Los dos permiten borrar productos/usuarios de la base.)
  - Generar factura te permite generar una factura detallada del usuario que haya realizado alguna compra.
