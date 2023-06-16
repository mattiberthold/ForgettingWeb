$\mathsf{f}_u$ forgets one atom.
It brings $P$ in normal form.
If $NF(P)$ has loops over $q$, $\mathsf{f}_u$ is calculated semantically, otherwise:

**Semi-shift**

All rules with $q$ in the head, are semi-shifted, i.e. replaced with two rules, where in one all head literals but $q$ are moved to the body, and in the other $q$ is moved to the negative body.
Semi-shifting $q$ in:

$$\begin{aligned}
q\vee a\vee b&\leftarrow \textrm{not}\, c
\end{aligned}$$

results in:

$$\begin{aligned}
q&\leftarrow \textrm{not}\, a,\textrm{not}\, b,\textrm{not}\, c &
a\vee b&\leftarrow \textrm{not}\, c, \textrm{not}\, q
\end{aligned}$$

Then the following derivation rules are employed:

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

Further $\mathsf{f}_u$ removes all rules that contain any appearance of $q$.

[(Goncalves et al. 2021)](a "Gonc¸alves, R.; Janhunen, T.; Knorr, M.; and Leite, J. 2021. On syntactic forgetting under uniform equivalence. In Proceedings of (JELIA-21), volume 12678 of Lecture Notes in Computer Science, 297–312. Springer.")
