# Lesson Plan Book Generator

Generates a teacher's lesson plan book for a school year from schedule data in a csv file. Uses a [jinja template](http://jinja.pocoo.org) to create a LaTeX file which can then be turned into a PDF with e.g. [pdftex](https://en.wikipedia.org/wiki/PdfTeX). 

Output is formatted for A4 paper with up to seven lessons per day and a two-week repeating schedule cycle ("A week" an "B week"). For other schedule structures the jinja template will have to be tweaked.
