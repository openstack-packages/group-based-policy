%global commit acb85f0fc91084a62fbc927e9079b5403bf8207e
%global commitseq 62
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		openstack-neutron-gbp
Version:	2014.2
Release:	0.2.%{shortcommit}git%{?dist}
Summary:	Group Based Policy service plugin for OpenStack Networking Service

Group:		Applications/System
License:	ASL 2.0
URL:		https://launchpad.net/group-based-policy

# The source tarball is created as follows:
#  git clone http://git.openstack.org/cgit/stackforge/group-based-policy
#  cd group-based-policy
#  git checkout %%{commit}
#  python setup.py sdist
Source0:	group-based-policy-%{version}.dev%{commitseq}.g%{shortcommit}.tar.gz

Patch0:		0001-remove-runtime-dependency-on-pbr.patch

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools

Requires:	openstack-neutron = %{version}


%description
Group Based Policy (GBP) provides declarative abstractions for
achieving scalable intent-based infrastructure automation. GBP
complements the OpenStack networking model with the notion of policies
that can be applied between groups of network endpoints.


%prep
%setup -qn group-based-policy-%{version}.dev%{commitseq}.g%{shortcommit}

%patch0 -p1

find gbp -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i 's/RPMVERSION/%{version}/' gbp/__init__.py

rm -f requirements.txt


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python_sitelib}/gbp/neutron/tests
rm -rf %{buildroot}%{python_sitelib}/gbp/tests


%files
%doc LICENSE
%doc README.rst
%{_bindir}/gbp-db-manage
%{python_sitelib}/gbp
%{python_sitelib}/group_based_policy-%%{version}*.egg-info


%changelog
* Thu Dec  4 2014 Robert Kukura <rk@theep.net> - 2014.2-0.2.acb85f0git
- Update to commmit with renamed resources

* Mon Nov 17 2014 Robert Kukura <rk@theep.net> - 2014.2-0.1.b3be657git
- Initial package for Fedora
