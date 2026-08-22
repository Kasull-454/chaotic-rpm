<div align="center">
  <h1 align="center">Chaotic-RPM</h2>
  <p align="center">COPR repository compiled for x86_64-v3.<br>Goodies from CachyOS ported to Fedora 44, 43 and Rawhide, highly optimized for modern CPUs.</p>
</div>

The **x86-64-v3** counterpart to my other COPR, [Chaotic-Blackbird](https://github.com/Kasull-454/chaotic-blackbird), extended with packages for this microarchitecture to ensure high performance across a wide range of hardware, while fully respecting the [CachyOS](https://cachyos.org/) philosophy brought over to Fedora.

> **WARNING:** The packages in this repository are compiled with the **x86-64-v3** microarchitecture flag and will **NOT work** on older CPUs that lack support for it (triggering an "illegal instruction" error or a kernel panic on boot).
> Requires support for v3 line instructions: **AVX, AVX2, FMA, BMI1, BMI2, MOVBE, and LZCNT** (roughly Intel 4th Gen *Haswell* / AMD *Zen 1* CPUs and newer). If you are using older hardware (v1 or v2), please use the standard repositories.

If your CPU supports the AVX-512 instruction set, you can use the v4 version, [Chaotic-Blackbird](https://github.com/Kasull-454/chaotic-blackbird).

The repository's name is inspired by **Chaotic-AUR** for Arch Linux, and it was created simply because, since I already have the `.spec` files flagged for x86-64-v4, it costs me nothing to build the v3 versions as well — at least until Fedora provides official v3 repositories.
