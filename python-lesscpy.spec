%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global pypi_name lesscpy

Name:           python-%{pypi_name}
Version:        0.9j
Release:        4%{?dist}
Summary:        Lesscss compiler

License:        MIT
URL:            https://github.com/robotis/lesscpy
Source0:        https://pypi.python.org/packages/source/l/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-ply
 
Requires:       python-ply
Patch0:         python-lesscpy-fix-setup-encoding-issue.patch
%description
A compiler written in python 3 for the lesscss language.  For those of us not 
willing/able to have node.js installed in our environment.  Not all features 
of lesscss are supported (yet).  Some features wil probably never be 
supported (JavaScript evaluation). 

%if 0%{?with_python3}
%package -n python3-lesscpy
Summary:    Lesscss compiler 
Requires:   python3-ply
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-ply
%description -n python3-lesscpy
A compiler written in python 3 for the lesscss language.  For those of us not
willing/able to have node.js installed in our environment.  Not all features
of lesscss are supported (yet).  Some features wil probably never be
supported (JavaScript evaluation).
%endif #with_python3

%prep
%setup -q -n %{pypi_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
#fix utf8 encoding issue occurring only under py3
pushd %{py3dir}
%patch0 -p1
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
popd
%endif

%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
export LANG=en_US.utf8
env
%{__python3} setup.py build
popd
%endif # with_python3


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/lesscpy %{buildroot}/%{_bindir}/py3-lesscpy
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}


%check

%{__python} lesscpy/test/__main__.py
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} lesscpy/test/__main__.py
popd
%endif # with_python3

%files
%doc LICENSE
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{_bindir}/lesscpy
%if 0%{?with_python3}
%files -n python3-lesscpy
%doc LICENSE
%{_bindir}/py3-lesscpy
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.egg-info
%endif # with_python3


%changelog
* Wed Jan 29 2014 Matthias Runge <mrunge@redhat.com> - 0.9j-4
- epel7 has no python3

* Thu Aug 29 2013 Matthias Runge <mrunge@redhat.com> - 0.9j-3
- use python instead of python3 in python2 package

* Wed Aug 21 2013 Matthias Runge <mrunge@redhat.com> - 0.9j-2
- add br python-ply

* Mon Jul 29 2013 Matthias Runge <mrunge@redhat.com> - 0.9j-1
- Initial package.
