import requests
import subprocess
from pathlib import Path
from prompts import RESUME_PROMPT, START_OF_RESUME

def tailor_resume(company_name: str, job_title: str, job_description: str) -> str:
    role = f"{job_title} at {company_name} " + job_description
    prompt = RESUME_PROMPT.replace("<<JOB_DESCRIPTION>>", role)
    text = prompt_ollama(prompt)
    return START_OF_RESUME + text

def prompt_ollama(prompt: str, model: str = "llama3.1") -> str:
    url = "http://127.0.0.1:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json().get("response", "")

def llm_response_to_latex(response: str, output_file: str | Path = "resume.tex") -> Path:
    out_path = Path(output_file)
    out_path.write_text(response.replace('"""', ''), encoding="utf-8")
    return out_path

def latex_to_pdf(tex_path: str | Path = "resume.tex") -> Path:
    tex_path = Path(tex_path)
    subprocess.run(["tectonic", str(tex_path)], check=True)
    return tex_path.with_suffix(".pdf")

if __name__ == "__main__":
    resume_str = tailor_resume("Google", "Software Engineer", "writes c++ code")
    tex_path = llm_response_to_latex(resume_str)
    pdf_path = latex_to_pdf(tex_path)
    print(f"Wrote PDF: {pdf_path}")
