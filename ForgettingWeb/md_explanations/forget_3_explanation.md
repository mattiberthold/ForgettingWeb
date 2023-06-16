$forget_3$ forgets one atom.
It pre-processes $P$ by eliminating some redundancies; removing all atoms appearing in negative rule bodies, if they do not appear in a rule's head; and
applying positive cut rule to $\textit{all}$ atoms appearing in $P$.
Then, $forget_3$ applies semi-shifting w.r.t. $q$, then applies negative cut.

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

Further $forget_3$ removes all rules that contain any appearance of $q$.

[(Eiter and Wang 2008)](a "Eiter, T., and Wang, K. 2008. Semantic forgetting in answer set programming. Artificial Intelligence 172(14):1644–1672.")