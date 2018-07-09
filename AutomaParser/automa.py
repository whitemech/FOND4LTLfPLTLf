import re

class Automa:
    """
        DFA Automa:
        - alphabet         => set() ;
        - states           => set() ;
        - initial_state    => str() ;
        - accepting_states => set() ;
        - transitions      => dict(), where
        **key**: *source* ∈ states
        **value**: {*action*: *destination*)
    """

    def __init__(self, alphabet, states, initial_state, accepting_states, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.validate()

    def valide_transition_start_states(self):
        for state in self.states:
            if state not in self.transitions:
                raise ValueError(
                    'transition start state {} is missing'.format(
                        state))

    def validate_initial_state(self):
        if self.initial_state not in self.states:
            raise ValueError('initial state is not defined as state')

    def validate_accepting_states(self):
        if any(not s in self.states for s in self.accepting_states):
            raise ValueError('accepting states not defined as state')

    def validate_input_symbols(self):
        alphabet_pattern = self.get_alphabet_pattern()
        for state in self.states:
            for action in self.transitions[state]:
                if not re.match(alphabet_pattern, action):
                    raise ValueError('invalid transition found')

    def get_alphabet_pattern(self):
        return re.compile("(^["+''.join(self.alphabet)+"]+$)")

    def validate(self):
        self.validate_initial_state()
        self.validate_accepting_states()
        self.valide_transition_start_states()
        self.validate_input_symbols()
        return True

    def __str__(self):
        automa = 'alphabet: {}\n'.format(str(self.alphabet))
        automa += 'states: {}\n'.format(str(self.states))
        automa += 'init_state: {}\n'.format(str(self.initial_state))
        automa += 'accepting_states: {}\n'.format(str(self.accepting_states))
        automa += 'transitions: {}'.format(str(self.transitions))
        return automa

    def create_operator_trans(self):
        '''create operator trans as a string'''
        operator  = '(:action trans\n'
        operator += '\t:parameters ()\n'
        operator += '\t:precondition (not turnDomain)\n'
        operator += '\t:effect (oneof {0}\t)\n'.format(' '.join(self.get_whens()))
        operator += ')'
        return operator


    def get_whens(self):
        whens = []
        for state in self.states:
            for action in self.transitions[state]:
                whens.append(self.get_formula_when(state,action))
        return whens

    def get_formula_when(self, state, action):
        formula_when  = '(when {0} {1})\n'.format(self.get_formula_condition(state, action),self.get_formula_statement(state, action))
        return formula_when

    def get_formula_condition(self, state, action):
        formula_condition = '(and (q = {0}) {1})'.format(state, ' '.join(self.get_condition_action(action)))
        return formula_condition

    def get_formula_statement(self, state, action):
        formula_statement = '(and (q = {0}) (turnDomain))'.format(self.transitions[state][action])
        return formula_statement

    def get_condition_action(self, action):
        temp = []
        for char in action:
            temp.append('('+char+')')
        return temp