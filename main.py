import cv2
import numpy as np
import os

# Load an image from the given path in grayscale mode
def load(input):
    try:
        image = cv2.imread(input, cv2.IMREAD_GRAYSCALE)  # Read image as grayscale
        if image is None:
            raise IOError(f"Cannot open image {input}")  # Handle invalid image path or format
        return image
    except Exception as e:
        print(e)
        return None

# Apply a 5x5 Gaussian blur filter to the image
def gaussian_filter(image):
    # Define a 5x5 Gaussian kernel with sigma ≈ 1.0
    kernel = np.array([
        [1, 4, 7, 4, 1],
        [4, 16, 26, 16, 4],
        [7, 26, 41, 26, 7],
        [4, 16, 26, 16, 4],
        [1, 4, 7, 4, 1]
    ], dtype=np.float32)
    kernel /= 273.0  # Normalize kernel weights

    # Apply convolution using the Gaussian kernel
    result = cv2.filter2D(image, -1, kernel)

    return result

# Save the processed image to the specified path
def save(output, result):
    try:
        cv2.imwrite(output, result)  # Write image to disk
    except Exception as e:
        print(f"Failed to save Image {output}: {e}")

# Process all .tiff/.tif images in a folder with Gaussian filtering
def process_images_in_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

    # Loop through all files in the input directory
    for filename in os.listdir(input_folder):
        # Filter only .tiff and .tif images
        if filename.lower().endswith(('.tiff', '.tif')):
            input = os.path.join(input_folder, filename)
            # Generate output filename with "_gaussian" suffix
            output = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_gaussian.tiff")

            image = load(input)  # Load input image
            if image is None:
                continue  # Skip if image loading fails

            result = gaussian_filter(image)  # Apply Gaussian filter

            save(output, result)  # Save the result to output folder

            print(f"Processed image saved to: {output}")

# Entry point of the script
def main():
    # Define input and output folders
    input_folder = "input_images"
    output_folder = "output_images"

    # Start processing
    process_images_in_folder(input_folder, output_folder)
    
# Run the script
if __name__ == "__main__":
    main()
