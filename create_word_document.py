import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_guide():
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("Brain Tumor Classification using CNN (DenseNet201)\n")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(26, 54, 93)

    run_sub = p_title.add_run("Complete Oral Learning, Presentation & External Viva Guide\n(Prepared for 4-Member Project Team)")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(74, 85, 104)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 1: ROLE DIVISION
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. 4-Member Team Role Division (Who Speaks What)", level=1)
    h1.runs[0].font.color.rgb = RGBColor(26, 54, 93)

    table1 = doc.add_table(rows=1, cols=3)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.autofit = False

    col_widths = [Inches(1.2), Inches(2.2), Inches(3.6)]
    hdr_cells = table1.rows[0].cells
    headers = ["Member", "Presentation Topic", "Key Responsibilities"]
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(hdr_cells[i], "1A365D")

    roles = [
        ("Member 1", "Introduction & Problem Statement", "What the project is, motivation, clinical problems, and project goals."),
        ("Member 2", "Dataset & Preprocessing Pipeline", "Dataset source, 4 tumor classes, resizing (224x224), normalization, augmentation."),
        ("Member 3", "Deep Learning Architecture", "DenseNet201, Transfer Learning, custom layers (Flatten, Dense, Dropout, Softmax)."),
        ("Member 4", "Live Demonstration & Future Scope", "Running the web app demo, evaluation curves, saved .h5 model, conclusion.")
    ]

    for mem, topic, resp in roles:
        row_cells = table1.add_row().cells
        row_cells[0].text = mem
        row_cells[0].paragraphs[0].runs[0].font.bold = True
        row_cells[1].text = topic
        row_cells[2].text = resp

    for row in table1.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = w

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 2: WORD-FOR-WORD PRESENTATION SCRIPTS
    # -------------------------------------------------------------
    h2 = doc.add_heading("2. Exact Word-for-Word Speaking Scripts", level=1)
    h2.runs[0].font.color.rgb = RGBColor(26, 54, 93)

    # Member 1
    m1_h = doc.add_heading("👤 Member 1: Introduction, Problem Statement & Objectives", level=2)
    m1_h.runs[0].font.color.rgb = RGBColor(43, 108, 176)
    p_m1 = doc.add_paragraph()
    p_m1.add_run("WHAT TO SAY (Memorize & Speak):\n").bold = True
    p_m1_script = doc.add_paragraph(
        "\"Good morning, respected teachers and external examiners. Our project is titled 'Brain Tumor Classification using Deep Learning and CNN'. "
        "It is an automated diagnostic system that takes a brain MRI scan image as input and accurately detects whether a tumor is present, and if present, classifies its exact clinical type.\n\n"
        "Brain tumors are among the most lethal neurological diseases. In traditional medical practice, radiologists analyze hundreds of MRI scan slices manually. "
        "This manual process has two major limitations: it is time-consuming (causing diagnostic delays in critical cases), and it is prone to human error, especially in rural clinics where specialized neuro-radiologists are unavailable.\n\n"
        "Our primary objective was to build an automated, deep learning system using Transfer Learning to provide doctors with a reliable, second-opinion diagnostic tool in under 1 second.\""
    )
    p_m1_script.paragraph_format.left_indent = Inches(0.3)
    p_m1_script.paragraph_format.right_indent = Inches(0.3)
    p_m1_script.runs[0].font.italic = True

    # Member 2
    m2_h = doc.add_heading("👤 Member 2: Dataset, Classes & Image Preprocessing", level=2)
    m2_h.runs[0].font.color.rgb = RGBColor(43, 108, 176)
    p_m2 = doc.add_paragraph()
    p_m2.add_run("WHAT TO SAY (Memorize & Speak):\n").bold = True
    p_m2_script = doc.add_paragraph(
        "\"For training and evaluating our model, we used the benchmark Brain Tumor Classification MRI dataset curated by Sartaj Bhuvaji on Kaggle. "
        "It contains 3,264 MRI images organized into a Training set (2,870 images) and a Testing set (394 images).\n\n"
        "The dataset covers 4 distinct categories:\n"
        "1. Glioma Tumor: Cancerous tumors originating in the glial tissue of the brain.\n"
        "2. Meningioma Tumor: Slow-growing, mostly benign tumors arising from brain membranes.\n"
        "3. Pituitary Tumor: Abnormal growths at the base of the skull in the pituitary gland.\n"
        "4. No Tumor: Healthy brain MRI scans with no tumor tissue.\n\n"
        "Before feeding images into our neural network, we applied three vital preprocessing steps:\n"
        "• Resizing: Standardized all scans to 224 x 224 pixels with 3 RGB channels.\n"
        "• Normalization: Divided pixel values by 255.0 to scale them into [0, 1] for faster gradient convergence.\n"
        "• Data Augmentation: Applied zoom (20%), shear (20%), and horizontal flips to prevent overfitting and help the model generalize.\""
    )
    p_m2_script.paragraph_format.left_indent = Inches(0.3)
    p_m2_script.paragraph_format.right_indent = Inches(0.3)
    p_m2_script.runs[0].font.italic = True

    # Member 3
    m3_h = doc.add_heading("👤 Member 3: Deep Learning Architecture & DenseNet201", level=2)
    m3_h.runs[0].font.color.rgb = RGBColor(43, 108, 176)
    p_m3 = doc.add_paragraph()
    p_m3.add_run("WHAT TO SAY (Memorize & Speak):\n").bold = True
    p_m3_script = doc.add_paragraph(
        "\"We implemented Transfer Learning using the DenseNet201 (Densely Connected Convolutional Network) architecture pre-trained on ImageNet.\n\n"
        "Why DenseNet201? In traditional CNNs, layers connect only sequentially. In DenseNet, each layer receives feature maps from all preceding layers. "
        "This completely eliminates the vanishing gradient problem, promotes feature reuse, and yields superior accuracy with fewer parameters.\n\n"
        "Architecture of our custom classifier head:\n"
        "1. Frozen Base: We set layer.trainable = False on the DenseNet201 backbone to retain ImageNet feature extractors.\n"
        "2. Flatten Layer: Converts 2D feature maps into a 1D feature tensor.\n"
        "3. Dense Layer (256 neurons, ReLU): Learns high-level tumor discrimination patterns.\n"
        "4. Dropout (0.3): Deactivates 30% of neurons during training to prevent overfitting.\n"
        "5. Output Dense Layer (4 neurons, Softmax): Outputs probability distribution summing to 1.0 across all 4 classes.\n\n"
        "The model is compiled with Categorical Crossentropy loss and the RMSprop optimizer (learning rate = 0.00001).\""
    )
    p_m3_script.paragraph_format.left_indent = Inches(0.3)
    p_m3_script.paragraph_format.right_indent = Inches(0.3)
    p_m3_script.runs[0].font.italic = True

    # Member 4
    m4_h = doc.add_heading("👤 Member 4: Live Demonstration, Results & Future Scope", level=2)
    m4_h.runs[0].font.color.rgb = RGBColor(43, 108, 176)
    p_m4 = doc.add_paragraph()
    p_m4.add_run("WHAT TO SAY (Memorize & Speak):\n").bold = True
    p_m4_script = doc.add_paragraph(
        "\"For clinical demonstration, we developed a user-friendly Streamlit web interface and a command-line script. "
        "When an MRI scan is loaded, our model performs inference in under 1 second, outputting the predicted diagnosis, confidence percentage, and a full probability distribution bar chart.\n\n"
        "Our training curves (training_curves.png) demonstrate consistent loss reduction and steady accuracy improvement. "
        "The final trained model weights are saved in HDF5 binary format (densenet101.h5, 268 MB) containing 42.4 million parameters.\n\n"
        "Future Scope:\n"
        "1. Incorporating Grad-CAM heatmaps to visually highlight the tumor boundary for explainable AI.\n"
        "2. Extending the architecture to process 3D volumetric MRI slices.\n"
        "3. Integration into hospital PACS (Picture Archiving and Communication Systems) and mobile tablet apps for bedside consultation.\""
    )
    p_m4_script.paragraph_format.left_indent = Inches(0.3)
    p_m4_script.paragraph_format.right_indent = Inches(0.3)
    p_m4_script.runs[0].font.italic = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 3: DATASET & TECH STACK TABLES
    # -------------------------------------------------------------
    h3 = doc.add_heading("3. Dataset Class Distribution & Statistics", level=1)
    h3.runs[0].font.color.rgb = RGBColor(26, 54, 93)

    t_data = doc.add_table(rows=1, cols=4)
    t_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    d_hdr = t_data.rows[0].cells
    d_hdr_titles = ["Class Name", "Training Scans", "Testing Scans", "Total Scans"]
    for i, title in enumerate(d_hdr_titles):
        d_hdr[i].text = title
        d_hdr[i].paragraphs[0].runs[0].font.bold = True
        d_hdr[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(d_hdr[i], "1A365D")

    ds_rows = [
        ("Glioma Tumor", "826", "100", "926"),
        ("Meningioma Tumor", "822", "115", "937"),
        ("Pituitary Tumor", "827", "74", "901"),
        ("No Tumor (Healthy)", "395", "105", "500"),
        ("TOTAL DATASET", "2,870", "394", "3,264")
    ]
    for r in ds_rows:
        row_c = t_data.add_row().cells
        for idx, val in enumerate(r):
            row_c[idx].text = val
            if r[0] == "TOTAL DATASET":
                row_c[idx].paragraphs[0].runs[0].font.bold = True
                set_cell_background(row_c[idx], "EDF2F7")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    h4 = doc.add_heading("4. Technology Stack Overview", level=1)
    h4.runs[0].font.color.rgb = RGBColor(26, 54, 93)

    t_tech = doc.add_table(rows=1, cols=3)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    th_cells = t_tech.rows[0].cells
    th_titles = ["Category", "Technology / Framework", "Role in Project"]
    for i, title in enumerate(th_titles):
        th_cells[i].text = title
        th_cells[i].paragraphs[0].runs[0].font.bold = True
        th_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(th_cells[i], "1A365D")

    tech_rows = [
        ("Programming Language", "Python 3.11", "Primary language for pipeline and deep learning modeling."),
        ("Deep Learning Framework", "TensorFlow 2.21 & Keras 3.15", "Neural network creation, layers, optimization, callbacks."),
        ("Pretrained Model", "DenseNet201 (ImageNet)", "201-layer transfer learning feature extraction backbone."),
        ("Web Dashboard UI", "Streamlit 1.66", "Interactive web application for uploading and classifying scans."),
        ("Image Processing", "Pillow (PIL) & Keras Preprocessing", "Image resizing to 224x224, pixel normalization, data augmentation."),
        ("Numerical Computing", "NumPy & SciPy", "Array manipulation, matrix operations, probability sorting (argmax)."),
        ("Data Visualization", "Matplotlib 3.11", "Plotting training vs. validation loss and accuracy curves."),
        ("Model Checkpoint Format", "HDF5 (.h5 binary)", "Stores 42.4M trained weights in densenet101.h5 (268 MB).")
    ]
    for cat, tech, role in tech_rows:
        rc = t_tech.add_row().cells
        rc[0].text = cat
        rc[0].paragraphs[0].runs[0].font.bold = True
        rc[1].text = tech
        rc[2].text = role

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 4: STEP-BY-STEP LIVE DEMO GUIDE
    # -------------------------------------------------------------
    h5 = doc.add_heading("5. Step-by-Step Live Implementation Guide (VS Code)", level=1)
    h5.runs[0].font.color.rgb = RGBColor(26, 54, 93)

    steps = [
        ("Step 1: Open VS Code Terminal", "Press Ctrl + ~ in VS Code to open the terminal."),
        ("Step 2: Launch the Web App", "Run run_app.bat by double-clicking it or execute in terminal:\n.\\Brain-Tumar-classificaltion-using-CNN-main\\.venv\\Scripts\\python.exe -m streamlit run app.py\nThis opens http://localhost:8501 in your browser."),
        ("Step 3: Test Real MRI Scans", "Under 'Choose a sample MRI:' in the sidebar, select 'Glioma Tumor' or 'No Tumor'.\nShow how the system instantly outputs the Diagnosis banner, Confidence percentage, and Probability distribution bars across all 4 classes."),
        ("Step 4: Run Terminal Prediction Script", "To demonstrate backend code, run:\n.\\Brain-Tumar-classificaltion-using-CNN-main\\.venv\\Scripts\\python.exe predict.py --image \"Brain-Tumar-classificaltion-using-CNN-main\\input\\brain-tumor-classification-mri\\Testing\\no_tumor\\image(10).jpg\"\nIt will output: Predicted Diagnosis: NO TUMOR with confidence and exact probabilities."),
        ("Step 5: Show the Model Code", "Open train.py and scroll to build_model() to show the DenseNet201 base, frozen layers, Flatten, Dense(256), Dropout(0.3), and Dense(4, softmax) layers."),
        ("Step 6: Show Training Curves & Weights", "Open training_curves.png to show loss/accuracy curves, and point to models/densenet101.h5 (268 MB).")
    ]

    for title, desc in steps:
        p_step = doc.add_paragraph()
        p_step.add_run(f"• {title}: ").bold = True
        p_step.add_run(desc)
        p_step.paragraph_format.left_indent = Inches(0.2)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 5: EXTERNAL EXAMINER VIVA Q&A
    # -------------------------------------------------------------
    h6 = doc.add_heading("6. External Examiner Viva Q&A Cheat Sheet", level=1)
    h6.runs[0].font.color.rgb = RGBColor(26, 54, 93)

    viva = [
        ("Q1: What is Transfer Learning?",
         "Transfer Learning means taking a network that was already trained on a massive dataset (like ImageNet with 1.4 million images) and fine-tuning it for our specialized medical task. This eliminates the need for millions of medical images and saves days of GPU training time."),
        ("Q2: Why DenseNet201 over VGG16 or ResNet50?",
         "DenseNet connects each layer to every other layer in a feed-forward manner. This allows maximum feature reuse, avoids vanishing gradients, and requires fewer parameters than ResNet or VGG while achieving higher accuracy."),
        ("Q3: Why Softmax activation at the output?",
         "Softmax converts the model's raw numerical outputs into probability values between 0.0 and 1.0 that sum up to exactly 1.0 (100%). This is required for mutually exclusive multi-class classification."),
        ("Q4: What is the purpose of Dropout (0.3)?",
         "Dropout randomly turns off 30% of neurons during each training step. This forces the remaining neurons to learn independent features and prevents the model from overfitting or memorizing the training data."),
        ("Q5: Why is the .h5 file not displayed in a text editor?",
         "The .h5 (Hierarchical Data Format 5) file is a compiled binary file containing 42.4 million 32-bit floating-point numbers representing the neural network's weights and biases. It cannot be opened as text; it is loaded directly into RAM by TensorFlow."),
        ("Q6: What is the difference between Glioma and Meningioma?",
         "Gliomas originate inside the brain from glial cells and are often malignant (cancerous). Meningiomas originate from the meninges (the membranes covering the brain) and are mostly benign (non-cancerous) and slow-growing."),
        ("Q7: Why normalize pixel values by 1/255?",
         "Raw image pixels have integer values from 0 to 255. Dividing by 255.0 scales them into the floating-point range [0.0, 1.0]. This prevents large weight updates, stabilizing gradient descent during training.")
    ]

    for q, a in viva:
        p_q = doc.add_paragraph()
        p_q.add_run(f"{q}\n").bold = True
        p_ans = p_q.add_run(f"Answer: {a}")
        p_ans.font.italic = True
        p_q.paragraph_format.left_indent = Inches(0.2)
        p_q.paragraph_format.space_after = Pt(6)

    doc.save("Brain_Tumor_Presentation_and_Viva_Guide.docx")
    print("Created Word Document: Brain_Tumor_Presentation_and_Viva_Guide.docx")

if __name__ == "__main__":
    create_guide()

