from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from .models import Client, Quotation # Import models
from .forms import ClientForm, QuotationForm

def landing_page(request):
    if request.method == 'POST':
        # Get form data
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save() #Save client to DB
            return redirect('quotation_page', client_id = form.instance.id)# Redirect to the quotation page
    else:
        form = ClientForm()
    return render(request, "quotation_app/landing_page.html", {'form':form})

def quotation_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.client = client
            quotation.save()
            return redirect('generate_pdf', quotation_id=quotation.id)
    else:
        form = QuotationForm()
    return render(request, 'quotation_app/quotation_page.html', {'form': form, 'client': client})

def generate_pdf(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    client = quotation.client

    # Create a PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"RFQ for {client.name}")
    p.drawString(100, 730, f"Email: {client.email}")
    p.drawString(100, 710, f"WhatsApp: {client.whatsapp}")
    p.drawString(100, 680, "Products:")

    y = 660
    p.drawString(100, y, "Product Name")
    p.drawString(250, y, "Quantity")
    p.drawString(350, y, "Price")
    p.drawString(450, y, "Total Price")
    y -= 20

    p.drawString(100, y, quotation.product_name)
    p.drawString(250, y, str(quotation.quantity))
    p.drawString(350, y, str(quotation.price))
    p.drawString(450, y, str(quotation.total_price()))
    y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=RFQ_{client.name}.pdf'
    return response