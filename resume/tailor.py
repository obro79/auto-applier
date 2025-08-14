# file: tailor.py
import re
import subprocess
from pathlib import Path
import requests

from prompts import RESUME_PROMPT, START_OF_RESUME, END_OF_RESUME, LATEX_PROMPT, COVER_LETTER_PROMPT, COVER_LETTER
from apply.apply import fetch_job_description

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
REQUEST_TIMEOUT = (30.0, 300.0)
RETRY_COUNT = 2

def tailor_resume(company_name: str, job_title: str, job_description: str) -> str:
    """
    Compose a job-specific resume by:
      1) Filling the base prompt with job/company details.
      2) Asking Ollama to produce content.
      3) Passing that content through a LaTeX cleanup/refinement prompt.
      4) Wrapping the result with START_OF_RESUME/END_OF_RESUME so it's a full TeX doc.

    Returns a FULL LaTeX document string (with preamble/macros supplied by START/END).
    """
    role = f"{job_title} at {company_name} {job_description}"
    prompt = RESUME_PROMPT.replace("<<JOB_DESCRIPTION>>", role)

    raw = prompt_ollama(prompt)
    cleaned = extract_resume_section(raw)
    #cleaned = extract_resume_section(raw)

    return (START_OF_RESUME + cleaned + END_OF_RESUME).replace('"""', '')

def clean_output(response: str, model: str = "llama3.1", prompt: str = LATEX_PROMPT, error="") -> str:
    """
    Feed the model's first response into a LaTeX-shaping prompt.
    Returns the LaTeX *body*
    """
    payload = {"model": model, "prompt": prompt + response + error, "stream": False}
    resp = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    latex_body = data.get("response", "").strip()
    if not latex_body:
        raise RuntimeError("Empty response from the model during LaTeX cleanup.")
    return latex_body

def prompt_ollama(prompt: str, model: str = "llama3.1") -> str:
    """Single pass to Ollama; returns raw LLM text."""
    payload = {"model": model, "prompt": prompt, "stream": False}
    resp = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    text = data.get("response", "")
    if not text:
        raise RuntimeError("Empty response from the model.")
    return text

def latex_to_pdf(tex_path: str | Path = "resume.tex", retry_count=RETRY_COUNT) -> Path:
    """
    Compile LaTeX to PDF using Tectonic.
    Requires Tectonic to be installed and on PATH.
    """
    tex_path = Path(tex_path)
    while retry_count:
        retry_count -= 1
        try:
            subprocess.run(["tectonic", str(tex_path)], check=True)
            #subprocess.run(["tectonic", "-X", "compile", str(tex_path)], check=True)
        except subprocess.CalledProcessError as e:

            tex_path = llm_response_to_latex(clean_output(tex_path + LATEX_PROMPT + e))
    return tex_path.with_suffix(".pdf")

def extract_resume_section(text: str) -> str:
    """
    helper to pull just the section between custom markers.
    Raises if not found.
    """
    m = re.search(r"(\\resumeSubHeadingListStart.*?\\resumeSubHeadingListEnd)", text, re.DOTALL)
    if not m:
        raise ValueError("Resume section not found in text.")
    return m.group(1)

def extract_coverletter_section(text: str) -> str:
    m = re.search(r"(?s)(\\documentclass\[11pt\]\s*\{article\}.*?\\end\{document\})", text)
    if not m:
        raise ValueError("Cover letter section not found in text.")
    return m.group(1)


def llm_response_to_latex(full_document_tex: str, output_file: str | Path = "resume.tex") -> Path:
    """
    Write the FULL LaTeX document to disk (preamble and body).
    """
    out_path = Path(output_file)
    out_path.write_text(full_document_tex, encoding="utf-8")
    return out_path

def get_tailored_resume(url: str):
    """Stub for future: fetch JD from URL and call tailor_resume()."""
    jd = fetch_job_description(url)
    resume_tex = tailor_resume("Google", "Software Engineer", jd)
    tex_path = llm_response_to_latex(resume_tex)
    pdf_path = latex_to_pdf(tex_path)
    print(f"Wrote PDF: {pdf_path}")

def tailor_cover_letter(prompt=COVER_LETTER_PROMPT,job_description="", model="llama3.1", example_cover_letter=COVER_LETTER):
    prompt = prompt.replace("<<COVER_LETTER_EX>>",example_cover_letter)
    prompt = prompt.replace("<<JOB_DESCRIPTION>>",job_description)
    raw_response = prompt_ollama(prompt)
    cleaned_response = extract_coverletter_section(raw_response)
    print(cleaned_response)

    llm_response_to_latex(cleaned_response, "coverletter.tex")

    latex_to_pdf("coverletter.tex")

if __name__ == "__main__":
    url="https://rbcborealis.com/program-applications/winter-2026-ml-researcher-internship/"
    #get_tailored_resume(url)
    tailor_cover_letter()


## TODO 1. save resume as role, company, name 2. make cover letter too, 3. be able to do it a list of links


