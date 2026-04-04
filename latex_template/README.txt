Corbis Literature Starter Kit — LaTeX Template

A clean article template for literature reviews and research notes.
Uses natbib for citations (\citet{} and \citep{}).

Files:
  academic_paper_template.tex  — Main document
  template_references.bib      — Sample bibliography (replace with yours)

How to use:
  1. Copy this folder: cp -r latex_template/ paper/
  2. Edit academic_paper_template.tex (title, author, sections)
  3. Replace template_references.bib with your own .bib file
     (use Corbis export_citations to generate BibTeX entries)
  4. Compile: pdflatex -> bibtex -> pdflatex -> pdflatex

Requires a LaTeX distribution (MacTeX, TeX Live, or MikTeX).
