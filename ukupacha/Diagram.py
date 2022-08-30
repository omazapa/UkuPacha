from ukupacha.Utils import is_dict
from blockdiag import parser, builder, drawer


def graph2blockdiag(regs, pdb):
    """
    Recursive algorithm to parse the graph to a blockdiag structure.
    """
    output = ""
    if is_dict(regs):
        parent = list(regs.keys())[0]
        if regs[parent] == None:
            output = f"'{parent}\n{pdb}';\n"
        else:
            for i in regs[parent]:
                db = i["DB"]
                sub_regs = i["TABLES"]
                out = graph2blockdiag(sub_regs, db)
                output += f" '{parent}\n{pdb}' -> {out}"
    else:
        for reg in regs:
            out = graph2blockdiag(reg, pdb)
            output += out
    return output


def model2diag(model: dict):
    """
    Given the model dict, takes the grap and the initial db to
    call grap2blockdiag
    """
    graph = model["GRAPH"]
    db = model["CHECKPOINT"]["DB"]
    out = graph2blockdiag(graph, db)
    output = "diagram { "+out+" }"
    return output


def diag2file(diag, filename, fmt):
    """
    Function to save the diag in a file.

    Parameters
    ------------
    diag:str
        String with the diagram generated by model2diag
    filename:str
        file to save the diagram
    fmt:str
        format of the file, supported "SVG", "PNG" and "PDF"
    """
    tree = parser.parse_string(diag)
    diagram = builder.ScreenNodeBuilder.build(tree)
    draw = drawer.DiagramDraw(fmt, diagram, filename=filename)
    draw.draw()
    draw.save()
