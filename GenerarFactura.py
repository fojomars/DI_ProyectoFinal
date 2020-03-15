import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


class GenerarFactura(Gtk.Window):


    def __init__(self):

        """
        Recogemos los numeros de cliente de la tabla factura y los cargamos en un combobox
        """
        Gtk.Window.__init__(self, title="Ventana de Facturas")

        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()

        cajaNumClientes = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.cmbNumeroCliente = Gtk.ComboBoxText()

        self.cursor.execute("select distinct numc from factura")
        n = 0
        for numc in self.cursor:
            self.cmbNumeroCliente.insert(n, "", str(numc[0]))
            n = n + 1

        boGenerarFactura = Gtk.Button("Generar Factura")
        boGenerarFactura.connect("clicked", self.on_boGenerarFactura_clicked)

        cajaNumClientes.pack_start(self.cmbNumeroCliente, False, False, 0)
        cajaNumClientes.pack_start(boGenerarFactura, False, False, 0)
        self.add(cajaNumClientes)
        self.show_all()

    def on_boGenerarFactura_clicked(self, boton):
        """
        Recogemos el numero de cliente seleccionado en el combobox y llamamos al método que genera el informe
        :param boton: Parametro que recibe el metodo
        :return: None
        """
        self.numc = self.cmbNumeroCliente.get_active_text()
        self.crearFactura()

    def crearFactura(self):
        """
        :param numc -> Numero de cliente que se recoge del combobox
        :return: None
        """

        numc = self.numc
        try:
            bbdd = dbapi2.connect("TiendaInformatica.db")
            cursor = bbdd.cursor()

            """
            :param detallefactura -> valores de la factura
            :param facturas -> numero de facturas
            """
            detalleFactura = []
            facturas = []

            # Primera linea de la factura. Codigo del cliente
            detalleFactura.append(['Codigo Cliente: ', numc])

            """
            Recogemos todos los datos del cliente que hemos seleccionado, y los añadimos a la lista detallefactura
            """
            cursorConsultaFactura = cursor.execute(
                "select nomc,apellidos,dni,direccion from clientes where numc = '" + str(numc) + "'")

            registroCliente = cursorConsultaFactura.fetchone()

            detalleFactura.append(['Nombre', registroCliente[0], '', '', ''])
            detalleFactura.append(['Apellidos', registroCliente[1], '', '', ''])
            detalleFactura.append(['DNI', registroCliente[2], '', '', ''])
            detalleFactura.append(['Direccion', registroCliente[3], '', '', ''])

            cursorConsultaDetalle = cursor.execute("select codp, cantidad from factura where numc = ?", (int(numc),))
            listaConsultaDetalleFactura = []

            """
            Seleccionamos el codigo de producto que ha comprado el cliente y la cantidad de ese producto
            y recorremos los productos obtenidos
            """
            for elementoFac in cursorConsultaDetalle:
                listaConsultaDetalleFactura.append([elementoFac[0], elementoFac[1]])
            detalleFactura.append(["", "", "", ""])

            detalleFactura.append(["Producto", "Descripción", "Cantidad", "Precio unitario", "Precio"])
            precioTotal = 0

            """
            Para cada producto obtenido recogemos sus datos de la base de datos, y lo recorremos para añadirlos a la
            factura.
            """
            for elemento in listaConsultaDetalleFactura:
                cursorConsultaProducto = cursor.execute(
                    "select descripcion, precio, nomp from productos where codp = '" +
                    str(elemento[0]) + "'")
                registroProducto = cursorConsultaProducto.fetchone()
                precio = elemento[1] * registroProducto[1]
                detalleFactura.append(
                    [registroProducto[2], registroProducto[0], elemento[1], registroProducto[1], precio])
                precioTotal = precioTotal + precio

            """
            Añadimos el precio total que es la suma de todos los productos
            """
            detalleFactura.append(["", "", "", "Precio total: ", precioTotal])
            facturas.append(list(detalleFactura))
            detalleFactura.clear()

        except(dbapi2.DatabaseError):
            print("Error en la base de datos")

        finally:
            print("Cerrando cursor y conexion de la base de datos")
            cursor.close()
            bbdd.close()

            """
            Creamos un documento, y le añadimos una tabla formateada a nuestro gusto
            """
            doc = SimpleDocTemplate(("Factura_" + str(numc) + ".pdf"), pagesize=A4)
            guion = []

            for factura in facturas:
                tabla = Table(factura, colWidths=80, rowHeights=30)

            tabla.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, 4), colors.blue),
                ('TEXTCOLOR', (0, 6), (-1, -1), colors.green),
                ('BACKGROUND', (0, 6), (-1, -1), colors.lightcyan),
                ('ALIGN', (2, 5), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, 4), 1, colors.black),
                ('BOX', (0, 6), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 6), (-1, -2), 0.5, colors.grey)

            ]))

            guion.append(tabla)

            doc.build(guion)

            bbdd = dbapi2.connect("TiendaInformatica.db")
            cursor = bbdd.cursor()

            """
            Una vez generamos la factura borramos el pedido del cliente de la tabla factura.
            """
            cursor.execute("delete from factura where numc = ?", [str(numc)])
            bbdd.commit()
