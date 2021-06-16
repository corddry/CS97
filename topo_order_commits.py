#!/usr/bin/python3
import os, sys, zlib


repository = None #output of get_dir()
nodes = []
branch_names = {}

def get_dir():
    global repository
    while(os.getcwd() != "/"):
        if os.path.isdir(os.getcwd() + "/.git"):
            repository = os.getcwd()
            return
        else:
            os.chdir("..")
    repository = None

def get_branches():
    global branch_names
    os.chdir(repository + "/.git/refs/heads")
    heads_dir = os.getcwd()
    ret = []
    for filename in os.listdir():
        hash = open(os.path.join(heads_dir, filename)).read()
        h = hash[:40]
        if not h in branch_names:
            branch_names[h] = filename
        else:
            branch_names[h] += (" " + filename)
        ret.append(hash)
    return ret

class CommitNode:
    def __init__(self, commit_hash, child):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash

        os.chdir(repository + "/.git/objects/" + commit_hash[0:2])
        decodeme = open(commit_hash[2:40], "rb").read()
        opened = (zlib.decompress(decodeme)).decode()


        self.parents = []
        self.children = []
        self.children.append(child)


        index = opened.find("\nparent ") + 8 #offset the len of parent

        global nodes
        
        while(index != (-1 + 8)): # find returns -1
            parent = opened[index:index + 40]   #checksums are 40 characters
            self.parents.append(parent)
            for node in nodes:
                if node.commit_hash == parent:
                    node.children.append(commit_hash)
                    index = opened.find("\nparent ", index) + 8 
                    break
            else:
                nodes.append(CommitNode(parent, commit_hash))
                index = opened.find("\nparent ", index) + 8 
            

def main():
    get_dir()
    if repository is None:
        sys.stderr.write("Not inside a Git repository")
        exit(1)
    branches = get_branches()
    for branch in branches:
        h = branch[:40]
        for node in nodes:
             if node.commit_hash == h:
                break
        else:
            nodes.append(CommitNode(h, "")) #CommitNode with empty string for children

        
    nodes.reverse() #Due to the nature of the __init__ of CommitNode, the reverse of nodes is ordered topologically

    out = ""    #return string
    for i in range(len(nodes)):
        node = nodes[i]
        out+=(nodes[i].commit_hash)
        if node.commit_hash in branch_names:
            out+=(" ")
            out+=(branch_names.get(node.commit_hash)) #Get name of branch(es) from dictionary
        out+=("\n")
        if (i != len(nodes)-1) and (not (nodes[i+1].commit_hash in node.parents)):
            for parent in node.parents:
                out+= (parent + " ")
            out+=("\b=\n\n=")
            for child in nodes[i+1].children:
               out+=(child + " ")
            out+=("\b\n")
    print(out)

if __name__ == "__main__":
    main()

