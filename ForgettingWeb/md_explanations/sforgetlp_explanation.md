$SForgetLP$ forgets one atom.
It brings $P$ in a normal form, then employs the following derivation rule:

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

Further $SForgetLP$ removes all rules that contain any appearance of $q$.

[(Zhang and Foo 2006)](a "Zhang, Y., and Foo, N. Y. 2006. Solving logic program conflict through strong and weak forgettings. Artificial Intelligence 170(8):739 – 778.")
