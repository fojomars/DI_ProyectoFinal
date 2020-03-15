import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from VentanaClientes import ApartadoClientes
from VentanaProductos import ApartadoProductos
from GenerarFactura import GenerarFactura

class VentanaAdmin(Gtk.Window):

    def __init__(self):

        """
        Constructor de la clase que crea la interfaz de la ventana

        Componentes:
        :param cajaComponentes: Caja que contiene todos los componentes
        :param grid: Forma de distribucion de los componentes
        :param lblClientes: Etiqueta de clientes
        :param lblProductos: Etiqueta de productos
        :param boClientes: Boton que abre el apartado de clientes
        :param boProductos: Boton que abre el apartado de productos
        :param boGenerarFactura: Boton que genera una factura de un cliente
        """
        Gtk.Window.__init__(self, title="Ventana de administracion")

        cajaComponentes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        grid = Gtk.Grid()
        grid.set_column_spacing(20)
        grid.set_row_spacing(20)

        lblClientes = Gtk.Label("Apartado de clientes")
        lblProductos = Gtk.Label("Apartado de productos")
        boClientes = Gtk.Button("Clientes")
        boProductos = Gtk.Button("Productos")
        boGenerarFactura = Gtk.Button("Generar Factura")

        grid.attach(lblClientes, 0, 0, 1, 1)
        grid.attach(lblProductos, 1, 0, 1, 1)
        grid.attach_next_to(boClientes, lblClientes, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(boProductos, lblProductos, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(boGenerarFactura,boClientes, Gtk.PositionType.BOTTOM, 2, 2)

        boClientes.connect("clicked", self.on_boClientes_clicked)
        boProductos.connect("clicked", self.on_boProductos_clicked)
        boGenerarFactura.connect("clicked", self.on_boGenerarFactura_clicked)


        cajaComponentes.add(grid)

        self.add(cajaComponentes)
        self.show_all()

    def on_boClientes_clicked(self, boton):
        """
        Método que llama al apartado de clientes
        :param boton: Parametro que recibe el metodo
        :return: None
        """
        ApartadoClientes()

    def on_boProductos_clicked(self, boton):
        """
        Metodo que llama al apartado de productos
        :param boton: Parametro que recibe el metodo
        :return: None
        """
        ApartadoProductos()

    def on_boGenerarFactura_clicked(self, boton):
        """
        Metodo que genera una factura
        :param boton: Parametro que recibe el metodo
        :return: None
        """
        GenerarFactura()

