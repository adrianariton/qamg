import re



themes={}

def compute_themes(filepath, i=-1):
    intheme = 0
    set_theme = ''
    theme = []
    nrv = 0
    nrp = 0
    i = 1000
    thms = []
    vars={}
    props={'nil': {'v' : 0}}
    for line in open(filepath, 'r'):
        if line.count('{') == 1 and not (line.count("=") > 0):
            if line.strip().startswith('.'):
                intheme = intheme + 1
                th = line.strip().split('{')[0].strip()
                if len(th) > 0:
                    theme  = re.split(', |,|\\.|\\#', th)
        if line.strip() == '}':
            if nrp == 0 and nrv > 0:
                # was theme
                thms = thms + theme
                thms = list(set(thms))
            nrv = 0
            nrp = 0
            intheme = 0
            theme = []
        if line.count(":") == 1 and not (line.count("=") > 0):
                id = line.split(":")[0].strip()
                vg = line.split(":")[1].strip().strip(';}{')
                
                for k in range(3):
                    res = re.split(',|_|!|\\"|\+|\\ \\-\\ |\\)|\\(|\\}|\\{|\\*|\\/', vg)
                    for ind,r in enumerate(res):
                        w = r.strip()
                        if w.startswith('--'):
                            if res[ind - 1].strip() == 'var':
                                res[ind] = 'var(' + w + ')'
                    for ind,r in enumerate(res):
                        w = r.strip()
                        if w == 'var' or len(w) == 0:
                            res.pop(ind)
                    
                    for ind,r in enumerate(res):
                        if not (r.strip() in vars):
                            #print(f'Not found: {r.strip()}')
                            continue
                        else:
                            #print(f'FOUND---- {r.strip()} :: {vars[r.strip()]}   vg: {vg} =>')
                            vg = vg.replace(r.strip(), vars[r.strip()], 100)
                            #print('|'+vg+'|')
        
                if id.startswith('--'):
                    if intheme == 1 and set_theme.strip() in theme:
                        vars['var(' + id + ')'] = vg.strip()
                    nrv = nrv + 1
                else:
                    #print(vg)
                    props[id.strip()] = vg.strip()
                    nrp = nrp + 1
                i = i - 1
                if i == 0:
                    break
    for ind,t in enumerate(thms):
        thms[ind] = t.strip()
    return thms

def get_theme(filepath,set_theme, themes, i=-1):
    intheme = 0
    theme = []
    nrv = 0
    nrp = 0
    vars={}
    props={}
    for line in open(filepath, 'r'):
        if line.count('{') == 1 and not (line.count("=") > 0):
            if line.strip().startswith('.'):
                intheme = intheme + 1
                th = line.strip().split('{')[0].strip()
                if len(th) > 0:
                    theme  = re.split(', |,|\\.|\\#', th)
        if line.strip() == '}':
            nrv = 0
            nrp = 0
            intheme = 0
            theme = []
        if line.count(":") == 1 and not (line.count("=") > 0):
                id = line.split(":")[0].strip()
                vg = line.split(":")[1].strip().strip(';}{')
                
                for k in range(3):
                    res = re.split(',|_|!|\\"|\+|\\ \\-\\ |\\)|\\(|\\}|\\{|\\*|\\/', vg)
                    for ind,r in enumerate(res):
                        w = r.strip()
                        if w.startswith('--'):
                            if res[ind - 1].strip() == 'var':
                                res[ind] = 'var(' + w + ')'
                    for ind,r in enumerate(res):
                        w = r.strip()
                        if w == 'var' or len(w) == 0:
                            res.pop(ind)
                    
                    for ind,r in enumerate(res):
                        if not (r.strip() in vars):
                            #print(f'Not found: {r.strip()}')
                            continue
                        else:
                            #print(f'FOUND---- {r.strip()} :: {vars[r.strip()]}   vg: {vg} =>')
                            vg = vg.replace(r.strip(), vars[r.strip()], 100)
                            #print('|'+vg+'|')
        
                if id.startswith('--'):
                    sw = 1
                    for thth in theme:
                        if not (thth.strip() in themes):
                            sw = 0
                    if intheme == 1 and set_theme.strip() in theme:
                        vars['var(' + id + ')'] = vg.strip()
                    if sw == 0:
                        vars['var(' + id + ')'] = vg.strip()

                    nrv = nrv + 1
                else:
                    #print(vg)
                    if not id.strip() in props:
                        props[id.strip()] = {}
                    for thth in theme:
                        props[id.strip()][thth] = vg.strip()
                    nrp = nrp + 1
                i = i - 1
                if i == 0:
                    break
    return vars, props

themes = compute_themes(filepath='input.txt')
vars, props = get_theme(filepath='input.txt', set_theme='theme-g10', themes=themes,i=3000)

print('---Themes----')
print(themes)
print()
print()


val = input("> Property:\n> ")

if val in props:
    print(props[val])
else:
    print(f'> Property {val} not found!')

val = input("> Var:\n> ")

if val in vars:
    print(vars[val])
else:
    print(f'> Variable {val} not found!')

'''
print(str(len(props)) + ' props')
print(props)
print()
print()
print(str(len(vars)) + ' vars')
print(vars)
'''

        