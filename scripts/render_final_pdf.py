import subprocess
import os
import sys

def main():
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_path = None
    for p in edge_candidates:
        if os.path.exists(p):
            edge_path = p
            break
            
    if not edge_path:
        print("Error: Edge executable not found.")
        sys.exit(1)

    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_file = os.path.join(project_dir, "VELOOP_TASK01_FINAL_TECHNICAL_HANDOVER_REPORT.html")
    pdf_file = os.path.join(project_dir, "VELOOP_TASK01_FINAL_TECHNICAL_HANDOVER_REPORT.pdf")

    if not os.path.exists(html_file):
        print(f"Error: {html_file} does not exist.")
        sys.exit(1)

    html_uri = "file:///" + html_file.replace("\\", "/")
    
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_uri
    ]

    print(f"Converting {html_file} -> {pdf_file} ...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Subprocess failed:", res.stderr)
        sys.exit(1)

    if os.path.exists(pdf_file):
        size = os.path.getsize(pdf_file)
        print(f"SUCCESS: Generated {pdf_file} ({size} bytes)")
        
        # Check page count using PyPDF or fitz if available
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_file)
            print(f"Total Page Count: {len(reader.pages)}")
        except Exception as e:
            print("Note: pypdf check skipped or error:", e)

        # Copy to Desktop
        desktop_path = os.path.join(r"C:\Users\ckart\Desktop", "VELOOP_TASK01_FINAL_TECHNICAL_HANDOVER_REPORT.pdf")
        try:
            import shutil
            shutil.copy2(pdf_file, desktop_path)
            shutil.copy2(html_file, os.path.join(r"C:\Users\ckart\Desktop", "VELOOP_TASK01_FINAL_TECHNICAL_HANDOVER_REPORT.html"))
            print(f"SUCCESS: Copied PDF & HTML to Desktop: {desktop_path}")
        except Exception as e:
            print("Warning: Could not copy to desktop:", e)
    else:
        print("Error: PDF file was not generated.")
        sys.exit(1)

if __name__ == "__main__":
    main()
