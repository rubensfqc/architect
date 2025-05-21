from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, Image
from io import BytesIO
from .models import Client, Quotation, Product, QuotationProduct, Seller # Import models
from .forms import ClientForm, QuotationForm, ProductForm, QuotationProductForm, QuotatioFormPerSeller
from django.urls import reverse
from .utils import list_all_urls

def home_view(request):
    urls = list_all_urls()
    return render(request, 'quotation_app/home.html', {'urls': urls})

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

def landing_page_per_seller(request, slug):
    seller = get_object_or_404(Seller, slug=slug)
    if request.method == 'POST':
        # Get form data
        form = ClientForm(request.POST)
        if form.is_valid():
            form.instance.seller = seller  # Set the seller for the client
            form.save() #Save client to DB
            return redirect('quotation_page_per_seller', slug=seller.slug, client_id = form.instance.id)# Redirect to the quotation page
    else:
        form = ClientForm()
    return render(request, "quotation_app/landing_page_per_seller.html", {'seller': seller, 'form':form})

def quotation_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    products = Product.objects.all()
    
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = Quotation.objects.create(client=client)
            total_amount = 0
            for product in products:
                quantity = form.cleaned_data.get(f'quantity_{product.id}', 0)
                if quantity and quantity > 0:
                    quotation.products.add(product, through_defaults={'quantity': quantity})
                    total_amount += product.price * quantity
            quotation.total_amount = total_amount
            quotation.save() # Save quotation to DB        
            return redirect('generate_pdf', quotation_id=quotation.id)
    else:
        form = QuotationForm()
   
    return render(request, 'quotation_app/quotation_page.html', {'form': form, 'client': client})

def quotation_page_per_seller(request, slug, client_id):
    seller = get_object_or_404(Seller, slug=slug)
    client = get_object_or_404(Client, id=client_id)
    products = Product.objects.filter(seller=seller)
    
    if request.method == 'POST':
        form = QuotatioFormPerSeller(request.POST, seller=seller)  # Pass the seller to the form
        if form.is_valid():
            quotation = Quotation.objects.create(client=client)
            total_amount = 0
            for product in products:
                quantity = form.cleaned_data.get(f'quantity_{product.id}', 0)
                if quantity and quantity > 0:
                    quotation.products.add(product, through_defaults={'quantity': quantity})
                    total_amount += product.price * quantity
            quotation.total_amount = total_amount
            quotation.save() # Save quotation to DB        
            return redirect('generate_pdf', slug=slug, quotation_id=quotation.id)
    else:
        form = QuotatioFormPerSeller(request.POST, seller=seller)  # Pass the seller to the form
   
    return render(request, 'quotation_app/quotation_page_per_seller.html', {'form': form, 'client': client, 'seller':seller})

def generate_pdf(request, slug, quotation_id):
    seller = get_object_or_404(Seller, slug=slug)
    quotation = get_object_or_404(Quotation, id=quotation_id)
    client = quotation.client

    # Create a buffer for the PDF
    buffer = BytesIO()

    # Create the PDF object
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add company logo
    logo_path = seller.profile_picture.path if seller.profile_picture else 'media/profile_pics/logoU_0.25.png'  # Path to your logo
    logo = ImageReader(logo_path)
    p.drawImage(logo, 50, height - 150, width=200, height=100, preserveAspectRatio=True)

    # Add company information
    p.setFont("Helvetica-Bold", 16)
    p.drawString(260, height - 80, "My Company Name")
    p.setFont("Helvetica", 12)
    p.drawString(260, height - 100, "123 Business Street")
    p.drawString(260, height - 120, "City, State, ZIP Code")
    p.drawString(260, height - 140, "Phone: (123) 456-7890")
    p.drawString(260, height - 160, "Email: info@mycompany.com")

    # Add RFQ title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 200, "Request for Quotation (RFQ)")

    # Add client information
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 240, f"Client Name: {client.name}")
    p.drawString(50, height - 260, f"Email: {client.email}")
    p.drawString(50, height - 280, f"WhatsApp: {client.whatsapp}")
    p.drawString(50, height - 280, f" ")
    # Add product table
    data = [
        ["Product Name", "Quantity", "Unit Price", "Total Price"],   
    ]
    # Loop through only products with quantity > 0
    quotation_items = quotation.quotationproduct_set.filter(quantity__gt=0)
 
    for item in quotation_items:
        data.append([
            item.product.name, 
            str(item.quantity), 
            f"${item.product.price:.2f}", 
            f"${item.quantity * item.product.price:.2f}"
        ])
    data.append(["", "", "Total Amount", f"${quotation.total_amount:.2f}"])

    table = Table(data, colWidths=[200, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Draw the table on the PDF
    table.wrapOn(p, width - 100, height)
    table.drawOn(p, 50, height - 400)

    # Add a thank-you message
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 450, "Thank you for your request. We will get back to you shortly.")

    # Close the PDF object
    p.showPage()
    p.save()

    # File response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=RFQ_{client.name}.pdf'
    return response