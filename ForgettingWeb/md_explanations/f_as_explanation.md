$\mathsf{f}_{as}$ forgets one atom.
It brings the input program into a normal form. It is only defined over such programs that do not contain self-cycles over $q$ in normal form.
$\mathsf{f}_{as}$ employs the following derivation rules:

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

Further $\mathsf{f}_{as}$ removes all rules that contain any appearance of $q$.

[(Knorr and Alferes 2014)](a "Knorr, M., and Alferes, J. J. 2014. Preserving strong equivalence while forgetting. In Proceedings of (JELIA-14), volume 8761 of LNCS, 412–425. Springer.")