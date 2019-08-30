# Matplot lib
import matplotlib.pyplot as plt
# Bibtex parser
import bibtexparser
# Graphs
import networkx as nx

def main():
    # Settings
    cite_as_noun = True

    # Open bibtext
    with open('bibtex.bib') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    print(bib_database.entries)
    print(bib_database.comments)
    print(bib_database.preambles)
    print(bib_database.strings)

    # Define graph
    G = nx.DiGraph()

    # Create nodes
    for entry in bib_database.entries:
        node_color = 'blue' if 'citations' in entry else 'red'
        node_name = extract_author_string(entry) if cite_as_noun else entry['ID']
        G.add_node(node_name, color=node_color)

    # Create edges
    for entry in bib_database.entries:
        if 'citations' in entry:
            for citation_id in entry['citations'].split(','):
                if citation_id:
                    if cite_as_noun:
                        citation_entry = find_by_attribute(bib_database.entries,'ID',citation_id)
                        if citation_entry:
                            node_name_a = extract_author_string(entry) if cite_as_noun else entry['ID']
                            node_name_b = extract_author_string(citation_entry)
                            G.add_edge(node_name_a, node_name_b)
                    else:
                        G.add_edge(entry['ID'], citation_id)

    # Calculate node colors as the number of citations it has
    node_colors = []
    for node in G.nodes:
        in_edges = G.in_degree(node)
        node_colors.append(in_edges)
    range_of_colors = max(node_colors) - min(node_colors)

    # Convert graph to figure
    plt.figure(figsize=(8,6))

    # Options
    nx.draw_networkx(G, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, vmin=min(node_colors)-range_of_colors*0.4, vmax=max(node_colors), font_weight='bold', pos=nx.planar_layout(G))
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for pos in ['right','top','bottom','left']:
        plt.gca().spines[pos].set_visible(False)
    plt.show()

    # Save plot
    plt.savefig("citation_graph.eps")

    # End main
    return 0


def extract_author_string(entry):
    """This extracts the authors from an entry"""
    authors = entry['author'].replace(';', ',').replace('and',',').split(',')
    citation_format = ''
    if authors:
        first_author_names = authors[0].split(' ')
        first_author_citation = first_author_names[0]
        if len(first_author_names) > 1:
            if len(first_author_names[1]) <= 3:
                first_author_citation += ' ' + first_author_names[1]
            else:
                first_author_citation += ' ' + first_author_names[1][0] + '.'
        citation_format = first_author_citation + (' et. al' if len(authors) > 1 else '')
    citation_format += ' (' + entry['year'] + ')'
    return citation_format


def find_by_attribute(entries,attribute_name,attribute_value):
    for entry in entries:
        if entry[attribute_name] == attribute_value:
            return entry
    return None


if __name__ == '__main__':
    exit(main())
