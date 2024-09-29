# Save this code in a file named 'streamlit_app.py'

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Set up the Streamlit app
def main():
    st.title('Exciton and Biexciton Intensity Spectra')
    
    # Sidebar for parameter inputs
    st.sidebar.header('Adjustable Parameters')
    
    # Constants with sliders
    E_X = st.sidebar.slider('Exciton Energy (E_X) [eV]', 1.0, 2.0, 1.5, 0.01)
    E_XX = st.sidebar.slider('Biexciton Energy (E_XX) [eV]', 1.0, 2.5, 1.8, 0.01)

    # Fixed energy range
    E_min = st.sidebar.slider('Energy Range Min [eV]', 0.8, 1.5, 1.2, 0.1)
    E_max = st.sidebar.slider('Energy Range Max [eV]', 1.8, 2.5, 2.0, 0.1)
    E = np.linspace(E_min, E_max, 1000)

    Gamma_X = st.sidebar.slider('Exciton Linewidth (Gamma_X) [eV]', 0.01, 0.1, 0.05, 0.005)
    Gamma_XX = st.sidebar.slider('Biexciton Linewidth (Gamma_XX) [eV]', 0.01, 0.1, 0.05, 0.005)
    
    fixed_FSS_meV = st.sidebar.slider('Fine Structure Splitting (FSS) [meV]', 0.0, 100.0, 30.0, 1.0)
    fixed_FSS = fixed_FSS_meV * 1e-3  # Convert to eV

    
    # Polarizer angles and power levels
    st.sidebar.subheader('Polarizer Angles and Power Levels')
    
    # Polarizer angles
    num_angles = st.sidebar.slider('Number of Polarizer Angles', 3, 20, 7)
    polarizer_angles_deg = np.linspace(0, 90, num_angles)
    polarizer_angles_rad = np.deg2rad(polarizer_angles_deg)
    
    # Power levels
    num_powers = st.sidebar.slider('Number of Power Levels', 2, 10, 5)
    max_power = st.sidebar.number_input('Maximum Power Level', 1.0, 100.0, 10.0, 1.0)
    power_levels = np.linspace(1.0, max_power, num_powers)
    
    # Fixed parameters for plotting
    fixed_power = st.sidebar.slider('Fixed Power for Angle Variation', 1.0, max_power, 10.0, 1.0)
    fixed_angle_deg = st.sidebar.slider('Fixed Polarizer Angle for Power Variation', 0.0, 90.0, 45.0, 1.0)
    fixed_angle_rad = np.deg2rad(fixed_angle_deg)
    
    # Proportionality constants
    k_alpha = 1.0  # For exciton intensity
    k_beta = 0.1   # For biexciton intensity
    
    # Define Lineshape Function (Lorentzian)
    def lorentzian(E, E0, Gamma):
        return (Gamma / 2)**2 / ((E - E0)**2 + (Gamma / 2)**2)
    
    def generate_spectrum(E, E_X, E_XX, Delta, Gamma_X, Gamma_XX, theta, alpha=1.0, beta=1.0):
        if Delta == 0:
            I_X = alpha * lorentzian(E, E_X, Gamma_X)
        else:
            I_X = alpha * (
                (np.cos(theta)**2 * lorentzian(E, E_X + Delta / 2, Gamma_X)) +
                (np.sin(theta)**2 * lorentzian(E, E_X - Delta / 2, Gamma_X))
            )
        I_XX = beta * (
            (np.sin(theta)**2 * lorentzian(E, E_XX + Delta / 2, Gamma_XX)) +
            (np.cos(theta)**2 * lorentzian(E, E_XX - Delta / 2, Gamma_XX))
        )
        I_total = I_X + I_XX
        return I_total, I_X, I_XX
    
    # Create plots
    fig, axs = plt.subplots(1, 2, figsize=(20, 10), sharex=True, sharey=True)
    
    # Plot 1: E vs I for varying angle, at fixed power
    alpha_fixed_power = k_alpha * fixed_power
    beta_fixed_power = k_beta * fixed_power**2
    
    cmap1 = plt.get_cmap('viridis')
    ax1 = axs[0]
    
    for i, (theta_deg, theta_rad) in enumerate(zip(polarizer_angles_deg, polarizer_angles_rad)):
        I_total, _, _ = generate_spectrum(
            E=E,
            E_X=E_X,
            E_XX=E_XX,
            Delta=fixed_FSS,
            Gamma_X=Gamma_X,
            Gamma_XX=Gamma_XX,
            theta=theta_rad,
            alpha=alpha_fixed_power,
            beta=beta_fixed_power
        )
        ax1.plot(E, I_total, label=f'θ = {theta_deg:.1f}°', color=cmap1(i / (len(polarizer_angles_deg) - 1)))
    
    ax1.set_title(f'Intensity vs Energy\nVarying Polarizer Angles (Power = {fixed_power})')
    ax1.set_xlabel('Energy (eV)')
    ax1.set_ylabel('Intensity (a.u.)')
    ax1.legend(fontsize='small')
    ax1.grid(True)
    ax1.set_xlim(E_min, E_max)
    
    # Plot 2: E vs I for varying power, at fixed angle
    cmap2 = plt.get_cmap('plasma')
    ax2 = axs[1]
    
    for i, P in enumerate(power_levels):
        alpha = k_alpha * P
        beta = k_beta * P**2
    
        I_total, _, _ = generate_spectrum(
            E=E,
            E_X=E_X,
            E_XX=E_XX,
            Delta=fixed_FSS,
            Gamma_X=Gamma_X,
            Gamma_XX=Gamma_XX,
            theta=fixed_angle_rad,
            alpha=alpha,
            beta=beta
        )
        ax2.plot(E, I_total, label=f'Power = {P:.1f}', color=cmap2(i / (len(power_levels) - 1)))
    
    ax2.set_title(f'Intensity vs Energy\nVarying Power Levels (Angle = {fixed_angle_deg}°)')
    ax2.set_xlabel('Energy (eV)')
    # ax2.set_ylabel('Intensity (a.u.)')  # Y-axis label shared with the first subplot
    ax2.legend(fontsize='small')
    ax2.grid(True)
    ax2.set_xlim(E_min, E_max)
    
    plt.tight_layout()
    
    # Display the plots in Streamlit
    st.pyplot(fig)
    
if __name__ == "__main__":
    main()