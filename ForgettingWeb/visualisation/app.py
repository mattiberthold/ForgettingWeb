import pathlib

from dash import Dash, html, dcc, Input, Output, State

import dash_bootstrap_components as dbc

from forgetting_operators_logic_programming.forgetting_modules.forget_operator_forget3 import ForgetOperatorForget3
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_r import ForgetOperatorR
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_semantic_wrapper import \
    ForgetOperatorSemanticWrapper
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_sp import ForgetOperatorSP
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_sps import ForgetOperatorSPs
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_u import ForgetOperatorUniform
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_ZFW_strong import ForgetOperatorZFWStrong
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_ZFW_weak import ForgetOperatorZFWWeak
from forgetting_operators_logic_programming.forgetting_modules.forget_operator_strong_as import ForgetOperatorStrongAS
from forgetting_operators_logic_programming.import_export.read_semantical_program import read_input_models
from forgetting_operators_logic_programming.import_export.read_input_program import read_input_program
from forgetting_operators_logic_programming.import_export.read_variables_to_be_forgotten import \
    read_atoms_to_be_forgotten
from forgetting_operators_logic_programming.semantic_modules.lp_to_models import LP2Models
from forgetting_operators_logic_programming.semantic_modules.models_to_lp import Models2LP

app = Dash(__name__, title='ForgettingWeb', routes_pathname_prefix='/forgettingweb/',
           external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# Read demo files for dropdown
demo_files = {'': ([], '')}
resource_path = pathlib.Path(__file__).parent.parent / 'resources'
for file_name in sorted(resource_path.iterdir()):
    with open(file_name, 'r') as read_file:
        name_only = file_name.stem
        variables_to_be_forgotten_line = read_file.readline()
        program_rule_lines = read_file.readlines()
        demo_files[name_only] = (program_rule_lines, variables_to_be_forgotten_line)

header_row = html.Div(children=[
    html.H1('ForgettingWeb', className='header-title', style={'text-align': 'center'})
], className='columns')

left_column = html.Div(children=[
    html.H4(children='Input'),
    html.P('Select a predefined example from the list below or insert your own program and atoms to be forgotten.'),
    html.Div(dcc.Dropdown(options=[{'label': example, 'value': example} for example in list(demo_files.keys())],
                          value=list(demo_files.keys())[0], id='example-input-dropdown'),
             className='dropdown-container'),
    html.B(children='Input program P'),
    html.Div(dcc.Textarea(id='input-program-textbox', value='',
                          placeholder='For example:\na :- q\nb :- not q\nq :- c')),
    html.B(children='Forgetting atoms V'),
    html.Div(dcc.Input(id='input-forgetting-atoms-textbox', type='text', value='', placeholder='For example: q')),
], className='column', style={'width': '30%'})

middle_column = html.Div([
    html.H4(children='Operator'),
    html.P('Choose the operator to be applied.'),
    html.Div(dcc.Dropdown(options=[
        {'label': dcc.Markdown('$\mathsf{f^*_{SP}}$ (Berthold 2022)', mathjax=True), 'value': 'Fsps'},
        {'label': dcc.Markdown('$\mathsf{f_R}$ (Berthold 2022)', mathjax=True), 'value': 'Fr'},
        {'label': dcc.Markdown('$\mathsf{f_{es}}$ (Aguardo et al. 2021)', mathjax=True), 'value': 'Fes'},
        {'label': dcc.Markdown('$\mathsf{f_u}$ (Goncalves et al. 2021)', mathjax=True), 'value': 'Fu'},
        {'label': dcc.Markdown('$\mathsf{f_{SP}^{sem}}$ (Goncalves et al. 2020)', mathjax=True), 'value': 'Fsp_sem'},
        {'label': dcc.Markdown('$\mathsf{f_R^{sem}}$ (Goncalves et al. 2020)', mathjax=True), 'value': 'Fr_sem'},
        {'label': dcc.Markdown('$\mathsf{f_M^{sem}}$ (Goncalves et al. 2020)', mathjax=True), 'value': 'Fm_sem'},
        {'label': dcc.Markdown('$\mathsf{f_{SP}}$ (Berthold et al. 2019)', mathjax=True), 'value': 'Fsp'},
        {'label': dcc.Markdown('$\mathsf{f_{as}}$ (Knorr and Alferes 2014)', mathjax=True), 'value': 'F_Strong_as'},
        {'label': dcc.Markdown('$\mathsf{forget_3}$ (Eiter and Wang 2008)', mathjax=True), 'value': 'forget_3'},
        {'label': dcc.Markdown('$\mathsf{SForgetLP}$ (Zhang and Foo 2006)', mathjax=True), 'value': 'ZFW_Strong'},
        {'label': dcc.Markdown('$\mathsf{WForgetLP}$ (Zhang and Foo 2006)', mathjax=True), 'value': 'ZFW_Weak'},
        {'label': dcc.Markdown('$\mathsf{aux_{cm}}$ (Cabalar and Ferraris 2007)', mathjax=True), 'value': 'Models2Program'}
    ], value='Fsps', id='operator-dropdown'), className='dropdown-container'),
    dbc.Modal([dbc.ModalHeader(dbc.ModalTitle('Operator explanation')),
               dbc.ModalBody(html.Div(id='operator-explanation'))],
              id='operator-explanation-modal', size='xl', is_open=False),
    html.Button('Operator explanation', n_clicks=0, id='explanation-button'),
    html.Br(),
    html.Button('Forget it!', id='submit-value', n_clicks=0, className='centered-button'),
], className='column', style={'width': '30%'})

right_column = html.Div([
    html.Div([
        html.H4('Result'),
        html.Div(id='result')
    ]),
], className='column', style={'width': '30%'})

footer_row = [
    'By ',
    html.A('Matti Berthold', href='https://www.informatik.uni-leipzig.de/~berthold/'),
    ' and ',
    html.A('Daphne Odekerken', href='https://webspace.science.uu.nl/~3827887/'),
    html.Img(src=app.get_asset_url('UniLeipzig-Logo-Neu_RGB_digital.png'), className='logo-image'),
    html.Img(src=app.get_asset_url('scads_ai_logo_von_web _klein.png'), className='logo-image'),
    html.Img(src=app.get_asset_url('UU_logo_2021_EN_RGB.png'), className='logo-image')
]

app.layout = html.Div([
    html.Div(header_row, className='columns'),
    html.Div([left_column, middle_column, right_column], className='columns'),
    html.Div(html.Div(footer_row, className='columns'), className='footer'),
], className='container')


@app.callback(
    Output('input-program-textbox', 'value'),
    Output('input-forgetting-atoms-textbox', 'value'),
    Input('example-input-dropdown', 'value')
)
def update_input(example_dropdown_value: str):
    if example_dropdown_value == '':
        return '', ''
    example_program_rule_lines, example_variables_to_be_forgotten_line = demo_files[example_dropdown_value]
    return ''.join(example_program_rule_lines), example_variables_to_be_forgotten_line


@app.callback(
    Output('result', 'children'),
    Input('submit-value', 'n_clicks'),
    State('input-program-textbox', 'value'),
    State('input-forgetting-atoms-textbox', 'value'),
    State('operator-dropdown', 'value')
)
def update_output(_nr_clicks, input_program_text, input_forgetting_atoms_text, operator_dropdown_text):
    input_program_text_lines = input_program_text.split('\n')
    input_program = read_input_program(input_program_text_lines)

    forgetting_atoms = list(read_atoms_to_be_forgotten(input_forgetting_atoms_text))

    if operator_dropdown_text == 'Fr':
        output_program = ForgetOperatorR.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Fsp':
        output_program = ForgetOperatorSP.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Fsps':
        output_program = ForgetOperatorSPs.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Fes':
        output_program, asd = ForgetOperatorStrongAS.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Fsp_sem':
        output_program = ForgetOperatorSemanticWrapper.apply_sem_sp(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Fr_sem':
        output_program = ForgetOperatorSemanticWrapper.apply_sem_r(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Fm_sem':
        output_program = ForgetOperatorSemanticWrapper.apply_sem_m(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'ZFW_Strong':
        output_program = ForgetOperatorZFWStrong.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'ZFW_Weak':
        output_program = ForgetOperatorZFWWeak.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Fu':
        output_program = ForgetOperatorUniform.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'forget_3':
        output_program = ForgetOperatorForget3.apply(input_program, forgetting_atoms)
    elif operator_dropdown_text == 'Models2Program':
        input_program, signature = read_input_models(input_program_text)
        output_program = Models2LP.apply(input_program, signature)
    else:
        output_program, p_forgettable = ForgetOperatorStrongAS.apply(input_program, forgetting_atoms)
        if not p_forgettable:
            return str(output_program) + '\n The iteration was stopped - The program was not q-forgettable for an ' \
                                         'element q in V. '
    if 'not' in input_program_text:
        output_program_str = output_program.long_str
    else:
        output_program_str = str(output_program)

    if operator_dropdown_text.endswith('_sem'):
        # This was a semantic operator
        original_models = LP2Models.apply(input_program)
        new_models = LP2Models.apply(output_program)

        def models_to_str(models):
            return '\n'.join([str(model) for model in models])

        return html.Div([
            html.B('Models of original program'),
            dcc.Textarea(value=models_to_str(original_models)),
            html.B('New program'),
            dcc.Textarea(value=output_program_str),
            html.B('Models of new program'),
            dcc.Textarea(value=models_to_str(new_models))
        ])
    return [html.B('New program'), dcc.Textarea(value=output_program_str)]


@app.callback(
    Output('operator-explanation-modal', 'is_open'),
    Output('operator-explanation', 'children'),
    Input('explanation-button', 'n_clicks'),
    State('operator-dropdown', 'value'),
    State('operator-explanation-modal', 'is_open')
)
def update_operator_explanation(button_pressed, operator_dropdown_text, was_open):
    if button_pressed:
        will_be_open = not was_open
    else:
        will_be_open = was_open

    explanations_folder = pathlib.Path(__file__).parent.parent / 'md_explanations'
    if operator_dropdown_text == 'Fsps':
        with open(explanations_folder / 'f_sps_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'Fr':
        with open(explanations_folder / 'f_r_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'Fes':
        with open(explanations_folder / 'f_es_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'Fu':
        with open(explanations_folder / 'f_u_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'Fsp':
        with open(explanations_folder / 'f_sp_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'F_Strong_as':
        with open(explanations_folder / 'f_as_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'forget_3':
        with open(explanations_folder / 'forget_3_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'ZFW_Strong':
        with open(explanations_folder / 'sforgetlp_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'Models2Program':
        with open(explanations_folder / 'counter_models_explanation.md', 'r') as file:
            latex_explanation = file.read()
    elif operator_dropdown_text == 'ZFW_Weak':
        with open(explanations_folder / 'wforgetlp_explanation.md', 'r') as file:
            latex_explanation = file.read()
    else:
        latex_explanation = ''

    return will_be_open, [html.Div([dcc.Markdown(latex_explanation, mathjax=True)])]


if __name__ == '__main__':
    app.run_server(debug=True)
