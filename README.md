VBinDiff - Visual Binary Diff
=============================

[Visual Binary Diff (VBinDiff)](https://www.cjmweb.net/vbindiff/) displays files in hexadecimal and ASCII (or EBCDIC).  It can also display two files at once, and highlight the differences between them.  Unlike diff, it works well with large files (up to 64 GB).

VBinDiff was inspired by the Compare Files function of the [ProSel utilities by Glen Bredon](http://www.apple2.org.za/gswv/USA2WUG/Glen.Bredon.In.Memoriam/A2.Software/), for the [Apple II](https://en.wikipedia.org/wiki/Apple_II).  When I couldn't find a similar utility for the PC, I wrote it myself.

The single-file mode was inspired by the LIST utility of [4DOS and friends](http://jpsoft.com/take-command-windows-scripting.html).  While [less](http://www.greenwoodsoftware.com/less/) provides a good line-oriented display, it has no equivalent to LIST's hex display.  (True, you can pipe the file through [hexdump](http://linux.die.net/man/1/hexdump), but that's incredibly inefficient on multi-gigabyte files.)


## This fork

This is a fork of [madsen/vbindiff](https://github.com/madsen/vbindiff), which
has had no upstream commits since 2017. It carries the fixes needed to build
and run on current openSUSE, plus the nine patches Debian has shipped since
2022 ([upstream PR #21](https://github.com/madsen/vbindiff/pull/21)): backward
search, file positions up to 64 GB, page scrolling on Space and Backspace, and
16/24/32-byte display lines. The openSUSE and Debian builds are therefore at
feature parity, and Debian's patches are commits in this fork rather than a
patch stack in the package.

![build](https://github.com/troed/vbindiff/actions/workflows/build.yml/badge.svg?branch=opensuse)

openSUSE packages are built from this fork at
<https://build.opensuse.org/project/show/home:troed:vbindiff>. Pick the
repository that matches your release:

| Release    | Repository |
| ---------- | ---------- |
| Tumbleweed | `https://download.opensuse.org/repositories/home:/troed:/vbindiff/openSUSE_Tumbleweed/` |
| Leap 16.1  | `https://download.opensuse.org/repositories/home:/troed:/vbindiff/16.1/` |
| Leap 16.0  | `https://download.opensuse.org/repositories/home:/troed:/vbindiff/16.0/` |

    zypper ar -f <repository> vbindiff
    zypper in vbindiff

When upgrading from Leap 16.0 to 16.1, point the repository at the `16.1` path
(or remove and re-add it): `zypper` does not rewrite home-project repository
URLs during a distribution upgrade.

The number of bytes per displayed line is fixed at compile time: define
`WIDTH24` or `WIDTH32` (for example in `AM_CXXFLAGS`) to show 3 or 4 groups of
8 bytes instead of the default 2.


Working with This Repository
----------------------------

This repository uses a submodule to pull in my [Free GetOpt](https://github.com/madsen/free-getopt) package, which makes it a bit trickier to get started with than the average Git repository.  Here's how to get started.

1. Clone this repository and `cd` into it.
2. Run `git submodule update --init`
3. If you're working on a Unix system, run `autoreconf -i`

Now you're ready to use the normal `./configure && make` process on Unix, or open `win32/vbindiff.dsw` on Windows.

To build the documentation, you'll also need [Perl](https://www.perl.org/), [Date::Format](https://metacpan.org/module/Date::Format), and [Template-Toolkit](https://metacpan.org/release/Template-Toolkit).  For Windows, I recommend [Strawberry Perl](http://strawberryperl.com/), which comes with the necessary modules.  On Unix, your distro may have packages, or you can install from [CPAN](https://metacpan.org/).  Package names for some distros are:

* [Arch Linux](https://www.archlinux.org/): `perl perl-template-toolkit perl-timedate`
* [Gentoo Linux](https://www.gentoo.org/): `dev-lang/perl dev-perl/Template-Toolkit dev-perl/TimeDate`
* [Ubuntu](https://www.ubuntu.com/): `perl libtemplate-perl libtimedate-perl`

If you're developing on Unix, I suggest you also `cp -a tools/post-commit .git/hooks/`.  That hook will touch `configure.ac` after each commit that modifies it, causing `configure` to be regenerated and making `AC_REVISION` reflect the new commit.


Copyright and License
---------------------

Visual Binary Diff is copyright 1995-2013 by Christopher J. Madsen

This program is free software; you can redistribute it and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl.html) as published by the Free Software Foundation; either [version 2 of the License](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html), or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
