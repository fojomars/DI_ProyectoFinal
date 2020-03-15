import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2
from Factura import FacturaSimplificada

class VentanaCompras(Gtk.Window):

    def __init__(self, nCliente):

        """
        Constructor que genera la interfaz del apartado de compras
        :param nCliente: Número de cliente que ha iniciado sesión recibido de la clase Login
        """
        Gtk.Window.__init__(self, title="Ventana de Compras")

        self.cajaProductos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        """
        Iniciamos la conexión a la base de datos.        
        Seleccionamos todos los datos de la tabla productos

        :param bbdd: Parámetro que conecta a la base de datos
        :param cursor: Cursor con el que recibimos datos de la base de datos.
        """

        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()
        self.cursor.execute("select * from productos")

        """
        Creamos un modelo al que le pasamos los tipos de valores de cada dato de la tabla
        modelo: Lista que recibe los datos de la tabla para añadirlo al TreeView
        """
        self.modelo = Gtk.ListStore(int, str, str, int, int)

        """
        Rellenamos el modelo recorriendo el cursor con un for
        """
        for rellenarModelo in self.cursor:
            codigo = rellenarModelo[0]
            nombre = rellenarModelo[1]
            descripcion = rellenarModelo[2]
            precio = rellenarModelo[3]
            self.modelo.append([codigo, nombre, descripcion, precio, 1])

        """
        vista: TreeView que contendrá los productos
        celdaText: CellRendererText que recibirá los valores
        columnaCodigo: columna del TreeView que contiene el codigo
        columnaNombre: columna del TreeView que contiene el nombre
        columnaDescripcion: columna del TreeView que contiene la descripción
        columnaPrecio: columna del TreeView que contiene el precio
        columnaCantidad: columna del TreeView que contiene la cantidad.
        """
        self.vista = Gtk.TreeView()

        celdaText = Gtk.CellRendererText()
        columnaCodigo = Gtk.TreeViewColumn('Codigo', celdaText, text=0)
        self.vista.append_column(columnaCodigo)

        celdaText2 = Gtk.CellRendererText(xalign=1)
        columnaNombre = Gtk.TreeViewColumn('Nombre', celdaText2, text=1)
        self.vista.append_column(columnaNombre)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaDescripcion = Gtk.TreeViewColumn('Descripción', celdaText3, text=2)
        self.vista.append_column(columnaDescripcion)

        celdaText4 = Gtk.CellRendererText(xalign=1)
        columnaPrecio = Gtk.TreeViewColumn('Precio', celdaText4, text=3)
        self.vista.append_column(columnaPrecio)

        """
        renderer_spin: Es un SpinButton que lo que hace es poder sumar +1 o restar -1 la cantidad.
        Se le establece la propiedrad adjustement.
        """

        renderer_spin = Gtk.CellRendererSpin()
        renderer_spin.connect("edited", self.on_amount_edited)
        renderer_spin.set_property("editable", True)

        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        renderer_spin.set_property("adjustment", adjustment)

        columnaCantidad = Gtk.TreeViewColumn('Cantidad', renderer_spin, text=4)
        self.vista.append_column(columnaCantidad)

        self.vista.set_model(self.modelo)

        """
        Hacemos que la variable nCliente pase a ser variable self de la clase
        """
        self.codcli = nCliente
        boComprar = Gtk.Button("Comprar")
        boComprar.connect('clicked', self.on_boComprar_clicked)
        boFinalizar = Gtk.Button("Finalizar Pedido")
        boFinalizar.connect('clicked', self.on_boFinalizar_clicked)

        self.cajaProductos.pack_start(self.vista, True, True, 0)
        self.cajaProductos.pack_start(boComprar, True, True, 0)
        self.cajaProductos.pack_start(boFinalizar, True, True, 0)

        self.add(self.cajaProductos)
        self.show_all()

    def on_amount_edited(self, widget, path, value):
        """
        Método que establece la cantidad en el TreeView cuando la cambias

        A ese componente del modelo se le asigna el valor que hemos editado

        :param widget: Componente en sí
        :param path: Puntero en el que está situado el cursor
        :param value: Valor que recibe del SpinButton
        :return: None
        """
        self.modelo[path][3] = int(value)

    def on_boComprar_clicked(self, boton):
        """
        Método que introduce lo que quieres comprar en la base de datos, en la tabla "factura"
        Establecemos la conexion con la base de datos, creamos el puntero e introducimos el valor en la tabla

        :param boton: Parametro que recibe el metodo
        :return: None

        """
        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()

        seleccion = self.vista.get_selection()

        self.modelo, puntero = seleccion.get_selected()

        # Si no hay ningún puntero seleccionado que no haga nada, si lo hay que lo meta en la tabla.
        if puntero is not None:
            codpr = self.modelo[puntero][0]
            cantidad = self.modelo[puntero][4]
            self.cursor.execute("insert into factura values(?,?,?)", (self.codcli, codpr, cantidad))
            self.bbdd.commit()

    def on_boFinalizar_clicked(self, boton):
        """
        Llamamos a la clase FacturaSimplificada y le pasamos el numero de cliente.
        :param boton: Parametro que recibe el metodo
        :return: None
        """
        FacturaSimplificada(self.codcli)

