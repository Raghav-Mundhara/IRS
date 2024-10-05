import os
from glob import glob
from fpdf import FPDF

# Function to convert a text file to a PDF with the same name
def text_to_pdf(text_file, output_pdf):
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font('Arial', size=12)
        
        # Open the text file
        with open(text_file, 'r') as file:
            # Read each line from the text file
            for line in file:
                # Clean line to avoid extra newlines in PDF
                line = line.strip()
                pdf.cell(200, 10, txt=line, ln=True)
        
        # Output the PDF with the same name as the text file
        pdf.output(output_pdf)
        print(f"Converted {text_file} to {output_pdf} successfully!")
    except Exception as e:
        print(f"Error converting {text_file} to PDF: {e}")

# Get all .txt files in the root folder
text_files = glob('*.txt')  # Make sure this is your root folder or adjust the path if necessary

# Check if any text files are found
if not text_files:
    print("No text files found in the directory.")
else:
    # Loop through each text file and convert it to PDF
    for text_file in text_files:
        # Create the output PDF file name (replace .txt with .pdf)
        output_pdf = text_file.replace('.txt', '.pdf')
        
        # Convert the text file to PDF
        text_to_pdf(text_file, output_pdf)

    print("All text files have been processed.")
