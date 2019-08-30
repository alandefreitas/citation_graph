# Citation Graphs

This script plots a graph with the relationship between bibtex citations.

Use the sample `bibtex.bib` to get started. Create a field `citations` in `bibtex.bib` to indicate that a paper cites another paper relevant to your bibliography:

```
citations = {kim2017nemo,miikkulainen2019evolving,real2017large,stanley2002evolving}
```

You will need the following libraries:

```
pip install matplotlib
pip install bibtexparser
pip install networkx
```
