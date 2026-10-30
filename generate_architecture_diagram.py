import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_system_architecture(output_path="system_architecture.png"):
    # High-resolution figure with professional 16:9 widescreen ratio
    fig, ax = plt.subplots(figsize=(16, 8.5), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Background color
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Main Header
    ax.text(8.0, 8.4, "Brain Tumor Classification System Architecture", 
            ha='center', va='center', fontsize=22, fontweight='bold', color='#1E293B', fontfamily='sans-serif')
    ax.text(8.0, 7.95, "End-to-End Deep Transfer Learning Pipeline using DenseNet201", 
            ha='center', va='center', fontsize=13, color='#64748B', fontfamily='sans-serif')

    # Stage Box Dimensions
    box_w = 2.4
    box_h = 4.8
    y_pos = 2.4

    # Stages data definition
    stages = [
        {
            "num": "Stage 1",
            "title": "Input MRI Scan",
            "x": 0.8,
            "header_color": "#0284C7",
            "bg_color": "#F0F9FF",
            "border_color": "#0284C7",
            "items": [
                "• Brain MRI Scans",
                "• Axial / Coronal slices",
                "• Formats: JPG / PNG",
                "• 4 Diagnostic Classes:",
                "   - Glioma Tumor",
                "   - Meningioma",
                "   - Pituitary Tumor",
                "   - No Tumor (Control)"
            ]
        },
        {
            "num": "Stage 2",
            "title": "Preprocessing &\nAugmentation",
            "x": 3.8,
            "header_color": "#0D9488",
            "bg_color": "#F0FDFA",
            "border_color": "#0D9488",
            "items": [
                "• Image Resizing:",
                "   Standardized 224x224",
                "• Normalization:",
                "   Pixel scaling by 1/255",
                "• Augmentation:",
                "   - Random Shear (0.2)",
                "   - Random Zoom (0.2)",
                "   - Horizontal Flips",
                "• Batch Generation (64)"
            ]
        },
        {
            "num": "Stage 3",
            "title": "DenseNet201\nBackbone",
            "x": 6.8,
            "header_color": "#2563EB",
            "bg_color": "#EFF6FF",
            "border_color": "#2563EB",
            "items": [
                "• Transfer Learning:",
                "   Pretrained on ImageNet",
                "• 201 Convolutional Layers",
                "• Dense Connectivity:",
                "   Layer-to-all connection",
                "• Frozen Base Weights",
                "• Rich Feature Reuse",
                "• Vanishing Gradient solved"
            ]
        },
        {
            "num": "Stage 4",
            "title": "Custom Classifier\nHead",
            "x": 9.8,
            "header_color": "#7C3AED",
            "bg_color": "#F5F3FF",
            "border_color": "#7C3AED",
            "items": [
                "• Flatten Layer:",
                "   2D map to 1D vector",
                "• Dense Layer (256):",
                "   ReLU activation",
                "• Dropout Layer (0.3):",
                "   Prevents overfitting",
                "• Output Dense (4):",
                "   Softmax activation",
                "• Loss: Crossentropy"
            ]
        },
        {
            "num": "Stage 5",
            "title": "Diagnosis &\nDeployment",
            "x": 12.8,
            "header_color": "#E11D48",
            "bg_color": "#FFF1F2",
            "border_color": "#E11D48",
            "items": [
                "• Multi-Class Softmax:",
                "   Normalized probabilities",
                "• Primary Diagnosis:",
                "   Predicted Tumor Type",
                "• Confidence Score (%)",
                "• Streamlit Web UI:",
                "   Instant analysis (< 1s)",
                "• Medical Insights Report"
            ]
        }
    ]

    for s in stages:
        # Outer Card Shadow Effect
        shadow = patches.FancyBboxPatch(
            (s['x'] + 0.05, y_pos - 0.05), box_w, box_h,
            boxstyle="round,pad=0.1,rounding_size=0.25",
            facecolor='#E2E8F0', edgecolor='none', zorder=1
        )
        ax.add_patch(shadow)

        # Main Card Box
        card = patches.FancyBboxPatch(
            (s['x'], y_pos), box_w, box_h,
            boxstyle="round,pad=0.1,rounding_size=0.25",
            facecolor=s['bg_color'], edgecolor=s['border_color'], linewidth=2.0, zorder=2
        )
        ax.add_patch(card)

        # Header Badge
        header_badge = patches.FancyBboxPatch(
            (s['x'] + 0.15, y_pos + box_h - 1.15), box_w - 0.3, 1.0,
            boxstyle="round,pad=0.08,rounding_size=0.18",
            facecolor=s['header_color'], edgecolor='none', zorder=3
        )
        ax.add_patch(header_badge)

        # Header Text
        ax.text(s['x'] + box_w/2, y_pos + box_h - 0.38, s['num'].upper(),
                ha='center', va='center', fontsize=9, fontweight='bold', color='#E2E8F0', zorder=4)
        ax.text(s['x'] + box_w/2, y_pos + box_h - 0.78, s['title'],
                ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=4, multialignment='center')

        # Content Text Items
        curr_y = y_pos + box_h - 1.55
        for item in s['items']:
            is_bold = item.startswith("•") and ":" in item
            font_w = 'bold' if is_bold else 'normal'
            f_color = '#0F172A' if is_bold else '#334155'
            ax.text(s['x'] + 0.2, curr_y, item, ha='left', va='center',
                    fontsize=9.5, fontweight=font_w, color=f_color, zorder=4)
            curr_y -= 0.36

    # Flow Arrows connecting stages
    for i in range(len(stages) - 1):
        x_start = stages[i]['x'] + box_w + 0.12
        x_end = stages[i+1]['x'] - 0.12
        arrow_y = y_pos + box_h / 2

        arrow = patches.FancyArrowPatch(
            (x_start, arrow_y), (x_end, arrow_y),
            arrowstyle='-|>,head_width=5.5,head_length=8',
            color='#475569', linewidth=2.5, zorder=5
        )
        ax.add_patch(arrow)

    # Bottom Pipeline Summary Banner
    banner = patches.FancyBboxPatch(
        (0.8, 0.8), 14.4, 1.0,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        facecolor='#1E293B', edgecolor='none', zorder=2
    )
    ax.add_patch(banner)

    ax.text(8.0, 1.45, "PIPELINE SUMMARY", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#38BDF8', zorder=3)
    ax.text(8.0, 1.05, "Raw MRI Scan (224x224x3)   ➔   Augmented Generators   ➔   DenseNet201 Feature Maps   ➔   Dense Classifier (Dropout 0.3)   ➔   Instant Diagnosis", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#F8FAFC', zorder=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"System architecture diagram successfully saved to {output_path}")

if __name__ == "__main__":
    draw_system_architecture("system_architecture.png")
