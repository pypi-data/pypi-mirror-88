# Universal HEP plot

[![Pipeline](https://gitlab.cern.ch/fsauerbu/uhepp/badges/master/pipeline.svg)](https://gitlab.cern.ch/fsauerbu/uhepp/-/pipelines)
[![Coverage](https://gitlab.cern.ch/fsauerbu/uhepp/badges/master/coverage.svg)](https://gitlab.cern.ch/fsauebu/uhepp)
[![Lint](https://gitlab.cern.ch/fsauerbu/uhepp/-/jobs/artifacts/master/raw/pylint.svg?job=pylint)](https://gitlab.cern.ch/fsauerbu/uhepp)
[![License](https://gitlab.cern.ch/fsauerbu/uhepp/-/jobs/artifacts/master/raw/license.svg?job=badges)](https://gitlab.cern.ch/fsauerbu/uhepp/-/blob/master/LICENSE)
[![PyPI](https://gitlab.cern.ch/fsauerbu/uhepp/-/jobs/artifacts/master/raw/pypi.svg?job=pypi)](https://pypi.org/project/uhepp/)
[![Docs](https://readthedocs.org/projects/uhepp/badge/?version=latest&amp;style=flat)](https://uhepp.readthedocs.io/en/latest/)

*Universal HEP plot* is a textual data format (JSON or YAML) to define plots used
in high-energy physics contexts, especially for my PhD within the ATLAS
Collaboration. Usually, analysis software processes a list of events (xAOD,
ntuple, HDF5 or similar formats) and converts them into a histograms and, in
most cases, also into plots.
This makes it hard to change the style retroactively. Alternatively, plots
might be saved in ROOT format (e.g. TH1F), which lose a lot of information
on how the data should be visualized.

The *universal HEP plot* format defines an interface **between** analysis software and
plotting software. The definition of a plot in UHEP contains 
histograms organized in stacks, their uncertainties (potentially systematic
variations) and the plotting style (colors, line widths, labels, etc.). The
separation of data processing and data visualization is mirrored in the file
format. The style can be changed without rerunning the analysis. The
universality of the interface allows for multiple analysis frameworks and
plotting frameworks to be wired together.

Typical applications include:
 - Bulk storage of plots in a database (e.g. `mongodb`) for later retrieval
   and reuse
 - Provide plots on multiple media, e.g. traditional files (png, pdf), or
   interactive web applications
 - Collaboration in an analysis team
 - Rebrand plots from "***ATLAS*** Internal" to "***ATLAS***"

## Links

 - Docs: [https://uhepp.readthedocs.io/](https://uhepp.readthedocs.io/)
 - PyPI: [https://pypi.org/project/uhepp/](https://pypi.org/project/uhepp/)
 - Hub: [https://uhepp.org/](https://uhepp.org)
