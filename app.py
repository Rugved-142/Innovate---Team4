import streamlit as st
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import joblib 

@st.cache_resource
def load_model_from_file():
    model = load_model("waste_cnn_model.h5")  
    return model

# Load the label encoder
@st.cache_resource
def load_label_encoder():
    label_encoder = joblib.load("label_encoder.pkl")  
    return label_encoder

def preprocess_image(image):
    img = np.array(image) 
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  
    img = cv2.resize(img, (224, 224))
    img = img / 255.0  
    return np.expand_dims(img, axis=0) 


def biogas_conversion(mass_vegetation_kg):
    water_ratio = 1.5
    inoculum_ratio = 0.1
    biogas_yield = 0.3
    dry_matter_content = 0.8
    methane_content = 0.6
    methane_energy = 35.8

    water_kg = mass_vegetation_kg * water_ratio
    total_slurry_kg = mass_vegetation_kg + water_kg
    inoculum_kg = total_slurry_kg * inoculum_ratio
    dry_matter_kg = mass_vegetation_kg * dry_matter_content
    biogas_volume_m3 = dry_matter_kg * biogas_yield
    methane_volume_m3 = biogas_volume_m3 * methane_content
    energy_content_mj = methane_volume_m3 * methane_energy
    energy_content_kwh = energy_content_mj * 0.2778
    biofuel_liters = methane_volume_m3  

    return {
        "water_kg": water_kg,
        "inoculum_kg": inoculum_kg,
        "total_slurry_kg": total_slurry_kg,
        "dry_matter_kg": dry_matter_kg,
        "biogas_volume_m3": biogas_volume_m3,
        "methane_volume_m3": methane_volume_m3,
        "energy_content_mj": energy_content_mj,
        "energy_content_kwh": energy_content_kwh,
        "biofuel_liters": biofuel_liters,
    }


def process_material(material_type, mass_kg):
    if material_type == "paper":
        biogas_yield = 0.25  # m³ per kg
        bioethanol_yield = 0.25  # liters per kg
        digestion_time_days = 25  # days
        fermentation_time_days = 6  # days

        biogas_volume = mass_kg * biogas_yield
        bioethanol_volume = mass_kg * bioethanol_yield

        return {
            "biogas_volume": biogas_volume,
            "bioethanol_volume": bioethanol_volume,
            "digestion_time_days": digestion_time_days,
            "fermentation_time_days": fermentation_time_days,
        }

    elif material_type == "glass":
        recycling_time_days = 1.5  # days
        return {"recycling_time_days": recycling_time_days}

    elif material_type == "plastic":
        biooil_yield = 0.65  # liters per kg
        syngas_yield = 1.25  # m³ per kg
        pyrolysis_time_hours = 1.5  # hours
        gasification_time_hours = 1.5  # hours

        biooil_volume = mass_kg * biooil_yield
        syngas_volume = mass_kg * syngas_yield

        return {
            "biooil_volume": biooil_volume,
            "syngas_volume": syngas_volume,
            "pyrolysis_time_hours": pyrolysis_time_hours,
            "gasification_time_hours": gasification_time_hours,
        }

    elif material_type == "cardboard":
        biogas_yield = 0.25  # m³ per kg
        bioethanol_yield = 0.25  # liters per kg
        digestion_time_days = 25  # days
        fermentation_time_days = 6  # days

        biogas_volume = mass_kg * biogas_yield
        bioethanol_volume = mass_kg * bioethanol_yield

        return {
            "biogas_volume": biogas_volume,
            "bioethanol_volume": bioethanol_volume,
            "digestion_time_days": digestion_time_days,
            "fermentation_time_days": fermentation_time_days,
        }

    elif material_type == "food organics":
        biogas_yield = 0.4  # m³ per kg
        compost_yield = 0.6  # kg compost per kg food waste
        digestion_time_days = 25  # days
        composting_time_days = 45  # days

        biogas_volume = mass_kg * biogas_yield
        compost_volume = mass_kg * compost_yield

        return {
            "biogas_volume": biogas_volume,
            "compost_volume": compost_volume,
            "digestion_time_days": digestion_time_days,
            "composting_time_days": composting_time_days,
        }

    elif material_type == "metal":
        recycling_time_days = 2  # days
        return {"recycling_time_days": recycling_time_days}

    else:
        return None

# Streamlit UI
st.title("Image Classification & Biofuel/Recycling Process")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
CATEGORIES = ["Cardboard", "Food Organics", "Glass", "Metal", "Miscellaneous Trash", "Paper", "Plastic", "Textile Trash", "Vegetation"]

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Load CNN model and Label Encoder
    model = load_model_from_file()
    label_encoder = load_label_encoder()

    # Preprocess image
    processed_img = preprocess_image(image)

    # Run inference
    prediction = model.predict(processed_img)
    predicted_class = CATEGORIES[np.argmax(prediction)]

    # Display result
    st.subheader("Model Prediction:")
    st.write(f"Predicted Class: {predicted_class}")

    # Enable biofuel/recycling calculation based on predicted class
    if predicted_class.lower() in ["vegetation", "paper", "cardboard", "food organics", "plastic", "glass", "metal"]:
        st.subheader(f"{predicted_class} Processing")
        mass_kg = st.number_input(f"Enter the mass of {predicted_class} (kg):", min_value=0.1, value=10.0, step=0.1)

        if st.button("Generate Process"):
            if predicted_class.lower() == "vegetation":
                results = biogas_conversion(mass_kg)
                st.write("### Step-by-Step Process for Vegetation to Biogas:")
                st.write("1. **Shred the vegetation** into small pieces (1–5 cm).")
                st.write(f"2. **Add water**: {results['water_kg']:.2f} liters (1:1.5 ratio with vegetation).")
                st.write(f"3. **Add inoculum**: {results['inoculum_kg']:.2f} kg (10% of total slurry).")
                st.write(f"4. **Total slurry**: {results['total_slurry_kg']:.2f} kg (vegetation + water).")
                st.write("5. **Transfer the slurry** to an anaerobic digester.")
                st.write("6. **Maintain temperature** at 35–40°C for 20–40 days.")
                st.write(f"7. **Biogas yield**: {results['biogas_volume_m3']:.2f} m³.")
                st.write(f"8. **Methane content**: {results['methane_volume_m3']:.2f} m³ (60% of biogas).")
                st.write(f"9. **Energy content**: {results['energy_content_mj']:.2f} MJ or {results['energy_content_kwh']:.2f} kWh.")
                st.write(f"10. **Biofuel production**: {results['biofuel_liters']:.2f} liters (diesel equivalent).")

            elif predicted_class.lower() == "paper":
                results = process_material(predicted_class.lower(), mass_kg)
                st.write("### Step-by-Step Process for Paper to Biogas/Bioethanol:")
                st.write("1. **Shred the paper** into small pieces.")
                st.write("2. **Mix with water** to create a slurry.")
                st.write("3. **Add inoculum** (10% of total slurry).")
                st.write("4. **Transfer the slurry** to an anaerobic digester.")
                st.write("5. **Maintain temperature** at 35–40°C for 25 days.")
                st.write(f"6. **Biogas yield**: {results['biogas_volume']:.2f} m³.")
                st.write("7. **For bioethanol**:")
                st.write("   - Treat the paper with enzymes to break down cellulose into sugars.")
                st.write("   - Ferment the sugars into ethanol.")
                st.write(f"   - **Bioethanol yield**: {results['bioethanol_volume']:.2f} liters.")

            elif predicted_class.lower() == "cardboard":
                results = process_material(predicted_class.lower(), mass_kg)
                st.write("### Step-by-Step Process for Cardboard to Biogas/Bioethanol:")
                st.write("1. **Shred the cardboard** into small pieces.")
                st.write("2. **Mix with water** to create a slurry.")
                st.write("3. **Add inoculum** (10% of total slurry).")
                st.write("4. **Transfer the slurry** to an anaerobic digester.")
                st.write("5. **Maintain temperature** at 35–40°C for 25 days.")
                st.write(f"6. **Biogas yield**: {results['biogas_volume']:.2f} m³.")
                st.write("7. **For bioethanol**:")
                st.write("   - Treat the cardboard with enzymes to break down cellulose into sugars.")
                st.write("   - Ferment the sugars into ethanol.")
                st.write(f"   - **Bioethanol yield**: {results['bioethanol_volume']:.2f} liters.")

            elif predicted_class.lower() == "food organics":
                results = process_material(predicted_class.lower(), mass_kg)
                st.write("### Step-by-Step Process for Food Organics to Biogas/Compost:")
                st.write("1. **Shred the food waste** into small pieces.")
                st.write("2. **Mix with water** to create a slurry.")
                st.write("3. **Add inoculum** (10% of total slurry).")
                st.write("4. **Transfer the slurry** to an anaerobic digester.")
                st.write("5. **Maintain temperature** at 35–40°C for 25 days.")
                st.write(f"6. **Biogas yield**: {results['biogas_volume']:.2f} m³.")
                st.write("7. **For composting**:")
                st.write("   - Aerate the food waste in a compost bin.")
                st.write("   - Maintain moisture and temperature for 45 days.")
                st.write(f"   - **Compost yield**: {results['compost_volume']:.2f} kg.")

            elif predicted_class.lower() == "plastic":
                results = process_material(predicted_class.lower(), mass_kg)
                st.write("### Step-by-Step Process for Plastic to Bio-oil/Syngas:")
                st.write("1. **Shred the plastic** into small pieces.")
                st.write("2. **Heat the plastic** in a pyrolysis reactor at 400–600°C in the absence of oxygen.")
                st.write(f"3. **Bio-oil yield**: {results['biooil_volume']:.2f} liters.")
                st.write(f"4. **Syngas yield**: {results['syngas_volume']:.2f} m³.")
                st.write("5. **Processing time**: 1.5 hours.")

            elif predicted_class.lower() == "glass":
                results = process_material(predicted_class.lower(), mass_kg)
                st.write("### Step-by-Step Process for Glass Recycling:")
                st.write("1. **Clean the glass** to remove impurities.")
                st.write("2. **Crush the glass** into small pieces.")
                st.write("3. **Melt the glass** in a furnace at high temperatures.")
                st.write("4. **Mold the molten glass** into new products.")
                st.write(f"5. **Processing time**: {results['recycling_time_days']} days.")
                st.write("### Products Made from Recycled Glass:")
                st.write("- **Bottles and jars**")
                st.write("- **Glass tiles**")
                st.write("- **Fiberglass**")
                st.write("- **Decorative items**")

            elif predicted_class.lower() == "metal":
                results = process_material(predicted_class.lower(), mass_kg)
                st.write("### Step-by-Step Process for Metal Recycling:")
                st.write("1. **Sort the metal** by type (e.g., aluminum, steel).")
                st.write("2. **Clean the metal** to remove contaminants.")
                st.write("3. **Melt the metal** in a furnace at high temperatures.")
                st.write("4. **Mold the molten metal** into new products.")
                st.write(f"5. **Processing time**: {results['recycling_time_days']} days.")
                st.write("### Products Made from Recycled Metal:")
                st.write("- **Cans and containers**")
                st.write("- **Automotive parts**")
                st.write("- **Construction materials**")
                st.write("- **Electronics**")

    else:
        st.subheader("Proper Waste Management")
        st.write("This item does not fall into a recyclable or biofuel-convertible category. ")
        st.write("To ensure a cleaner and more sustainable Boston, this waste will be responsibly processed at the Boston dumping field, where it will be managed in an eco-friendly manner.")
        st.write("By disposing of waste properly, we contribute to a healthier environment for future generations!")
