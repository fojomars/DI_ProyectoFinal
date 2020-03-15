import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class ApartadoProductos(Gtk.Window):
    """
    Clase Apartado productos en la que el administrador gestiona los productos.

    Métodos de la clase:

    __init__ -> Constructor de la clase
    on_seleccion_changed -> boton que recoge los datos del producto de la base de datos
    on_boInsertar_clicked -> boton que añade un producto a la base de datos
    on_boBorrarProductos_clicked -> boton que borra un producto de la base de datos
    """

    def __init__(self):
        """
        Constructor que da forma a la ventana
        :param cajaCrearProductos: Box con los componentes para crear un nuevo producto
        :param notebook: Gtk.Notebook para diferenciar crear producto de mostrar producto
        :param grid: forma de disposición de los componentes para insertar un producto
        :param vista: TreeView donde se cargan los productos de la base de datos
        """
        Gtk.Window.__init__(self, title="GestiónS de Productos")

        self.set_border_width(10)

        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()

        """
        Creamos el Gtk.Notebook, la caja y el grid
        """
        notebook = Gtk.Notebook()

        # Pagina de crear productos

        cajaCrearProductos = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        grid = Gtk.Grid()
        grid.set_row_spacing(20)
        grid.set_column_spacing(10)

        """
        Creamos los botones y labels del apartado de insertar producto
        """
        lblCodigo = Gtk.Label("Codigo:")
        lblNombre = Gtk.Label("Nombre:")
        lblDescripcion = Gtk.Label("Descripcion:")
        lblPrecio = Gtk.Label("Precio:")

        self.txtCodigo = Gtk.Entry()
        self.txtNombre = Gtk.Entry()
        self.txtDescripcion = Gtk.Entry()
        self.txtPrecio = Gtk.Entry()

        boInsertar = Gtk.Button("Insertar Producto")
        boInsertar.connect("clicked", self.on_boInsertar_clicked)

        """
        Introducimos los componentes en el grid y les especificamos la posicion y tamaño
        """
        grid.attach(lblCodigo, 0, 0, 1, 1)
        grid.attach(self.txtCodigo, 1, 0, 1, 1)
        grid.attach_next_to(lblNombre, self.txtCodigo, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtNombre, lblNombre, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblDescripcion, lblCodigo, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtDescripcion, lblDescripcion, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblPrecio, self.txtDescripcion, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtPrecio, lblPrecio, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(boInsertar, self.txtPrecio, Gtk.PositionType.BOTTOM, 1, 1)

        """
        Añadimos el grid a la caja, y añadimos la caja a una nueva ventana del notebook
        """
        cajaCrearProductos.add(grid)

        notebook.append_page(cajaCrearProductos, Gtk.Label('Crear Producto'))

        # Pagina de mostrar productos

        self.cajaMostrarProductos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()

        """
        Creamos un combobox y añadimos los codigos de los productos
        """

        self.cmbNumeroProductos = Gtk.ComboBoxText()

        self.cursor.execute("select codp from productos")
        n = 0
        for codp in self.cursor:
            self.cmbNumeroProductos.insert(n, "", str(codp[0]))
            n = n + 1

        self.cmbNumeroProductos.connect("changed", self.on_seleccion_changed)

        self.boBorrarProducto = Gtk.Button("Borrar Producto")
        self.boBorrarProducto.connect("clicked", self.on_boBorrarProducto_clicked)

        """
        Creamos un treeview donde se cargarán los datos de los productos y añadimos las columnas con el tipo de datos
        """
        self.vista = Gtk.TreeView()

        celdaText = Gtk.CellRendererText()
        columnaNombre = Gtk.TreeViewColumn('Nombre', celdaText, text=0)
        self.vista.append_column(columnaNombre)

        celdaText2 = Gtk.CellRendererText(xalign=1)
        columnaDescripcion = Gtk.TreeViewColumn('Descripcion', celdaText2, text=1)
        self.vista.append_column(columnaDescripcion)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaPrecio = Gtk.TreeViewColumn('Precio', celdaText3, text=2)
        self.vista.append_column(columnaPrecio)

        """
        Añadimos los componentes creados a la caja y añadimos la caja al notebook como una nueva pagina
        """
        self.cajaMostrarProductos.pack_start(self.cmbNumeroProductos, False, False, 0)
        self.cajaMostrarProductos.pack_start(self.vista, True, True, 0)
        self.cajaMostrarProductos.pack_start(self.boBorrarProducto, False, False, 0)

        notebook.append_page(self.cajaMostrarProductos, Gtk.Label('Mostrar Producto'))

        self.add(notebook)
        self.show_all()

    def on_boInsertar_clicked(self, boton):
        """
        Método que introduce un nuevo producto en la base de datos.
        Seleccionamos los valores de los entry y se los pasamos al cursor.

        :param boton: Parametro que recibe el metodo
        :return: None

        """
        self.cursor.execute("insert into productos values(?,?,?,?)",
                            (int(self.txtCodigo.get_text()),
                             self.txtNombre.get_text(),
                             self.txtDescripcion.get_text(),
                             int(self.txtPrecio.get_text())
                             )
                            )

        self.bbdd.commit()
        self.txtCodigo.set_text("")
        self.txtNombre.set_text("")
        self.txtDescripcion.set_text("")
        self.txtPrecio.set_text("")

    def on_seleccion_changed(self, boton):
        """
        Método que selecciona los datos del producto con el numero que esté seleccionado en el combobox
        Seleccionamos los datos, creamos un modelo (ListStore), y añadimos los datos recogidos al modelo y lo
        cargamos en el treeview

        :param boton: Parametro que recibe el metodo
        :return: None


        """

        self.cursor.execute("select nomp,descripcion,precio from productos where codp ='" +
                            str(self.cmbNumeroProductos.get_active_text()) + "'")
        self.modelo = Gtk.ListStore(str, str, int)

        valores = self.cursor.fetchone()
        print(valores)
        nombre = valores[0]
        descripcion = valores[1]
        precio = valores[2]
        self.modelo.append([nombre, descripcion, precio])
        print(self.modelo)
        self.vista.set_model(self.modelo)

    def on_boBorrarProducto_clicked(self, boton):
        """
        Metodo que borra un cliente de la base de datos y del treeview
        Borramos el producto que esté seleccionado en el treeview

        :param boton: Parametro que recibe el método
        :return: None

        """
        self.cursor.execute(
            "delete from productos where codp = '" + str(self.cmbNumeroProductos.get_active_text()) + "'")
        self.bbdd.commit()
        self.cmbNumeroProductos.remove(self.cmbNumeroProductos.get_active())
        self.modelo.append(["", "", "", "", ""])
        self.vista.set_model(self.modelo)
