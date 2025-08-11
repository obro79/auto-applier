RESUME_PROMPT = r"""
System: You are a precise LaTeX resume editor.

Task:
- Modify ONLY the Technical Projects bullets to match the job. Do NOT change Technical Skills or any other section.
- Keep exactly 18 bullets across all projects (the total count of \resumeItem lines must equal 18 NO MORE THAN 18)
- Each bullet ≤110 visible characters (ignore LaTeX markup). Prefer “I did X to solve Y, resulting in Z” with metrics.
- Bold at most 1–2 key terms per bullet using \textbf{}.
- Do not invent technologies that aren’t listed in PROJECT_DESCRIPTIONS.
- Output ONLY the rewritten Technical Projects block as LaTeX; no commentary or extra text.

### PROJECT_DESCRIPTIONS
Smart Grocery Saver Web App — Java, Node.js (Express, Mongoose, MongoDB), React. Compares local store prices for list-based savings; itemized transparency; Git; IntelliJ.
Pantry Pal — React + Flask + SQLite. OpenAI API parses receipts; auto pantry population & expiry tracking; recipe suggestions for soon-to-expire items.
Financely — Next.js (TypeScript), Tailwind, shadcn UI. Appwrite auth/data; Plaid bank linking; Dwolla ACH; CI/CD (Vercel); Sentry; Chart.js.
PrepMe — Next.js/React/TS. Vapi SDK voice; Firebase auth; AI question gen/analysis; live transcription; call state handling.
Option Pricing & Portfolio — Python/Streamlit. Black–Scholes, Monte Carlo; pandas/numpy/matplotlib; yfinance; interactive risk viz and parameter sweeps.
Staff Scheduler — Java + Google OR-Tools (MILP). Automates 500+ weekly shifts; roles/availability constraints; GUI; logging; MVC/Observer/Singleton; high JUnit coverage.
RL Trading — Python/PyTorch with PPO/A2C; custom Gym env modeling transaction costs; yfinance pipeline; Streamlit performance dashboards.
XGBoost Forecasting — Python + XGBoost; NumPy indicators; MAE 1.5, MRE ~1%; 20y backtests vs. buy-and-hold; Streamlit viz.

### CURRENT_TECHNICAL_PROJECTS
\resumeSubHeadingListStart

  \resumeProjectHeading
  {\textbf{Bayesian Gaussian Process Modeling of SPY Implied Volatility}$|$\href{https://www.notion.so/Bayesion-Non-Parametric-Model-Paper-206b9c270459808bb413dadf3f9126eb}{\underline{Paper}}$|$
  \emph{Stan, R, Python}}{}
  \resumeItemListStart
      \resumeItem{Built Bayesian GP model in Stan for SPY IV surfaces with linear mean and Matérn 3/2 kernel.}
      \resumeItem{Optimized MCMC via blocked Gibbs \& Elliptical Slice Sampling with $k=20$, reducing complexity to $\mathcal{O}(Nk^2)$.}
      \resumeItem{Generated out-of-sample forecasts with $<4\%$ error, enhancing option pricing and risk management.}
  \resumeItemListEnd

  \resumeProjectHeading
  {\textbf{Orderbook Engine} {\underline{Github}}$|$ \emph{C++, STL}}{}
  \resumeItemListStart
    \resumeItem{Built an in-memory limit order book supporting GTC \& FAK orders with $O(\log n)$ complexity.}
    \resumeItem{Implemented real-time bid/ask aggregation using C++17 lambdas and STL algorithms for analytics.}
    \resumeItem{Created unit-test suite and VS integration, ensuring robust order-matching logic.}
  \resumeItemListEnd

  \resumeProjectHeading
  {\textbf{Reinforcement Learning Trading Strategy} \href{https://github.com/obro79/RL-trading-strat?tab=readme-ov-file}{\underline{Github}}$|$\href{https://rl-trading-strat.streamlit.app}{\underline{Live Demo}}$|$\emph{Python, PyTorch, Gymnasium}}{}
  \resumeItemListStart
     \resumeItem{Trained PPO and A2C agents in a custom Gym trading environment for transaction cost modeling.}
     \resumeItem{Built a data pipeline using yfinance and pandas to engineer OHLCV features and indicators for agent inputs.}
     \resumeItem{Developed a Streamlit dashboard for visualization of agent performance, indicator trends, and backtest metrics.}
  \resumeItemListEnd

  \resumeProjectHeading
  {\textbf{Stock Price Forecasting with XGBoost}
  \href{https://github.com/obro79/arima}{\underline{Github}}$|$\emph{Python, NumPy, Scikit-Learn, Matplotlib}}{}
  \resumeItemListStart
      \resumeItem{Built \textbf{XGBoost} model on yfinance data with engineered NumPy indicators; achieved MAE 1.5 and MRE 1\%.}
      \resumeItem{Backtested signals over 20 years to compare ROI vs.\ buy-and-hold, guiding model refinements.}
      \resumeItem{Created Streamlit dashboard for prediction visualization, indicator plots, and strategy metrics.}
      \resumeItem{Analyzed tree-based model limits in capturing long-term trends, prompting advanced ML exploration.}
  \resumeItemListEnd

  \resumeProjectHeading
  {\textbf{Financely}
  \href{https://github.com/obro79/financely}{\underline{Github}}$|$\href{https://financely-nine.vercel.app/sign-in}{\underline{Live Demo}}$|$\emph{Node.js, Next.js, React, Tailwind CSS}}{}
  \resumeItemListStart
    \resumeItem{Configured Vercel \textbf{CI/CD} pipeline to auto-build/test/deploy, cutting manual steps 75\%.}
    \resumeItem{Built ETL services in Python/Node to load transactions into SQL, boosting reporting speed 40\%.}
    \resumeItem{Implemented Cypress tests, ensuring \textbf{100\%} sandbox pass with zero integration failures.}
  \resumeItemListEnd

  \resumeProjectHeading
  {\textbf{Option Pricing \& Portfolio Management Web App} \href{https://github.com/obro79/optionStrategyApp}{\underline{Github}}$|$ \emph{Python, NumPy, Pandas, Matplotlib}}{}
  \resumeItemListStart
    \resumeItem{Implemented Black-Scholes and Monte Carlo models; accelerated pricing loops by 4x.}

    \resumeItem{Achieved 98\% PyTest coverage; CI on Linux verifies every commit before merge.}
  \resumeItemListEnd

\resumeSubHeadingListEnd

### JOB_DESCRIPTION
<<JOB_DESCRIPTION>>

### OUTPUT_FORMAT
Return exactly one fenced block:

### OUTPUT_TECHNICAL_PROJECTS
<full LaTeX for the projects list: \resumeSubHeadingListStart ... \resumeSubHeadingListEnd, totaling 18 \resumeItem bullets>

End.
"""

START_OF_RESUME = r"""\documentclass[letterpaper,11pt]{article}

% ---------- Packages ----------
\usepackage[dvipsnames]{xcolor}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage[left=.95in, right=1.1in, bottom=.25in, includehead, headheight=0pt]{geometry}
\usepackage[
  colorlinks=true,
  urlcolor=black,
  linkcolor=black,
  citecolor=black,
  pdfborder={0 0 0}
]{hyperref}
\usepackage{url}

% ---------- Global settings ----------
\emergencystretch=2em
\sloppy

% List spacing — ultra compact (kills white space around bullets)
\setlistdepth{6}
\renewlist{itemize}{itemize}{6}
\setlist[itemize]{label=\textbullet,leftmargin=*,itemsep=0pt,topsep=0pt,parsep=0pt,partopsep=0pt}
\setlist[enumerate]{leftmargin=*,itemsep=0pt,topsep=0pt,parsep=0pt,partopsep=0pt}

% ---------- Page style ----------
\urlstyle{same}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\headsep}{0.18in} % small but readable

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-0.9in}
\addtolength{\textheight}{0.0in}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% ---------- Section formatting (tighten space under headers) ----------
\titlespacing*{\section}{0pt}{6pt}{8pt}
\titleformat{\section}{
  \scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-6pt}]

% ---------- Custom commands ----------
\newcommand{\resumeItem}[1]{\item\small{{#1}}}
\newcommand{\resumeSubheading}[4]{
  \item
  \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
    \textbf{#1} & #2 \\
    \textit{\small #3} & \textit{\small #4} \\
  \end{tabular*}
}
\newcommand{\resumeSubSubheading}[2]{
  \item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \textit{\small #1} & \textit{\small #2} \\
  \end{tabular*}
}
\newcommand{\resumeProjectHeading}[2]{
  \item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \small #1 & #2 \\
  \end{tabular*}
}
\newcommand{\resumeSubItem}[1]{\resumeItem{#1}}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.12in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}}

% ---------- Document start ----------
\begin{document}

% ---------- Header ----------
\begin{flushleft}
{\huge\bfseries Owen Fisher}\\[-0.1em]
\href{https://owen-portfolio-git-main-owens-projects-e5b63a60.vercel.app/}{Portfolio}\,$|$\,%
\href{https://www.linkedin.com/in/fisherowen}{LinkedIn}\,$|$\,%
\href{https://github.com/obro79}{GitHub}\,$|$\,%
\href{mailto:owenfisher46@gmail.com}{OwenFisher46@gmail.com}\,$|$\,778--700--5680
\end{flushleft}
\vspace{-10pt}

% ---------- Education ----------
\section{\textcolor{Plum}{Education}}
\resumeSubHeadingListStart
  \resumeSubheading
  {The University of British Columbia}{\textbf{Vancouver, BC}}
  {\textbf{B.Sc., Math, Minor Computer Science} (GPA: 3.7/4.0)}{Expected Graduation: May 2027}
  \resumeItemListStart
    \resumeItem{Coursework: Software Engineering, Probability, DSA, Stochastic Processes, Machine Learning}
  \resumeItemListEnd
\resumeSubHeadingListEnd

% ---------- Technical Skills ----------
\section{\textcolor{Plum}{Technical Skills}}
\textbf{Languages}: Python (NumPy, Pandas, Matplotlib), C++, Java, R, PostgreSQL, MATLAB, TypeScript\\
\textbf{Tools \& Testing}: Git, CI/CD --- GitHub Actions \& Vercel, PyTest, Cypress

% ---------- Experience ----------
\section{\textcolor{Plum}{Experience}}
\resumeSubHeadingListStart
  \resumeSubheading
  {Quantitative Developer}{Vancouver, BC}
  {RBC Global Asset Management}{Sept.\ 2025 -- Dec.\ 2025}
  \resumeItemListStart
    \resumeItem{Will re-engineer MATLAB pricing–risk engine to modular Python + Dask on Helios—forecast for 70\% faster valuations and 50\% shorter releases via CI/CD.}
  \resumeItemListEnd

  \resumeSubheading
  {Quantitative Developer}{Vancouver, BC}
  {Quantico Research}{Jan.\ 2025 -- May 2025}
  \resumeItemListStart
    \resumeItem{Built real-time pipelines to ingest \& clean seismic streams at sub-200ms latency.}
    \resumeItem{Applied \textbf{HMM} for real-time seismic risk adjustment, improving internal alert thresholds.}
    \resumeItem{Automated walk-forward validation and stress tests in CI/CD for reproducible model releases.}
  \resumeItemListEnd

  \resumeSubheading
  {Frontend Engineer}{Vancouver, BC}
  {UBC Actuarial Science Club}{May 2025 -- Present}
  \resumeItemListStart
    \resumeItem{Spearheaded website build using Next.js, React \& Tailwind CSS, boosting club engagement +200\%.}
    \resumeItem{Built interactive course planning tool serving 150+ students, streamlining semester planning workflows.}
  \resumeItemListEnd
\resumeSubHeadingListEnd
% ---------- Technical Projects ----------
\section{\textcolor{Plum}{Technical Projects}}
"""
END_OF_RESUME = r"""
\end{document}
"""
