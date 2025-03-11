import streamlit as st
import subprocess
import os

st.title('Trajectory Evaluation with evo')

# File uploader
uploaded_files = st.file_uploader("Upload trajectory files", type="txt", accept_multiple_files=True)

if uploaded_files:
    output_dir = "output_plots"
    os.makedirs(output_dir, exist_ok=True)

    for uploaded_file in uploaded_files:
        # Save uploaded file to a temporary location
        file_path = os.path.join(output_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Define the output plot file path
        plot_file = os.path.join(output_dir, f"{uploaded_file.name}_plot.pdf")

        # Construct and execute the evo_traj command
        command = [
            "evo_traj", "tum", file_path,
            "--plot_mode=xy",
            "--save_plot", plot_file,
            "--silent"
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            st.success(f"Plot saved successfully: {plot_file}")
            # Display the plot
            with open(plot_file, "rb") as f:
                st.download_button(
                    label="Download plot",
                    data=f,
                    file_name=f"{uploaded_file.name}_plot.pdf",
                    mime="application/pdf"
                )
        else:
            st.error(f"Failed to process {uploaded_file.name}. Error: {result.stderr}")