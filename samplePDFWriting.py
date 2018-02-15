import fpdf

pdf = fpdf.FPDF(format='letter')
pdf.add_page()
pdf.set_font("Arial", size=12)
#pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
#pdf.cell(200,10,'Powered by FPDF',0,1,'C')
pdf.write(0,'Maria Lol Lanchex Labexude')
pdf.write(0,'ACTURA')
pdf.write(18,'Odontologa')

pdf.output("tutorial.pdf")
