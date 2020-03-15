import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from RegistrarUsuario import RegistrarUsuario
from VentanaAdmin import VentanaAdmin
from VentanaCompras import VentanaCompras
from sqlite3 import dbapi2

class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        """
        Componentes:
        cajaComponentes: Caja que contiene todos los componentes
        lblUsuario: Etiqueta usuario
        txtUsuario: Entrada de texto para introducir el usuario
        btnRegistrarse: Boton para registrar usuario
        btnLogin: Boton para iniciar sesion
        grid: componente que da forma de visualizacion
        """
        Gtk.Window.__init__(self, title="Proyecto Desarrollo de interfaces")
        cajaComponentes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lblUsuario = Gtk.Label("Usuario:")
        self.txtUsuario = Gtk.Entry()
        btnRegistrarse = Gtk.Button("Registrarse")
        btnLogin = Gtk.Button("Login")
        btnSalir = Gtk.Button("Salir")
        btnRegistrarse.connect("clicked", self.on_btnRegistrarse_clicked)
        btnLogin.connect("clicked", self.on_btnLogin_clicked)
        btnSalir.connect("clicked", self.on_btnSalir_clicked)

        grid = Gtk.Grid()
        grid.set_column_spacing(20)
        grid.set_row_spacing(20)

        grid.attach(lblUsuario, 0, 0, 1, 1)
        grid.attach(self.txtUsuario, 1, 0, 1, 1)
        grid.attach_next_to(btnLogin, lblUsuario, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(btnRegistrarse, btnLogin, Gtk.PositionType.RIGHT, 1, 2)
        grid.attach(btnSalir, 0, 3, 3, 3)

        cajaComponentes.add(grid)

        self.connect("destroy", Gtk.main_quit)
        self.add(cajaComponentes)
        self.show_all()

    def on_btnRegistrarse_clicked(self, boton):
        """
        Llama a la clase que registra un usuario

        :param boton: Parametro que recibe el metodo
        :return: None
        """
        RegistrarUsuario()

    def on_btnLogin_clicked(self, boton):
        """
        Si el usuario que recibe el TextEntry es "Administrador" llama a la clase VentanaAdmin() que administra
        la parte del administrador.
        Por el contrario comprueba si el usuario está en la base de datos y si es así loguea, si no cambia el color
        del texto del Entry a rojo y muestra que el usuario es incorrecto
        :param boton: Parametro que recibe el metodo
        :return: None
        """

        if self.txtUsuario.get_text() == "Administrador":
            VentanaAdmin()
        else:
            self.bbdd = dbapi2.connect("TiendaInformatica.db")
            self.cursor = self.bbdd.cursor()
            self.cursor.execute("select numc from clientes where numc = ?", [self.txtUsuario.get_text()])

            valor = self.cursor.fetchone()
            # Valor recibe el resultado del cursor, si no recibe nada es que no existe el usuario en la base de datos.
            if valor is None:
                COLOR_INVALID = Gdk.color_parse('#de1212')
                self.txtUsuario.modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
                print("Usuario Incorrecto")
            else:
                numc = valor[0]
                VentanaCompras(numc)

    # Este evento sirve para cerrar la aplicación
    def on_btnSalir_clicked(self, boton):
        """
        Salir de la aplicación
        :param btnSalir
        :return: nothing
        """
        print("Cerrando aplicación")
        Gtk.main_quit()


if __name__ == "__main__":
    VentanaPrincipal()
Gtk.main()
