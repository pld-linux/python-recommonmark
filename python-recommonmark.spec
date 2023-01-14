#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	docutils-compatibility bridge to CommonMark
Summary(pl.UTF-8):	Pomost zgodności z docutils dla CommonMark
Name:		python-recommonmark
Version:	0.7.1
Release:	4
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/recommonmark/
Source0:	https://files.pythonhosted.org/packages/source/r/recommonmark/recommonmark-%{version}.tar.gz
# Source0-md5:	3c550a76eb62006bf007843a9f1805bb
# from https://github.com/readthedocs/recommonmark/pull/124
# https://github.com/readthedocs/recommonmark/commit/917e0359fa93acd9b22d7122e2c03d994d9fda44.patch
Patch0:		%{name}-math.patch
Patch1:		%{name}-docutils.patch
URL:		https://recommonmark.readthedocs.io/en/latest/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Sphinx >= 1.3.1
BuildRequires:	python-commonmark >= 0.8.1
BuildRequires:	python-docutils >= 0.11
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.3.1
BuildRequires:	python3-commonmark >= 0.8.1
BuildRequires:	python3-docutils >= 0.11
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-commonmark >= 0.8.1
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This allows you to write CommonMark inside of Docutils & Sphinx
projects.

%description -l pl.UTF-8
Ten moduł pozwala na pisanie z użyciem CommonMark wewnątrz projektów
Docutils i Sphinksa.

%package -n python3-recommonmark
Summary:	docutils-compatibility bridge to CommonMark
Summary(pl.UTF-8):	Pomost zgodności z docutils dla CommonMark
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-recommonmark
This allows you to write CommonMark inside of Docutils & Sphinx
projects.

%description -n python3-recommonmark -l pl.UTF-8
Ten moduł pozwala na pisanie z użyciem CommonMark wewnątrz projektów
Docutils i Sphinksa.

%package apidocs
Summary:	Documentation for Python recommonmark module
Summary(pl.UTF-8):	Dokumentacja modułu Pythona recommonmark
Group:		Documentation

%description apidocs
Documentation for Python recommonmark module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu Pythona recommonmark.

%prep
%setup -q -n recommonmark-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
# skip: python2 uses different XML formatting, tests expect python3 formatting
%{__python} -m pytest tests -k 'not CustomExtensionTests'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# sphinx tests are too dependent on Sphinx version
%{__python3} -m pytest tests -k 'not test_sphinx'
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

for f in cm2{html,latex,man,pseudoxml,xetex,xml} ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${f} $RPM_BUILD_ROOT%{_bindir}/${f}-2
done
%endif

%if %{with python3}
%py3_install

for f in cm2{html,latex,man,pseudoxml,xetex,xml} ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${f} $RPM_BUILD_ROOT%{_bindir}/${f}-3
	ln -sf ${f}-3 $RPM_BUILD_ROOT%{_bindir}/${f}
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md license.md
%attr(755,root,root) %{_bindir}/cm2html-2
%attr(755,root,root) %{_bindir}/cm2latex-2
%attr(755,root,root) %{_bindir}/cm2man-2
%attr(755,root,root) %{_bindir}/cm2pseudoxml-2
%attr(755,root,root) %{_bindir}/cm2xetex-2
%attr(755,root,root) %{_bindir}/cm2xml-2
%{py_sitescriptdir}/recommonmark
%{py_sitescriptdir}/recommonmark-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-recommonmark
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md license.md
%attr(755,root,root) %{_bindir}/cm2html
%attr(755,root,root) %{_bindir}/cm2latex
%attr(755,root,root) %{_bindir}/cm2man
%attr(755,root,root) %{_bindir}/cm2pseudoxml
%attr(755,root,root) %{_bindir}/cm2xetex
%attr(755,root,root) %{_bindir}/cm2xml
%attr(755,root,root) %{_bindir}/cm2html-3
%attr(755,root,root) %{_bindir}/cm2latex-3
%attr(755,root,root) %{_bindir}/cm2man-3
%attr(755,root,root) %{_bindir}/cm2pseudoxml-3
%attr(755,root,root) %{_bindir}/cm2xetex-3
%attr(755,root,root) %{_bindir}/cm2xml-3
%{py3_sitescriptdir}/recommonmark
%{py3_sitescriptdir}/recommonmark-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
