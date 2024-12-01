# Intellistat for Home Assistant

The IntelliStat Home Assistant Component provides an easy-to-use interface to manage a zoned heating systems. It integrates seamlessly with your Home Assistant setup, enabling you to customize and control your heating efficiently. 

## Features

- **Zoned Heating Configuration:** Manage multiple climate controllers automatically
- **Customizable Heating Limits:** Set maximum allowable temperatures to avoid overheating.
- **Delayed Heating Start:** Specify delays to prevent frequent changes of your heating system.
- **Temperature Difference Limits:** Define maximum temperature differences to protect your heating system.
- **Input Ignoring:** Toggle a switch to ignore all inputs on the controller when needed.
- **Fallback States:** Set a fallback state for the controller to ensure minimal modulation during inactivity.

---

## Installation

Since IntelliStat is not yet available in the official HACS repository, you will need to add it manually:

1. **Install HACS (if not already installed):**
   - Visit the [HACS website](https://hacs.xyz/) for instructions on how to install HACS in your Home Assistant.

2. **Add IntelliStat to HACS:**
   - Open Home Assistant, go to **HACS**.
   - Click on **Integrations** and then **Explore & Add Repositories**.
   - Click the three dots in the top-right corner and select **Custom Repositories**.
   - Add the URL of this repository and choose **Integration** as the category.
   - Click **Add** to save.

3. **Install IntelliStat:**
   - Search for **IntelliStat** in your HACS Integrations list.
   - Click **Download** to install it.

4. **Restart Home Assistant:**
   - Once installed, restart Home Assistant to ensure the integration is properly loaded.

5. **Add IntelliStat Integration:**
   - Navigate to **Settings > Devices & Services > Add Integration**.
   - Search for **IntelliStat** and select it.

6. **Configure IntelliStat:**
   - Choose your controller and configure the following options:
     - **Maximum Temperature:** The maximum temperature the controller is allowed to heat to.
     - **Delay Start:** Delay before the heating system activates.
     - **Max Temperature Difference:** The maximum temperature variance allowed, preventing system strain.
     - **Input Ignore Switch:** Enable to override all inputs to the controller.
     - **Fallback State:** Specify the fallback state to keep the controller modulating slightly when inactive.

---

## How Zoned Heating Works

Zoned heating allows you to add multiple climate controllers, each one referring most likely to a "zone", each managed independently. With IntelliStat, you can configure multiple climate controllers to operate in harmony, ensuring optimal comfort and energy efficiency.

### Setting Up Zoned Heating with IntelliStat

1. **Add Climate Controllers:**
   - After setting up the IntelliStat integration, add all relevant climate controllers to the configuration.
  
2. **Automate Heating:**
   - Use IntelliStat to automate your climate controller based on your individual controllers

Enjoy efficient and intelligent heating with IntelliStat!
