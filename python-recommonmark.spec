# TODO:
# - package tools
#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		commit	33b5c2a4ec50d18d3f659aa119d3bd11452327da
%define		commit_date 20180907

Summary:	docutils-compatibility bridge to CommonMark
Name:		python-recommonmark
Version:	0.5.0
Release:	0.%{commit_date}.1
License:	MIT
Group:		Libraries/Python
Source0:	https://github.com/rtfd/recommonmark/archive/%{commit}/recommonmark-%{commit}.tar.gz
# Source0-md5:	64cc2f674a76bf740594055a3be32a2d
URL:		https://recommonmark.readthedocs.io/en/latest/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This allows you to write CommonMark inside of Docutils & Sphinx
projects.

%package -n python3-recommonmark
Summary:	docutils-compatibility bridge to CommonMark
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-recommonmark
This allows you to write CommonMark inside of Docutils & Sphinx
projects.

%prep
%setup -q -n recommonmark-%{commit}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/recommonmark
%{py_sitescriptdir}/recommonmark-%{version}.dev0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-recommonmark
%defattr(644,root,root,755)
%{py3_sitescriptdir}/recommonmark
%{py3_sitescriptdir}/recommonmark-%{version}.dev0-py*.egg-info
%endif
