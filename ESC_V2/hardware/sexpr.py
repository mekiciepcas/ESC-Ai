import re, json

def parse(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text)
    stack = [[]]
    for t in tokens:
        if t == '(':
            v=[]; stack[-1].append(v); stack.append(v)
        elif t == ')': stack.pop()
        elif t.startswith('"'): stack[-1].append(json.loads(t))
        else: stack[-1].append(t)
    return stack[0][0]

def children(tree, key): return [x for x in tree if isinstance(x,list) and x and x[0]==key]
def child(tree,key): return next((x for x in children(tree,key)),None)

def pins(tree):
    found=[]
    for x in tree:
        if isinstance(x,list):
            if x and x[0]=='pin' and child(x,'number'):
                found.append({'number':child(x,'number')[1], 'name':child(x,'name')[1], 'type':x[1]})
            else: found.extend(pins(x))
    return found

def load_symbol(lib,name):
    from pathlib import Path
    tree=parse((Path('C:/Program Files/KiCad/10.0/share/kicad/symbols')/(lib+'.kicad_sym')).read_text(encoding='utf-8'))
    table={x[1]:x for x in children(tree,'symbol')}
    s=table[name]
    while child(s,'extends'):s=table[child(s,'extends')[1]]
    return s
