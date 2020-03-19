# Matplot lib
import matplotlib.pyplot as plt
# Bibtex parser
import bibtexparser
# Graphs
import networkx as nx
from networkx.drawing.layout import *


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

    # Calculate year range
    min_year = int(bib_database.entries[0]['year'])
    max_year = int(bib_database.entries[0]['year'])
    for e in bib_database.entries:
        min_year = min(min_year, int(e['year']))
        max_year = max(max_year, int(e['year']))
    year_range = int(max_year) - int(min_year)

    # Calculate number of paper in each year
    papers_per_year = {}
    papers_per_year_counter = {}
    for i in range(min_year, max_year+1):
        quantity = count_by_attribute(bib_database.entries, 'year', str(i))
        if quantity > 0:
            papers_per_year[str(i)] = quantity
            papers_per_year_counter[str(i)] = 0

    # Define graph and node position
    dict_pos = {}
    mapping = {}
    G = nx.DiGraph()
    i = 1
    for entry in bib_database.entries:
        # blue if it cites anyone
        node_color = 'blue' if 'citations' in entry else 'red'
        # get paper ID
        node_name = entry['ID']
        # add node to the graph
        G.add_node(node_name, color=node_color)
        # year as a float (for vertex position in the graph)
        year = float(entry['year'])
        # position_x for a year is (0,1,2,...,n)/n
        positionx = (papers_per_year_counter[entry['year']])/papers_per_year[entry['year']]
        papers_per_year_counter[entry['year']] += 1
        current_year_offset = year - int(min_year)
        position = [positionx + current_year_offset / 1000,
                    current_year_offset / (year_range) + positionx / 5]
        # papers_per_year_counter.update({entry['year']: papers_per_year_counter[entry['year']]+1 })
        # give position to this index
        dict_pos[i] = position
        # map node name to the index
        mapping[node_name] = i
        i += 1

    # Create edges
    for entry in bib_database.entries:
        if 'citations' in entry:
            print(entry['ID'])
            for citation_id in entry['citations'].replace('\n', '').split(','):
                print('   ' + citation_id)
                # if there is a citation id
                if citation_id:
                    # if we will cite as noun
                    if cite_as_noun:
                        # find entry with this id
                        citation_entry = find_by_attribute(bib_database.entries, 'ID', citation_id)
                        # if found, create edge
                        if citation_entry:
                            G.add_edge(entry['ID'], citation_entry['ID'])
                    else:
                        # else, create edge
                        G.add_edge(entry['ID'], citation_id)

    # Calculate node colors as the number of citations it has
    node_colors = []
    for node in G.nodes:
        in_edges = G.in_degree(node)
        node_colors.append(in_edges)
    range_of_colors = max(node_colors) - min(node_colors)
    
    # Convert graph to figure
    plt.figure(figsize=(8,6))

    # Plot graph as planar (if small) or by year (if large)
    if G.number_of_nodes() < 10:
        try: 
            dict_pos = nx.planar_layout(G)
            nx.draw_networkx(G, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, vmin=min(node_colors)-range_of_colors*0.4, vmax=max(node_colors), font_weight='bold', pos=nx.planar_layout(G))
        except:
            dict_pos = nx.circular_layout(G)
            nx.draw_networkx(G, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, vmin=min(node_colors)-range_of_colors*0.4, vmax=max(node_colors), font_weight='bold', pos=nx.circular_layout(G))
    else:
        G = nx.relabel_nodes(G, mapping)
        i = 1
        for e in mapping:
            print(str(i)+': ' + e)
            i +=1
        nx.draw_networkx(G, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, vmin=min(node_colors)-range_of_colors*0.4, vmax=max(node_colors), font_weight='bold', pos=dict_pos)
        for i in range(int(min_year), int(max_year)+1):
            plt.text(-0.2, (i - int(min_year))/(int(max_year)-int(min_year))-0.03, str(i)+':')

    # Insert text with years
    maxDP = 0.0
    for e in dict_pos:
        if maxDP < dict_pos[e][1]:
            maxDP = dict_pos[e][1]
    for node in G:
        plt.text(dict_pos[node][0], dict_pos[node][1]-1.28/(32*maxDP), str(G.in_degree(node)), fontsize=4, color='red')

    # Insert ticks
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for pos in ['right','top','bottom','left']:
        plt.gca().spines[pos].set_visible(False)

    # Show plot
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


def count_by_attribute(entries, attribute_name, attribute_value):
    count = 0
    for entry in entries:
        if entry[attribute_name] == attribute_value:
            count = count + 1
    return count

if __name__ == '__main__':
    main()
