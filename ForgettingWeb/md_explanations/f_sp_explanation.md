$\mathsf{f}_{SP}$ forgets one atom.
It brings the input program into a normal form, then employs the following derivation rules (where a rule is copied, in order to apply each derivation to it):

**Positive Cut**

Appearances of $q$ in a rule's body are replaced with the body of a rule that has $q$ in its head.
Forgetting $q$ from:

$$\begin{aligned}
a&\leftarrow q &
q&\leftarrow b &
q&\leftarrow c
\end{aligned}$$

results in:

$$\begin{aligned}
a&\leftarrow b &
a&\leftarrow c
\end{aligned}$$

**Positive Entanglement**

If there is a self-cycle over $q$,
rules with $q$ in the body are entangled with rules with $\textrm{not}\, q$ in the body.
Forgetting $q$ from:

$$\begin{aligned}
a&\leftarrow q &
b&\leftarrow c, \textrm{not}\, q &
q&\leftarrow\textrm{not}\,\textrm{not}\, q
\end{aligned}$$

results in:

$$\begin{aligned}
a&\leftarrow \textrm{not}\, b,\textrm{not}\,\textrm{not}\,\textrm{not}\, c
\end{aligned}$$

**Positive Cycle Transference**

If there is a self-cycle over $q$,
rules with $q$ in the body are cyclicity supporting themselves.
Forgetting $q$ from:

$$\begin{aligned}
a&\leftarrow q &
q&\leftarrow\textrm{not}\,\textrm{not}\, q
\end{aligned}$$

results in:

$$\begin{aligned}
a&\leftarrow\textrm{not}\,\textrm{not}\, a
\end{aligned}$$

**Negative Cut**

Appearances of $\textrm{not}\, q$ in a rule's body are replaced with literals proving $q$ to be not derivable.
Forgetting $q$ from:

$$\begin{aligned}
a&\leftarrow \textrm{not}\, q &
q&\leftarrow b,c &
q&\leftarrow d
\end{aligned}$$

results in:

$$\begin{aligned}
a&\leftarrow \textrm{not}\, b, \textrm{not}\, d &
a&\leftarrow \textrm{not}\, c, \textrm{not}\, d
\end{aligned}$$

**Negative Entanglement**

If there is a self-cycle over $q$,
rules with $\textrm{not}\, q$ in the body are entangled with rules with $q$ in the body.
Forgetting $q$ from:

$$\begin{aligned}
a&\leftarrow \textrm{not}\, q &
b&\leftarrow c, q &
q&\leftarrow\textrm{not}\,\textrm{not}\, q
\end{aligned}$$

results in:

$$\begin{aligned}
a&\leftarrow \textrm{not}\, b,\textrm{not}\,\textrm{not}\, c
\end{aligned}$$

**Negative Cycle Transference**

If there is a self-cycle over $q$,
rules with $\textrm{not}\, q$ in the body are cyclicity supporting themselves.
Forgetting $q$ from:

$$\begin{aligned}
a&\leftarrow \textrm{not}\, q &
q&\leftarrow\textrm{not}\,\textrm{not}\, q
\end{aligned}$$

results in:

$$\begin{aligned}
a&\leftarrow\textrm{not}\,\textrm{not}\, a
\end{aligned}$$

Further $\mathsf{f}_{SP}$ removes all rules that contain any appearance of $q$.

[(Berthold et al. 2019)](a "Berthold, M.; Gonc¸alves, R.; Knorr, M.; and Leite, J. 2019. A syntactic operator for forgetting that satisfies strong persistence. Theory and Practice of Logic Programming 19(5-6):1038–1055.")