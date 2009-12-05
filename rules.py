# -*- coding: utf-8 -*-

def init(rule_dict, pwd='./data/rules'):
    '''Initialize rules from file.'''

    f = file(pwd+'/rules.rule', 'r')
    for elem in map(lambda(s): s[:-1], f.readlines()):
        if elem != '' and elem[0] != '#':
            rule_dict[elem] = Rule(elem)
    f.close()

    rules_list = ['nominal', 'verbal']
    for rule_name in rules_list:
        f = file(pwd+'/'+rule_name+'.rule', 'r')
        for elem in map(lambda(s): s[:-1], f.readlines()):
            if elem != '' and elem[0] != '#':
                tmp = elem.split(':')
                rule_dict[tmp[0]].insert(tmp[1], tmp[2])
        f.close()

class Rule:
    '''
    Defines how to declinate/conjugate words based on roots/lists.
    '''

    def __init__(self, name):
        '''Attributes:
        - self.name: the rule's name/identifier;
        - self.subs: the substitution rule's dict;
        - self.kind: defines the rule's kind among verbal, nominal1
          and nominal2.
        '''

        self.name = name
        self.subs = {}
        self.kind = None

    def insert(self, par, subs):
        if subs[0] == '@':
            self.kind = 'verbal'
            for i in range(6):
                self.subs[(par, i)] = subs.split('/')[0] + '/' + \
                        subs[1:].split('/')[1].split(',')[i]
        elif subs[0] == '#':
            self.kind = 'nominal1'
            self.subs[tuple(par.split(','))] = subs[1:]
        else:
            self.kind = 'nominal2'
            self.subs[tuple(par.split(','))] = subs.split(',')

    def apply(self, txt, par, pn=''):
        aux = txt
        if self.kind == 'nominal1':
            for k in self.subs:
                if not filter(lambda x: x, \
                                map(lambda y: k[y] != par[y] and \
                                      k[y] != '*', range(len(k)))):
                    return txt.split(',')[int(self.subs[k])-1]
            return txt
        elif self.kind == 'nominal2':
            for k in self.subs:
                if not filter(lambda x: x, \
                                map(lambda y: k[y] != par[y] and \
                                      k[y] != '*', range(len(k)))):
                    for j in self.subs[k]:
                        sub = j.split('/')
                        if sub[0][-1] == '$':
                            aux = (aux + '$').replace(sub[0],
                                                        sub[1])
                        if aux[-1] == '$':
                            aux = aux[:-1]
                        else:
                            aux = aux.replace(sub[0], sub[1])
                    return aux
            return txt
        elif self.kind == 'verbal':
            sub = self.subs[(par, {
                        '1s': 0, '2s': 1, '3s': 2,
                        '1p': 3, '2p': 4, '3p': 5
                        }[pn])].split('/')
            if sub[0][-1] == '$':
                return (aux + '$').replace(sub[0][1:], sub[1])
            if aux[-1] == '$':
                aux = aux[:-1]
            else:
                return aux.replace(sub[0][1:], sub[1])
        else:
            raise 'Rule kind not defined', self.name
