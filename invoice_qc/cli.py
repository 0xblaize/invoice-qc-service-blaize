import typer
import json
import os
from .extractor import parse_invoice
from .validator import validate_invoice
from .models import Invoice

app = typer.Typer()

@app.command()
def extract(pdf_dir: str, output: str = "extracted.json"):
    data = []
    for f in os.listdir(pdf_dir):
        if f.endswith(".pdf"):
            path = os.path.join(pdf_dir, f)
            inv = parse_invoice(path)
            # mode='json' converts dates to strings automatically
            data.append(inv.model_dump(mode='json'))
    with open(output, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Extracted to {output}")

@app.command()
def validate(input_json: str, report: str = "report.json"):
    with open(input_json, "r") as f:
        raw_data = json.load(f)
    results = []
    for item in raw_data:
        inv_obj = Invoice(**item)
        res = validate_invoice(inv_obj)
        # mode='json' converts dates to strings automatically
        results.append(res.model_dump(mode='json'))
    with open(report, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Report saved to {report}")

@app.command()
def full_run(pdf_dir: str, report: str = "final_report.json"):
    results = []
    for f in os.listdir(pdf_dir):
        if f.endswith(".pdf"):
            print(f"Processing {f}...")
            path = os.path.join(pdf_dir, f)
            inv = parse_invoice(path)
            res = validate_invoice(inv)
            # FIX: Added mode='json' here to handle dates correctly
            results.append(res.model_dump(mode='json'))
    with open(report, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Full run complete! Saved to {report}")

if __name__ == "__main__":
    app()