import tkinter as tk
from tkinter import ttk
import webbrowser

def calculate():
    try:
        lambda_val = float(lambda_entry.get())
        epsilon_val = float(epsilon_entry.get())
        power_val = float(power_entry.get())
        t90_val = float(t90_entry.get())
        
        Ephot = h * c / (lambda_val * 1e-9)  # Energy of a photon in J
        I = power_val / (1000 * Ephot * avo)  # Intensity in mol photons per second
        result = 1/(I * epsilon_val * t90_val * 1000)  # Quantum yield calculation
        
        if result < 0:
            result_label.config(text="Error: Quantum yield cannot be negative. Maybe check your units?")
            return
        
        if result < 0:
            result_label.config(text="Error: Quantum yield cannot be greater than 1. Maybe check your units?")
            return

        # Update the result in the text widget and select it to make it easy to copy
        result_entry.config(state="normal")
        result_entry.delete(0, tk.END)
        result_entry.insert(0, f"{result:.4f}")
        result_entry.select_range(0, tk.END)
        result_entry.config(state="readonly")
        
    except ValueError:
        result_entry.config(state="normal")
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "Invalid Input")
        result_entry.config(state="readonly")

def open_link(url):

    def _open_link(event):
        webbrowser.open_new(url)    
    return _open_link

# Constants
h = 6.62607015e-34  # Planck's constant in J.s
c = 3e8  # Speed of light in m/s
avo = 6.022e23  # Avogadro's number in mol^-1


# Create the main window
root = tk.Tk()
root.title("Quantum Yield Calculator v1.0")
root.geometry("800x550")
root.resizable(False, False)

try:
    # Create icon
    root.iconbitmap("phi.ico")
except tk.TclError:
    # In case the .ico file isn't found
    print("Icon file not found, using default icon")
    
# Create a frame for better organization
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# Create left frame for inputs
input_frame = ttk.Frame(main_frame, padding="20", width=200)
input_frame.pack(side="left", fill="both", expand=False)
input_frame.pack_propagate(False) 

# Create right frame for explanation
explanation_frame = ttk.LabelFrame(main_frame, text="Estimating Quantum Yield", padding="10")
explanation_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Create a Text widget for the explanation with a hyperlink
explanation_text = tk.Text(explanation_frame, wrap="word", width=30, height=12, 
                          font="TkDefaultFont", bg=root.cget("background"), 
                          relief="flat", highlightthickness=0)
explanation_text.pack(fill="both", expand=True)

# Add explanation text
explanation_text.insert("1.0", "This calculator estimates quantum yield using the derivation originally described in ")
explanation_text.insert("end", "Parker, 1956", "hyperlink1")
explanation_text.insert("end", " and more clearly explained in ")
explanation_text.insert("end", "Bader et al., 2019", "hyperlink2")
explanation_text.insert("end", ". \n\n")
explanation_text.insert("end", "Quantum yield (Φ) is a ratio representation of photon conversion efficiency (via fluorescence, bond breaking, etc).\n\n")
explanation_text.insert("end", "Φ = number of reaction events/number of photons absorbed\n\n", "formula_center")
explanation_text.insert("end", u"As long as the photoreaction follows first-order kinetics with rate constant k [s\u207B\u00b9], quantum yield can be expressed as:\n\n")
explanation_text.insert("end", "Φ = k/Iε\n\n", "formula_center")
explanation_text.insert("end", u"where Iε is the moles of incident photons multiplied by the extinction coefficient. k must be converted to k' to match the log\u2081\u2080 units of absorbance:\n\n")
explanation_text.insert("end", "k' = k/2.303\n\n", "formula_center")
explanation_text.insert("end", u"k' is the same as 1/t90 (obtained by solving for t\u2089\u2080 in the first order reaction equation). Substituting this relationship into the equation for Φ gives:\n\n")
explanation_text.insert("end", u"Φ = (Iεt\u2089\u2080)\u207B\u00b9\n", "formula_center")

parker_url = "https://royalsocietypublishing.org/doi/10.1098/rspa.1956.0102"
bader_url = "https://pubs.acs.org/doi/10.1021/acs.joc.9b02751"

# Configure the hyperlinks
explanation_text.tag_configure("hyperlink1", foreground="blue", underline=1)
explanation_text.tag_bind("hyperlink1", "<Button-1>", open_link(parker_url))

explanation_text.tag_configure("hyperlink2", foreground="blue", underline=1)
explanation_text.tag_bind("hyperlink2", "<Button-1>", open_link(bader_url))

# Configure justification for formulas
explanation_text.tag_configure("formula_center", justify="center")

# Make the Text widget read-only
explanation_text.config(state="disabled")

# Create input fields with labels
ttk.Label(input_frame, text="Wavelength (nm)").grid(row=0, column=0, sticky="w", pady=5)
lambda_entry = ttk.Entry(input_frame, width=15)
lambda_entry.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(input_frame, text=u"Extinction coefficient (M\u207B\u00b9cm\u207B\u00b9)").grid(row=1, column=0, sticky="w", pady=5)
epsilon_entry = ttk.Entry(input_frame, width=15)
epsilon_entry.grid(row=1, column=1, pady=5, padx=5)

ttk.Label(input_frame, text=u'Power (mWcm\u207B\u00b2)').grid(row=2, column=0, sticky="w", pady=5)
power_entry = ttk.Entry(input_frame, width=15)
power_entry.grid(row=2, column=1, pady=5, padx=5)

ttk.Label(input_frame, text=u't\u2089\u2080').grid(row=3, column=0, sticky="w", pady=5)
t90_entry = ttk.Entry(input_frame, width=15)
t90_entry.grid(row=3, column=1, pady=5, padx=5)

# Create calculate button
calculate_button = ttk.Button(input_frame, text="Calculate", width=43, command=calculate)
calculate_button.grid(row=4, column=0, columnspan=2, pady=15)

# Create result label
result_label = ttk.Label(input_frame, text="Quantum Yield: ")
result_label.grid(row=5, column=0, sticky="w", pady=5)

# Create a read-only Entry widget for the result that can be copied
result_entry = ttk.Entry(input_frame, width=15)
result_entry.grid(row=5, column=1, sticky="w", pady=5, padx=5)
result_entry.config(state="readonly")  # Makes it non-editable but selectable/copyable

# Add a "Copy Result" button (optional)
copy_button = ttk.Button(input_frame, text="Copy Result", command=lambda: copy_result(result_entry.get()))
copy_button.grid(row=5, column=2, columnspan=1, sticky="e", pady=5)

# Function to copy result to clipboard
def copy_result(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Required to finalize clipboard change

# Start the main loop
root.mainloop()