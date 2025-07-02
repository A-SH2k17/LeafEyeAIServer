# Treatment recommendations for each disease
DISEASE_RECOMMENDATIONS = {
    "Apple___Apple scab": [
        "Apply fungicide treatments during the growing season",
        "Remove and destroy infected leaves",
        "Ensure good air circulation by pruning"
    ],
    "Apple___Black rot": [
        "Prune out dead or diseased wood",
        "Apply fungicides during the growing season",
        "Remove mummified fruits from trees"
    ],
    "Apple___Cedar apple rust": [
        "Remove nearby juniper trees if possible",
        "Apply fungicides early in the season",
        "Prune and dispose of infected leaves"
    ],
    "Apple___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Blueberry___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Cherry (including sour)___Powdery mildew": [
        "Apply sulfur or potassium bicarbonate fungicides",
        "Ensure good airflow by pruning",
        "Avoid overhead watering"
    ],
    "Cherry (including sour)___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Corn (maize)___Cercospora leaf spot / Gray leaf spot": [
        "Rotate crops annually",
        "Use resistant hybrids if available",
        "Apply fungicide at tasseling if needed"
    ],
    "Corn (maize)___Common rust": [
        "Use resistant varieties",
        "Apply fungicides if rust appears early and is widespread",
        "Encourage proper plant spacing"
    ],
    "Corn (maize)___Northern Leaf Blight": [
        "Plant resistant hybrids",
        "Apply fungicides at early tasseling",
        "Practice crop rotation"
    ],
    "Corn (maize)___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Grape___Black rot": [
        "Remove infected mummies and canes",
        "Apply fungicides starting at bud break",
        "Ensure proper pruning and airflow"
    ],
    "Grape___Esca (Black Measles)": [
        "Remove and destroy infected vines",
        "Avoid pruning during wet conditions",
        "Apply protective fungicides if needed"
    ],
    "Grape___Leaf blight (Isariopsis Leaf Spot)": [
        "Remove infected leaves",
        "Apply fungicides at early signs",
        "Improve air circulation in the canopy"
    ],
    "Grape___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Orange___Haunglongbing (Citrus greening)": [
        "Remove and destroy infected trees",
        "Control psyllid vector with insecticides",
        "Use certified disease-free nursery stock"
    ],
    "Peach___Bacterial spot": [
        "Use resistant varieties if available",
        "Apply copper-based bactericides during early bloom",
        "Avoid overhead irrigation"
    ],
    "Peach___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Pepper bell___Bacterial spot": [
        "Use disease-free seeds",
        "Apply copper-based bactericides",
        "Avoid working with wet plants"
    ],
    "Pepper bell___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Potato___Early blight": [
        "Practice crop rotation",
        "Apply fungicides at early signs of disease",
        "Remove and destroy infected plant debris"
    ],
    "Potato___Late blight": [
        "Use certified seed potatoes",
        "Apply systemic fungicides",
        "Remove infected plants promptly"
    ],
    "Potato___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Raspberry___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Soybean___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Squash___Powdery mildew": [
        "Use resistant varieties",
        "Apply sulfur or neem oil sprays",
        "Ensure adequate spacing and sunlight"
    ],
    "Strawberry___Leaf scorch": [
        "Remove infected leaves",
        "Avoid overhead watering",
        "Apply fungicides such as captan or myclobutanil"
    ],
    "Strawberry___healthy": [
        "No treatment needed – plant is healthy"
    ],
    "Tomato___Bacterial spot": [
        "Use copper-based bactericides",
        "Avoid working with wet foliage",
        "Rotate crops annually"
    ],
    "Tomato___Early blight": [
        "Rotate crops every 2–3 years",
        "Keep foliage dry with drip irrigation",
        "Apply fungicide at first sign of disease"
    ],
    "Tomato___Late blight": [
        "Apply fungicides like chlorothalonil or mancozeb",
        "Remove and destroy infected plants",
        "Avoid overhead watering"
    ],
    "Tomato___Leaf Mold": [
        "Ensure good air circulation",
        "Apply fungicides such as chlorothalonil or copper-based sprays",
        "Avoid high humidity environments"
    ],
    "Tomato___Septoria leaf spot": [
        "Remove infected leaves",
        "Use fungicides with chlorothalonil",
        "Practice crop rotation"
    ],
    "Tomato___Spider mites Two spotted spider mite": [
        "Spray water to knock off mites",
        "Use insecticidal soap or neem oil",
        "Maintain humidity around plants"
    ],
    "Tomato___Target Spot": [
        "Apply preventive fungicides early",
        "Remove lower infected leaves",
        "Avoid overhead irrigation"
    ],
    "Tomato___Tomato Yellow Leaf Curl Virus": [
        "Use virus-resistant tomato varieties",
        "Control whitefly populations",
        "Remove and destroy infected plants"
    ],
    "Tomato___Tomato mosaic virus": [
        "Avoid tobacco use near plants",
        "Disinfect tools and hands",
        "Remove and destroy infected plants"
    ],
    "Tomato___healthy": [
        "No treatment needed – plant is healthy"
    ]
}



# Disease classes that the model can predict
DISEASE_CLASSES = [
    "Apple___Apple scab",
    "Apple___Black rot",
    "Apple___Cedar apple rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry (including sour)___Powdery mildew",
    "Cherry (including sour)___healthy",
    "Corn (maize)___Cercospora leaf spot / Gray leaf spot",
    "Corn (maize)___Common rust",
    "Corn (maize)___Northern Leaf Blight",
    "Corn (maize)___healthy",
    "Grape___Black rot",
    "Grape___Esca (Black Measles)",
    "Grape___Leaf blight (Isariopsis Leaf Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing (Citrus greening)",
    "Peach___Bacterial spot",
    "Peach___healthy",
    "Pepper bell___Bacterial spot",
    "Pepper bell___healthy",
    "Potato___Early blight",
    "Potato___Late blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery mildew",
    "Strawberry___Leaf scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial spot",
    "Tomato___Early blight",
    "Tomato___Late blight",
    "Tomato___Leaf Mold",
    "Tomato___Septoria leaf spot",
    "Tomato___Spider mites Two spotted spider mite",
    "Tomato___Target Spot",
    "Tomato___Tomato Yellow Leaf Curl Virus",
    "Tomato___Tomato mosaic virus",
    "Tomato___healthy"
]

#Description
DISEASE_DESCRIPTIONS = {
    "Apple___Apple scab": "A fungal disease causing dark, scabby lesions on leaves, fruit, and twigs. It can severely reduce fruit quality and yield if untreated.",
    "Apple___Black rot": "A fungal infection that produces dark, sunken spots on apples and cankers on branches, spreading rapidly in warm, moist conditions.",
    "Apple___Cedar apple rust": "A fungus that causes bright orange spots on apple leaves and fruit, needing both apple and cedar trees to complete its lifecycle.",
    "Apple___healthy": None,
    "Blueberry___healthy": None,
    "Cherry (including sour)___Powdery mildew": "A fungal disease that forms a white, powdery coating on cherry leaves, shoots, and fruit, stunting growth and yield.",
    "Cherry (including sour)___healthy": None,
    "Corn (maize)___Cercospora leaf spot / Gray leaf spot": "A fungal disease causing rectangular gray or tan lesions on corn leaves, reducing photosynthesis and crop yield.",
    "Corn (maize)___Common rust": "A fungal disease producing reddish-brown pustules on corn leaves, commonly affecting growth in warm, humid conditions.",
    "Corn (maize)___Northern Leaf Blight": "A fungal disease marked by long, gray-green lesions on corn leaves, significantly impacting crop health and productivity.",
    "Corn (maize)___healthy": None,
    "Grape___Black rot": "A fungal disease that causes brown spots on leaves and shriveled, rotted fruit, often leading to major grapevine loss.",
    "Grape___Esca (Black Measles)": "A complex fungal disease causing dark spots, leaf scorch, and fruit drying, often leading to vine decline and death.",
    "Grape___Leaf blight (Isariopsis Leaf Spot)": "A fungal infection causing brownish lesions on grape leaves, reducing vine vigor and fruit quality.",
    "Grape___healthy": None,
    "Orange___Haunglongbing (Citrus greening)": "A bacterial disease spread by insects, causing yellow shoots, misshapen fruit, and eventually tree death if unmanaged.",
    "Peach___Bacterial spot": "A bacterial disease causing dark, sunken spots on peach fruit and leaves, often leading to fruit cracking and leaf drop.",
    "Peach___healthy": None,
    "Pepper bell___Bacterial spot": "A bacterial disease forming water-soaked spots on pepper leaves and fruit, leading to defoliation and reduced yields.",
    "Pepper bell___healthy": None,
    "Potato___Early blight": "A fungal disease causing brown leaf spots with concentric rings, leading to premature leaf death and reduced potato yields.",
    "Potato___Late blight": "A devastating disease responsible for the Irish Potato Famine, causing dark, water-soaked lesions on leaves, stems, and tubers.",
    "Potato___healthy": None,
    "Raspberry___healthy": None,
    "Soybean___healthy": None,
    "Squash___Powdery mildew": "A fungal disease that produces a white, powdery growth on squash leaves, leading to reduced photosynthesis and weaker plants.",
    "Strawberry___Leaf scorch": "A fungal disease that causes reddish-brown spots and eventual browning and death of strawberry leaves.",
    "Strawberry___healthy": None,
    "Tomato___Bacterial spot": "A bacterial infection causing small, dark spots on tomato leaves and fruit, often leading to leaf drop and poor fruit quality.",
    "Tomato___Early blight": "A fungal disease causing dark concentric spots on tomato leaves, stems, and fruit, weakening plant structure and yield.",
    "Tomato___Late blight": "A highly destructive disease causing large, dark, water-soaked lesions on tomatoes, quickly killing plants if untreated.",
    "Tomato___Leaf Mold": "A fungal disease that leads to yellow spots on leaf tops and moldy gray patches underneath, affecting tomato yield indoors and outdoors.",
    "Tomato___Septoria leaf spot": "A fungal infection causing small, circular spots with dark borders on tomato leaves, leading to significant leaf loss.",
    "Tomato___Spider mites Two spotted spider mite": "Tiny pests that create yellow speckling and webbing on tomato leaves, weakening plants and reducing yield.",
    "Tomato___Target Spot": "A fungal disease producing large, dark lesions with concentric rings on tomato leaves and fruit, reducing plant vigor.",
    "Tomato___Tomato Yellow Leaf Curl Virus": "A viral disease causing curling, yellowing, and stunted growth in tomato plants, spread by whiteflies.",
    "Tomato___Tomato mosaic virus": "A viral infection causing mottled, light and dark green patterns on leaves, affecting tomato plant growth and fruit quality.",
    "Tomato___healthy": None
}

