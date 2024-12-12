import spacy
import networkx as nx
import matplotlib.pyplot as plt

NLP = spacy.load('pt_core_news_lg')
FILE_NAME = './files/test.txt'
graph = nx.DiGraph()

def loadSpacy():
    with open(FILE_NAME, 'r', encoding='utf-8') as archive:
        text = archive.read()
    text = text.replace("\n"," ")
    text.strip()
    text.lower()
    
    document = NLP(text)
    document = NLP(' '.join([token.text for token in document if not token.is_stop]))

    return document

def relations():
    doc = loadSpacy()
    ents, rels = [], []

    for ent in doc.ents:
        ents.append([ent.text, ent.label_])

    for token in doc:
        if token.pos_ == "VERB":
            rels.append([token.head.text, token.text, [child.text for child in token.children]])
 
    return ents, rels

def visualize(ents, rels):
    for entity, label in ents:
        graph.add_node(entity, label=label)

    for head, relation, children in rels:
        for child in children:
            graph.add_edge(head, child, label=relation)

    newNodeInputs()
    consultNodesRelations("filmes", "crítica")

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color="red", node_size=2000, font_size=10)
    labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

def addNode(node_txt='no_text', node_label='MISC', head=None, relationType="child", relations=None):
    graph.add_node(node_txt, label=node_label)

    if head != None:
        if relationType == "child":
            graph.add_edge(head, node_txt, label=relations)
        else:
            graph.add_edge(node_txt, head, label=relations)

def removeNode(node_text):
    if node_text not in graph:
        return

    in_edges = list(graph.in_edges(node_text))
    out_edges = list(graph.out_edges(node_text))

    graph.remove_edges_from(in_edges + out_edges)

    graph.remove_node(node_text)

def newNodeInputs():
    addNode(node_txt="test",head="TEST",relationType="head", relations="t")
    removeNode("test")

def consultNodesRelations(nodeA, nodeB): 
    relation = graph.edges[nodeA, nodeB]["label"]
    print(f"\"{nodeA}\" tem uma relação de \"{relation}\" para \"{nodeB}\"")

def main():
    ents, rels = relations()
    visualize(ents, rels)

if __name__=="__main__":
    main()