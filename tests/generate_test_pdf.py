from fpdf import FPDF

# Create a sample market report PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(40, 10, "EcoTech Solutions - 2025 Market Report")
pdf.ln(20)

pdf.set_font("Arial", "B", 12)
pdf.cell(40, 10, "Executive Summary")
pdf.ln(10)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 5, "EcoTech Solutions has seen a 25% year-over-year revenue increase due to the success of their solar-cell glass panels. The company currently dominates the mid-sized commercial building retrofit market but faces significant competition from low-cost imports from East Asia.")
pdf.ln(5)

pdf.set_font("Arial", "B", 12)
pdf.cell(40, 10, "Key Strengths")
pdf.ln(10)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 5, "- Proprietary 'SolarGlass' technology with 22% efficiency.\n- Exclusive 5-year partnership with the Global Green Building Council.\n- Strong R&D team with 15+ patents in thin-film photovoltaics.")
pdf.ln(5)

pdf.set_font("Arial", "B", 12)
pdf.cell(40, 10, "Challenges and Risks")
pdf.ln(10)
pdf.set_font("Arial", "", 10)
pdf.multi_cell(0, 5, "- High manufacturing costs compared to traditional solar panels.\n- Limited presence in the residential market.\n- Recent supply chain disruptions in silicon carbide sourcing.")

pdf.output("sample_report.pdf")
print("PDF generated: sample_report.pdf")
