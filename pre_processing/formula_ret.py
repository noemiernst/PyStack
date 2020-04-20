

def formula_ret(text):
    formulas = []

    error = False
    if text.find('$') > -1:
        _,found,after = text.partition('$')
        while found:
            if text.find('$') > -1:
                formula,found,after = after.partition('$')

                if(formula.endswith('\\')):
                    formula_temp,found_temp,after = after.partition('$')
                    formula = formula + found + formula_temp
                if formula != '':
                    if found:
                        formulas.append(formula)
                    else:
                        #raise ValueError("Missing end tag: " + after)
                        print('missing end tag $')
                        error = True

                    _,found,after = after.partition('$')
                else:
                    formula,found,after = after.partition('$$')
                    if found:
                        formulas.append(formula)
                    else:
                        #raise ValueError("Missing end tag: " + after)
                        print('missing end tag $$')
                        after = formula
                        error = True

                    _,found,after = after.partition('$')
            if error:
                break
    return formulas, error

# operatoren: z.B. &amp, &lt, &gt



#formula_ret("test 123 $formel$ lala$ich bin noch eine formel$")
#formula_ret("$ich bin noch eine formel$")
#formula_ret("test 123 $$formel$$ lala")
#formula_ret("$$test 123 ormel$$ lala")
#formula_ret("$$ich bin noch eine formel$$ test 123 $for\$mel1$ lala test 123 $formel2$ lala test 123 $formel3$ lala")

#formula_ret("<blockquote>\n  <p>A 10-year loan of $500 is repaid with\n  payments at the end of each year. The lender charges interest at an\n  annual effective rate of 10%. \n  Each of the first ten payments is\n  150% of the amount of interest due. \n  Each of the last ten payments is X. \n  Calculate X.</p>\n</blockquote>\n\n<p>I came across this practice question while studying for my actuary exam. I tried it on my own and got stuck:</p>\n\n<p>$\\$ $500 will earn $\\$ $50 interest each year, so each of the first 10 payments must be $\\$ $75.  </p>\n\n<p>Then after 10 years, a total of 750 has been repaid.<br>\nIn 10 years, I can find the accumulated debt by saying <code>PV</code>=500, <code>I/Y</code>=10, <code>N</code>=10, giving me <code>FV</code>=$\\$ $1296.87. So the balance would be $\\$ $1296.87-$\\$ $750=$\\$ $546.97.  </p>\n\n<p>Now I am stuck! How do I find out what the last payments should be? I know I can't just divide $\\$ $546.97/10=$\\$ $54.697, because the lender is still charging interest while the borrower pays off this remaining debt, so there would still be the interest left over.</p>\n\n<p>This situation isn't mentioned anywhere in my calculator manual! Can one of you give me some explanation about what is going on so that I can do it by hand?</p>\n\n<hr>\n\n<p>I tried working on it some more, and came up with a really great idea! Since the payments are 1.5x the 10% interest, it's just like paying off 5% of the principal each year! This saves me a lot of time, because I can just set <code>I/Y=-5</code> and get <code>FV=598.74</code> on my calculator. I did it the long way by calculating the future value of each interest payment (turns out they were not all $75, because the outstanding principal got smaller), and they were the same. Is this always going to work, or did I just get lucky here?  </p>\n\n<hr>\n\n<p>Another update!<br>\nI think I solved it. All I needed to do was to set <code>FV=0</code>, <code>I/Y=10</code>, <code>N=10</code>, <code>PV=598.74</code>, and then I got <code>PMT=97.44</code>. I never used the <code>PMT</code> button before, though, so is there some other way I can check the answer is right?</p>\n")
#print(formula_ret("<p>Say there are three jars, $j_1, j_2, j_3$ filled with different binary sequences of length two.  </p>\n\n<p>The distribution of the binary sequences in each of the jars is given by the $p_i^k(1-p_i)^{n-k}$, where \n$p_i = \\frac{i}{m + 1}$ where $m$ is the number of jars, $i$ is the jar index, $k $is number of 1$$'s and $n$ is the length of the string.  </p>\n\n<p>So for three jars we have $p_1 = 0.25, p_2 = 0.5$, and $p_3 = 0.75$ for $j_1, j_2, j_3$ respectively.  </p>\n\n<p>Here are the sequences and their probabilities for $j_1$ with $p_1 = 0.25$:</p>\n\n<p>\\begin{align*}\nP(00) = 9 / 16 \\\\\nP(10) = 3 / 16 \\\\  \nP(01) = 3 / 16 \\\\  \nP(11) = 1 / 16.\n\\end{align*}</p>\n\n<p>If I tell you that I have selected a binary sequence and the first element is $1$ what is the E($p_i$)?</p>\n\n<p>Well, this can be calculated by looking at each of the jars and adding up the probability of candidate sequences times the value of $p_i$.</p>\n\n<p><strong>Edit:</strong> I wasn't normalizing this conditionally space properly. I'm skipping a step which I'll explain, someone wants.</p>\n\n<p>\\begin{equation*}\nE(p_i) = (4/24 * 1/4) + (8/24 * 1/2) + (12/24 * 3/4) = 14 / 24 = 0.58.\n\\end{equation*}</p>\n\n<p>So the question is ... what is $E(p_i)$ when the numbers of jars goes to infinity (or alternatively, when $p$ can take on values between $0$ and $1$)? Also what happens when the size of the binary strings goes to infinity? Does it have an effect on the outcome? If it does, does the order we take the limits change the answer?</p>\n\n<p>And most importantly what is the general case for when I have $s$ 1's and $r$ $0$'s?, with a continuous $p$ from $0$ to $1$ and infinite sequences?</p>\n"))
