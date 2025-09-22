# MasterThesis

A repository containing the materials for the Master’s thesis submitted to the Technical University of Munich (TUM).

---

## Table of Contents

- [Overview](#overview)  
- [Contents](#contents)  
- [How to Use](#how-to-use)  
- [Setup & Requirements](#setup--requirements)  
- [Structure](#structure)  
- [License](#license)  
- [Contact](#contact)  

---

## Overview

This repo houses everything related to the Master's thesis project including the thesis manuscript, presentation materials, experimental code and demos, and supporting files like bibliography. The primary purpose is to collect all artifacts of the thesis in one place for version control, reproducibility, and dissemination.

---

## Contents

Here is a high-level look at what is inside:

| Folder / File | Description |
|---------------|-------------|
| `thesis formatting` | Templates, LaTeX and .pdf files, style files etc., used for writing and formatting the thesis. The formatting is used for Latex projects. Courtesy of TUM. |
| `Qiskit setup and demos` | Code notebooks / scripts for quantum computing demos using Qiskit. Contains setiing up qiskit, and introducing circuits, gates and measurements. |
| `PPT folder` | Presentation slides for defense or progress reports. Contains the final work itself. |
| `Bibliography` | Reference files (BibTeX, etc.) and related citation management. |
| `KBtoTN` | Basic files needed for the thesis. All the mapping modules, amplitude amplification implementation, plotting algorithms. The whole procedure itself houses all the previously mentioned primitives, and is included in this folder. |
| `dump` | Miscellaneous files, old versions, or data that don’t fit neatly elsewhere. Usually deleted in a monthly (or so) basis. |

---

## Structure

The directory structure is (including sub-folders and file extensions):

```

MasterThesis/
├── Bibliography/
    ├── .pdf and .nbib files
├── KBtoTN/
    ├── .png and .ipynb files
├── PPT folder/
    ├── ToDo notelist
    ├── .pdf files for describing the assingment and for the roadmap, as well as presenting the results
    ├── THESIS/
        ├── All the formatting files and the final work (.pdf) itself
        ├──pics/
            ├── .png and .jpg files for the thesis
├── Qiskit setup and demos/
    ├── Q programming - IBM
        ├── Basics of qiskit with circuits, gates, measurements -- .ipynb
    ├── TNReason Demos
        ├── Notebooks for demonstrating TNReason nomenclature and module workflows -- .ipynb
    ├── Tutorials
        ├── The two primitives together in a collective of notebooks showcasing the fit and possibilities with basic demos and assignments -- .ipynb
├── thesis formatting/
    ├── the complete fileset for the thesis formatting in use. Also included in '/PPT folder/THESIS/'
├── dump/
    ├── dump files -- soon to be deleted

```

- **Codes and jupyter notebooks** are under `KBtoTN` folder (as in Knowledge Base to Tensor Networks).
- The **fileset for the thesis formatting** is included under `thesis formatting` as well as within `/PPT folder/THESIS/`.  
- **Demos** are in `Qiskit setup and demos` & possibly in `HUBOQUBO` / `KBtoTN`.  
- **Presentations, main manuscript and formatted thesis** are in the `PPT folder`.  
- **Supporting references** are stored in `Bibliography`.  

---

## Setup & Requirements

Steps / requirements for running the code and generating quantum circuits from TNReason suitable knowledge bases (propositional logical formulas):

1. Install Python (version used in this work: 3.9.x)  
2. Use a virtual environment (venv or conda)  
3. Install dependencies, probably including `qiskit`, `numpy`, `scipy` and of course `TNReason`.  
4. Jupyter / JupyterLab to view notebooks  


---

## How to Use

- **Reading the thesis manuscript**: go to the `thesis formatting` folder, open the compiled PDF (if available), or build from source (LaTeX etc.).  
- **Running demos**: use notebooks in `Qiskit setup and demos`. Follow any instructions, ensure required packages are installed.  
- **Presenting**: the `PPT folder` has slides ready for defense / seminars.  

---


## Contact

For questions, feedback, or collaboration, please contact:

**Author**: Simon Botond 
**Email**: ipobobo66@gmail.com
