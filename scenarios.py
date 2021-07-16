# -*- coding: utf-8 -*-

def read_diagram(diagram_name):
    f = open(diagram_name, "rt", encoding="utf-8")
    diagram = (f.read())
    f.close()
    return (diagram)

def split_lines(text_diagram):
    return text_diagram.split('\n')

def check_conditional_exist(text_diagram):
    conditional = None

    for text in text_diagram:

        if text.startswith('if'):
            conditional = True
            break
        else:
            conditional = False

    return (conditional)

def get_feature_name(text_diagram):
    tag = 'floating note'

    for i in range(len(text_diagram)):

        if text_diagram[i] == tag:
            feature_name = text_diagram[i+1]

    return feature_name

def remove_feature_tittle(feature, text_diagram):
    for i in text_diagram:

        if i == feature:
            text_diagram.remove(feature)

    return (text_diagram)

def remove_syntax_tags(text_diagram):
    # Remove plantUML syntax tags from file
    tags = ['(', ')', 'if', 'then', 'yes', 'else', 'elseif', '@startuml', 'floating note',
        'end note', 'start', 'end', 'endif', '@enduml','stop']

    for tag in tags:

        if tag in text_diagram:
            text_diagram.remove(tag)
    return (text_diagram)

def generate_feature(feature_name,text_diagram):
    f = open("gherkin_scenarios.txt", "w", encoding="utf-8")
    f.write("Feature: "+feature_name+"\n")
    for _ in text_diagram:
        f.write("   "+format_scenario_line(_)+'\n')
    f.close()

def format_scenario_line(line):
    tags = [':',';']
    for tag in tags:
        if tag in line:
            line = line.replace(tag,'')

    return line

def clean_scenario_name(scenario_string): #R
    tags = ['(', ')', 'if', 'then', 'yes', 'else', 'elseif']

    for tag in tags:

        if tag in scenario_string:
            scenario_string = scenario_string.replace(tag,'')

    return (scenario_string)

def check_conditionals(text_diagram): #R
    '''
    This function checks whether the diagram has conditionals, and groups the flow paths
    In the structure: {conditional:scenario}
    '''
    scenarios_dict = {}
    main_key = ''

    for i in text_diagram:

        if i.startswith('if'):
            scenario_key = clean_scenario_name(i)
            scenarios_dict[scenario_key] = []
            # Setting main key to dict(conditional reason).
            main_key = scenario_key

        elif i.startswith('else') or i.startswith('elseif'):
            scenario_key = clean_scenario_name(i)
            scenarios_dict[scenario_key] = [] 
                 
        scenarios_dict[scenario_key].append(i)

    return scenarios_dict

def generate_feature_conditional(tittle, scenarios_dict, givens): #R
    f = open("gherkin_scenarios.feature", "w", encoding='utf-8')
    f.write('# language: pt'+'\n')
    f.write(tittle+'\n')
    for key in scenarios_dict.keys():
        f.write("Cenário: "+key+'\n')
        for _ in givens:
            f.write("\t"+format_scenario_line(_)+'\n')
        for _ in scenarios_dict[key]:
            if _ == scenarios_dict[key][0]:
                f.write("\t"+"Quando "+format_scenario_line(_)+'\n')
            else:
                f.write("\t"+format_scenario_line(_)+'\n')
        f.write('\n')
    f.close()

def check_given_before(text_diagram):

    gherkin_givens = []

    for _ in text_diagram:
        if _.startswith(':'):
            gherkin_givens.append(_)
        else:
            break
    return (gherkin_givens)

def remove_givens(given_list, text_diagram):
    for _ in given_list:
        for text in text_diagram:
            if _ == text:
                text_diagram.remove(text)
    return text_diagram

def generate_scenario(text_diagram):
    feature_name = get_feature_name(text_diagram)
    remove_feature_tittle(feature_name,text_diagram)
    remove_syntax_tags(text_diagram)
    if check_conditional_exist(text_diagram):
        gherkin_givens = check_given_before(text_diagram)
        remove_givens(gherkin_givens, text_diagram)
        scenarios_dict = check_conditionals(text_diagram)
        generate_feature_conditional(feature_name,scenarios_dict, gherkin_givens)
    else:
        generate_feature(feature_name,text_diagram)