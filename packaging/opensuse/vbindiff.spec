#
# spec file for package vbindiff
#
# Built from the troed/vbindiff fork, which carries fixes for current
# openSUSE (upstream has had no commits since 2017).
#

Name:           vbindiff
Version:        3.0~beta5
Release:        0
Summary:        Visual binary diff
License:        GPL-2.0-or-later
URL:            https://www.cjmweb.net/vbindiff/
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  perl-Template-Toolkit
BuildRequires:  perl-TimeDate

%description
VBinDiff (Visual Binary Diff) displays files in hexadecimal and ASCII (or
EBCDIC). It can also display two files at once, and highlight the differences
between them. Unlike diff, it works well with large files (up to 4 GB).

This package is built from the troed/vbindiff fork, which carries the fixes
needed to build and run on current openSUSE.

%prep
%autosetup -n %{name}-%{version}

%build
autoreconf -fi
%configure
%make_build

%install
%make_install

%files
%license COPYING
%doc README.md AUTHORS
%{_bindir}/vbindiff
%{_mandir}/man1/vbindiff.1%{?ext_man}

%changelog
* Sun Nov 01 2026 troed <github@troed.se> - 3.0~beta5-0
- Initial openSUSE package: upstream 3.0 beta5 plus fixes carried in the
  troed/vbindiff fork.
