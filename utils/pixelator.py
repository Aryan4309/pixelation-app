import numpy as np
from PIL import Image
import cv2

class Pixelator:
    """
    A class to handle pixelation of images.
    Converts smooth drawings into blocky pixel art.
    """
    
    def __init__(self, pixel_size=20):
        """
        Initialize the Pixelator.
        
        Args:
            pixel_size (int): Size of each pixel block in the output
        """
        self.pixel_size = pixel_size
    
    def pixelate(self, image):
        """
        Convert an image to pixelated version.
        
        Args:
            image (PIL.Image): Input image to pixelate
            
        Returns:
            PIL.Image: Pixelated version of the input image
        """
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Get dimensions
        height, width = img_array.shape[:2]
        
        # Calculate new dimensions
        temp_height = height // self.pixel_size
        temp_width = width // self.pixel_size
        
        # Ensure dimensions are at least 1
        temp_height = max(1, temp_height)
        temp_width = max(1, temp_width)
        
        # Shrink image
        temp_image = cv2.resize(
            img_array,
            (temp_width, temp_height),
            interpolation=cv2.INTER_LINEAR
        )
        
        # Expand back to original size with nearest neighbor
        # This creates the blocky pixelated effect
        pixelated_image = cv2.resize(
            temp_image,
            (width, height),
            interpolation=cv2.INTER_NEAREST
        )
        
        # Convert back to PIL Image
        return Image.fromarray(pixelated_image)
    
    def pixelate_to_grid(self, image, grid_size=(28, 28)):
        """
        Convert image to a specific grid size (useful for ML datasets like MNIST).
        
        Args:
            image (PIL.Image): Input image
            grid_size (tuple): Target grid dimensions (height, width)
            
        Returns:
            PIL.Image: Resized pixelated image
        """
        # Convert to grayscale first
        gray_image = image.convert('L')
        
        # Resize to grid size
        pixelated = gray_image.resize(grid_size, Image.Resampling.NEAREST)
        
        return pixelated
    
    def get_pixel_matrix(self, image):
        """
        Get the pixel intensity matrix of the image.
        Useful for ML applications.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            numpy.ndarray: 2D array of pixel intensities
        """
        gray_image = image.convert('L')
        return np.array(gray_image)
