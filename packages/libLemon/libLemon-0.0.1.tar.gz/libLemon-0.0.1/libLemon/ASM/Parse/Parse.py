#!/usr/bin/env python3

import json

from libLemon.ASM.Entity import ASMMain
from libLemon.ASM.Entity.State import ASMState
from libLemon.ASM.Entity.Layer import ASMLayer
from libLemon.ASM.Entity.Parameter import ASMParameter
from libLemon.ASM.Entity.Transition import ASMTransition

from libLemon.Utils.Utilities import str2typ, typ2str


def load_asm(asm: ASMMain, path: str):
    asm_struct = json.load(open(path, 'r'))

    for param in asm_struct['asm']['params']:
        param_single = ASMParameter(
            str2typ(param['type']), param['name'], param['value'])
        asm.add_param(param_single)

    for layer in asm_struct['asm']['layers']:
        layer_single = ASMLayer(
            asm, layer['name'], default_state_name=layer['default_state'])
        for state in layer['states']:
            layer_single.add_state(ASMState(
                layer['name'], state['name'], state['exec_path']))
        for transition in layer['transitions']:
            known_states = [
                state.name for state in layer_single.get_all_states()]
            assert(transition['from_state'] in known_states)
            assert(transition['to_state'] in known_states)
            layer_single.add_transition(ASMTransition(
                transition['name'], transition['from_state'], transition['to_state'], transition['condition'], transition['priority']))
        asm.add_layer(layer_single)


def dump_asm(asm: ASMMain, path: str):
    output_dict = {
        'asm': {
            'layers': [],
            'params': []
        }
    }
    for param in asm.get_all_params():
        output_dict['asm']['params'].append({
            'type': typ2str(param.typee),
            'name': param.name,
            'value': param.value
        })

    for layer in asm.get_all_layers():
        output_dict['asm']['layers'].append({
            'name': layer.name,
            'states': [],
            'default_state': layer.get_current_state_name(),
            'transitions': []
        })

        for state in layer.get_all_states():
            output_dict['asm']['layers'][-1]['states'].append({
                'name': state.name,
                'exec_path': state.exec_path
            })

        for transition in layer.get_all_transitions():
            output_dict['asm']['layers'][-1]['transitions'].append({
                'name': transition.name,
                'from_state': transition.from_state,
                'to_state': transition.to_state,
                'condition': transition.condition,
                'priority': transition.priority
            })

    json.dump(output_dict, open(path, 'w'))
