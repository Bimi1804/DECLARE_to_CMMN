# DECLARE to CMMN Converter
Code for Business Process Analytics course

This code is for the course "0822 - Business Process Analytics" at Wu Vienna in the winter semester 2021/2022.

The code takes a DECLARE model as .decl and outputs a CMMN model as .cmmn
The script was tested with RuM (as the source of .decl) and Camunda v3.6 (as the editor for the .cmmn)

Creator: Markus Bimassl


Files:
- DECL_to_CMMN.py : The actual script that takes the content from "input.decl" and writes to "output.cmmn"
- input.decl      : Store the code for the DECLARE model that you want to transform
- output.cmmn     : The resulting code for the CMMN model is written to this file
- xml_components.py : Some static components of the .cmmn that are imported into "ECL_to_CMMN.py"
