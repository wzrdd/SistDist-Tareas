\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{udpreport} [2014/12/19 v0.01 Report of the UDP]

\DeclareOption*{\InputIfFileExists{\CurrentOption.udp}{}{
\PassOptionsToClass{\CurrentOption}{report}}}
\ProcessOptions \relax % chktex 1

\LoadClass{article}

%% Definición de colores
\RequirePackage{xcolor}
\RequirePackage{colortbl}
\definecolor{cgreen}{rgb}{0.25,0.5,0.35}
\definecolor{jpurple}{rgb}{0.5,0,0.35}
\definecolor{darkgreen}{rgb}{0.0, 0.2, 0.13}
\definecolor{gray75}{gray}{0.75}

%% Spanish
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}

% es-noquoting is used for no clash with tikz (see http://tex.stackexchange.com/a/48787/7561)
% es-noshorthands is used to remove "a ordinal shorthand (see http://tex.stackexchange.com/a/203422/7561)
\RequirePackage[spanish,es-lcroman,es-tabla,es-noquoting, es-noshorthands]{babel}
\decimalpoint% changes the coma in the numbers to period
\RequirePackage{csquotes}

%% Hyperref para que el table of content sea clickeable
\RequirePackage{hyperref}
\RequirePackage{bookmark} %% quita un warning
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}

%% Chapter Structure
\RequirePackage{subfiles}

% Images
\RequirePackage{graphicx}

% Matemática
\RequirePackage{amsmath,amssymb}
\RequirePackage{mathtools}

% For using the empty verification
% Esto lo dejó Adín, no sé qué hace y me da miedo borrarlo.
\RequirePackage{etoolbox}

% Headers and footers
\RequirePackage{fancyhdr}

% Layout de la página
\RequirePackage[left=2.5cm,right=2.5cm,top=3cm,bottom=2cm]{geometry}

% Estilo de cada página, esto necesita fancyhdr
\fancypagestyle{followingpage}{
  \fancyhf{}
  \rhead{ \nouppercase{\rightmark} }
  \cfoot{ \thepage } % chktex 1
}

\pagestyle{followingpage}

% Contains all the udp logos and other stuff
% Esto lo dejó Adín, es el archivo udp.sty
\RequirePackage{udp}

%% Definitions and commands
% Strings to typeset the logo
\newcommand{\udp@school}{Escuela de Informática y Telecomunicaciones}
\newcommand{\udp@faculty}{Facultad de Ingeniería}
\newcommand{\udp@university}{Universidad Diego Portales}
% Default logo to UDP (see logo definition at the bottom)
\setlogo{UDP}

\newcommand{\udpschool}[1]{\gdef\udp@school{#1}}
\newcommand{\udpfaculty}[1]{\gdef\udp@faculty{#1}}
\newcommand{\udpuniversity}[1]{\gdef\udp@university{#1}}

% string for email
\newcommand{\udp@mail}{}
\newcommand{\email}[1]{\gdef\udp@mail{#1}}

% Re-define the title
\def\maketitle{%
  \udp@titlepage%
  \setcounter{page}{1}% page 1 (frontmatter)
  \thispagestyle{followingpage}
}

\RequirePackage{titlesec, blindtext, color, fontenc}

%% Portada hecha por Adín, se le sacó la fecha en la portada
%% todo lo demás solo Dios sabe lo que hace
\setlogosz{66.5mm}% tweaked by hand
\newcommand{\udp@titlepage}{%
  \thispagestyle{empty}%
  % logo here
  \begin{center}%
    \bfseries%
    \ifdefempty{\@logo}{}{%ifnotempty
    \begin{minipage}{\@logosz}
    \@logo\\%
    \end{minipage}%
    }%ifnotmtarg
    \par\vspace{20pt}%
    \udp@faculty\par%
    \udp@school\par%
    \rule[1pt]{\textwidth}{1pt}%
  \end{center}%
  % form the cover page
  \vskip 1em%
  {\bfseries%
    \vspace{40pt}%
    \begin{center}%
      {\LARGE\@title\par}%
      \vskip 40pt%
      {\large\@author}%
      \vfill%
      %% uncomment below to get date on the cover
      %% \@date%
    \end{center}%
  }%
  \newpage%
}

%% Java Snippets
\RequirePackage{listings}
\newcommand{\JavaCode}{
  \lstset{
    language=Java,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{jpurple}\bfseries,
    stringstyle=\color{red},
    commentstyle=\color{green},
    morecomment=[s][\color{blue}]{/**}{*/},
    extendedchars=true,
    showspaces=false,
    showstringspaces=false,
    numbers=left,
    breaklines=true,
    backgroundcolor=\color{cyan!10},
    breakautoindent=true,
    captionpos=b,
    xleftmargin=10pt,
    tabsize=2,
    % listings no tiene definido utf-8 por defecto
    % definimos cada carácter especial
    literate=
      {á}{{\'a}}1
      {é}{{\'e}}1
      {í}{{\'\i}}1
      {ó}{{\'o}}1
      {ú}{{\'u}}1
      {ñ}{{\~n}}1
      {¡}{{!`}}1
      {¿}{{?`}}1
  }
}

%% Epígrafe
\RequirePackage{epigraph}
\renewcommand{\textflush}{flushepinormal}

%% Para enmarcar en cuadros las definiciones o conceptos.
\RequirePackage{mdframed}

%% Para los cuadros en los que se enmarcan los objetivos de un capítulo.
\RequirePackage{tcolorbox}

%% Ornamentos para cuando termina una sección
\newcommand{\SubsectionEnding}{
  \bigskip
  \hrulefill\hspace{0.2cm}
  $\circ$
  \hspace{0.2cm}\hrulefill{}
  \bigskip
}

% Definicón del formato de \section y \chapter
\newcommand{\hsp}{\hspace{20pt}}
\titleformat{\section}[block]{\Large\bfseries}{\thesection\hsp\textcolor{gray75}{|}\hsp}{0pt}{\Large\bfseries}

\titleformat{\chapter}[display]
  {\Large\raggedleft}
  {\MakeUppercase{\chaptertitlename}%
    \rlap{ \resizebox{!}{1.5cm}{\thechapter} \rule{5cm}{1.5cm}}}
  {10pt}{\Huge}
\titlespacing*{\chapter}{0pt}{0pt}{20pt}

% Definiciones necesarias para las tablas
\RequirePackage{longtable}
\RequirePackage{array}
\RequirePackage{makecell}
\RequirePackage{booktabs}

\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

\aboverulesep=0ex
\belowrulesep=0ex

\RequirePackage{float}