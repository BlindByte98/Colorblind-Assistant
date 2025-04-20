# Colorblind Assistant 🔍  
*A real-time color recognition tool developed by a colorblind individual for the colorblind community*  
*Displays RGB, HEX, and named color categories under the cursor using `pynput`, `mss`, and `customtkinter`*

---

## Table of Contents

- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Configuration](#configuration)  
- [Fun & Surprising Facts About Color](#fun--surprising-facts-about-color)  
- [Insights into Color and Color Blindness](#insights-into-color-and-color-blindness)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)  

---

## Features

- Real-time sampling at **60 FPS** (adjustable)  
- **Nearest color match** using perceptual HSV distance  
- **Dark/light mode** support with customizable accent color  
- Inline hotkeys: **Toggle Sampling (`Alt`)**, **Exit (`F1`)**  
- On-screen tooltip with:  
  - Color **Name**  
  - Color **Category**  
  - **RGB** and **HEX** values  

---

## Installation

*No separate `requirements.txt`. Dependencies are installed inline.*

```bash
# Clone the repository
git clone https://github.com/yourusername/colorblind-assistant.git
cd colorblind-assistant

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install pynput mss pillow customtkinter
```

---

## Usage

```bash
# Launch the application
python main.py
```

- **Hold `Alt`** — Start real-time sampling  
- **Release `Alt`** — Pause sampling  
- **Press `F1`** — Exit the application  

---

## Configuration

Edit the `APP_CONFIG` dictionary in `main.py` to customize:

- `FPS`: Sampling frame rate (default: 60)  
- `THEME_MODE`: `"dark"` or `"light"`  
- `THEME_COLOR`: e.g., `"blue"`, `"green"`  
- `HOTKEY_TOGGLE` / `HOTKEY_EXIT`: Key bindings  
- UI offsets, fonts, tooltip size, and more  

---

## Fun & Surprising Facts About Color

- **Blue Didn’t Exist (Linguistically)**  
  Some ancient cultures, like the Himba tribe in Namibia or the ancient Greeks, had no word for "blue" and likely didn't perceive it as distinct. Homer described the ocean as "wine-dark."

- **Bananas Look Red to Some Animals**  
  Under UV light, bananas appear red to animals with UV-sensitive vision, like bees or birds.

- **There's No Pink in the Spectrum**  
  Pink is a blend of red and violet—two ends of the spectrum. It doesn’t exist as a pure wavelength.

- **Octopuses Are Colorblind (Sort Of)**  
  Despite their camouflage skills, octopuses likely don’t see color the way humans do, though they may detect color via chromatic aberration.

- **Your Brain Fakes Most of What You See**  
  About 90% of color perception is cognitive interpretation. Context, memory, and lighting all affect what we perceive as color.

- **Red Enhances Physical Performance**  
  Exposure to red can temporarily boost strength and speed by increasing adrenaline.

- **Color Preferences Are Universal... and Not**  
  Blue is globally the most liked color, yellow-green the least—though culture and environment strongly influence this.

- **Goldfish See More Colors Than You**  
  Goldfish are tetrachromats, able to see UV light and a broader color spectrum than humans.

- **Some Women Are Tetrachromats**  
  A minority of women possess four cone types, potentially perceiving up to 100 million colors.

- **White Isn't Real**  
  White is a perceptual trick—your brain normalizing lighting conditions (color constancy).

---

## Insights into Color and Color Blindness

### 🧬 Evolution and Genetics

- Color vision evolved for survival—detecting food, predators, and mates.  
- Human trichromatic vision helps identify ripe fruits and foliage.  
- Color blindness is usually genetic and X-linked, affecting males more often.  

### 🎨 Historical Perspectives

- Aristotle believed all colors came from black and white, linked to the four elements.  
- Newton identified the seven spectral colors through prism experiments.  
- John Dalton, himself colorblind, proposed early (incorrect) theories about its cause.  

### 🌈 Color Perception and Phenomena

- Modern research can stimulate individual photoreceptors, revealing new colors like “olo”—a highly saturated blue-green.  
- The **trichromatic theory** (Young and Helmholtz) explains human color vision through red, green, and blue cones.  
- Color perception varies—lighting and cognitive bias cause effects like *The Dress* illusion.

### 🐾 Animal Color Vision

- Mantis shrimps have up to 16 photoreceptors, enabling detection of polarized light and a vast spectrum.  
- Animal color vision evolved for camouflage, mating, signaling, and varies widely by species.  

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

- Developed with gratitude for the colorblind community  
- Powered by Python and open-source libraries: `pynput`, `mss`, `pillow`, and `customtkinter`  
- Thanks to everyone contributing knowledge on color science and perception  
