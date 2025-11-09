# 🎨 Digital Canvas - Pixelation App

A beautiful and interactive Streamlit application that allows you to draw freehand and convert your drawings into pixelated images in real-time. Perfect for creating synthetic datasets for machine learning projects, especially digit recognition tasks like MNIST.

## Features

✨ **Interactive Drawing Canvas**
- Multiple drawing tools (freedraw, line, rectangle, circle)
- Customizable brush sizes
- Rich color palette with 10+ preset colors
- Custom color picker

🔲 **Pixelation Engine**
- Real-time pixelation with adjustable pixel sizes
- Convert drawings to MNIST-style 28×28 grids
- Export pixel matrices for ML training

💾 **Export Capabilities**
- Save pixelated images as PNG
- Export pixel arrays for data science workflows
- Integration-ready for synthetic data generation

🎯 **Perfect For**
- Data Scientists creating training datasets
- ML Engineers building digit recognition models
- Creating custom synthetic data (similar to your RyoFaker project)
- Educational purposes and prototyping

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone or create the project directory:**
mkdir pixelation-app
cd pixelation-app

text

2. **Create the file structure** as shown above

3. **Install dependencies:**
pip install -r requirements.txt

text

## Usage

### Running the App

streamlit run app.py

text

The app will automatically open in your default browser at `http://localhost:8501`

### How to Use

1. **Draw:** Use your mouse/touchpad to draw on the left canvas
2. **Customize:** Adjust brush size, colors, and pixel size from the sidebar
3. **Process:** Click "Process Image" to generate the pixelated version
4. **Toggle:** Use the arrow button to show/hide the result
5. **Save:** Download your pixelated artwork as PNG

### For ML Applications

To extract pixel data for machine learning:

from utils.image_processor import ImageProcessor
from utils.pixelator import Pixelator

Load your drawn image
processor = ImageProcessor()
pixelator = Pixelator()

Convert to MNIST-style 28×28 grayscale
mnist_style = pixelator.pixelate_to_grid(your_image, grid_size=(28, 28))

Get normalized pixel array
pixel_array = processor.preprocess_for_ml(mnist_style)

Now you have a numpy array ready for ML models!
text

## Project Structure

pixelation-app/
│
├── app.py # Main Streamlit application
├── utils/
│ ├── init.py
│ ├── pixelator.py # Pixelation algorithms
│ └── image_processor.py # Image processing utilities
├── assets/
│ └── styles.css # Custom styling
├── requirements.txt
├── README.md
└── .streamlit/
└── config.toml # App configuration

text

## Integration with Your Data Science Workflow

This app complements your **RyoFaker** synthetic data generation library:

- **Generate visual training data** for computer vision models
- **Create custom digit datasets** beyond standard MNIST
- **Build domain-specific character recognition** datasets
- **Augment existing datasets** with handdrawn variations

## Technical Details

### Pixelation Algorithm

The app uses a two-step resize approach:
1. **Downsampling:** Reduces image to grid size using linear interpolation
2. **Upsampling:** Expands back using nearest-neighbor interpolation for blocky effect

### Canvas Technology

- Built on **Fabric.js** via `streamlit-drawable-canvas`
- Real-time drawing with low latency
- Supports multiple drawing modes and transformations

## Customization

### Changing Default Pixel Size

Edit `app.py`:
st.session_state.pixel_size = 30 # Change from 20 to 30

text

### Adding More Colors

Extend the `color_palette` dictionary in `app.py`:
color_palette = {
...
"Navy": "#000080",
"Teal": "#008080"
}

text

### Adjusting Canvas Size

Modify the `st_canvas` component:
canvas_result = st_canvas(
...
height=600, # Increase from 500
width=600, # Increase from 500
)

text

## Troubleshooting

**Issue:** Canvas not drawing
- **Solution:** Clear browser cache and reload

**Issue:** Pixelation too blocky
- **Solution:** Decrease pixel size in sidebar

**Issue:** Import errors
- **Solution:** Ensure all files in `utils/` directory and `__init__.py` exists

## Future Enhancements

- [ ] Batch processing multiple drawings
- [ ] Auto-save drawings to folder
- [ ] Integration with cloud storage
- [ ] Direct export to pandas DataFrame
- [ ] Undo/Redo functionality enhancement
- [ ] Real-time ML prediction overlay

## License

MIT License - feel free to use in your projects!

## Credits

Built with ❤️ for the Data Science community
- Streamlit framework
- streamlit-drawable-canvas component
- OpenCV and Pillow for image processing

---

**Note:** This app is designed for VS Code development and can be easily integrated into your existing data science pipelines alongside tools like RyoFaker for comprehensive synthetic data generation.