import time
import hashlib
from bs4 import BeautifulSoup
from lxml import html
import networkx
import matplotlib.pyplot as plt
import sys
from queue import Queue
import logging

logger = logging.Logger("Logger")

# class Node:
#     """
#         This is the node if the graph (Data type)
#     """
#     def __init__(self,htmlElement):
#         self.htmlElement = htmlElement
#         self.md5Hash = hashlib.md5(str(html.tostring(htmlElement)).encode())
#         self.children = set()
#
#     def __eq__(self, o: object) -> bool:
#         return self.md5Hash == o.md5Hash
#
#     def addChild(self,child):
#         self.children.insert(child)
#
#     def removeChild(self,child):
#         self.children.remove(child)
#
#
# class Tree:
#     """
#
#     """
#     def __init__(self,root):
#         self.root = root
#
#     def addEdge(self,parent:Node,child:Node):
#         parent.addChild(child)
#
#     def removeEdge(self,parent:Node,child:Node):
#         parent.removeChild(child)
#
#     def returnRoot(self):
#         return self.root


class HtmlTree:
    """
        The tree is DiGraph internally. This is created in order to get hashes of all the elements in the html.
    """
    def __init__(self,tree:networkx.DiGraph,root):
        self.tree = tree
        self.root = root


def dfs_add_util(graph:networkx.DiGraph,parent)->(html.HtmlElement,hex):
    """
    :param graph:
    :param parent:
    :return:
    """
    parentNode = (parent,hashlib.md5(str(html.tostring(parent)).encode()).hexdigest())

    for node in parent.getchildren():
        tempNode = (node,hashlib.md5(str(html.tostring(node)).encode()).hexdigest())
        graph.add_edge(parentNode,tempNode)
        dfs_add_util(graph,node)

    return parentNode


def buildGraph(rawString:str,link="")->(networkx.DiGraph,(html.HtmlElement,hex)):
    """
    :param rawString:
    :param link:
    :return: nothing
    """
    try:
        graph = networkx.DiGraph()
        htmlObject = html.document_fromstring(rawString)
        root = dfs_add_util(graph,htmlObject)

    except Exception as e :
        logger.error(f" Error : {e}")

    return (graph,root)


def traverseLxmlHtml(parent:html.HtmlElement):
    """
    :param parent:
    :return:
    """
    print(parent.tag)
    for node in parent.getchildren():
        print(node.tag,type(node),end="\t")
        traverseLxmlHtml(node)


def traverseTree(root,graph:networkx.DiGraph):
    """

    :param htmlTree:
    :return:
    """
    children = graph.successors(root)
    print(list(graph.predecessors(root)),"->",root)
    for each in children:
        traverseTree(each,graph)

def isChange(defaultWebPage:str,newWebPage:str)->bool:
    """
        returns true if there is some diff in newWebPage compared to old one
    :param defaultWebPage:
    :param newWebPage:
    :return: boolean
    """
    return hashlib.md5(defaultWebPage.encode()).hexdigest() != hashlib.md5(newWebPage.encode()).hexdigest()

def setDiff(set1:set,set2:set)->set:
    """
        this function is not a general set diff and only be used in diff for set of HtmlTree Nodes
    :param set1:
    :param set2:
    :return:
    """
    diff = set()
    dict1,dict2 = {k:v for v,k in set1},{k:v for v,k in set2}

    for k in dict1.keys():
        if dict2.get(k) == None:
            diff.add((k,dict1[k]))
    for k in dict2.keys():
        if dict1.get(k) == None:
            diff.add((k,dict2[k]))

    return diff

def detectElementChanges(webPageTree1:HtmlTree,webPageTree2:HtmlTree)->list:
    """
        This function returns the list of all the changed elements in the html in pair
    :param webPageTree1:
    :param webPageTree2:
    :return:
    """
    changes = []
    tree1,tree2 = webPageTree1.tree,webPageTree2.tree
    root1,root2 = webPageTree1.root,webPageTree2.root
    queue1,queue2 = Queue(maxsize=0),Queue(maxsize=0)
    queue1.put(root1),queue2.put(root2)
    queue1.put(None), queue2.put(None)
    set1,set2 = set(),set()
    while queue1.qsize() != 1 and queue2.qsize() != 1:
        parent1,parent2 = queue1.get(),queue2.get()
        if parent1 == None and parent2 == None :
            symmetricDiff = setDiff(set1,set2)
            print(symmetricDiff)
            changes.append(symmetricDiff)
            queue1.put(None)
            queue2.put(None)
            set1.clear(),set2.clear()

        else:
            for each in tree1.successors(parent1):
                queue1.put(each)
                set1.add(each)
            for each in tree2.successors(parent2):
                queue2.put(each)
                set2.add(each)

    return changes


if __name__ == '__main__':
    with open("test1.html","r") as fd:
        textHTML1 = fd.read()
        webpageHash1 = hashlib.md5(textHTML1.encode())
        print("webpage 1 hash :",webpageHash1.hexdigest())
    with open("test.html","r") as fd:
        textHTML = fd.read()
        webpageHash2 = hashlib.md5(textHTML.encode())
        print("webPage 2 hash :",webpageHash2.hexdigest())

    start = time.time()
    if isChange(textHTML,textHTML1):
        tree1,root1 = buildGraph(textHTML1)
        tree2,root2 = buildGraph(textHTML)
        print("Time taken to build the graph",time.time()-start)
        htmlTree1 = HtmlTree(tree1,root1)
        htmlTree2 = HtmlTree(tree2,root2)
        print(len(detectElementChanges(htmlTree1,htmlTree2)))

    else:
        print("No Change !")


