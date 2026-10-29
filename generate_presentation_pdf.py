import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Brain Tumor Classification using CNN (DenseNet201) — Presentation & Viva Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "Confidential — Academic Project Presentation Reference")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 52, 558, 52)
        self.restoreState()

def build_pdf(filename="Brain_Tumor_Project_Presentation_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"),
        alignment=1, # Center
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=15,
        spaceAfter=4
    )

    script_quote = ParagraphStyle(
        'ScriptQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#EDF2F7"),
        borderColor=colors.HexColor("#4299E1"),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=4,
        spaceAfter=8
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#2D3748")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A365D")
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Brain Tumor Classification using CNN", title_style))
    story.append(Paragraph("Comprehensive Project Presentation & External Viva Examination Guide<br/><b>Architecture: DenseNet201 with Custom Transfer Learning Classifier</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=15))

    # Executive Overview
    story.append(Paragraph("1. Executive Project Summary", h1_style))
    story.append(Paragraph(
        "This project provides an automated, computer-aided diagnostic system to classify Magnetic Resonance Imaging (MRI) "
        "brain scans into four categories: three malignant/benign brain tumor types (<b>Glioma, Meningioma, Pituitary</b>) "
        "and a <b>No Tumor</b> healthy control group. By leveraging <b>Transfer Learning</b> with the <b>DenseNet201</b> architecture, "
        "the model achieves high diagnostic accuracy, mitigating the scarcity of specialized radiologists and providing rapid, objective second opinions.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Role Division Table
    story.append(Paragraph("2. 4-Member Team Role Division & Responsibilities", h1_style))
    role_data = [
        [Paragraph("Member", table_header), Paragraph("Presentation Topic", table_header), Paragraph("Key Responsibilities & Deliverables", table_header)],
        [Paragraph("Member 1", table_cell_bold), Paragraph("Introduction & Problem Statement", table_cell), Paragraph("What the project is, motivation, real-world clinical challenges, and project objectives.", table_cell)],
        [Paragraph("Member 2", table_cell_bold), Paragraph("Dataset & Image Preprocessing", table_cell), Paragraph("Dataset source, 4 tumor classes, image resizing (224x224), normalization, and data augmentation.", table_cell)],
        [Paragraph("Member 3", table_cell_bold), Paragraph("Deep Learning Architecture", table_cell), Paragraph("DenseNet201 backbone, feature reuse, custom classifier head (Flatten, Dense, Dropout, Softmax), loss function.", table_cell)],
        [Paragraph("Member 4", table_cell_bold), Paragraph("Live Implementation & Conclusion", table_cell), Paragraph("Demonstrating web app (Streamlit) and CLI, training curves analysis, metrics, and future scope.", table_cell)]
    ]
    t_roles = Table(role_data, colWidths=[65, 150, 289])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_roles)
    story.append(Spacer(1, 14))

    # Page Break for Detailed Presentation Scripts
    story.append(PageBreak())

    # Detailed Member Scripts
    story.append(Paragraph("3. Detailed Presentation Scripts (Member by Member)", h1_style))

    # Member 1
    story.append(Paragraph("Member 1: Project Overview & Motivation", h2_style))
    story.append(Paragraph("<b>Script to memorize & speak:</b>", body_style))
    story.append(Paragraph(
        "\"Good morning, respected teachers and external examiners. Our project is titled <b>Brain Tumor Classification using Deep Learning and CNN</b>. "
        "Brain tumors are among the most lethal neurological diseases. Every year, thousands of patients undergo MRI scans, but the manual analysis of these scans "
        "is time-consuming and subjective to human fatigue and inter-observer variability.<br/><br/>"
        "In developing regions, the acute shortage of trained neuro-radiologists causes significant diagnostic delays. Our primary goal was to engineer an automated, "
        "high-accuracy classification pipeline capable of identifying specific tumor categories within seconds, providing clinicians with a dependable diagnostic second opinion.\"",
        script_quote
    ))

    # Member 2
    story.append(Paragraph("Member 2: Dataset, Classes & Preprocessing Pipeline", h2_style))
    story.append(Paragraph("<b>Script to memorize & speak:</b>", body_style))
    story.append(Paragraph(
        "\"We utilized the benchmark Brain Tumor MRI dataset created by Sartaj Bhuvaji et al. The dataset comprises <b>3,264 MRI slices</b> divided into "
        "<b>2,870 training images</b> and <b>394 testing images</b> across four classes: <b>Glioma Tumor</b> (malignant brain tissue cancer), "
        "<b>Meningioma Tumor</b> (membrane-originating tumor), <b>Pituitary Tumor</b> (endocrine base tumor), and <b>No Tumor</b> (healthy scans).<br/><br/>"
        "Our preprocessing pipeline implements three critical steps:<br/>"
        "1. <b>Resizing:</b> Normalized all scan resolutions to 224x224 pixels with 3 channels.<br/>"
        "2. <b>Pixel Normalization:</b> Scaled pixel intensities by 1/255 into [0, 1] to accelerate gradient descent.<br/>"
        "3. <b>Data Augmentation:</b> Applied real-time shear, zoom (20%), and horizontal flips to prevent overfitting and ensure rotational invariance.\"",
        script_quote
    ))

    # Member 3
    story.append(Paragraph("Member 3: Deep Learning Engine & DenseNet201", h2_style))
    story.append(Paragraph("<b>Script to memorize & speak:</b>", body_style))
    story.append(Paragraph(
        "\"Rather than training a CNN from random weights on a modest medical dataset, we implemented <b>Transfer Learning</b> using <b>DenseNet201</b> pre-trained on ImageNet. "
        "In DenseNet, each layer receives feature maps from all prior layers, which resolves vanishing gradients, encourages feature reuse, and drastically reduces required parameters.<br/><br/>"
        "We froze the 201 base convolutional layers to preserve visual feature extraction, and added our custom top classifier:<br/>"
        "• <b>Flatten Layer:</b> Converts multidimensional feature maps into a 1D tensor.<br/>"
        "• <b>Dense Layer (256 units, ReLU):</b> Learns high-level tumor discrimination patterns.<br/>"
        "• <b>Dropout (0.3):</b> Randomly deactivates 30% of neurons to prevent co-adaptation.<br/>"
        "• <b>Dense Layer (4 units, Softmax):</b> Outputs normalized probabilities summing to 1.0 across the 4 classes.<br/>"
        "Trained using <b>Categorical Crossentropy loss</b> and <b>RMSprop optimizer</b> (LR = 0.00001).\"",
        script_quote
    ))

    # Member 4
    story.append(Paragraph("Member 4: Live Demonstration, Results & Future Scope", h2_style))
    story.append(Paragraph("<b>Script to memorize & speak:</b>", body_style))
    story.append(Paragraph(
        "\"For clinical deployment, we developed an interactive <b>Streamlit Web Application</b> and command-line interface. "
        "When an MRI scan is uploaded, our pipeline processes the image and returns the predicted diagnosis, confidence score, "
        "and a complete probability breakdown across all tumor types in under one second.<br/><br/>"
        "Our evaluation metrics demonstrate steady loss reduction and accuracy improvement, with model weights checkpointed into an HDF5 binary file (`densenet101.h5`).<br/>"
        "<b>Future Enhancements:</b> We plan to integrate <b>Grad-CAM visual heatmaps</b> to visually highlight tumor boundaries for explainable AI, "
        "and expand the model to handle multi-sequence 3D volumetric MRI scans.\"",
        script_quote
    ))

    # Page Break for Dataset & Tech Stack
    story.append(PageBreak())

    # Dataset Breakdown Table
    story.append(Paragraph("4. Dataset Class Distribution & Statistics", h1_style))
    dataset_data = [
        [Paragraph("Tumor Class", table_header), Paragraph("Clinical Origin & Characteristics", table_header), Paragraph("Training", table_header), Paragraph("Testing", table_header), Paragraph("Total", table_header)],
        [Paragraph("Glioma Tumor", table_cell_bold), Paragraph("Cancerous glial cells; infiltrative, requires aggressive treatment.", table_cell), Paragraph("826", table_cell), Paragraph("100", table_cell), Paragraph("926", table_cell)],
        [Paragraph("Meningioma", table_cell_bold), Paragraph("Arises from meninges membranes; mostly benign, slow growing.", table_cell), Paragraph("822", table_cell), Paragraph("115", table_cell), Paragraph("937", table_cell)],
        [Paragraph("Pituitary Tumor", table_cell_bold), Paragraph("Base skull adenoma affecting hormonal equilibrium.", table_cell), Paragraph("827", table_cell), Paragraph("74", table_cell), Paragraph("901", table_cell)],
        [Paragraph("No Tumor", table_cell_bold), Paragraph("Normal control brain scan without focal mass or edema.", table_cell), Paragraph("395", table_cell), Paragraph("105", table_cell), Paragraph("500", table_cell)],
        [Paragraph("<b>Total Dataset</b>", table_cell_bold), Paragraph("<b>Benchmark Dataset by Sartaj Bhuvaji et al.</b>", table_cell_bold), Paragraph("<b>2,870</b>", table_cell_bold), Paragraph("<b>394</b>", table_cell_bold), Paragraph("<b>3,264</b>", table_cell_bold)]
    ]
    t_dataset = Table(dataset_data, colWidths=[90, 244, 55, 55, 60])
    t_dataset.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F7FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#EDF2F7")),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_dataset)
    story.append(Spacer(1, 14))

    # Technology Stack Table
    story.append(Paragraph("5. Complete Technology Stack", h1_style))
    tech_data = [
        [Paragraph("Technology Layer", table_header), Paragraph("Tool / Library", table_header), Paragraph("Version", table_header), Paragraph("Role in System", table_header)],
        [Paragraph("Programming Language", table_cell_bold), Paragraph("Python", table_cell), Paragraph("3.11", table_cell), Paragraph("Core development and neural computation pipeline.", table_cell)],
        [Paragraph("Deep Learning Framework", table_cell_bold), Paragraph("TensorFlow", table_cell), Paragraph("2.21", table_cell), Paragraph("Backpropagation, tensor optimization, CPU computation.", table_cell)],
        [Paragraph("High-Level Neural API", table_cell_bold), Paragraph("Keras", table_cell), Paragraph("3.15", table_cell), Paragraph("Model architecture, layers (Dense, Dropout, Flatten).", table_cell)],
        [Paragraph("Transfer Learning Model", table_cell_bold), Paragraph("DenseNet201", table_cell), Paragraph("ImageNet", table_cell), Paragraph("201-layer deep feature extraction backbone.", table_cell)],
        [Paragraph("Web Application UI", table_cell_bold), Paragraph("Streamlit", table_cell), Paragraph("1.66", table_cell), Paragraph("Interactive front-end dashboard for real-time MRI upload.", table_cell)],
        [Paragraph("Image Processing", table_cell_bold), Paragraph("Pillow & Keras Preprocessing", table_cell), Paragraph("13.0", table_cell), Paragraph("Resizing, normalization, data augmentation generator.", table_cell)],
        [Paragraph("Numerical & Science", table_cell_bold), Paragraph("NumPy & SciPy", table_cell), Paragraph("2.4 / 1.17", table_cell), Paragraph("Tensor shaping, probability array parsing, math operations.", table_cell)],
        [Paragraph("Data Visualization", table_cell_bold), Paragraph("Matplotlib", table_cell), Paragraph("3.11", table_cell), Paragraph("Plotting training loss and validation accuracy curves.", table_cell)],
        [Paragraph("Model Checkpoint Format", table_cell_bold), Paragraph("HDF5 (.h5)", table_cell), Paragraph("Binary", table_cell), Paragraph("Stores 42.4M trained weights in densenet101.h5 (268 MB).", table_cell)],
    ]
    t_tech = Table(tech_data, colWidths=[120, 130, 54, 200])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)

    # Page Break for Implementation & Viva Q&A
    story.append(PageBreak())

    # VS Code Step-by-Step Live Execution Guide
    story.append(Paragraph("6. Step-by-Step VS Code Demonstration Walkthrough", h1_style))
    story.append(Paragraph("Follow these exact steps during your practical presentation:", body_style))
    
    steps = [
        ("Step 1: Open VS Code Terminal", "Press <b>Ctrl + ~</b> in VS Code to display the PowerShell terminal."),
        ("Step 2: Launch the Interactive Web App", "Execute: <code>.\\Brain-Tumar-classificaltion-using-CNN-main\\.venv\\Scripts\\python.exe -m streamlit run app.py</code><br/>Your browser will immediately open <b>http://localhost:8501</b>."),
        ("Step 3: Test Real MRI Scans Live", "Under the <b>Sample MRI Scans</b> dropdown in the left sidebar, choose <b>Glioma Tumor</b> or <b>No Tumor</b>.<br/>Show the examiner how the system instantly renders the predicted diagnosis, confidence percentage, and the probability breakdown across all 4 categories."),
        ("Step 4: Demonstrate Command-Line Prediction", "To demonstrate backend scripting, run in terminal:<br/><code>.\\Brain-Tumar-classificaltion-using-CNN-main\\.venv\\Scripts\\python.exe predict.py --image \"Brain-Tumar-classificaltion-using-CNN-main\\input\\brain-tumor-classification-mri\\Testing\\no_tumor\\image(10).jpg\"</code>"),
        ("Step 5: Show Model Architecture Code", "Open <b>train.py</b> and scroll to <b>build_model()</b> to explain the DenseNet201 base and custom Flatten -> Dense(256) -> Dropout(0.3) -> Dense(4, Softmax) head."),
        ("Step 6: Show Saved Artifacts", "Show <b>training_curves.png</b> for the accuracy/loss progression, and <b>models/densenet101.h5</b> (268 MB binary weight file).")
    ]

    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, bullet_style))

    story.append(Spacer(1, 10))

    # Top 10 Viva Questions & Answers
    story.append(Paragraph("7. External Examiner Viva Q&A Cheat Sheet", h1_style))
    
    viva_qa = [
        ("Q1: What is Transfer Learning and why did you use it?",
         "Transfer Learning reuses feature weights learned from a massive benchmark dataset (ImageNet with 1.4M images) as a foundation for a new, specialized task. This prevents overfitting on small medical datasets and drastically reduces training time."),
        
        ("Q2: Why DenseNet201 instead of standard CNNs like VGG16 or ResNet?",
         "DenseNet connects each layer to every subsequent layer in a feed-forward manner. This ensures maximum feature reuse, mitigates the vanishing gradient problem, and requires fewer parameters than ResNet or VGG while achieving superior accuracy."),
         
        ("Q3: Why Softmax activation for the output layer?",
         "Softmax normalizes the raw neural output logits into probability values between 0.0 and 1.0 that sum to exactly 1.0 (100%), which is mathematically required for mutually exclusive multi-class classification."),
         
        ("Q4: What is the function of Dropout (0.3)?",
         "Dropout randomly turns off 30% of neuron connections during each training forward-pass. This prevents neurons from co-adapting and memorizing the training images, directly curbing overfitting."),
         
        ("Q5: Why is the .h5 file not readable in a text editor?",
         "The .h5 (Hierarchical Data Format 5) file is a compiled binary array holding 42.4 million 32-bit floating-point numbers representing neural network weights and layer parameters. It is designed for high-speed numerical loading by TensorFlow, not text viewing."),
         
        ("Q6: Why is the input resolution 224 x 224 x 3?",
         "DenseNet201 was originally trained on ImageNet images of size 224x224x3. Retaining this resolution allows us to directly utilize its pre-trained convolutional filters without re-engineering spatial dimensions."),
         
        ("Q7: What is Categorical Crossentropy?",
         "It is the loss function used when true targets are one-hot encoded multi-class vectors. It measures the performance of a classification model whose output is a probability value between 0 and 1.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(f"<b>Answer:</b> <i>{a}</i>", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully created: {filename}")

if __name__ == "__main__":
    build_pdf()

