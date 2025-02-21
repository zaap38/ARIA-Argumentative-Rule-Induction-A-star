# ARIA - Argumentative Rule Induction A-star
This project contains early-stage research code for learning argumentation-based representations of logical rules that have been inferred from data.

## Prerequisites
C++ compiler - MinGW32 was used.

## Run
Edit `main.cpp` to:
- Change the maximum number of iterations.
- Change the dataset.

Edit `dataset.h` and `dataset.cpp` if you wish to add a new dataset by:
- Setting the path to your data (all in one file).
- Setting your attribute names, as well as the label position, and ignored attributes.
  
Compile using `./makefile make` then run the generated .exe

## Authors
B. Alcaraz<br>
A. Kaliski<br>
C. Leturc<br>
