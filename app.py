import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import cv2
from utils.pixelator import Pixelator
from utils.image_processor import ImageProcessor
import io

# Page configuration
st.set_page_config(
    page_title="Digital Canvas - Pixelation App",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load custom CSS
def local_css(file_name):
    """Load custom CSS from file"""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{file_name}' not found. Using default styling.")

# Load custom CSS from assets folder
local_css("assets/styles.css")

# Inline CSS for better UI (fallback if CSS file not found)
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #00c4cc;
        color: white;
        border-radius: 8px;
        padding: 10px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00a3aa;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,196,204,0.3);
    }
    .title-text {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    .subtitle-text {
        color: #7f8c8d;
        font-size: 1rem;
        margin-top: 0;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 2rem;
    }
    .stDownloadButton>button {
        width: 100%;
        background-color: #e74c3c;
        color: white;
        border-radius: 8px;
        padding: 10px;
        font-weight: 600;
    }
    .info-box {
        background-color: #ecf0f1;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #00c4cc;
        margin: 10px 0;
    }
    .canvas-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state - ADDED: canvas_key for clearing
if 'show_pixelated' not in st.session_state:
    st.session_state.show_pixelated = False
if 'pixelated_image' not in st.session_state:
    st.session_state.pixelated_image = None
if 'pixel_size' not in st.session_state:
    st.session_state.pixel_size = 20
if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = 0

# Header
st.markdown('<p class="title-text">🎨 Digital Canvas</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Draw and create pixelated art in real-time</p>', unsafe_allow_html=True)

# Sidebar - Tools Configuration
with st.sidebar:
    st.header("🛠️ Tools")
    
    # Drawing mode
    drawing_mode = st.selectbox(
        "Drawing Tool:",
        ("freedraw", "line", "rect", "circle", "transform"),
        index=0
    )
    
    st.markdown("---")
    
    # Brush Size
    st.subheader("Brush Size")
    brush_size = st.slider(
        "Size:",
        min_value=1,
        max_value=50,
        value=5,
        help="Adjust brush stroke width"
    )
    
    st.markdown("---")
    
    # Colors Section
    st.subheader("🎨 Colors")
    
    # Predefined color palette
    color_palette = {
        "Black": "#000000",
        "White": "#FFFFFF",
        "Red": "#FF0000",
        "Green": "#00FF00",
        "Blue": "#0000FF",
        "Yellow": "#FFFF00",
        "Magenta": "#FF00FF",
        "Cyan": "#00FFFF",
        "Orange": "#FFA500",
        "Purple": "#800080"
    }
    
    # Color selection with visual buttons
    cols = st.columns(5)
    selected_color = "#000000"
    
    for idx, (color_name, color_hex) in enumerate(color_palette.items()):
        col_idx = idx % 5
        with cols[col_idx]:
            if st.button(
                "⬤",
                key=f"color_{color_name}",
                help=color_name
            ):
                selected_color = color_hex
    
    # Custom color picker
    stroke_color = st.color_picker("Custom Color:", selected_color)
    
    st.markdown("---")
    
    # Pixelation Settings
    st.subheader("🔲 Pixelation Settings")
    pixel_size = st.slider(
        "Pixel Size:",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="Size of each pixel block in the output"
    )
    st.session_state.pixel_size = pixel_size
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <strong>💡 Tips:</strong><br>
        • Draw your number or shape<br>
        • Click "Process Image" to pixelate<br>
        • Toggle arrow to show result<br>
        • Save your pixelated art!
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
    st.subheader("✏️ Drawing Canvas")
    
    # Canvas component - FIXED: Using dynamic key
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=brush_size,
        stroke_color=stroke_color,
        background_color="#FFFFFF",
        background_image=None,
        update_streamlit=True,
        height=500,
        width=500,
        drawing_mode=drawing_mode,
        point_display_radius=0,
        key=f"canvas_{st.session_state.canvas_key}",
    )
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        # FIXED: Clear canvas by changing key
        if st.button("🔄 Clear Canvas"):
            st.session_state.canvas_key += 1
            st.session_state.pixelated_image = None
            st.session_state.show_pixelated = False
            st.rerun()
    
    with col_btn2:
        process_button = st.button("⚡ Process Image")
    
    with col_btn3:
        toggle_button = st.button("➡️ Toggle View")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats
    if canvas_result.image_data is not None:
        st.markdown(f"**Strokes:** {canvas_result.json_data['objects'].__len__() if canvas_result.json_data else 0}")

with col2:
    st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
    st.subheader("🔲 Pixelated Output")
    
    # Process image when button is clicked
    if process_button and canvas_result.image_data is not None:
        with st.spinner("Creating pixelated art..."):
            # Convert to PIL Image
            image_data = canvas_result.image_data.astype(np.uint8)
            pil_image = Image.fromarray(image_data)
            
            # Apply pixelation
            pixelator = Pixelator(pixel_size=st.session_state.pixel_size)
            pixelated = pixelator.pixelate(pil_image)
            
            st.session_state.pixelated_image = pixelated
            st.session_state.show_pixelated = True
            st.success("✅ Pixelation complete!")
    
    if toggle_button:
        st.session_state.show_pixelated = not st.session_state.show_pixelated
    
    # Display pixelated image - FIXED: removed use_container_width
    if st.session_state.show_pixelated and st.session_state.pixelated_image is not None:
        st.image(
            st.session_state.pixelated_image,
            caption="Your Pixelated Masterpiece"
        )
        
        # Download button
        img_buffer = io.BytesIO()
        st.session_state.pixelated_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        st.download_button(
            label="💾 Save Pixelated Image",
            data=img_buffer,
            file_name="pixelated_art.png",
            mime="image/png"
        )
        
        # Display pixel array info
        processor = ImageProcessor()
        pixel_array = processor.get_pixel_array(st.session_state.pixelated_image)
        st.markdown(f"**Array Shape:** {pixel_array.shape}")
        
    else:
        st.info("👈 Draw something and click 'Process Image' to see the pixelated result!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>Built with ❤️ using Streamlit | Perfect for ML Dataset Creation & Digit Recognition</p>
</div>
""", unsafe_allow_html=True)
