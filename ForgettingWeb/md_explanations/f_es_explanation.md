$\mathsf{f}_{es}$ forgets one atom.
It brings the input program into a normal form. It is only defined over such programs that do not contain self-cycles over $q$ in normal form, nor have rule's with $q$ and other atoms in their head.
$\mathsf{f}_{es}$ employs the following derivation rules:

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

Further $\mathsf{f}_{es}$ removes all rules that contain any appearance of $q$.

