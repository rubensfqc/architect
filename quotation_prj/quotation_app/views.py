from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO

def landing_page(request):
    if request.method == 'POST':
        # Save user details in session
        request.session['name'] = request.POST.get('name')
        request.session['email'] = request.POST.get('email')
        request.session['whatsapp'] = request.POST.get('whatsapp')
        return redirect('quotation_page')
    return render(request, "quotation_app/landing_page.html")

def quotation_page(request):
    if not request.session.get('name'):
        return redirect('landing_page')  # Redirect if user details are not set

    if request.method == 'POST':
        # Save quotation details in session
        request.session['quantity'] = request.POST.get('quantity')
        request.session['product'] = request.POST.get('product')
        return redirect('generate_pdf')

    return render(request, 'quotation_app/quotation_page.html')

def generate_pdf(request):
    if not request.session.get('name'):
        return redirect('landing_page')  # Redirect if user details are not set

    # Get session data
    name = request.session.get('name')
    email = request.session.get('email')
    whatsapp = request.session.get('whatsapp')
    quantity = request.session.get('quantity')
    product = request.session.get('product')

    # Create a PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Quotation for {name}")
    p.drawString(100, 730, f"Email: {email}")
    p.drawString(100, 710, f"WhatsApp: {whatsapp}")
    p.drawString(100, 690, f"Product: {product}")
    p.drawString(100, 670, f"Quantity: {quantity}")
    p.showPage()
    p.save()

    # Get the PDF content
    pdf = buffer.getvalue()
    buffer.close()

    # Return the PDF as a response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="quotation_{name}.pdf"'
    response.write(pdf)
    return response