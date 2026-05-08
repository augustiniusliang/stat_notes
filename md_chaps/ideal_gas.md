# 量子理想气体

现在我们已经准备好了一切必要的工具来分析理想气体的统计性质。理想气体指的是：粒子间没有相互作用的气体。在全同性的假设下，粒子自然地分为 Bose 统计与 Fermi 统计两类。我们将分别分析这两类气体的性质。一般来说，低温下和高温下量子理想气体的性质很不一样，这是因为低温下，粒子的 de Broglie 波长会变得很大，粒子之间的量子统计效应会变得很显著；或者说粒子的简并度会变得很高；但其中一种粒子是玻色子，而另一种是费米子，所以在低温下它们的表现很不一样。而在高温下，两种粒子的表现趋同，便成为近经典理想气体。前一种情况称为简并气体，后一种情况称为非简并气体。我们先研究简并气体，它与我们熟悉的理想气体最为相似。

## 非简并量子气体的热力学量

我们看到，对于两种气体来说，巨配分函数的对数可以统一的写成如下形式：
$$
\ln \varXi = g \frac{1}{h^3}\int d^3p d^3 q D(p,q)\ln \left( 1 +g e^{-\beta(\varepsilon(p) - \mu)} \right).
$$
其中 $g\in\left\{ 1,-1 \right\}, g=1$ 对应 Fermi 气体，$g=-1$ 对应 Bose 气体。在 \ref{fermi_bose_boltzmann} 节中我们已经分析过，Bose 与 Fermi 统计在稀薄、高温的极限下会趋近于 Boltzmann 统计，现在根据量子力学我们知道，这实际上就是粒子非简并的条件。

现在写出态密度，我们可以先不计及简并度：
$$
D(p,q) = \frac{1}{h^3}.
$$
对于经典气体，我们有色散关系 $\varepsilon = \frac{p^2}{2m}.$ 变到能量表象，这就是：
$$
D(\varepsilon) = \frac{V}{h^3} 4\pi (2m)^{\frac32} \varepsilon^{\frac12}.
$$
这样，巨配分函数的对数就是：
$$
\ln \varXi = g \frac{V}{h^3} 4\pi (2m)^{\frac32} \int_{0}^{\infty} \varepsilon^{\frac{1}{2}} \ln \left( 1 +g e^{-\beta(\varepsilon - \mu)} \right) d\varepsilon.
$$
现在对这个式子作分部积分，得到：
$$
\ln \varXi = \frac{2}{3k_BT}\frac{V}{h^3} 4\pi (2m)^{\frac32} \int_{0}^{\infty} \frac{\varepsilon^{\frac{3}{2}}\exp(-\beta(\varepsilon - \mu))}{1 + g\exp(-\beta(\varepsilon - \mu))} d\varepsilon.
$$
其中已经用到 $g^2=1.$ 因此巨热力学势为
$$
\Omega = -k_B T \ln \varXi = - \frac{2}{3}\frac{V}{h^3} 4\pi (2m)^{\frac32} \int_{0}^{\infty} \frac{\varepsilon^{\frac{3}{2}}\exp(-\beta(\varepsilon - \mu))}{1 + g\exp(-\beta(\varepsilon - \mu))} d\varepsilon.
$$
按照第一章中所述的方式，我们便可以获得其他所有的热力学量：
粒子数：
$$
N = -\left( \frac{\partial \Omega}{\partial \mu} \right)_{V,T} = \frac{V}{h^3} 4\pi (2m)^{\frac32} \int_{0}^{\infty} \frac{\varepsilon^{\frac{1}{2}}}{e^{\beta(\varepsilon - \mu)} + g} d\varepsilon.
$$
内能：
$$
U = \Omega + TS + \mu N = \frac{V}{h^3} 4\pi (2m)^{\frac32} \int_{0}^{\infty} \frac{\varepsilon^{\frac{3}{2}}}{e^{\beta(\varepsilon - \mu)} + g} d\varepsilon.
$$
压强：
$$
p = -\left( \frac{\partial \Omega}{\partial V} \right)_{\mu,T} = \frac{2}{3}\frac{1}{h^3} 4\pi (2m)^{\frac32} \int_{0}^{\infty} \frac{\varepsilon^{\frac{3}{2}}}{e^{\beta(\varepsilon - \mu)} + g} d\varepsilon.
$$
### 广义 Zeta 函数

可以看到，以上的积分都具有如下的形式：
$$
I_g(s,\mu)=\int_{0}^{\infty} \frac{\varepsilon^{s-1}}{e^{\beta(\varepsilon - \mu)} + g} d\varepsilon.
$$
我们可以通过级数展开计算这个积分：
$$
I_g(s,\mu) = \int_{0}^{\infty} \frac{\varepsilon^{s-1}}{e^{\beta(\varepsilon - \mu)} + g} d\varepsilon = \frac{\Gamma(s)}{\beta^s} \sum_{n=1}^{\infty} \frac{(-g)^{n-1} e^{n\beta\mu}}{n^s}.
$$
定义如下的广义 Zeta 函数：
$$
\zeta_g(s,z) = \sum_{n=1}^{\infty} \frac{(-g)^{n-1} z^n}{n^s}.
$$
则我们可以将 $I_g(s,\mu)$ 写成如下的形式：
$$
I_g(s,\mu) = \frac{\Gamma(s)}{\beta^s} \zeta_g(s,e^{\beta\mu}).
$$
所以我们便可以将热力学量写成用广义 Zeta 函数写成的形式：
$$
\Omega = - \frac{2}{3}\frac{V}{h^3} 4\pi (2m)^{\frac32} \Gamma\left( \frac{5}{2} \right) \zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right) = - k_BT \frac{V}{\lambda^3}\zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right).
$$
$$
N = \frac{V}{h^3} 4\pi (2m)^{\frac32} \Gamma\left( \frac{3}{2} \right) \zeta_g\left( \frac{3}{2}, e^{\beta\mu} \right) = \frac{V}{\lambda^3} \zeta_g\left( \frac{3}{2}, e^{\beta\mu} \right).
$$
$$
U = \frac{V}{h^3} 4\pi (2m)^{\frac32} \Gamma\left( \frac{5}{2} \right) \zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right) = \frac{3}{2} k_BT \frac{V}{\lambda^3} \zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right).
$$
$$
p = \frac{2}{3} \frac{1}{h^3} 4\pi (2m)^{\frac32} \Gamma\left( \frac{5}{2} \right) \zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right) = k_BT \frac{1}{\lambda^3}\zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right).
$$
其中 $\lambda = \sqrt{\frac{2\pi\hbar^2}{mk_BT}}$ 是热波长。

### 高温展开

在高温下，粒子非简并，因此 $e^{\beta\mu} \ll 1.$（见3.1.3节） 这时我们可以将广义 Zeta 函数展开成 $e^{\beta\mu}$ 的幂级数：
$$
\zeta_g(s,e^{\beta\mu}) = e^{\beta\mu} - g \frac{e^{2\beta\mu}}{2^s} + g^2 \frac{e^{3\beta\mu}}{3^s} + \cdots
$$
我们先计算化学势的高温展开。根据粒子数的表达式，我们有
$$
N = \frac{V}{\lambda^3} \zeta_g\left( \frac{3}{2}, e^{\beta\mu} \right) = \frac{V}{\lambda^3} \left( e^{\beta\mu} - g \frac{e^{2\beta\mu}}{2^{3/2}} + g^2 \frac{e^{3\beta\mu}}{3^{3/2}} + \cdots \right).
$$
保留到含 $g$ 的最低阶，我们有：
$$
N = \frac{V}{\lambda^3} e^{\beta\mu} \left( 1 - g \frac{e^{\beta\mu}}{2^{3/2}} \right).
$$
零阶的解是： $\mu_0 = \frac{1}{\beta} \ln \left( \frac{N}{V} \lambda^3 \right).$ 现在，因为 $\exp(\beta\mu) \ll 1,$ 修正项带来的影响很小。因此我们可以设
$$
\mu = \mu_0 + \delta \mu, \quad \frac{\delta \mu}{\mu_0} = \mathcal{O}\left( \frac{N}{V} \lambda^3 \right).
$$
这样便可以作展开：
$$
e^{\beta\mu} = e^{\beta\mu_0} \left( 1 + \beta \delta \mu + \cdots \right).
$$
代入粒子数的表达式，得到：
$$
N = \frac{V}{\lambda^3} e^{\beta\mu_0} \left( 1 + \beta \delta \mu - g \frac{e^{\beta\mu_0}}{2^{3/2}} + \cdots \right).
$$
解出 $\delta \mu$ 的表达式：
$$
\delta \mu = g \frac{1}{2^{3/2}} \frac{N}{V} \lambda^3 k_B T.
$$
因此化学势的高温展开为
$$
\mu = k_B T \ln \left( \frac{N}{V} \lambda^3 \right) + g \frac{1}{2^{3/2}} \frac{N}{V} \lambda^3 k_B T + \cdots.
$$
让我们再计算一下内能的高温展开。根据内能的表达式，我们有
$$
U = \frac{3}{2} k_B T \frac{V}{\lambda^3} \zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right) = \frac{3}{2} k_B T \frac{V}{\lambda^3} \left( e^{\beta\mu} - g \frac{e^{2\beta\mu}}{2^{5/2}} + g^2 \frac{e^{3\beta\mu}}{3^{5/2}} + \cdots \right).
$$
这里，我们不仅要计及 $\mu$ 的高温修正项，还要计及 $\zeta_g$ 的高温修正项。保留到含 $g$ 的最低阶，我们有：
$$
U = \frac{3}{2} k_B T \frac{V}{\lambda^3} e^{\beta\mu} \left( 1 - g \frac{e^{\beta\mu}}{2^{5/2}} \right).
$$
现在代入 $\mu$ 的高温展开，得到：
$$
U = \frac{3}{2} k_B T \frac{V}{\lambda^3} e^{\beta\mu_0} \left( 1 + \beta \delta \mu - g \frac{e^{\beta\mu_0}}{2^{5/2}} + \cdots \right).
$$
解出 $U$ 的高温展开：
$$
U = \frac{3}{2} N k_B T \left( 1 + g \frac{1}{2^{5/2}} \frac{N}{V} \lambda^3 + \cdots \right).
$$
类似地，也可以求出压强 $p$ 的高温展开：
$$
p = k_B T \frac{1}{\lambda^3} \zeta_g\left( \frac{5}{2}, e^{\beta\mu} \right) = k_B T \frac{1}{\lambda^3} \left( e^{\beta\mu} - g \frac{e^{2\beta\mu}}{2^{5/2}} + g^2 \frac{e^{3\beta\mu}}{3^{5/2}} + \cdots \right).
$$
保留到含 $g$ 的最低阶，我们有：
$$
p = k_B T \frac{1}{\lambda^3} e^{\beta\mu} \left( 1 - g \frac{e^{\beta\mu}}{2^{5/2}} \right).
$$
代入 $\mu$ 的高温展开，得到：
$$
p = \frac{N k_B T}{V} \left( 1 + g \frac{1}{2^{5/2}} \frac{N}{V} \lambda^3 + \cdots \right).
$$
我们可以看到，Fermi 气体的压强比理想气体的压强要大，这说明 Fermi 子之间存在有效排斥；而对于 Bose 子来说，这种效果则是有效吸引。这种效应是由于粒子全同造成的交换效应，所以也被称为交换力。

## 简并理想 Fermi 气体

我们已经分析了非简并量子气体的热力学量，现在我们来分析一下简并量子气体的热力学量。简并极限就是 $N\to \infty, T\to 0.$ 这时，Fermi 气体与 Bose 气体的表现完全不同。我们可以先分析 Fermi 气体。

Fermi 气体的能级简并度需要计及自旋简并度。对于三维空间中的 Fermi 气体来说，这个态密度是
$$
D(p,q) = 2s+1,
$$
因此
$$
\ln \varXi = \frac{2s+1}{h^3}\int d^3p d^3 q \ln \left( 1 + e^{-\beta(\varepsilon(p) - \mu)} \right).
$$
于是各能级上占据的粒子数为
$$
\langle n(p) \rangle = \frac{2s+1}{e^{\beta(\varepsilon(p) - \mu)} + 1}.
$$
其他物理量可以由前面所述的方式得出。

### 零温度下的理想经典 Fermi 气体

在零温度下， Fermi 气体的分布函数退化为一个阶梯函数：
$$
\langle n(p) \rangle = \begin{cases}
2s+1, & \varepsilon(p) < \mu\\
0, & \varepsilon(p) > \mu
\end{cases}.
$$
因此在零温度下，所有能量小于化学势 $\mu$ 的态都被占据，而所有能量大于化学势 $\mu$ 的态都没有被占据.
粒子数与化学势的关系这时候是：
$$
N = \frac{2s+1}{h^3}\int_{\varepsilon(p) < \mu} d^3p d^3 q.
$$
当我们采用经典色散关系
$$
\varepsilon(p) = \frac{p^2}{2m},
$$
我们可以得到化学势 $\mu$ 与粒子数 $N$ 的关系：
$$
N = \frac{2s+1}{h^3}\int_{\varepsilon(p) < \mu} d^3p d^3 q = \frac{2s+1}{h^3}\int_{p^2 < 2m\mu} d^3p d^3 q = \frac{4\pi(2s+1)}{3h^3} (2m\mu)^{\frac{3}{2}}V.
$$
因此粒子数密度 $n:= \frac{N}{V}$ 便和化学势 $\mu$ 的关系为
$$
\mu = \frac{1}{2m}\left( \frac{6\pi^2 n}{2s+1} \right)^{\frac{2}{3}}.
$$
这个化学势 $\mu$ 也被称为 **Fermi 能量** $\varepsilon_F.$ 量 $(\frac{6\pi^2 n}{2s+1})^{\frac13}$ 具有波矢量纲，因此记作 $k_F,$ 被称为 Fermi 波矢。我们可以看到， Fermi 能量与 Fermi 波矢的关系为
$$
\varepsilon_F = \frac{\hbar^2k_F^2}{2m}.
$$
这时， Fermi 气体的内能是
$$
U = V\int_{0}^{p_F}\frac{p^2}{2m} 4\pi p^2 dp  = \frac{3}{5}N\varepsilon_F.
$$
压强是：
$$
p = -\left( \frac{\partial U}{\partial V} \right)_{N} = \frac{2}{5}\frac{N}{V}\varepsilon_F.
$$
因此对于零温度下的理想 Fermi 气体，我们有
$$
U = \frac32 pV.
$$
### 低温下 Fermi 气体的 Sommerfeld 展开

在 $T$ 很低时，Fermi 分布与阶梯函数产生了偏离，但若 $T$ 足够低，理想上我们便可以将这个偏离展成 $T$ 的级数。这种技术的系统展开方法首先是由 Sommerfeld 提出的，因此被称为 Sommerfeld 展开。

核心问题是计算如下的积分：
$$
I(T) = \int_{0}^{\infty} \frac{f(\varepsilon) (2s+1)}{e^{\beta(\varepsilon - \varepsilon_F)} + 1} d\varepsilon.
$$
其中 $f(\varepsilon)$ 是一个在 $\varepsilon = \varepsilon_F$ 处光滑的函数。
现在，将 $f(\varepsilon)$ 在 $\varepsilon<0$ 处定义为 $0,$ 这样我们就可以将积分的下限改为 $-\infty$：
$$
I(T) = \int_{-\infty}^{\infty} \frac{f(\varepsilon) (2s+1)}{e^{\beta(\varepsilon - \mu)} + 1} d\varepsilon.
$$
定义函数$\tilde{\Theta}(x)$ 如下：
$$
\tilde{\Theta}(z-z_F) = \begin{cases}
1, & x<0\\
\frac12, & x = 0\\
0, & x>0
\end{cases}.
$$
我们看到，有
$$
\int_{0}^{\mu} f(\varepsilon)  d\varepsilon = \int_{-\infty}^{\infty} f(\varepsilon) \tilde{\Theta}(\beta(\varepsilon-\mu)) d\varepsilon.
$$
则我们可以将积分分离为零温极限与温度修正项：
$$
I(T) = \int_{0}^{\mu} f(\varepsilon) (2s+1) d\varepsilon + (2s+1)\int_{-\infty}^{\infty} f(\varepsilon) g(\varepsilon) d\varepsilon,
$$
其中
$$
g(\varepsilon) = \frac{1}{e^{\beta(\varepsilon - \mu)} + 1} - \tilde{\Theta}(\varepsilon-\mu).
$$
我们在能量空间对二者作 Laplace 变换：
$$
\tilde{f}(p) = \int_{0}^{\infty} e^{-p\varepsilon} f(\varepsilon) d\varepsilon, \quad \tilde{g}(p) = \int_{-\infty}^{\infty} g(\varepsilon) e^{p\varepsilon} d\varepsilon.
$$
利用复平面上的解析性质，温度修正项的积分可以化为：
$$
\int_{-\infty}^{\infty} f(\varepsilon) g(\varepsilon) d\varepsilon = \frac{1}{2\pi i} \int_{-i\infty}^{i\infty} \tilde{f}(p) \tilde{g}(p) dp.
$$
下面我们求出 $\tilde{g}(p)$ 的表达式：
$$
\begin{aligned}
\tilde{g}(p) &= \int_{-\infty}^{\infty} g(\varepsilon) e^{p\varepsilon} d\varepsilon\\
&= \int_{-\infty}^{\infty} \left( \frac{1}{e^{\beta(\varepsilon - \mu)} + 1} - \tilde{\Theta}(\varepsilon-\mu) \right) e^{p\varepsilon} d\varepsilon\\
&= e^{p\mu}\int_{-\infty}^{\infty} \left( \frac{1}{e^{\beta(\varepsilon - \mu)} + 1} - \tilde{\Theta}(\beta(\varepsilon-\mu)) \right) e^{px} dx\\
&= e^{p\mu}\int_{-\infty}^{\infty} \frac{e^{p\varepsilon}}{e^{\beta(\varepsilon - \mu)} + 1} dx - \frac1p e^{p\mu}.
\end{aligned}
$$
我们可以通过留数定理求出 $\int_{-\infty}^{\infty} \frac{e^{p\varepsilon}}{e^{\beta(\varepsilon - \mu)} + 1} d\varepsilon$ 的值，现在直接给出结果：
$$
\int_{-\infty}^{\infty} \frac{e^{p\varepsilon}}{e^{\beta(\varepsilon - \mu)} + 1} d\varepsilon = \frac{\pi}{\beta\sin \left( \frac{\pi p}{\beta} \right)}.
$$
将 $\beta = \frac{1}{k_BT}$ 代入得到：
$$
\tilde{g}(p) = {e^{p\mu}} \left( \frac{\pi  k_B T}{\sin(\pi p k_B T)} - \frac1p \right).
$$
这是一个复平面上解析的函数。把括号内的函数记作 $G(p)$ 在 $p=0$ 处展开成 Taylor 级数：
$$
G(p) = \frac{\pi^2}{6}(k_B T)^2 p + \frac{7\pi^4}{360}(k_B T)^4 p^3 + \frac{31\pi^6}{15120}(k_B T)^6 p^5 + \dots = \sum_{k=1}^{\infty} c_{2k} (k_B T)^{2k} p^{2k-1}.
$$
将此级数代回复积分中，并交换积分与求和顺序：
$$
\begin{aligned}
\frac{1}{2\pi i} \int_{-i\infty}^{i\infty} \tilde{f}(p) e^{p\mu} \left[ \sum_{k=1}^{\infty} c_{2k} (k_B T)^{2k} p^{2k-1} \right] dp &= \sum_{k=1}^{\infty} c_{2k} (k_B T)^{2k} \left[ \frac{1}{2\pi i} \int_{-i\infty}^{i\infty} p^{2k-1} \tilde{f}(p) e^{p\mu} dp \right].
\end{aligned}
$$
根据 Laplace 逆变换的导数定理，对于平滑函数 $f(\varepsilon)$，其 Laplace 变换 $\tilde{f}(p)$ 乘以 $p^n$ 的逆变换，恰好对应于对 $\varepsilon$ 求 $n$ 阶导数。因此方括号内的复积分严格等于：
$$
\frac{1}{2\pi i} \int_{-i\infty}^{i\infty} \left[ p^{2k-1} \tilde{f}(p) \right] e^{p\mu} dp = \left. \frac{d^{2k-1}}{d\varepsilon^{2k-1}} f(\varepsilon) \right|_{\varepsilon = \mu} = f^{(2k-1)}(\mu).
$$
由于化学势 $\mu > 0$，函数 $f(\varepsilon)$ 在积分下限 $\varepsilon = 0$ 处的截断（即使得 $f(\varepsilon<0)=0$ 引入的阶跃函数及其求导产生的 $\delta(\varepsilon)$ 等奇点）并不会对 $\varepsilon = \mu$ 处的导数值产生任何影响。
因此我们得到了 Sommerfeld 展开的最终结果：
$$
\boxed{ \int_{0}^{\infty} \frac{f(\varepsilon)}{e^{\beta(\varepsilon - \mu)} + 1} d\varepsilon = \int_{0}^{\mu} f(\varepsilon) d\varepsilon + \sum_{k=1}^{\infty} \left.\frac{d^{2k}}{dp^{2k}}\left(\frac{p\pi}{\sin\left( p\pi \right)} - 1\right)\right|_{p=0} \frac{(k_B T)^{2k}}{(2k)!} f^{(2k-1)}(\mu) }
$$
代入前几项系数，可以直接写出：
$$
\int_{0}^{\infty} \frac{f(\varepsilon)}{e^{\beta(\varepsilon - \mu)} + 1} d\varepsilon = \int_{0}^{\mu} f(\varepsilon) d\varepsilon + \frac{\pi^2}{6}(k_B T)^2 f'(\mu) + \frac{7\pi^4}{360}(k_B T)^4 f^{(3)}(\mu) + \mathcal{O}(T^6).
$$
### 三维低温理想 Fermi 气体

现在我们使用 Sommerfeld 展开来计算三维情况下的低温理想 Fermi 气体相对于零温 Fermi 气体的微扰。对于三维理想 Fermi 气体来说，能量与动量的关系为 $\varepsilon = \frac{p^2}{2m},$ 因此态密度为
$$
D(\varepsilon) = V\frac{(2s+1)}{h^3} 4\pi p^2 \frac{dp}{d\varepsilon} = V\frac{(2s+1)}{h^3} 4\pi (2m)^{\frac32} \varepsilon^{\frac12}=\frac23N\frac{\varepsilon^{\frac12}}{\varepsilon_F^{\frac32}}.
$$
这样，在有限温度下粒子数与化学势的关系为
$$
N = \int_{0}^{\infty} \frac{D(\varepsilon)}{e^{\beta(\varepsilon - \mu)} + 1} d\varepsilon.
$$
用 Sommerfeld 展开，精确到 $T^2$ 的项，我们有
$$
N = N\left( \frac{\mu}{\mu_F} \right)^{\frac32} + \frac{\pi^2}{6}(k_B T)^2 D'(\mu) + \mathcal{O}(T^4) \doteq N\left( \frac{\mu}{\mu_F} \right)^{\frac32} + \frac{\pi^2}{6}(k_B T)^2 D'(\mu).
$$
设 $\mu = \varepsilon_F + \delta\mu,$ 其中 $\delta\mu$ 是一个小量，我们可以将上式中的 $\left( \frac{\mu}{\mu_F} \right)^{\frac32}$ 展开成 $\delta\mu$ 的级数：
$$
\left( \frac{\mu}{\mu_F} \right)^{\frac32} = 1 + \frac{3}{2}\frac{\delta\mu}{\varepsilon_F} + \mathcal{O}(\delta\mu^2).
$$
代入得到：
$$
N = N + \frac{3}{2}N\frac{\delta\mu}{\varepsilon_F} + \frac{\pi^2}{6}(k_B T)^2 D'(\varepsilon_F) + \mathcal{O}(\delta\mu^2, T^4).
$$
解出
$$
\delta\mu = -\frac{\pi^2}{6}(k_B T)^2 \frac{D'(\varepsilon_F)}{N} \varepsilon_F = -\frac{\pi^2}{12}(k_B T)^2 \frac{1}{\varepsilon_F}.
$$
因此得到化学势的领头阶修正：
$$
\mu = \varepsilon_F - \frac{\pi^2}{12} \frac{(k_B T)^2}{\varepsilon_F} + \mathcal{O}(T^4).
$$
同样地，内能的表达式为
$$
U = \int_{0}^{\infty} \frac{\varepsilon D(\varepsilon)}{e^{\beta(\varepsilon - \mu)} + 1} d\varepsilon.
$$
用 Sommerfeld 展开，精确到 $T^2$ 的项，我们有
$$
U = \int_{0}^{\mu} \varepsilon D(\varepsilon) d\varepsilon + \frac{\pi^2}{6}(k_B T)^2 \left. \frac{d}{d\varepsilon} \left( \varepsilon D(\varepsilon) \right) \right|_{\varepsilon = \mu} + \mathcal{O}(T^4).
$$
代入化学势的修正，得到内能的表达式为
$$
U = \frac{3}{5}N\varepsilon_F + \frac{\pi^2}{4} N \frac{(k_B T)^2}{\varepsilon_F} + \mathcal{O}(T^4).
$$
这说明在低温下，Fermi 气体的热容是
$$
C_V = \left( \frac{\partial U}{\partial T} \right)_V = \frac{\pi^2}{2} N k_B \frac{k_B T}{\varepsilon_F} + \mathcal{O}(T^3).
$$
因此在低温下， Fermi 气体的热容与温度成正比，而不是像经典气体那样与温度无关。这和热力学第三定律是完全一致的，因为当 $T\to 0$ 时，热容 $C_V \to 0.$

下面研究压强的表达式：
$$
p = -\left( \frac{\partial U}{\partial V} \right)_{N} = \frac{2}{5}\frac{N}{V}\varepsilon_F + \frac{\pi^2}{6} N k_B^2 \frac{T^2}{\varepsilon_F V} + \mathcal{O}(T^4).
$$
求导时要注意，$\varepsilon_F$ 是与 $V$ 相关的。因此在低温下， Fermi 气体的压强也会有一个 $T^2$ 的修正项。

## 理想 Bose 气体

理想 Bose 气体的巨配分函数的对数可以写成：
$$
\ln \varXi = -\frac{1}{h^3}\int d^3p d^3 q D(p,q)\ln \left( 1 - e^{-\beta(\varepsilon(p) - \mu)} \right).
$$
对于 Bose 气体来说，能级简并度也是 $D(p,q) = 2s+1,$ 但这里 $s$ 是整数。
