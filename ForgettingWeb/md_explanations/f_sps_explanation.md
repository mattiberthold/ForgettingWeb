$\mathsf{f}^*_{SP}$ forgets any number of atoms.
It brings the input program into a normal form, then employs involved recursions over the derivation rules of
$\mathsf{f}_{SP}$, which are:

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
    q&\leftarrow \textrm{not}\,\textrm{not}\, q
\end{aligned}$$

results in:

$$\begin{aligned}
    a&\leftarrow \textrm{not}\, b,\textrm{not}\,\textrm{not}\, c
\end{aligned}$$

**Positive Cycle Transference**

If there is a self-cycle over $q$, rules with $q$ in the body are cyclicity supporting themselves.
Forgetting $q$ from:

$$\begin{aligned}
    a&\leftarrow q &
    q&\leftarrow \textrm{not}\,\textrm{not}\, q
\end{aligned}$$

results in:

$$\begin{aligned}
    a&\leftarrow \textrm{not}\,\textrm{not}\, a
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

Rules with $\textrm{not}\, q$ in the body are entangled with rules with $q$ in the body.
$\textit{Note, that negative entanglement in } \mathsf{f}^*_{SP} \textit{ as opposed to } \mathsf{f}_{SP} \textit{ does not require a self-cycle over q.}$

Forgetting $q$ from:

$$\begin{aligned}
    a&\leftarrow \textrm{not}\, q &
    b&\leftarrow c, q &
    q&\leftarrow \textrm{not}\,\textrm{not}\, q
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
    q&\leftarrow \textrm{not}\,\textrm{not}\, q
\end{aligned}$$

results in:

$$\begin{aligned}
    a&\leftarrow \textrm{not}\,\textrm{not}\, a
\end{aligned}$$

[(Berthold, 2022)](a "Berthold, M. 2022. On syntactic forgetting with strong persistence. In Kern-Isberner, G.; Lakemeyer, G.; and Meyer, T., eds., Proceedings of the 19th International Conference on Principles of Knowledge Representation and Reasoning, KR 2022, Haifa, Israel. July 31 - August 5, 2022.")