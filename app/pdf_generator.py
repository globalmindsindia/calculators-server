from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether,
    BaseDocTemplate,
    PageTemplate,
    Frame,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import os



def generate_cost_report_pdf(user_data, expenses, selected_country, answers):
    """Generate cost calculator PDF report matching original frontend design"""
    buffer = io.BytesIO()

    # --- CHANGED: use BaseDocTemplate instead of SimpleDocTemplate ---
    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.3 * inch,
        bottomMargin=0.5 * inch,
    )
    styles = getSampleStyleSheet()
    story = []

    # Colors matching original design
    primary_color = colors.HexColor("#e0f2fe")  # Hero gradient color
    light_blue = colors.HexColor("#f0f8ff")
    dark_gray = colors.HexColor("#2f4f4f")
    light_gray = colors.HexColor("#808080")
    accent_orange = colors.HexColor("#ff8c00")

    # Header with Logo on left and Addresses on right
    try:
        logo_path = os.path.join(
            os.path.dirname(__file__), "..", "static", "GMI_Logo.jpeg"
        )
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2 * inch, height=1 * inch)
        else:
            logo = Paragraph(
                "GMI LOGO",
                ParagraphStyle(
                    "LogoPlaceholder", fontSize=12, textColor=primary_color
                ),
            )
    except:
        logo = Paragraph(
            "GMI LOGO",
            ParagraphStyle("LogoPlaceholder", fontSize=12, textColor=primary_color),
        )

    # Create header table with logo left, addresses right
    office_style = ParagraphStyle(
        "OfficeStyle",
        fontSize=9,
        textColor=colors.HexColor("#223877"),
        fontName="Helvetica-Bold",
        alignment=TA_RIGHT,
    )

    address_style = ParagraphStyle(
        "AddressStyle",
        fontSize=8,
        textColor=colors.HexColor("#223877"),
        fontName="Helvetica",
        alignment=TA_RIGHT,
    )

    # Addresses formatted for right side
    addresses = [
        Paragraph("Corporate Office - India", office_style),
        Paragraph("23, CJ VenkataDas road", address_style),
        Paragraph(" Padmanabhanagar, Bangalore", address_style),
        Spacer(1, 3),
        Paragraph("Overseas Office - Germany", office_style),
        Paragraph("Koenigsheideweg Berlin, Germany", address_style),
    ]

    # Create table with logo left, addresses right
    header_data = [[logo, addresses]]
    header_table = Table(header_data, colWidths=[3 * inch, 4 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 25))

    # Main Header Strip
    header_strip = Table(
        [["Study Abroad Cost Calculator Report"]], colWidths=[7 * inch]
    )
    header_strip.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 24),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(header_strip)

    # Subtitle
    subtitle_strip = Table(
        [[f"Personalized Cost Breakdown for {selected_country}"]], colWidths=[7 * inch]
    )
    subtitle_strip.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 14),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(subtitle_strip)
    story.append(Spacer(1, 30))

    # User details table (without "Report Details" header)
    user_details = [
        [
            f'Name: {user_data.get("name", "N/A")}',
            f'Phone: {user_data.get("phone", "N/A")}',
        ],
        [
            f'Email: {user_data.get("email", "N/A")}',
            f'Date: {datetime.now().strftime("%B %d, %Y")}',
        ],
    ]

    user_table = Table(user_details, colWidths=[3.5 * inch, 3.5 * inch])
    user_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), dark_gray),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )
    story.append(user_table)
    story.append(Spacer(1, 30))

    # Total Cost Highlight
    total_cost_table = Table(
        [[f'Total Monthly Cost: EUR {expenses.get("total", 0):,}']],
        colWidths=[7 * inch],
    )
    total_cost_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 18),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(total_cost_table)
    story.append(Spacer(1, 30))

    # Monthly Expense Breakdown
    breakdown_title = Paragraph(
        "Monthly Expense Breakdown",
        ParagraphStyle(
            "BreakdownTitle",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=dark_gray,
            spaceAfter=10,
        ),
    )
    story.append(breakdown_title)

    expense_data = [["Category", "Amount (EUR)"]]
    expense_items = [
        ("Accommodation", expenses.get("accommodation", 0)),
        ("Food & Dining", expenses.get("food", 0)),
        ("Transportation", expenses.get("transport", 0)),
        ("Leisure & Entertainment", expenses.get("leisure", 0)),
        ("Mobile & Internet", expenses.get("mobile", 0)),
        ("Miscellaneous", expenses.get("miscellaneous", 0)),
    ]

    for item, amount in expense_items:
        expense_data.append([item, f"EUR {amount:,}"])

    expense_table = Table(expense_data, colWidths=[4 * inch, 2 * inch])
    expense_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#223877")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 11),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(expense_table)

    # --- REMOVED: explicit PageBreak and big spacer ---
    # story.append(PageBreak())
    # story.append(Spacer(1, 380))

    # Footer disclaimer
    disclaimer_data = [
        [
            "This report is based on average costs and your selected preferences.\n"
            "Actual costs may vary depending on lifestyle and location within the country.\n"
            "Generated by Study Abroad Cost Calculator Tool"
        ]
    ]

    disclaimer_table = Table(disclaimer_data, colWidths=[7 * inch])
    disclaimer_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 0), (-1, -1), light_gray),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )

    # Contact footer
    contact_data = [
        [
            "Feel free to contact for any Clarification\n"
            "Phone: +91 7353446655 | Phone: +91 9071331230 | Email: connect@globalmindsindia.com"
        ]
    ]

    contact_table = Table(contact_data, colWidths=[7 * inch])
    contact_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )

    # --- NEW: put disclaimer + contact into a separate footer frame on page 1 ---

    def first_page_footer(canvas, doc_):
        canvas.saveState()
        # Build the footer flowables into the footer frame
        from reportlab.platypus import Frame, PageTemplate

        footer_story = [disclaimer_table, Spacer(1, 10), contact_table]

        # Footer frame dimensions: full width, fixed height at bottom
        footer_frame = Frame(
            doc_.leftMargin,
            doc_.bottomMargin,  # y from bottom
            doc_.width,
            2.0 * inch,  # height for footer block
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
            showBoundary=0,
        )
        footer_frame.addFromList(footer_story, canvas)
        canvas.restoreState()

    # Main frame for normal content (everything in `story`)
    main_frame = Frame(
        doc.leftMargin,
        doc.bottomMargin + 2.0 * inch,  # leave space for footer block
        doc.width,
        doc.height - 2.0 * inch,
        leftPadding=0,
        bottomPadding=0,
        rightPadding=0,
        topPadding=0,
        showBoundary=0,
    )

    # Page template with custom footer for first page
    first_page_template = PageTemplate(
        id="FirstPage", frames=[main_frame], onPage=first_page_footer
    )
    doc.addPageTemplates([first_page_template])

    # Build PDF (story contains main content; footer drawn via onPage)
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_custom_package_pdf(user_data, selected_packages, total_cost):
    """Generate custom package PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, topMargin=0.3 * inch, bottomMargin=0.5 * inch
    )
    styles = getSampleStyleSheet()
    story = []

    # Colors matching original design
    primary_color = colors.HexColor("#e0f2fe")  # Hero gradient color
    dark_gray = colors.HexColor("#2f4f4f")
    light_gray = colors.HexColor("#808080")

    # Calculate total from selected_buckets using backend pricing
    selected_buckets = user_data.get('selected_buckets', [])
    bucket_costs = {
        'Bucket-1': 1500, 'Bucket-2': 75000, 'Bucket-3': 21000,
        'Bucket-4': 75000, 'Bucket-5': 125000, 'Bucket-6': 100000, 'Bucket-7': 80000
    }
    calculated_total = sum(bucket_costs.get(bucket, 0) for bucket in selected_buckets)
    
    print(f"DEBUG PDF: Selected buckets: {selected_buckets}")
    print(f"DEBUG PDF: Calculated total: {calculated_total}")
    
    # Use package_details for content
    package_details = user_data.get('package_details', [])
    print(f"DEBUG PDF: Package details count: {len(package_details)}")

    # Header with Logo on left and Addresses on right
    try:
        logo_path = os.path.join(
            os.path.dirname(__file__), "..", "static", "GMI_Logo.jpeg"
        )
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2 * inch, height=1 * inch)
        else:
            logo = Paragraph(
                "GMI LOGO",
                ParagraphStyle(
                    "LogoPlaceholder", fontSize=12, textColor=primary_color
                ),
            )
    except:
        logo = Paragraph(
            "GMI LOGO",
            ParagraphStyle("LogoPlaceholder", fontSize=12, textColor=primary_color),
        )

    # Create header table with logo left, addresses right
    # CHANGED: textColor for office_style and address_style
    office_style = ParagraphStyle(
        "OfficeStyle",
        fontSize=9,
        textColor=colors.HexColor("#223877"),  # changed from primary_color
        fontName="Helvetica-Bold",
        alignment=TA_RIGHT,
    )

    address_style = ParagraphStyle(
        "AddressStyle",
        fontSize=8,
        textColor=colors.HexColor("#223877"),  # changed from dark_gray
        fontName="Helvetica",
        alignment=TA_RIGHT,
    )

    # Addresses formatted for right side
    addresses = [
        Paragraph("Corporate Office - India", office_style),
        Paragraph("23, CJ VenkataDas road", address_style),
        Paragraph(" Padmanabhanagar, Bangalore", address_style),
        Spacer(1, 3),
        Paragraph("Overseas Office - Germany", office_style),
        Paragraph("Koenigsheideweg Berlin, Germany", address_style),
    ]

    # Create table with logo left, addresses right
    header_data = [[logo, addresses]]
    header_table = Table(header_data, colWidths=[3 * inch, 4 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 25))

    # Main Header Strip
    header_strip = Table(
        [["Custom Study Abroad Package Report"]], colWidths=[7 * inch]
    )
    header_strip.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 24),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(header_strip)

    # Subtitle
    subtitle_strip = Table([["Personalized Package Selection"]], colWidths=[7 * inch])
    subtitle_strip.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 14),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(subtitle_strip)
    story.append(Spacer(1, 30))

    # User details table
    user_details = [
        [
            f'Name: {user_data.get("name", "N/A")}',
            f'Phone: {user_data.get("phone", "N/A")}',
        ],
        [
            f'Email: {user_data.get("email", "N/A")}',
            f'Date: {datetime.now().strftime("%B %d, %Y")}',
        ],
    ]

    user_table = Table(user_details, colWidths=[3.5 * inch, 3.5 * inch])
    user_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), dark_gray),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )
    story.append(user_table)
    story.append(Spacer(1, 30))

    # Total Cost Highlight - use calculated total
    total_cost_table = Table(
        [[f"Total Package Cost: Rs {calculated_total:,} (Indian Rupees)"]],
        colWidths=[7 * inch],
    )
    total_cost_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 18),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(total_cost_table)
    story.append(Spacer(1, 30))

    # Selected Packages Section
    packages_title = Paragraph(
        "Selected Services & Packages",
        ParagraphStyle(
            "PackagesTitle",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=dark_gray,
            spaceAfter=10,
        ),
    )
    story.append(packages_title)

    # Show selected packages with correct content from package_details
    for i, package in enumerate(package_details, 1):
        # Package header
        header_style = ParagraphStyle(
            "PackageHeader",
            fontSize=12,
            textColor=dark_gray,
            fontName="Helvetica-Bold",
            leftIndent=10,
            rightIndent=10,
            spaceAfter=8,
            backColor=colors.HexColor("#e5e7eb"),
            borderPadding=8,
        )
        story.append(Paragraph(f"{i}. {package.get('name', 'Unknown').upper()}", header_style))

        # Package description
        desc_style = ParagraphStyle(
            "PackageDesc",
            fontSize=10,
            textColor=light_gray,
            fontName="Helvetica-Oblique",
            leftIndent=10,
            rightIndent=10,
            spaceAfter=6,
        )
        story.append(Paragraph(package.get('description', 'No description available'), desc_style))

        # Features header
        features_header = Paragraph(
            "Included Services:",
            ParagraphStyle(
                "FeaturesHeader",
                fontSize=10,
                textColor=dark_gray,
                fontName="Helvetica-Bold",
                leftIndent=10,
                spaceAfter=4,
            ),
        )
        story.append(features_header)

        # Features list
        for feature in package.get('features', []):
            feature_style = ParagraphStyle(
                "FeatureItem",
                fontSize=9,
                textColor=light_gray,
                fontName="Helvetica",
                leftIndent=20,
                rightIndent=10,
                spaceAfter=3,
            )
            story.append(Paragraph(f"• {feature}", feature_style))

        story.append(Spacer(1, 12))

    # Add minimal spacer before footer
    story.append(Spacer(1, 100))

    # Footer disclaimer
    disclaimer_data = [
        [
            "This report shows your selected packages and estimated costs.\n"
            "Final pricing may vary based on current market rates and specific requirements.\n"
            "Generated by Custom Package Selection Tool"
        ]
    ]

    disclaimer_table = Table(disclaimer_data, colWidths=[7 * inch])
    disclaimer_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 0), (-1, -1), light_gray),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )
    story.append(disclaimer_table)
    story.append(Spacer(1, 8))

    # Contact footer
    contact_data = [
        [
            "Feel free to contact for any Clarification\n"
            "Phone: +91 7353446655 | Phone: +91 9071331230 | Email: connect@globalmindsindia.com"
        ]
    ]

    # CHANGED: textColor for footer to match header blue
    contact_table = Table(contact_data, colWidths=[7 * inch])
    contact_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#223877")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )
    story.append(contact_table)

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_grade_certificate_pdf(user_data, grade_data):
    """Generate grade certificate PDF matching exact frontend design from LetterHead.tsx"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch
    )
    styles = getSampleStyleSheet()
    story = []

    # Colors matching frontend
    primary_color = colors.HexColor("#223877")  # Primary blue
    muted_color = colors.HexColor("#6b7280")  # Muted gray

    # Header section with logo and title (matching frontend header)
    try:
        logo_path = os.path.join(
            os.path.dirname(__file__), "..", "static", "GMI_Logo.jpeg"
        )
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2.5 * inch, height=1.25 * inch)  # Increased width
        else:
            logo = Paragraph(
                "GMI LOGO",
                ParagraphStyle("LogoPlaceholder", fontSize=12, textColor=colors.white),
            )
    except:
        logo = Paragraph(
            "GMI LOGO",
            ParagraphStyle("LogoPlaceholder", fontSize=12, textColor=colors.white),
        )

    # Header with gradient background (matching Hero.tsx)
    hero_gradient_start = colors.HexColor(
        "#e0f2fe"
    )  # HSL(210 100% 96%) converted to hex
    hero_gradient_end = colors.HexColor("#bae6fd")  # HSL(210 80% 92%) converted to hex

    header_data = [
        [logo],
        ["Grade Conversion Certificate"],
        ["Official German Grade Conversion"],
    ]

    header_table = Table(header_data, colWidths=[7 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), hero_gradient_start),  # Use hero gradient color
                ("TEXTCOLOR", (0, 0), (-1, -1), primary_color),  # Change text to primary color
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 1), (0, 1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 1), (0, 1), 20),
                ("FONTNAME", (0, 2), (0, 2), "Helvetica"),
                ("FONTSIZE", (0, 2), (0, 2), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 30))

    # Main grade result with increased spacing
    german_grade = grade_data.get("german_grade", "N/A")
    grade_result = Paragraph(
        f"Your German Grade: {german_grade}",
        ParagraphStyle(
            "GradeResult",
            fontSize=24,
            fontName="Helvetica-Bold",
            textColor=primary_color,
            alignment=TA_CENTER,
            spaceAfter=30,
        ),
    )
    story.append(grade_result)

    # Subtitle with proper spacing
    subtitle = Paragraph(
        "Based on the German grading system (1.0 - 4.0 scale)",
        ParagraphStyle(
            "Subtitle",
            fontSize=12,
            textColor=muted_color,
            alignment=TA_CENTER,
            spaceAfter=30,
        ),
    )
    story.append(subtitle)

    # Conversion Details section (center the header)
    details_title = Paragraph(
        "Conversion Details",
        ParagraphStyle(
            "DetailsTitle",
            fontSize=16,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
            spaceAfter=15,
        ),
    )
    story.append(details_title)

    # Grade details in 2x2 grid (fix data mapping)
    grade_details = [
        [
            f"Maximum Grade\n{grade_data.get('best_grade', 'N/A')}",
            f"Minimum Passing\n{grade_data.get('min_passing_grade', 'N/A')}",
        ],
        [
            f"Your Grade\n{grade_data.get('your_grade', 'N/A')}",
            f"German Equivalent\n{german_grade}",
        ],
    ]

    details_table = Table(grade_details, colWidths=[3.5 * inch, 3.5 * inch])
    details_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (1, 0), colors.white),
                ("BACKGROUND", (0, 1), (0, 1), colors.white),
                (
                    "BACKGROUND",
                    (1, 1),
                    (1, 1),
                    colors.HexColor("#e0f2fe"),
                ),  # Light blue for German grade
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )
    story.append(details_table)
    story.append(Spacer(1, 30))

    # German Grading Scale Reference (center the header)
    scale_title = Paragraph(
        "German Grading Scale Reference",
        ParagraphStyle(
            "ScaleTitle",
            fontSize=14,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
    )
    story.append(scale_title)

    scale_data = [
        ["1.0 - 1.5", "Very Good (Sehr gut)"],
        ["1.6 - 2.5", "Good (Gut)"],
        ["2.6 - 3.5", "Satisfactory (Befriedigend)"],
        ["3.6 - 4.0", "Sufficient (Ausreichend)"],
    ]

    scale_table = Table(scale_data, colWidths=[1.5 * inch, 3 * inch])
    scale_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fef3c7")),  # Light yellow
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ]
        )
    )
    story.append(scale_table)
    story.append(Spacer(1, 30))

    # About This Conversion (center the header)
    about_title = Paragraph(
        "About This Conversion",
        ParagraphStyle(
            "AboutTitle",
            fontSize=14,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
    )
    story.append(about_title)

    about_text = Paragraph(
        "This conversion uses the official German grade conversion formula as recognized by German universities. "
        "The certificate can be used for university applications and official documentation.",
        ParagraphStyle(
            "AboutText",
            fontSize=10,
            textColor=muted_color,
            alignment=TA_CENTER,
            spaceAfter=30,
        ),
    )
    story.append(about_text)

    # Contact footer
    contact_footer = Paragraph(
        "Feel free to contact for any Clarification<br/>"
        "Customer Care Number: +91 7353446655 | Email: connect@globalmindsindia.com",
        ParagraphStyle(
            "ContactFooter",
            fontSize=10,
            fontName="Helvetica-Bold",
            textColor=primary_color,
            alignment=TA_CENTER,
        ),
    )
    story.append(contact_footer)

    doc.build(story)
    buffer.seek(0)
    return buffer
