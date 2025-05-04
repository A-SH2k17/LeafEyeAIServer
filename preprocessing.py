import numpy as np
import cv2
from rembg import remove


"""
first the target size is initialized
"""

def check_green_percentage(image):
    # Check if the image is predominantly green (likely a close-up of a leaf)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower_green = np.array([20, 30, 30])
    upper_green = np.array([100, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_percentage = np.sum(green_mask > 0) / (image.shape[0] * image.shape[1])
    return green_percentage

def initialize_preprocessor(target_size=(224, 224)):
    """
    Initialize preprocessing configuration

    Parameters:
    -----------
    target_size : tuple, optional
        Desired output image size (width, height). Default is (224, 224)

    Returns:
    --------
    dict
        Configuration dictionary for preprocessing
    """
    return {
        'target_size': target_size
    }


def remove_background(image, config=None):
    """
    Remove background using rembg with enhanced parameters and segment the main leaf.

    Parameters:
    -----------
    image : numpy.ndarray
        Input image to process in RGB format
    config : dict, optional
        Preprocessing configuration

    Returns:
    --------
    numpy.ndarray
        Processed image with the background removed and focused on the main leaf
    """
    try:

        green_percentage = check_green_percentage(image)

        # If image is almost entirely green (>90%), skip rembg
        if green_percentage > 0.9999:
            final_image = image.copy()
            return final_image

        # For regular images, use rembg with carefully tuned parameters
        image_copy = image.copy()

        # Remove background with more conservative settings to avoid cutting the leaf
        output = remove(
            image_copy,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,  # Higher threshold to include more of the leaf
            alpha_matting_background_threshold=10,   # Lower threshold for better background separation
            alpha_matting_erode_size=5,             # Reduced erosion to preserve leaf edges
            post_process_mask=True
        )

        """
        the output of the rembg function has an alpha channel
        the model needs an rbg image the following steps seperates the rgn from the alpha
        and finds the leaf edge and adds it to the white background
        """

        # Separate RGB and alpha channels
        output_rgb = output[:, :, :3]
        alpha_channel = output[:, :, 3]


        # Threshold the alpha channel to create a binary mask with a lower threshold to keep more of the leaf
        _, binary_mask = cv2.threshold(alpha_channel, 50, 255, cv2.THRESH_BINARY)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Find contours in the binary mask
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            # If no contours found, use the original binary mask
            refined_mask = binary_mask
        else:
            # Find the largest contour by area
            largest_contour = max(contours, key=cv2.contourArea)

            # Create a refined mask from the largest contour
            refined_mask = np.zeros_like(binary_mask)
            cv2.drawContours(refined_mask, [largest_contour], -1, color=255, thickness=-1)

            # If there are other contours that are disease spots, preserve them
            for contour in contours:
                if contour is not largest_contour:
                    cv2.drawContours(refined_mask, [contour], -1, color=255, thickness=-1)

        # Convert the single channel mask to a 3-channel mask
        refined_mask_3 = cv2.merge([refined_mask, refined_mask, refined_mask])
        mask_norm = refined_mask_3.astype(np.float32) / 255.0

        # Create a white background image
        white_background = np.ones_like(output_rgb, dtype=np.uint8) * 255

        # Composite the output_rgb using the refined mask
        final_image = (output_rgb * mask_norm + white_background * (1 - mask_norm)).astype(np.uint8)

        return final_image
    except Exception as e:
        print(f"Background removal error: {e}")
        # On failure, return the original image but with increased contrast
        return enhance_contrast(image.copy())





def enhance_contrast(image):
    """
    Enhance image contrast using CLAHE

    Parameters:
    -----------
    image : numpy.ndarray
        Input image to enhance

    Returns:
    --------
    numpy.ndarray
        Contrast-enhanced image
    """
    # Convert to YCrCb color space
    image_ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCR_CB)

    # Split channels
    y_channel, cr_channel, cb_channel = cv2.split(image_ycrcb)

    # Apply CLAHE to luminance channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    y_enhanced = clahe.apply(y_channel)

    # Merge channels back
    enhanced = cv2.merge([y_enhanced, cr_channel, cb_channel])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_YCR_CB2RGB)

    return enhanced


def resize_with_padding(image, config):
    """
    Resize image to target size while preserving aspect ratio with padding

    Parameters:
    -----------
    image : numpy.ndarray
        Input image to resize
    config : dict
        Configuration dictionary containing target_size

    Returns:
    --------
    numpy.ndarray
        Resized image with padding
    """
    target_size = config['target_size']
    h, w = image.shape[:2]
    target_h, target_w = target_size

    # Calculate scaling factor to maintain aspect ratio
    scale = min(target_h / h, target_w / w)

    # Calculate new dimensions
    new_h, new_w = int(h * scale), int(w * scale)

    # Resize the image
    resized = cv2.resize(image, (new_w, new_h))

    # Create a white canvas of target size
    canvas = np.ones((target_h, target_w, 3), dtype=np.uint8) * 255

    # Calculate offsets for centering
    offset_h = (target_h - new_h) // 2
    offset_w = (target_w - new_w) // 2

    # Place the resized image on the canvas
    canvas[offset_h:offset_h + new_h, offset_w:offset_w + new_w] = resized

    return canvas


def preprocess_image(image_path, config=None):
    """
    Full preprocessing pipeline for a single image

    Parameters:
    -----------
    image_path : str
        Path to input image
    config : dict, optional
        Preprocessing configuration

    Returns:
    --------
    numpy.ndarray
        Preprocessed image ready for neural network input
    """
    # Use default configuration if not provided
    if config is None:
        config = initialize_preprocessor()

    try:
        # Read the image in BGR and convert to RGB
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #Check if image actually has leaf:
        if check_green_percentage(image)<0.3:
            return None
        # Remove the background and segment the leaf
        no_bg_image = remove_background(image)

        # Check if the result is mostly empty (failed segmentation
        non_white_pixels = np.sum(no_bg_image < 250) / no_bg_image.size
        if non_white_pixels < 0.01:  # If less than 1% non-white pixels
            enhanced_image = enhance_contrast(image)  # Fall back to original image
        else:
            enhanced_image = enhance_contrast(no_bg_image)

        # Resize with padding
        final_image = resize_with_padding(enhanced_image, config)

        # Normalize image for neural network input (values between 0 and 1)
        normalized_image = final_image.astype(np.float32) / 255.0

        return normalized_image

    except Exception as e:
        print(f"Preprocessing error for {image_path}: {e}")
        # In case of any error, attempt basic preprocessing
        try:
            # Read and resize the image
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, config['target_size'])
            return image.astype(np.float32) / 255.0
        except:
            # If all else fails, return zeros with the right shape
            return np.zeros((*config['target_size'], 3), dtype=np.float32)
