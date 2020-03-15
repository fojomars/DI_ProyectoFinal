import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2
from reportlab.platypus import (Table, TableStyle)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet


class FacturaSimplificada(Gtk.Window):

    def __init__(self, nCliente):
        """
        Recibimos el numero de cliente cuando un cliente finaliza una compra
        :param nCliente: Número del cliente que ha iniciado sesión
        """

        numc = nCliente
        try:
            bbdd = dbapi2.connect("TiendaInformatica.db")
            cursor = bbdd.cursor()

            detalleFactura = []
            facturas = []


            detalleFactura.append(['Codigo Cliente: ', numc])
            """
            Seleccionamos el nombre y la dirección de la tabla clientes del cliente que ha iniciado sesión
            """
            cursorConsultaFactura = cursor.execute(
                "select nomc, direccion from clientes where numc = '" + str(numc) + "'")

            registroCliente = cursorConsultaFactura.fetchone()

            """Creamos las cabeceras del informe y los textos junto con los datos recogidos de la base de datos"""
            follaEstilo = getSampleStyleSheet()
            cabecera = follaEstilo['Heading4']
            cabecera.backColor = colors.lightcyan

            cabeceraFac = Paragraph((registroCliente[0] + " ¡¡¡GRACIAS POR REALIZAR TU PEDIDO!!!"), cabecera)
            cabeceraInfo = Paragraph("Información del pedido", cabecera)

            cadena = "Te informamos que su pedid ya esta en espera para la recogida del repartidor " + registroCliente[1] + "." \
                                                                                                                  "\nDado que este pedido se encuentra en proceso de envío, " \
                                                                                                                  "ya no podrás realizar ninguna modificación. "

            estilo = follaEstilo['BodyText']
            parrafo = Paragraph(cadena, estilo)

            """
            Recogemos los productos y la cantidad que el cliente ha comprado
            """
            cursorConsultaDetalle = cursor.execute("select codp, cantidad from factura where numc = ?", (int(numc),))
            listaConsultaDetalleFactura = []
            """
            Recorremos el cursor y añadimos los datos a una lista
            """
            for elementoFac in cursorConsultaDetalle:
                listaConsultaDetalleFactura.append([elementoFac[0], elementoFac[1]])
            detalleFactura.append(["", "", "", ""])

            detalleFactura.append(["Producto", "Descripción", "Cantidad", "Precio unitario", "Precio"])
            precioTotal = 0
            """
            Recogemos los datos del producto para cada producto que ha comprado
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
            Creamos un documento con el nombre "FacturaSimplificada" y el codigo del cliente
            """
            doc = SimpleDocTemplate(("FacturaSimplificada_" + str(numc) + ".pdf"), pagesize=A4)
            guion = []

            for factura in facturas:
                tabla = Table(factura, colWidths=80, rowHeights=30)

            """
            Creamos una tabla y le aplicamos los estilos que queremos para que se muestre en el informe
            """
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

            """
            Añadimos los componentes al guion
            """
            guion.append(cabeceraFac)
            guion.append(parrafo)
            guion.append(cabeceraInfo)
            guion.append(tabla)

            doc.build(guion)
