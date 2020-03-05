import datetime

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

    # Define graph
    G = nx.DiGraph()
    
    dict_pos = {}
    dict_qpycurr = {}
    
    initial_year = datatime.date.today().year - 20
    current_year = datatime.date.today().year
    dict_qpy = {}
    i = initial_year
    while i <= current_year:
        qtde = count_by_attribute(bib_database.entries,'year',str(i))
        if qtde > 0:
            dict_qpy[str(i)] = qtde
            dict_qpycurr[str(i)] = 0
        i += 1
    
    for e in dict_qpy:
        initial_year = e
        break
    
    for e in dict_qpy:
        final_year = e
    
  
    # Create nodes
    mapping = {}
    i = 1
    for entry in bib_database.entries:
        node_color = 'blue' if 'citations' in entry else 'red'
        node_name = entry['ID']
        G.add_node(node_name, color=node_color)
        year = float(entry['year'])
        positionx = (dict_qpycurr[entry['year']])/dict_qpy[entry['year']]
        dict_qpycurr.update({entry['year']: dict_qpycurr[entry['year']]+1 })
        position = [positionx + (year - int(initial_year))/1000, (year - int(initial_year))/(int(final_year)-int(initial_year))+positionx/5]
        dict_pos[i] =  position
        mapping[node_name] = i
        i+=1

    
    # Create edges
    for entry in bib_database.entries:
        if 'citations' in entry:
            print(entry['ID'])
            for citation_id in entry['citations'].split(','):
                print('   ' + citation_id)
                if citation_id:
                    if cite_as_noun:
                        citation_entry = find_by_attribute(bib_database.entries,'ID',citation_id)
                        if citation_entry:
                            node_name_a = entry['ID']
                            node_name_b = citation_entry['ID']
                            #print(node_name_a + ' : ' + node_name_b)
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
    
    #pos=nx.planar_layout(G)
    
    if G.number_of_nodes() <30:
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
        for i in range(int(initial_year), int(final_year)+1):
            plt.text(-0.2, (i - int(initial_year))/(int(final_year)-int(initial_year))-0.03, str(i)+':')
            
    maxDP = 0.0
    for e in dict_pos:
        if maxDP < dict_pos[e][1]:
            maxDP = dict_pos[e][1]
    for node in G:
        plt.text(dict_pos[node][0], dict_pos[node][1]-1.28/(32*maxDP), str(G.in_degree(node)), fontsize=4, color='red')
    
            
    
        
    
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for pos in ['right','top','bottom','left']:
        plt.gca().spines[pos].set_visible(False)
        

    #plt.show()
    
    
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

def count_by_attribute(entries,attribute_name,attribute_value):
    count = 0
    for entry in entries:
        if entry[attribute_name] == attribute_value:
            count = count + 1
    return count





if __name__ == '__main__':
    main()
