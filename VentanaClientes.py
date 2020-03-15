import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class ApartadoClientes(Gtk.Window):

    def __init__(self):
        """
        Constructor que da forma a la ventana
        :param crearCliente: Box con los componentes para crear un nuevo cliente
        :param notebook: Gtk.Notebook para diferenciar crear cliente de mostrar cliente
        :param grid: forma de disposición de los componentes para insertar un usuario
        :param vista: TreeView donde se cargan los clientes de la base de datos
        """
        Gtk.Window.__init__(self, title="Ventana de Clientes")
        self.set_border_width(10)

        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()

        """
        Creamos el Gtk.Notebook, la caja y el grid
        """
        notebook = Gtk.Notebook()

        # Pagina de crear clientes

        crearCliente = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        grid = Gtk.Grid()
        grid.set_row_spacing(20)
        grid.set_column_spacing(10)

        """
        Creamos los botones y labels del apartado de insertar cliente
        """

        lblNombre = Gtk.Label("Nombre:")
        lblApellido = Gtk.Label("Apellidos:")
        lblDni = Gtk.Label("DNI:")
        lblDireccion = Gtk.Label("Direccion:")
        lblNumeroCliente = Gtk.Label("Numero de cliente:")
        lblSexo = Gtk.Label("Sexo: ")

        self.txtNombre = Gtk.Entry()
        self.txtApellido = Gtk.Entry()
        self.txtDni = Gtk.Entry()
        self.txtDireccion = Gtk.Entry()
        self.txtNumeroCliente = Gtk.Entry()

        self.cmbSexo = Gtk.ComboBoxText()
        self.cmbSexo.insert(0, '0', "M")
        self.cmbSexo.insert(1, '1', "H")

        boInsertar = Gtk.Button("Insertar Cliente")
        boInsertar.connect("clicked", self.on_boInsertar_clicked)

        """
        Introducimos los componentes en el grid y les especificamos la posicion y tamaño
        """
        grid.attach(lblNombre, 0, 0, 1, 1)
        grid.attach(self.txtNombre, 1, 0, 1, 1)
        grid.attach_next_to(lblApellido, self.txtNombre, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtApellido, lblApellido, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblDni, lblNombre, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtDni, lblDni, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblDireccion, self.txtDni, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtDireccion, lblDireccion, Gtk.PositionType.RIGHT, 1, 1)

        grid.attach_next_to(lblNumeroCliente, lblDni, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtNumeroCliente, lblNumeroCliente, Gtk.PositionType.RIGHT, 1, 1)

        grid.attach_next_to(lblSexo, self.txtNumeroCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.cmbSexo, lblSexo, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(boInsertar, self.cmbSexo, Gtk.PositionType.BOTTOM, 1, 1)

        """
        Añadimos el grid a la caja, y añadimos la caja a una nueva ventana del notebook
        """
        crearCliente.add(grid)

        notebook.append_page(crearCliente, Gtk.Label('Crear Cliente'))

        # Pagina de mostrar clientes

        self.cajaMostrarClientes = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()
        """
        Creamos un combobox y añadimos los numeros de los clientes
        """
        self.cmbNumeroCliente = Gtk.ComboBoxText()

        self.cursor.execute("select numc from clientes")
        n = 0
        for numc in self.cursor:
            self.cmbNumeroCliente.insert(n, "", str(numc[0]))
            n = n + 1

        self.cmbNumeroCliente.connect("changed", self.on_seleccion_changed)

        self.boBorrarCliente = Gtk.Button("Borrar Cliente")
        self.boBorrarCliente.connect("clicked", self.on_boBorrarCliente_clicked)

        """
        Creamos un treeview donde se cargarán los datos de los clientes y añadimos las columnas con el tipo de datos
        """
        self.vista = Gtk.TreeView()

        celdaText = Gtk.CellRendererText()
        columnaNombre = Gtk.TreeViewColumn('Nombre', celdaText, text=0)
        self.vista.append_column(columnaNombre)

        celdaText2 = Gtk.CellRendererText(xalign=1)
        columnaApellidos = Gtk.TreeViewColumn('Apellidos', celdaText2, text=1)
        self.vista.append_column(columnaApellidos)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaDNI = Gtk.TreeViewColumn('DNI', celdaText3, text=2)
        self.vista.append_column(columnaDNI)

        celdaText4 = Gtk.CellRendererText(xalign=1)
        columnaDireccion = Gtk.TreeViewColumn('Dirección', celdaText4, text=3)
        self.vista.append_column(columnaDireccion)

        celdaText5 = Gtk.CellRendererText(xalign=1)
        columnaSexo = Gtk.TreeViewColumn('Sexo', celdaText5, text=4)
        self.vista.append_column(columnaSexo)

        """
        Añadimos los componentes creados a la caja y añadimos la caja al notebook como una nueva pagina
        """
        self.cajaMostrarClientes.pack_start(self.cmbNumeroCliente, False, False, 0)
        self.cajaMostrarClientes.pack_start(self.vista, True, True, 0)
        self.cajaMostrarClientes.pack_start(self.boBorrarCliente, False, False, 0)

        notebook.append_page(self.cajaMostrarClientes, Gtk.Label('Mostrar Cliente'))

        self.add(notebook)
        self.show_all()

    def on_seleccion_changed(self, boton):
        """
        Método que selecciona los datos del cliente con el numero que esté seleccionado en el combobox
        Seleccionamos los datos, creamos un modelo (ListStore), y añadimos los datos recogidos al modelo y lo
        cargamos en el treeview

        :param boton: Parametro que recibe el metodo
        :return: None


        """

        self.cursor.execute("select nomc,apellidos,dni,direccion,sexo from clientes where numc ='" +
                            str(self.cmbNumeroCliente.get_active_text()) + "'")
        self.modelo = Gtk.ListStore(str, str, str, str, str)

        valores = self.cursor.fetchone()
        print(valores)
        nombre = valores[0]
        apellidos = valores[1]
        dni = valores[2]
        direccion = valores[3]
        sexo = valores[4]
        self.modelo.append([nombre, apellidos, dni, direccion, sexo])
        print(self.modelo)
        self.vista.set_model(self.modelo)

    def on_boInsertar_clicked(self, boton):
        """
        Seleccionamos los valores de los entry y se los pasamos al cursor.

        Método que introduce un nuevo cliente en la base de datos.
        :param boton: Parametro que recibe el metodo
        :return: None

        """
        self.cursor.execute("insert into clientes values(?,?,?,?,?,?)",
                            (int(self.txtNumeroCliente.get_text()),
                             self.txtNombre.get_text(),
                             self.txtApellido.get_text(),
                             self.txtDni.get_text(),
                             self.txtDireccion.get_text(),
                             self.cmbSexo.get_active_text())
                            )

        self.bbdd.commit()
        self.txtNombre.set_text("")
        self.txtApellido.set_text("")
        self.txtDireccion.set_text("")
        self.txtNumeroCliente.set_text("")
        self.txtDni.set_text("")

    def on_boBorrarCliente_clicked(self, boton):

        """
        Metodo que borra un cliente de la base de datos y del treeview
        Borramos el cliente que esté seleccionado en el treeview
        :param boton: Parametro que recibe el método
        :return: None

        """
        self.cursor.execute("delete from clientes where numc = '" + str(self.cmbNumeroCliente.get_active_text()) + "'")
        self.bbdd.commit()
        self.cmbNumeroCliente.remove(self.cmbNumeroCliente.get_active())
        self.modelo.append(["", "", "", "", ""])
        self.vista.set_model(self.modelo)
