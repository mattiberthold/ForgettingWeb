$\mathsf{aux_{cm}}$ takes a set of HT-models as an input and returns a canonical program with these models.

Given $\mathcal{M}$,

$\Sigma =\bigcup\{Y\mid (X,Y)\in\mathcal{M}\}$

For any $\langle Y,Y\rangle$ that is not a model there is a rule $\leftarrow\textrm{not}\ \Sigma\setminus Y, \textrm{not}\ \textrm{not}\ Y$.

For any $\langle X,Y\rangle$ that is not a model, s.t. $\langle Y,Y\rangle$ is a model, there is a rule $\Sigma\setminus X\leftarrow X,\textrm{not}\ \Sigma\setminus Y, \textrm{not}\ \textrm{not}\ Y\setminus X$.

Use the operator by listing HT-models in the 'Input program P' textbox, like, for example:

'<ab,ab><a,ab><b,ab><,ab><a,a><,>'
