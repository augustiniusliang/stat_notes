# 过渡到准经典的情形

现在我们已经学习了量子统计的基本原理与热力学，我们可以着手开始统计力学的工作。需要指出，在实际遇到的问题当中，系统的能级是甚密的，在一定范围可以看成是近似于连续。所以，我们不需要，在大多时候也并不能计算出这些粒子的所有能级，而是简单地指出这些能级就是经典能量。

## 半经典统计

### 例子：箱内的粒子

我们现在考虑一个简单的问题：一个无限深的三维势阱中的粒子能级。设势阱的维度是 $l_a, l_b, l_c,$ 则粒子能级为

$$
E_{n_a, n_b, n_c} = \frac{\hbar^2 \pi^2}{2m} \left( \frac{n_a^2}{l_a^2} + \frac{n_b^2}{l_b^2} + \frac{n_c^2}{l_c^2} \right),
$$

其中 $n_a, n_b, n_c$ 是正整数。我们可以看到，能级是离散的，并且随着 $n_a, n_b, n_c$ 的增大，能级也会增大。当 $l_a, l_b, l_c$ 足够大时，严格来说就是：

$$
E \gg \frac{\hbar^2 \pi^2}{2ml^2}
$$
时，
能级之间的间隔就会变得非常小，我们可以近似地将能级看成是连续的。
在这种情况下，在 $(E, E+\Delta E)$ 范围内的能级数可以如此求：我们可以将 $\left( \frac{n_a}{l_a}, \frac{n_b}{l_b}, \frac{n_c}{l_c} \right)$ 看成是三维空间中的一个点，那么能级 $E$ 就对应于一个球面，能级 $E+\Delta E$ 就对应于另一个球面。我们需要计算这两个球面之间的体积，这个体积就对应于能级数。具体来说，能级数 $g(E) \Delta E$ 可以通过以下公式计算：

$$
g(E) \Delta E = n_{E+\Delta E} - n_E,
$$

其中 $n_E$ 是满足 $E_{n_a, n_b, n_c} = E$ 的 $n_a, n_b, n_c$ 的值。但是，$n_E$ 的数值可以近似地通过计算上述三维空间的体积关系来得到：

$$
n_E \cdot \frac{1}{l_al_bl_c} = \frac 43 \pi \left( \frac{E}{\hbar^2 \pi^2 / (2m)} \right)^{3/2}
$$

因此，我们可以得到能级数 $g(E) \Delta E$ 的表达式：

$$
g(E) \Delta E = \frac{4\pi l_al_bl_c}{3} \left( \frac{2m}{\hbar^2 \pi^2} \right)^{3/2} E^{1/2} \Delta E.
$$

这就是

$$
g(E) = \frac{4\pi l_al_bl_c}{3} \left( \frac{2m}{\hbar^2 \pi^2} \right)^{3/2} E^{1/2}.
$$

在这个简单的例子中，我们计算出的正则配分函数是：

$$
Z = \sum_{n_a, n_b, n_c} e^{-\beta E_{n_a, n_b, n_c}} \approx \int_0^\infty g(E) e^{-\beta E} dE = \frac{V}{\lambda^3},
$$

其中 $V = l_a l_b l_c$ 是势阱的体积，$\lambda = h / \sqrt{2\pi m k_B T}$ 是热波长。我们得到了粒子处于能量 $E = \frac{p^2}{2m}$ 的概率是：

$$
P(E) dE = \frac{g(E) e^{-\beta E}}{Z} dE = \frac{4\pi V}{\lambda^3} \left( \frac{2m}{\hbar^2 \pi^2} \right)^{3/2} E^{1/2} e^{-\beta E} dE = \left( \frac{m}{\pi k_BT} \right)^{3/2} \exp\left( -\frac{p^2}{2m k_B T} \right) 4\pi p^2 dp.
$$

最后一个式子叫做 Maxwell 分布函数，描述了粒子在动量空间中的分布情况。我们可以看到，粒子在动量空间中的分布是一个高斯分布，中心在 $p=0$，宽度由温度 $T$ 和粒子质量 $m$ 决定。这个结果中不含有 $\hbar,$ 因而可以由经典统计力学得到。

### 正则配分函数的半经典近似

{  这部分参考了知乎用户 *Gzz* 的文章。 感兴趣的读者也可以参考 M. Kardar 的书 *Statistical Physics of Particles* 的第 7 章。这一小节的内容对应的是 7.2 节，下一小节的内容对应的是 7.3 节。}

现在我们在坐标表象下来计算配分函数。我们知道，对于处于位置 $\left( \vec{q_1},\vec{q_2},\cdots, \vec{q_N} \right)$ 的 $N-$ 粒子系统（让我们不考虑各个粒子位置相同的情况，这样的情况在 $V\to\infty$ 的情况下成为“测度为零”的），二次量子化的基矢量是：

$$
\ket{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} = \frac{1}{\sqrt{N!}} \hat{\psi}^\dagger(\vec{q_1}) \hat{\psi}^\dagger(\vec{q_2}) \cdots \hat{\psi}^\dagger(\vec{q_N}) \ket{0},
$$

或者用单粒子坐标基矢量写作

$$
\ket{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} = \frac{1}{\sqrt{N!}} \sum_{\sigma}\left( \pm 1 \right)^\sigma \ket{\vec{q_{\sigma(1)}}}\ket{\vec{q_{\sigma(2)}}}\cdots\ket{\vec{q_{\sigma(N)}}},
$$

其中正负号分别对应 Bose 子和 Fermi 子。按照完备性有

$$
\frac{1}{N!} \int_V d\vec{q_1} \int_V d\vec{q_2} \cdots \int_V d\vec{q_N} \ket{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} \bra{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} = 1.
$$

当然，右侧的单位算符是作用在 $N-$ 粒子空间上的。乘以因子 $\frac{1}{N!}$ 的原因是：对于 $N$ 个粒子，我们在积分中考虑了 $N!$ 个相同的情况（即粒子位置的排列），因此需要除以 $N!$ 来避免重复计算。
我们可以将配分函数写成如下形式：

$$
Z  = \mathrm{tr}\left( \exp\left( -\beta \hat{H} \right) \right) = \frac{1}{N!}\int d^N\vec{q} \bra{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} \exp\left( -\beta \hat{H} \right) \ket{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}}.
$$

典型的的哈密顿算符形式是

$$
\hat{H} = \hat{T}\left( \hat{\vec{p}}_1,\cdots,\hat{\vec{p}}_N \right) + \hat{V}\left( \hat{\vec{q}}_1,\cdots,\hat{\vec{q}}_N \right).
$$

代入得到：

$$
Z = \frac{1}{N!} \int d^N\vec{q} \bra{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} e^{-\beta \hat{T}-\beta \hat{V}} \ket{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}}.
$$

在热力学极限下，我们可以作如下近似：

$$
e^{-\beta \hat{T}-\beta \hat{V}} = \exp\left( -\frac{\beta \hat{V}}{2} \right)\exp\left( -\beta \hat{T} \right) \exp\left( -\frac{\beta \hat{V}}{2} \right) + O(\beta^3).
$$

这个近似被称为 Trotter-Suzuki 近似。代入上式，我们可以得到：

$$
Z = \frac{1}{N!} \int d^N\vec{q} \bra{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} e^{-\frac{\beta \hat{V}}{2}} e^{-\beta \hat{T}} e^{-\frac{\beta \hat{V}}{2}} \ket{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}}.
$$

势能算符 $\hat{V}$ 是位置算符的函数，因此它在位置表象下是对角的。因此，配分函数可以写成：

$$
Z = \frac{1}{N!} \int d^N\vec{q} e^{-\beta V(\vec{q_1},\cdots,\vec{q_N})} \bra{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}} e^{-\beta \hat{T}} \ket{\vec{q_1},\vec{q_2},\cdots, \vec{q_N}}.
$$

为了计算这个矩阵元，我们可以引入动量表象的完备性关系：

$$
\frac{1}{N!h^{3N}}\int d^N\vec{p} \ket{\vec{p_1},\vec{p_2},\cdots, \vec{p_N}} \bra{\vec{p_1},\vec{p_2},\cdots, \vec{p_N}} = 1.
$$

其中的 $h^{3N}$ 来自动量波函数的箱归一化，并取 $V\to \infty$ 的极限（因而化求和为积分是容许的）。具体来说，对于长度是 $\left( l_1,l_2,l_3 \right)$的箱来说， $\vec{p} = \frac{2\pi\hbar}{L}\left( n_1,n_2,n_3 \right),$ 因此可以知道在动量空间中每个态占据的体积是 $\left( \frac{2\pi\hbar}{L} \right)^3 = \frac{h^3}{V}.$ 在 $V\to \infty$ 的极限下，化求和为积分，就有

$$
\sum_p \to \frac{V}{h^3} \int d^3\vec{p}.
$$

这样，我们就有：

$$
\begin{aligned}
            Z &= \frac{1}{\left( N! \right)^3h^{3N}} \int d^N\vec{q} e^{-\beta V(\vec{q_1},\cdots,\vec{q_N})} \int d^N\vec{p} \bra{\vec{p_1},\vec{p_2},\cdots, \vec{p_N}} e^{-\beta \hat{T}} \ket{\vec{p_1},\vec{p_2},\cdots, \vec{p_N}} 
            \\ &\braket{\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N|\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N} \braket{\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N|\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N}.
    \end{aligned}
$$

同样，动量算符 $\hat{T}$ 是动量表象下的函数，因此它在动量表象下是对角的。因此，配分函数可以写成：

$$
\begin{aligned}
            Z &= \frac{1}{\left( N! \right)^2 h^{3N}} \int d^N\vec{q} e^{-\beta V(\vec{q_1},\cdots,\vec{q_N})} \int d^N\vec{p} e^{-\beta T(\vec{p_1},\cdots,\vec{p_N})} 
    \\ &\braket{\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N|\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N} \braket{\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N|\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N}.
    \end{aligned}
$$

剩下的问题是计算位置表象和动量表象之间的矩阵元 $\braket{\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N|\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N}$. 按照原始定义，我们有

$$
\begin{aligned}
            \braket{\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N|\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N} &= \frac{1}{{N!}} \sum_{\sigma}\sum_{\tau}\left( \pm 1 \right)^\sigma\left( \pm 1 \right)^\tau \braket{\hat{\vec{q}}_{\sigma(1)}|\hat{\vec{p}}_{\tau(1)}} \braket{\hat{\vec{q}}_{\sigma(2)}|\hat{\vec{p}}_{\tau(2)}} \cdots \braket{\hat{\vec{q}}_{\sigma(N)}|\hat{\vec{p}}_{\tau(N)}}
            \\ &= \sum_{\sigma}\left( \pm 1 \right)^\sigma e^{\frac{i}{\hbar}(\vec{p}_1\cdot\vec{q}_{\sigma(1)} + \vec{p}_2\cdot\vec{q}_{\sigma(2)} + \cdots + \vec{p}_N\cdot\vec{q}_{\sigma(N)})}
    \end{aligned}
$$

第二个等号是一个简单的计数。现在两个矩阵元的乘积可以写成：

$$
\begin{aligned}
            &\braket{\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N|\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N} \braket{\hat{\vec{p}}_1,\hat{\vec{p}}_2,\cdots, \hat{\vec{p}}_N|\hat{\vec{q}}_1,\hat{\vec{q}}_2,\cdots, \hat{\vec{q}}_N} 
    \\ =& \sum_{\sigma}\sum_{\tau}\left( \pm 1 \right)^{\sigma+\tau} e^{\frac{i}{\hbar}(\vec{p}_1\cdot\vec{q}_{\sigma(1)} + \vec{p}_2\cdot\vec{q}_{\sigma(2)} + \cdots + \vec{p}_N\cdot\vec{q}_{\sigma(N)})} e^{-\frac{i}{\hbar}(\vec{p}_1\cdot\vec{q}_{\tau(1)} + \vec{p}_2\cdot\vec{q}_{\tau(2)} + \cdots + \vec{p}_N\cdot\vec{q}_{\tau(N)})}.
    \end{aligned}
$$

现在，通过同样的计数，我们可以写有：

$$
\begin{aligned}
            &\sum_{\sigma}\sum_{\tau}\left( \pm 1 \right)^{\sigma+\tau} e^{\frac{i}{\hbar}(\vec{p}_1\cdot\vec{q}_{\sigma(1)} + \vec{p}_2\cdot\vec{q}_{\sigma(2)} + \cdots + \vec{p}_N\cdot\vec{q}_{\sigma(N)})} e^{-\frac{i}{\hbar}(\vec{p}_1\cdot\vec{q}_{\tau(1)} + \vec{p}_2\cdot\vec{q}_{\tau(2)} + \cdots + \vec{p}_N\cdot\vec{q}_{\tau(N)})} 
    \\ =& N! \sum_{\sigma}\left( \pm 1 \right)^{\sigma} e^{\frac{i}{\hbar}(\vec{p}_1\cdot\vec{q}_{\sigma(1)} + \vec{p}_2\cdot\vec{q}_{\sigma(2)} + \cdots + \vec{p}_N\cdot\vec{q}_{\sigma(N)})} e^{-\frac{i}{\hbar}(\vec{p}_1\cdot\vec{q}_{1} + \vec{p}_2\cdot\vec{q}_{2} + \cdots + \vec{p}_N\cdot\vec{q}_{N})}
    \\ =& N! \sum_{\sigma}\left( \pm 1 \right)^{\sigma} e^{\frac{i}{\hbar}(\vec{p}_1\cdot\left( \vec{q}_{\sigma_1}-\vec{q}_1 \right) + \vec{p}_2\cdot\left( \vec{q}_{\sigma_2}-\vec{q}_2 \right) + \cdots + \vec{p}_N\cdot\left( \vec{q}_{\sigma_N}-\vec{q}_N \right))}.
    \end{aligned}
$$

现在，我们可以将配分函数写成如下形式：

$$
\begin{aligned}
            Z &= \frac{1}{N!h^{3N}} \int d^N\vec{q} e^{-\beta V(\vec{q_1},\cdots,\vec{q_N})} \int d^N\vec{p} e^{-\beta T(\vec{p_1},\cdots,\vec{p_N})} \sum_{\sigma}\left( \pm 1 \right)^{\sigma} e^{\frac{i}{\hbar}(\vec{p}_1\cdot\left( \vec{q}_{\sigma_1}-\vec{q}_1 \right) + \vec{p}_2\cdot\left( \vec{q}_{\sigma_2}-\vec{q}_2 \right) + \cdots + \vec{p}_N\cdot\left( \vec{q}_{\sigma_N}-\vec{q}_N \right))} 
    \\ =& \frac{1}{N!h^{3N}} \int d^N\vec{q} e^{-\beta V(\vec{q_1},\cdots,\vec{q_N})} \int d^N\vec{p} e^{-\beta T(\vec{p_1},\cdots,\vec{p_N})} \quad \left( h \to 0 \right)
    \end{aligned}
$$

在 $h$ 趋于零时，除了恒等置换以外的所有置换都会导致指数中的相位迅速振荡，从而在积分中相互抵消。所以，我们就得到了半经典波函数的表达式：

$$
\boxed{Z = \frac{1}{N!h^{3N}} \int d^N\vec{q} e^{-\beta V(\vec{q_1},\cdots,\vec{q_N})} \int d^N\vec{p} e^{-\beta T(\vec{p_1},\cdots,\vec{p_N})}}.
$$

一般地，若是一个系统的所有粒子加起来共有 $s-$ 个自由度，那么配分函数可以写成如下形式：

$$
\boxed{Z = \frac{1}{N!h^s} \int d^s q d^s p e^{-\beta H}}.
$$

这就是 Maxwell-Boltzmann 统计。对于自由粒子来说，哈密顿量 $H$ 就是动能 $T$，因此配分函数可以写成：

$$
Z = \frac{1}{N!h^{3N}} \int d^N\vec{q} \int d^N\vec{p} e^{-\beta \sum_{i=1}^N \frac{\vec{p}_i^2}{2m}} = \frac{V^N}{N!\lambda^{3N}} = \frac{1}{N!} \left( \frac{V}{\lambda^3} \right)^N.
$$

其中，我们看到，$Z_1 = V\lambda^{-3}$ 就是我们在上节使用纯粹的统计办法算出的单粒子正则配分函数。
这个结果可以解释为：一个能级在相空间内占据的体积是 $\frac{dqdp}{h}.$ 另外，我们看到尽管我们已经做了半经典近似，配分函数中仍然包含了 $h$。这就说明，纯粹的经典统计是不存在的，必须要有量子效应的修正才能得到正确的结果。

### 半经典 Fermi 和 Bose 统计

在上面的近似中，理论上对于 $h^{-1}$ 作逐级微扰展开就可以得到半经典 Fermi 和 Bose 统计的修正项，但是这个过程很繁琐。更加简单的办法是使用粒子数可变的统计，也就是巨配分函数的半经典近似。本节就要讨论这种近似。

从第一章得出的 (\ref{bose}) 和 (\ref{fermi}) 两个式子中，我们得到巨配分函数的一般表达式：

$$
\Xi = \prod_i \left( 1 \pm e^{-\alpha -\beta E_i } \right)^{\pm 1}.
$$

正负分别代表 Fermi 和 Bose 统计（而不是反过来，就像通常做的那样）。对上式取对数，有：

$$
\ln \Xi = \pm \sum_i \ln\left( 1 \pm e^{-\alpha -\beta E_i } \right).
$$

现在我们知道，一个能级在相空间内占据的体积是 $\frac{dqdp}{h}$，因此我们可以将求和转化为积分：

$$
\ln \Xi = \pm \frac{1}{h^s} \int d^s q d^s p \ln\left( 1 \pm e^{-\alpha -\beta H} \right).
$$

### 从 Fermi 和 Bose 统计到 Boltzmann 统计

从一个准确的角度讲，没有任何粒子满足 Boltzmann 统计，因为任何粒子都是全同的，必须满足 Fermi 或者 Bose 统计。但是，在某些极限下，Fermi 和 Bose 统计可以近似为 Boltzmann 统计。本节讨论这样近似的合理性。
我们知道，根据 (\ref{bose}) 和 (\ref{fermi}) 两个式子，有每一个能级的占据数是：

$$
\bar n_i = \frac{1}{e^{+\alpha + \beta E_i} \pm 1}.
$$

可以看到，当 $\alpha + \beta E_i \gg 1$ 时，占据数 $\bar n_i$ 就会变得非常小，这时就可以近似地写成：

$$
\bar n_i \approx e^{-\alpha - \beta E_i}.
$$

这就是 Boltzmann 统计的占据数。让我们将这个结果与严格的 Boltzmann 统计的占据数进行比较。在 Boltzmann 统计中，单粒子能级 $E_i$ 的占据数是：

$$
\bar n_i = \frac{N}{Z_1} e^{-\beta E_i},
$$

让这两个式子相等，我们可以得到：

$$
\frac{Z_1}{N} = e^{\alpha}.
$$

然而，对于自由粒子，$Z_N$ 我们已经求出如前：

$$
Z_1 = \frac{V}{\lambda^{3}}.
$$

因此，在下述两种情况下，Fermi 和 Bose 统计可以近似为 Boltzmann 统计：

- 当 $V \to \infty$ 时，$Z_1 \to \infty$，因此 $\alpha \to \infty$，满足 $\alpha + \beta E_i \gg 1$ 的条件。注意，这个条件同样可以表述为所谓稀薄粒子假设（dilute gas hypothesis）.
- 当 $T \to \infty$ 时，$\lambda \to 0$，因此 $Z_1 \to \infty$，同样满足 $\alpha + \beta E_i \gg 1$ 的条件。
- 当 $N \to 0$ 时，$\alpha \to \infty$，同样满足 $\alpha + \beta E_i \gg 1$ 的条件。

注意到，这就是我们推导正则配分函数的半经典近似时所做的近似条件，因此我们可以说，在半经典近似下，Fermi 和 Bose 统计就近似为 Boltzmann 统计。这不得不让人惊叹天主的神奇化工。

让我们进而导出正则配分函数和巨配分函数的关系。首先，对于 Bose 子，我们有：

$$
\begin{aligned}
            \Xi &= \prod_i \left( 1 - e^{-\alpha -\beta E_i } \right)^{-1} \\
            &= \prod_i \sum_{n_i=0}^\infty e^{-n_i\alpha - n_i\beta E_i} \\
            &= \sum_{n_1=0}^\infty \sum_{n_2=0}^\infty \cdots e^{-\alpha(n_1+n_2+\cdots) -\beta(n_1E_1 + n_2E_2 + \cdots)} \\
            &= \sum_{N=0}^\infty e^{-\alpha N} \sum_{n_1+n_2+\cdots = N} e^{-\beta(n_1E_1 + n_2E_2 + \cdots)} \\
            &= \sum_{N=0}^\infty e^{-\alpha N} Z_N.
    \end{aligned}
$$

对于 Fermi 子，我们有：

$$
\begin{aligned}
            \Xi &= \prod_i \left( 1 + e^{-\alpha -\beta E_i } \right) \\
            &= \prod_i \sum_{n_i=0}^1 e^{-n_i\alpha - n_i\beta E_i} \\
            &= \sum_{n_1=0}^1 \sum_{n_2=0}^1 \cdots e^{-\alpha(n_1+n_2+\cdots) -\beta(n_1E_1 + n_2E_2 + \cdots)} \\
            &= \sum_{N=0}^\infty e^{-\alpha N} \sum_{n_1+n_2+\cdots = N} e^{-\beta(n_1E_1 + n_2E_2 + \cdots)} .
    \end{aligned}
$$

这里，最后一个式子中的求和 $\sum_{n_1+n_2+\cdots = N}$ 是在满足 $n_i=0$ 或 $1$ 的条件下进行的，因此当 $N$ 大于单粒子能级数时，这个求和就会变成零。总之，我们得到了正则配分函数和巨配分函数之间的关系：

$$
\boxed{\Xi = \sum_{N=0}^\infty e^{-\alpha N} Z_N}.
$$

## 示例：谐振子

### 单个谐振子

让我们计算一个具体的粒子来说明这一点。单个谐振子的哈密顿量是

$$
\hat{H} = \frac{\hat{p}^2}{2m} + \frac{1}{2} m \omega^2 \hat{q}^2.
$$

在半经典情况下，配分函数的计算很简单：

$$
Z = \frac{1}{h} \int_{-\infty}^\infty dq \int_{-\infty}^\infty dp e^{-\beta \left( \frac{p^2}{2m} + \frac{1}{2} m \omega^2 q^2 \right)} = \frac{1}{\beta \hbar \omega}.
$$

粒子处在 $dpdq$ 的概率是

$$
P(p,q) dp dq = \frac{1}{Z} e^{-\beta \left( \frac{p^2}{2m} + \frac{1}{2} m \omega^2 q^2 \right)} dp dq = \frac{\beta \omega}{2\pi} e^{-\beta \left( \frac{p^2}{2m} + \frac{1}{2} m \omega^2 q^2 \right)} dp dq.
$$

在经典的情况下，粒子在相空间中的分布是一个高斯分布，中心在 $p=0$ 和 $q=0$，宽度由温度 $T$ 和谐振子的频率 $\omega$ 决定。这个结果中不含有 $\hbar,$ 因而可以由经典统计力学得到。

让我们来看看量子统计具有什么样的结果。在量子力学中，通过解 Schrodinger 方程，我们可以得到单个谐振子的能级是

$$
E_n = \hbar \omega \left( n + \frac{1}{2} \right), \quad n=0,1,2,\cdots.
$$

每一个能级的简并度都是 $1$。于是在能量表象下对于密度矩阵取迹，我们可以得到单个谐振子的配分函数是

$$
Z = \sum_{n=0}^\infty e^{-\beta \hbar \omega \left( n + \frac{1}{2} \right)} = \frac{e^{-\beta \hbar \omega / 2}}{1 - e^{-\beta \hbar \omega}}.
$$

在量子统计中，我们无法同时知道粒子的位置和动量。因此，我们无法得到粒子在相空间中的分布情况。但是，我们可以得到粒子在位置空间中的分布情况。这种分布是通过如下的方式计算出来的。

考虑正则分布的密度矩阵在坐标表象下的表达式。按照式 (\ref{coord_basis}) 可以写出

$$
\bra{q} e^{-\beta \hat{H}} \ket{q} = \frac1Z\sum_{n=0}^\infty e^{-\beta E_n} |\psi_n(q)|^2,
$$

其中 $\psi_n(q)$ 是单个谐振子第 $n-$ 个能级的波函数。由量子力学熟知这些波函数的显式表达式是：

$$
\psi_n(q) = \left( \frac{m\omega}{\pi \hbar} \right)^{1/4} \frac{1}{\sqrt{2^n n!}} e^{-\frac{m\omega q^2}{2\hbar}} H_n\left( \sqrt{\frac{m\omega}{\hbar}} q \right) = \sqrt{\frac{\alpha}{2^n n!\pi}} e^{-\frac{\xi^2}{2}} H_n\left( \xi \right),
$$

其中 $H_n(x)$ 是第 $n-$ 个 Hermite 多项式，最后一个等号中使用了简化记号 $\alpha = m\omega/\hbar$ 和 $\xi = \sqrt{\alpha} q.$ 代入上式，我们可以得到单个谐振子在位置空间中的分布情况：

$$
P(q) dq = \bra{q} e^{-\beta \hat{H}} \ket{q} dq = (1-\exp(-\beta\hbar \omega))\frac{\alpha}{\sqrt{\pi}} \sum_{n=0}^\infty \exp\left( -n\beta\hbar\omega \right)\frac{1}{2^n n!} e^{-\xi^2} H_n^2\left( \xi \right) dq.
$$

考虑函数

$$
\begin{aligned}
f(\xi):&=\sum_{n=0}^\infty \exp\left( -n\beta\hbar\omega \right)\frac{1}{2^n n!} H_n^2\left( \xi \right)\\
        &=\sum_{n=0}^\infty \frac{1}{n!}\left(  \frac{\exp(-\beta\hbar\omega)}{2} \right)^n  H_n^2\left( \xi \right).\\
        f^\prime(\xi) &= 2\sum_{n=0}^{\infty} \frac{1}{n!}\left(  \frac{\exp(-\beta\hbar\omega)}{2} \right)^n H_n\left( \xi \right)H_n^\prime\left( \xi \right) \\
        &= 2\sum_{n=0}^{\infty}\frac{1}{n!} \left(  \frac{\exp(-\beta\hbar\omega)}{2} \right)^n H_n\left( \xi \right) \cdot 2n H_{n-1}\left( \xi \right) \\
        &= 4\sum_{n=1}^{\infty} \frac{1}{\left( n-1 \right)!}\left(  \frac{\exp(-\beta\hbar\omega)}{2} \right)^n \left( 2\xi H_{n-1}\left( \xi \right) - H_{n-1}^\prime\left( \xi \right)\right) \cdot  H_{n-1}\left( \xi \right) \\
        &= 8\xi\sum_{n=1}^{\infty} \frac{1}{\left( n-1 \right)!}\left(  \frac{\exp(-\beta\hbar\omega)}{2} \right)^n  H_{n-1}\left( \xi \right)H_{n-1}\left( \xi \right) \\&\quad\quad\qquad- 4\sum_{n=1}^{\infty} \frac{1}{\left( n-1 \right)!}\left(  \frac{\exp(-\beta\hbar\omega)}{2} \right)^n H_{n-1}\left( \xi \right)H_{n-1}^{\prime}\left( \xi \right) \\
        &= 4\exp(-\beta\hbar\omega) \xi f\left( \xi \right) - \exp(-\beta\hbar\omega) f^\prime\left( \xi \right)
\end{aligned}
$$

这样就有微分方程：

$$
\left(1 + \exp(-\beta\hbar\omega) \right)f^\prime(\xi) = 4\exp(-\beta\hbar\omega) \xi f\left( \xi \right).
$$

这个微分方程的解是：

$$
f\left( \xi \right) = f\left( 0 \right) \exp\left( \frac{2\xi^2}{1+\exp\left( \beta\hbar\omega \right)} \right)
$$

结合初值条件是：

$$
f\left( 0 \right) = \sum_{n=0}^\infty \frac1{n!}\left(\frac{\exp\left( -\beta\hbar\omega \right)}{2}\right)^n H_n^2(0).
$$

为了求解它，我们需要知道 $H_n(0)$ 的值。我们知道，$H_n(x)$ 是一个 $n-$ 次多项式，因此当 $n$ 是奇数时，$H_n(0) = 0$. 当 $n$ 是偶数时，$H_n(0) = (-1)^{n/2} \frac{n!}{(n/2)!}$. 代入上式，我们可以得到：

$$
f\left( 0 \right) = \sum_{n=0}^\infty \frac1{n!}\left(\frac{\exp\left( -\beta\hbar\omega \right)}{2}\right)^n \left( (-1)^n \frac{(2n)!}{n!} \right)^2 = \sum_{n=0}^\infty \frac{(2n)!}{(n!)^2}\left(\frac{\exp\left( -\beta\hbar\omega \right)}{2}\right)^n.
$$

这个无穷级数的求和结果是 

$$
f(0) = \frac{1}{\sqrt{1-\exp\left( -2\beta\hbar\omega \right)}}.
$$

代入上式，我们可以得到单个谐振子在位置空间中的分布情况：

$$
f(\xi) = \frac{1}{\sqrt{1-\exp\left( -2\beta\hbar\omega \right)}} \exp\left( \frac{2\xi^2}{1+\exp\left( \beta\hbar\omega \right)} \right)
$$

及

$$
P(q) dq = (1-\exp(-\beta\hbar \omega))\frac{\alpha}{\sqrt{\pi}} \frac{\exp\left( -\xi^2 \right)}{\sqrt{1-\exp\left( -2\beta\hbar\omega \right)}} \exp\left( \frac{2\xi^2}{1+\exp\left( \beta\hbar\omega \right)} \right) dq.
$$

整理得

$$
\boxed{
        P\left( q \right) dq = \sqrt{\frac{m\omega\tanh\left( \frac{\beta\hbar\omega}{2} \right)}{\pi\hbar}}\exp\left( -\tanh\left( \frac{\beta\hbar\omega}{2} \right) \frac{m\omega q^2}{\hbar} \right) dq.}
$$

在温度很高 ($\beta \ll 1$) 的情形下，这个分布退回到经典的 Boltzmann 分布，这一点容易验证。而在温度很低 ($\beta \gg 1$) 时，$\tanh \left( \beta\hbar\omega/2 \right)\to 1.$ 这时这个分布变成了基态的波函数模方：

$$
P(q) dq = \sqrt{\frac{m\omega}{\pi\hbar}} \exp\left( -\frac{m\omega q^2}{\hbar} \right) dq.
$$

在单个谐振子的的情形下，我们看到，整个密度矩阵的表达式都是可以求出的，（Landau \& Lifschitz, \S 30）求得的方法如下：首先写出单个谐振子在位置表象下的密度矩阵的表达式：

$$
\rho\left( q,q' \right) = \frac{1}{Z}\sum_{0}^{\infty} \exp\left(-\beta \left( n+\frac{1}{2} \right) \hbar \omega \right) \psi_n^*(q')\psi_n(q).
$$

将波函数的显式代入得到：

$$
\rho\left( q,q^{\prime} \right)=(1-\exp(-\beta\hbar \omega))\frac{\alpha}{\sqrt{\pi}} \sum_{n=0}^\infty \exp\left( -n\beta\hbar\omega \right)\frac{1}{2^n n!} e^{-\frac{\xi^2+\eta^2}{2}} H_n\left( \eta \right) H_n\left( \xi \right).
$$

其中 $\eta = \sqrt{\alpha} q'$. 现在定义新变量：

$$
\begin{aligned}
            x &= \frac{\xi + \eta}{2} \\
            y &= \frac{\xi - \eta}{2}
        \end{aligned}
$$
将密度矩阵的表达式用 $x,y$ 改写得到：

$$
\rho\left( q,q^{\prime} \right) = (1-\exp(-\beta\hbar \omega))\frac{\alpha}{\sqrt{\pi}} e^{-x^2-y^2} \sum_{n=0}^\infty \exp\left( -n\beta\hbar\omega \right)\frac{1}{2^n n!} H_n\left( x-y \right) H_n\left( x+y \right).
$$

现在考虑二元函数：

$$
f(x,y) = \sum_{n=0}^\infty \exp\left( -n\beta\hbar\omega \right)\frac{1}{2^n n!} H_n\left( x-y \right) H_n\left( x+y \right).
$$

可以导出对于 $y$ 的偏微分方程：

$$
\begin{aligned}
\partial_y f(x,y)&=\sum_{n=0}^{\infty} \exp(-n\beta \hbar\omega)\frac{1}{2^n n!} \left[ \left( -H_n^\prime (x-y) \right) H_n(x+y) + H_n(x-y)H_n^\prime(x+y) \right] \\
        &=\sum_{n=0}^{\infty} \exp(-n\beta \hbar\omega)\frac{1}{2^n \left( n-1 \right)!} [ \left( 2\left( x+y \right) H_{n-1}\left( x+y \right) - H_{n-1}^{\prime}\left( x+y \right) \right) H_{n-1}\left( x-y \right) \\  &\quad\quad\quad  -\left( 2\left( x-y \right) H_{n-1}\left( x-y \right) - H_{n-1}^{\prime}\left( x-y \right) \right) H_{n-1}(x+y)]\\
        &=\sum_{n=0}^{\infty} \exp(-n\beta \hbar\omega)\frac{1}{2^n \left( n-1 \right)!} [ 4y H_{n-1}\left( x+y \right) H_{n-1}\left( x-y \right) \\  &\quad\quad\quad - 2(H_{n-1}\left( x+y \right) H_{n-1}^{\prime}\left( x-y \right)  - H_{n-1}^{\prime}\left( x+y \right) H_{n-1}\left( x-y \right)) ] \\
        &=
\end{aligned}
$$

### 大量全同谐振子

考虑 $N$ 个全同的一维谐振子。现在根据粒子的统计性质，应当分成 Fermi 子和 Bose 子分别考虑。
