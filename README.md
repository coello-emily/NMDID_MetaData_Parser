# NMDID Metadata Parser

## Project Overview

The goal of this Python project is to develop a reliable and reusable codebase capable of parsing complex metadata from the New Mexico Decedent Imaging Database (NMDID). This metadata is densely structured, making manual parsing impractical. The objective is to automate the process using Python to efficiently extract and analyze relevant medical data.

This repository serves as the central location for all scripts, documentation, and output related to the parsing and analysis of the NMDID metadata. 

## About the Data

- The dataset includes **3 zip files**, which collectively contain **1,145 patient metadata files** in `.csv` format.
- These metadata files are detailed and structured based on a **data dictionary** available under NMDID Reference Documents.
- The dataset was shared via email and uploaded to the MS Teams chat under the **General** tab, in a folder named **Python Project**.

## Requirements

The final deliverable must:

1. **Consolidate Data**  
   - Automatically stitch together all individual `.csv` metadata files into a single master DataFrame using `pandas`.
   
2. **Preserve Original Files**  
   - Copy all files before processing. Do not modify or delete the originals.

3. **Keyword-Based Parsing**  
   - Implement medical history parsing through keyword matching (or equivalent parsing methods).

4. **Exclusion Filtering**  
   - Exclude specific entries based on exclusion criteria defined in the dataset.

5. **Data Visualization**  
   - Generate medically relevant visualizations using a Python plotting library (e.g., `matplotlib` or `plotly`).

6. **Version Control**  
   - All work must be committed to a **private GitHub repository**, to be shared with the client upon completion.

7. **Documentation**  
   - Include:
     - A complete `README.md` file (this document)
     - Thorough in-code commenting and docstrings
     - A clear and organized file structure

8. **Final Presentation**  
   - Create and present a PowerPoint outlining:
     - Research and methodology
     - Division of labor
     - Live demonstration of the program
     - Known limitations and potential future improvements

9. **Client Communication**  
   - The client, **Sheridan Perry**, should only be contacted for clarification of requirements—not for troubleshooting or development help.

10. **Progress Updates**  
    - This project is exempt from weekly task updates. Instead:
      - **Emily Coello** (mentor/advisor) will provide updates in her weekly reports or meeting summaries.
      - A short update (5–7 minutes) will be delivered during weekly meetings.

11. **Project Management**  
    - Use project planning tools (e.g., ClickUp, Notion, Excel) for workload delegation.
    - Use a dedicated **MS Teams channel** for internal team communication.

12. **Due Date**  
    - The final project is tentatively due on **June 23, 2025**.

## Team & Roles

- **Mentor/Supervisor:** Emily Coello
- **Team Members:** Danny Charpentier, Ruben Nunez Silvera, and Jack Jordan
- **Client:** Sheridan Perry  
- **Internal communication** and **division of labor** are to be decided by the team.

---
## Syntax Confusion
If you are confused on any syntax, especially in GitHub, I recommend using this link:
(https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
This link will teach you the quicks bits about GitHub's special Markdown stuff (like the important, warning, and other boxes). More questions can go straight to me!

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/your-private-org/nmdid-metadata-parser.git
   cd nmdid-parser

