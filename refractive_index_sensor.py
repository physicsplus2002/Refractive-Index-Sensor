import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Refractive Index Sensor", layout="wide")
st.title("🔬 Refractive Index Sensor: Resonance Shift Simulation")
st.sidebar.header("🔧 Adjust Simulation Parameters")

# Define wavelength range
wavelengths = np.linspace(300, 700, 401)

# Optical Structure Selection
optical_structure = st.sidebar.selectbox(
    "Select Optical Structure",
    ["1D Grating", "Ring Resonator", "Fabry-Pérot Resonator", "Bragg Stack"]
)

# **Updated Analytes**
analytes = {
    # Biosensing Analytes
    "Blood Plasma": 1.35, "DNA Solution": 1.46, "Glucose Solution": 1.37, "Hemoglobin": 1.41,
    "Protein Solution": 1.40, "Antibody Solution": 1.38, "Enzyme Solution": 1.39, "RNA Solution": 1.44,
    "Lipid Solution": 1.42, "Cell Cytoplasm": 1.36, "Serum": 1.34, "Urine": 1.33, 
    "Saliva": 1.32, "Tear Fluid": 1.31, "Cerebrospinal Fluid": 1.34,

    # Chemical Sensing Analytes
    "Ethanol": 1.36, "Methanol": 1.33, "Acetone": 1.35, "Chloroform": 1.44,
    "Benzene": 1.50, "Toluene": 1.49, "Xylene": 1.48, "Ammonia": 1.32, 
    "Sulfuric Acid": 1.43, "Hydrochloric Acid": 1.42, "Nitric Acid": 1.40, 
    "Hydrogen Peroxide": 1.38, "Sodium Hydroxide": 1.36, "Potassium Hydroxide": 1.37, 
    "Formaldehyde": 1.39
}

# Select analyte
selected_analyte = st.sidebar.selectbox("Select an Analyte", list(analytes.keys()))
selected_ri = analytes[selected_analyte]

# **Tunable Parameters**
if optical_structure == "1D Grating":
    grating_height = st.sidebar.slider("Grating Height (µm)", 0.1, 2.0, 0.3, 0.05)
    waveguide_thickness = st.sidebar.slider("Waveguide Thickness (µm)", 0.2, 2.0, 0.5, 0.1)
    periodicity = st.sidebar.slider("Periodicity (nm)", 200, 1200, 500, 50)

elif optical_structure == "Ring Resonator":
    ring_radius = st.sidebar.slider("Ring Radius (µm)", 2.0, 20.0, 5.0, 0.5)
    coupling_coefficient = st.sidebar.slider("Coupling Coefficient", 0.1, 1.0, 0.5, 0.05)
    waveguide_width = st.sidebar.slider("Waveguide Width (µm)", 0.2, 2.0, 0.5, 0.1)

elif optical_structure == "Fabry-Pérot Resonator":
    cavity_length = st.sidebar.slider("Cavity Length (µm)", 1.0, 10.0, 5.0, 0.5)
    mirror_reflectivity = st.sidebar.slider("Mirror Reflectivity", 0.5, 1.0, 0.95, 0.01)
    waveguide_thickness = st.sidebar.slider("Waveguide Thickness (µm)", 0.2, 2.0, 0.5, 0.1)

elif optical_structure == "Bragg Stack":
    num_layers = st.sidebar.slider("Number of Layers", 2, 10, 5, 1)
    layer_thickness = st.sidebar.slider("Layer Thickness (nm)", 50, 500, 200, 10)
    ri_contrast = st.sidebar.slider("Refractive Index Contrast", 0.1, 1.0, 0.5, 0.05)

# **Function to Calculate Resonance**
def calculate_resonance(wavelengths, ri, structure):
    if structure == "1D Grating":
        peak_wavelength = periodicity * (ri / 1.5)
    elif structure == "Ring Resonator":
        peak_wavelength = (2 * np.pi * ring_radius * ri) / (1 + coupling_coefficient)
    elif structure == "Fabry-Pérot Resonator":
        peak_wavelength = 2 * cavity_length * ri / (1 - mirror_reflectivity)
    elif structure == "Bragg Stack":
        peak_wavelength = 4 * layer_thickness * ri_contrast
    
    width_factor = 10 + periodicity * 0.02 if structure == "1D Grating" else 15
    reflectance = np.exp(-((wavelengths - peak_wavelength) ** 2) / (2 * width_factor ** 2))
    transmittance = 1 - reflectance

    return reflectance, transmittance, peak_wavelength

# Compute Reflectance & Transmittance
reflectance, transmittance, predicted_peak = calculate_resonance(wavelengths, selected_ri, optical_structure)

# **Plot**
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

ax1.plot(wavelengths, reflectance, color="blue", label=f"Reflectance ({selected_analyte}, RI: {selected_ri:.2f})", linewidth=2)
ax2.plot(wavelengths, transmittance, color="red", linestyle="dashed", label="Transmittance", linewidth=2)

ax1.set_xlabel("Wavelength (nm)", fontsize=14, fontweight='bold')
ax1.set_ylabel("Reflectance", fontsize=14, color='blue', fontweight='bold')
ax2.set_ylabel("Transmittance", fontsize=14, color='red', fontweight='bold')

ax1.set_title(f"Resonance Shift for {selected_analyte} ({optical_structure})", fontsize=14, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10, frameon=True)
ax1.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# **Predicted Values**
st.subheader("📊 Predicted Values")
st.write(f"🔹 **Refractive Index (RI)**: {selected_ri:.2f}")
st.write(f"🔹 **Predicted Resonance Peak**: {predicted_peak:.2f} nm")
st.success("Developed by \nAman Kumar Patel \nM.Sc. Physics(Condensed Matter Physics) \nGovernment College, Sundargarh")