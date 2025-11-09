import numpy as np
from PIL import Image, ImageOps
import cv2

class ImageProcessor:
    """
    Utility class for various image processing operations.
    """
    
    @staticmethod
    def preprocess_for_ml(image, target_size=(28, 28)):
        """
        Preprocess image for machine learning (MNIST-style).
        
        Args:
            image (PIL.Image): Input image
            target_size (tuple): Target dimensions
            
        Returns:
            numpy.ndarray: Normalized pixel array
        """
        # Convert to grayscale
        gray = image.convert('L')
        
        # Resize
        resized = gray.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(resized)
        
        # Normalize to 0-1 range
        normalized = img_array.astype('float32') / 255.0
        
        return normalized
    
    @staticmethod
    def get_pixel_array(image):
        """
        Get raw pixel array from image.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            numpy.ndarray: Pixel array
        """
        return np.array(image)
    
    @staticmethod
    def apply_threshold(image, threshold=128):
        """
        Apply binary threshold to image.
        
        Args:
            image (PIL.Image): Input image
            threshold (int): Threshold value (0-255)
            
        Returns:
            PIL.Image: Thresholded image
        """
        gray = image.convert('L')
        img_array = np.array(gray)
        
        # Apply threshold
        _, binary = cv2.threshold(img_array, threshold, 255, cv2.THRESH_BINARY)
        
        return Image.fromarray(binary)
    
    @staticmethod
    def invert_colors(image):
        """
        Invert image colors.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Inverted image
        """
        return ImageOps.invert(image.convert('RGB'))
    
    @staticmethod
    def remove_background(image, bg_color=(255, 255, 255, 255)):
        """
        Remove specific background color and make it transparent.
        
        Args:
            image (PIL.Image): Input image
            bg_color (tuple): Background color to remove (RGBA)
            
        Returns:
            PIL.Image: Image with transparent background
        """
        img_array = np.array(image)
        
        # Create mask for background
        mask = np.all(img_array[:, :, :3] == bg_color[:3], axis=-1)
        
        # Set alpha channel to 0 for background pixels
        img_array[mask, 3] = 0
        
        return Image.fromarray(img_array)
    
    @staticmethod
    def add_border(image, border_size=5, border_color=(0, 0, 0)):
        """
        Add border to image.
        
        Args:
            image (PIL.Image): Input image
            border_size (int): Border thickness
            border_color (tuple): RGB color for border
            
        Returns:
            PIL.Image: Image with border
        """
        return ImageOps.expand(image, border=border_size, fill=border_color)
    
    @staticmethod
    def center_image(image, canvas_size=(560, 560), bg_color=(255, 255, 255)):
        """
        Center image on a larger canvas.
        
        Args:
            image (PIL.Image): Input image
            canvas_size (tuple): Canvas dimensions
            bg_color (tuple): Background color
            
        Returns:
            PIL.Image: Centered image
        """
        canvas = Image.new('RGB', canvas_size, bg_color)
        
        # Calculate position to center
        x = (canvas_size[0] - image.width) // 2
        y = (canvas_size[1] - image.height) // 2
        
        canvas.paste(image, (x, y))
        
        return canvas
