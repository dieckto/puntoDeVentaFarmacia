# app/services/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from app.db.models import Sale, SaleDetail

def generate_sale_ticket_pdf(sale: Sale) -> BytesIO:
    """
    Genera un PDF del ticket de venta.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Título
    story.append(Paragraph("Ticket de Venta - Farmacia POS", styles['Title']))
    story.append(Spacer(1, 12))

    # Información de la venta
    story.append(Paragraph(f"ID de Venta: {sale.id}", styles['Normal']))
    story.append(Paragraph(f"Fecha: {sale.created_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Paragraph(f"Total: ${sale.total:.2f}", styles['Normal']))
    if sale.discount > 0:
        story.append(Paragraph(f"Descuento: ${sale.discount:.2f}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Detalles de productos
    data = [['Producto', 'Cantidad', 'Precio Unit.', 'Subtotal']]
    for detail in sale.details:
        data.append([
            detail.medication.name,
            str(detail.quantity),
            f"${detail.unit_price:.2f}",
            f"${detail.subtotal:.2f}"
        ])
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)

    # Puntos si aplica
    if sale.customer:
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Puntos acumulados: {sale.customer.points}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
