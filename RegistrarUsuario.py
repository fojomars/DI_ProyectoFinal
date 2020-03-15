import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class RegistrarUsuario(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Registrar un Usuario")
        self.set_border_width(10)

        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()

        cajaCrearClientes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        grid = Gtk.Grid()
        grid.set_row_spacing(20)
        grid.set_column_spacing(10)

        """
        Etiquetas con los nombres de los datos que queremos insertar
        """

        lblNombre = Gtk.Label("Nombre:")
        lblApellido = Gtk.Label("Apellidos:")
        lblDni = Gtk.Label("DNI:")
        lblDireccion = Gtk.Label("Direccion:")
        lblNumeroCliente = Gtk.Label("Numero de cliente:")
        lblSexo = Gtk.Label("Sexo:")

        """
        Componentes entry para introducir los datos.
        ComboBox para el sexo.
        """
        self.txtNombre = Gtk.Entry()
        self.txtApellido = Gtk.Entry()
        self.txtDni = Gtk.Entry()
        self.txtDireccion = Gtk.Entry()
        self.txtNumeroCliente = Gtk.Entry()

        self.cmbSexo = Gtk.ComboBoxText()
        self.cmbSexo.insert(0, '0', "M")
        self.cmbSexo.insert(1, '1', "H")

        btnInsertar = Gtk.Button("Insertar Cliente")
        btnInsertar.connect("clicked", self.on_btnInsertar_clicked)

        btnVolver = Gtk.Button("Volver")
        btnVolver.connect("clicked", self.on_btnVolver_clicked)

        """
        Con grid attach lo que hacemos es establecer el orden en los que se colocan los componentes en el grid
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

        grid.attach_next_to(btnInsertar, self.lblSexo, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(btnVolver, btnInsertar, Gtk.PositionType.RIGHT, 1, 1)

        cajaCrearClientes.add(grid)

        self.add(cajaCrearClientes)
        self.show_all()

    def on_btnInsertar_clicked(self, boton):
        """
        Método que introduce en la base de datos un nuevo cliente
        :param boton: Parámetro que recibe el método
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

        """
        Hacemos un commit en la base de datos y reestablecemos los valores de los entry a null
        """
        self.bbdd.commit()
        self.txtNombre.set_text("")
        self.txtApellido.set_text("")
        self.txtDireccion.set_text("")
        self.txtNumeroCliente.set_text("")
        self.txtDni.set_text("")
"""
    def on_btnVolver_clicked(self, boton):
        
        Método para volver a login
        
        VentanaPrincipal()
"""