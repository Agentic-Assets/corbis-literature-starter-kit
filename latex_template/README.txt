ACADEMIC PAPER TEMPLATE

Files
-----
- academic_paper_template.tex : main LaTeX template
- template_references.bib     : sample BibTeX file
- jf.bst                      : bibliography style copied from the uploaded package
- images/                     : example figures used in the template
- academic_paper_template.pdf : compiled preview

How to reuse
------------
1. Open academic_paper_template.tex.
2. Replace the title, running title, JEL codes, keywords, and abstract.
3. Toggle the blind-review switch: set \blindfalse to show authors or \blindtrue to anonymize the title page.
4. Replace the sample section text with your paper content.
5. Replace the example tables and figures, or keep the formatting and swap in your own numbers.
6. Replace template_references.bib with your own bibliography database.

Compile
-------
pdflatex academic_paper_template.tex
bibtex academic_paper_template
pdflatex academic_paper_template.tex
pdflatex academic_paper_template.tex

Notes
-----
- The example prose, coefficients, and graphics are placeholders only.
- Figures and tables are placed after the references to mirror the source draft.
  Move them inline if your target journal prefers that layout.
