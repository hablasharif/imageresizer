import streamlit as st
from PIL import Image
import io
import base64

# Streamlit app title
st.title("Advanced Image Resizer")

# User input for uploading an image file
uploaded_image = st.file_uploader("Upload an image file:", type=["jpg", "jpeg", "png", "gif"])

# User input for custom dimensions
st.subheader("Image Resize Configuration")
width = st.number_input("Width (pixels):", value=300, step=1)
height = st.number_input("Height (pixels):", value=300, step=1)

# Checkbox for maintaining aspect ratio
maintain_aspect_ratio = st.checkbox("Maintain Aspect Ratio", value=True)

# Function to resize the image
def resize_image(image, width, height, maintain_aspect_ratio=True):
    try:
        img = Image.open(image)
        if maintain_aspect_ratio:
            img.thumbnail((width, height))
        else:
            img = img.resize((width, height))
        return img
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Display the resized image
if uploaded_image:
    st.subheader("Original Image:")
    st.image(uploaded_image, use_column_width=True)
    
    if st.button("Resize Image"):
        resized_img = resize_image(uploaded_image, width, height, maintain_aspect_ratio)
        if resized_img:
            st.subheader("Resized Image:")
            st.image(resized_img, use_column_width=True, caption=f"Width: {width}px, Height: {height}px")

            # Option to download the resized image
            st.markdown(get_binary_file_downloader_html(resized_img, "resized"), unsafe_allow_html=True)

# Function to create a download link for the image
def get_binary_file_downloader_html(image, file_label):
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format="PNG")
    b64 = base64.b64encode(img_byte_array.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{file_label}.png">Download {file_label}</a>'
    return href
