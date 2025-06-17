# Skill Check - Automated Image Handling & Comparison

## 📋 Overview

This project provides a Python-based automated image handling and comparison task titled **Skill Check**. It performs operations such as loading, processing, and comparing images, while ensuring specific files are preserved or overwritten as needed. It supports integration with external image comparison tools.

---

## 🧰 System & Tool Configuration

- **Operating System:** Windows 11 Pro  
  - **Version:** 23H2  
  - **OS Build:** 22631.5335

- **Python Version:** 3.8.10

- **IDE Used:** PyCharm 2024.2.4 (Community Edition)

- **Image Comparison Tool:**  
  - **Tool:** Paint.NET  
  - **Version:** 5.1.8 (latest)  
  - **Executable Path:**  
    ```
    C:\Program Files\paint.net\PaintDotNet.exe
    ```

## 🚀 How to Run the Script

To execute the test script for image handling and validation, open your terminal or PyCharm's terminal window and run:

```bash
pytest test_skill_check_image_handling.py -s
```
📁 Project Structure
```
.
├── input/
│   ├── IMAGE1.png          # Source image
│   ├── IMAGE2.png          # Second image used for comparison
├── output/
│   ├── NEW.png             # Will be created or overwritten by the script
│   ├── EXPORT.jpg          # Preserved by the script
│   ├── diff.png            # Diff image generated (also preserved)
├── test_skill_check_image_handling.py  # Main test script
```
