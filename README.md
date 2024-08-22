**Fake PAN Card Detection App**

This Flask application allows users to upload a PAN card image and compares it with an existing reference image using Structural Similarity Index (SSI). The application determines whether the uploaded PAN card is original or fake based on the SSI score.

**Features**

- Upload PAN card images for verification.
- Compares the uploaded image with a pre-existing reference image.
- Uses Structural Similarity Index (SSI) to calculate the similarity score between the uploaded and reference images.
- Highlights the differences between the two images with bounding boxes.
- Displays results with appropriate styling: green for valid PAN card, red for fake PAN card.
- Saves images showing differences and the analysis results.

**Tech Stack**

- **Flask:** Web framework used to create the application.
- **OpenCV:** Library used for image processing and manipulation.
- **Pillow:** Python Imaging Library (PIL) for image manipulation.
- **skimage:** Used to compute the Structural Similarity Index (SSI) for comparing images.
- **HTML/CSS:** Front-end for rendering the forms and results.

**Prerequisites**

Before you begin, ensure you have the following installed:

- Python 3.x
- pip (Python package manager)

**Installation**

***1. Clone the repository:***

   ``` 

   git clone <https://github.com/your-username/pan-card-verification.git>

   cd pan-card-verification

   ```

***2. Install the required dependencies:***

   ```

   pip install -r requirements.txt

   ```

***3. Ensure the following directories exist inside the static directory:***
   1. uploads: To store the uploaded PAN card images.
   2. original: To store the reference PAN card image.
   3. generated: To store the generated comparison images.

  You can create them using the following commands:
  
  ```
  
  mkdir -p static/uploads static/original static/generated
  
  ```

***4. Place the reference PAN card image inside the static/original folder. Rename it to pan-card.png.***

**Usage**

1. Start the Flask application:

```bash

python app.py

```

2. Open your browser and go to http://127.0.0.1:5000/ or http://0.0.0.0:5000/.
3. Upload a PAN card image to verify its authenticity. The result will be displayed based on the similarity score.

**File Structure**

Fake\_pan\_detector/

│

├── static/

│   ├── uploads/         # Stores uploaded images

│   ├── original/        # Stores the reference PAN card image

│   └── generated/       # Stores the generated output images

│

├── templates/

│   ├── index.html       # Upload form page

│   ├── test.html        # Image upload and processing page

│   └── results.html     # Results page displaying the similarity score

│

├── app.py               # Main Flask application file

└── README.md            # Project documentation
