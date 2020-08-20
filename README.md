# Citation Graphs

This script plots a graph with the relationship between bibtex citations.

Use the sample `bibtex.bib` to get started. Create a field `citations` in `bibtex.bib` to indicate that a paper cites another paper relevant to your bibliography:

```
citations = {kim2017nemo,miikkulainen2019evolving,real2017large,stanley2002evolving}
```

## Dependencies

Run

```
$ python -m pip install -r requirements.txt
```

to install the dependencies.
