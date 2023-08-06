#!/usr/bin/env python3

from libLemon.ASM.Delegate import ParamDelegate
from libLemon.ASM.Entity import ASMState, ASMTransition

import libLemon.Utils.Logger as Logger
from libLemon.Utils.Utilities import judge_condition
from libLemon.Error import ScheduleError, NoStateFoundError, StateExistedError, NoTransitionFoundError, TransitionExistedError


class ASMLayer(ParamDelegate):

    _delegate: ParamDelegate

    name: str

    _current_state_name: str
    _states: dict[str: ASMState]
    _transitions: dict[str: ASMTransition]

    def __init__(self, name: str, states: list[ASMState] = list(), transitions: list[ASMTransition] = list(), default_state_name: str = '', delegate: ParamDelegate=None):
        self.name = name
        self._delegate = delegate
        self._states = {state.name: state for state in states}
        self._transitions = {
            transition.name: transition for transition in transitions}
        self._current_state_name = default_state_name

    def __str__(self) -> str:
        return 'ASMLayer `%s`: (%d states, %d transitions)' % (self.name, len(self._states), len(self._transitions))

    """
    delegate methods
    """
    # simply forward requests to ASM now.
    # maybe add some cache feature in the future. 
    def get_parameter_value(self, name: str):
        if not self._delegate:
            raise RuntimeError('layer `%s` delegate not initialized' % self.name)
        return self._delegate.get_parameter_value(name)

    def get_all_params_name(self) -> list[str]:
        if not self._delegate:
            raise RuntimeError('layer `%s` delegate not initialized' % self.name)
        return self._delegate.get_all_params_name()

    def set_parameter_value(self, name: str, value):
        if not self._delegate:
            raise RuntimeError('layer `%s` delegate not initialized' % self.name)
        return self._delegate.set_parameter_value(name, value)

    """
    state getter/setter methods
    """

    def add_state(self, state: ASMState):
        if state.name in self._states:
            raise StateExistedError('existed state named `%s` in layer `%s`' %
                                    (state.name, self.name))
        self._states.update({state.name: state})

    def get_state(self, name: str) -> ASMState:
        try:
            return self._states[name]
        except KeyError:
            raise NoStateFoundError('no state `%s` in layer `%s`' %
                                    (name, self.name))

    def del_state(self, name: str):
        try:
            del self._states[name]
        except KeyError:
            raise NoStateFoundError('no state named `%s` in layer `%s`' %
                                    (name, self.name))

    def get_all_states(self) -> list[ASMState]:
        return [state for _, state in self._states.items()]

    def del_all_states(self):
        self._states.clear()

    """
    transition getter/setter methods
    """

    def add_transition(self, transition: ASMTransition):
        if transition.name in self._transitions:
            raise TransitionExistedError("existed transition named `%s` in layer `%s`" %
                                         (transition.name, self.name))
        self._transitions.update({transition.name: transition})

    def get_transition(self, name: str) -> ASMTransition:
        try:
            return self._transitions[name]
        except KeyError:
            raise NoTransitionFoundError('no transition `%s` in layer `%s`' %
                                         (name, self.name))

    def del_transition(self, name: str):
        try:
            del self._transitions[name]
        except KeyError:
            raise NoTransitionFoundError('no transition named `%s` in layer `%s`' %
                                         (name, self.name))

    def get_all_transitions(self) -> list[ASMTransition]:
        return [transition for _, transition in self._transitions.items()]

    def del_all_transitions(self):
        self._transitions.clear()

    def get_current_state_name(self) -> str:
        return self._current_state_name

    def set_current_state_name(self, name: str):
        self._current_state_name = self.get_state(name).name

    def start(self):
        while True:
            # blocking!
            Logger.info('layer `%s` is going to schedule state `%s`' % (self.name, self._current_state_name))
            self._states[self._current_state_name].schedule()

            # prepare for the next schedule
            available_trans = [
                trans for trans in self.get_all_transitions() if trans.from_state == self._current_state_name]
            if not available_trans:
                # ASMLayer dead!
                raise ScheduleError(
                    "No available transitions in layer `%s`" % self.name)
            available_trans.sort(key=lambda t: t.priority, reverse=True)

            touched = False
            for t in available_trans:
                if judge_condition(self._delegate, t.condition):
                    self._current_state_name = t.to_state
                    Logger.info('layer `%s` just decided transition `%s`' % (self.name, t.name))
                    touched = True
                    break
            if not touched:
                raise ScheduleError(
                    "No available transitions in layer `%s`" % self.name)
