%define name    bruco
%define version 0.1.4
%define release 1

Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   Brute force coherence

Group:     Development/Libraries
License:   GPLv3
Url:       https://git.ligo.org/gabriele-vajente/bruco
Source0:   https://pypi.io/packages/source/b/%{name}/%{name}-%{version}.tar.gz
Vendor:    Gabriele Vajente <gabriele.vajente@ligo.org>
Packager:  Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch

# build dependencies
BuildRequires: rpm-build
BuildRequires: python-rpm-macros
BuildRequires: python2-rpm-macros
BuildRequires: python2-setuptools

%description
Brute force coherence

# -- python2-bruco

%package -n python2-%{name}
Summary:  %{summary}
Requires: matplotlib
Requires: numpy
Requires: python2-gwdatafind
Requires: python2-gwpy
Requires: scipy
%{?python_provide:%python_provide python2-%{name}}
%description -n python2-%{name}
Brute force coherence

# -- build steps

%prep
%autosetup -n %{name}-%{version}

%build
%py2_build

%install
%py2_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license LICENSE
%doc README.md
%{_bindir}/bruco
%{python2_sitelib}/*
%{_datarootdir}/bruco

# -- changelog

%changelog
* Fri Nov 27 2020 Gabriele Vajente <gabriele.vajente@ligo.org> 0.1.3
- fixed matplotlib warning
* Fri Mar 15 2019 Gabriele Vajente <gabriele.vajente@ligo.org> 0.1.1-1
- added range computation
* Wed Mar 13 2019 Gabriele Vajente <gabriele.vajente@ligo.org> 0.1.0-1
- ready for release
* Tue Jan 29 2019 Duncan Macleod <duncan.macleod@ligo.org> 0.1.0-1
- first packaging
