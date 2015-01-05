Name:		openstack-neutron-gbp
Version:	2014.2
Release:	0.5.rc2%{?dist}
Summary:	Group Based Policy service plugin for OpenStack Networking Service

License:	ASL 2.0
URL:		https://launchpad.net/group-based-policy

Source0:	http://tarballs.openstack.org/group-based-policy/group-based-policy-2014.2rc2.tar.gz

Patch0:		0001-remove-runtime-dependency-on-pbr.patch

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools

Requires:	openstack-neutron >= 2014.2
Requires:	openstack-neutron < 2014.3


%description
Group Based Policy (GBP) provides declarative abstractions for
achieving scalable intent-based infrastructure automation. GBP
complements the OpenStack networking model with the notion of policies
that can be applied between groups of network endpoints.


%prep
%setup -qn group-based-policy-%{version}rc2

%patch0 -p1

find gbpservice -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i 's/RPMVERSION/%{version}/' gbpservice/__init__.py

rm -f requirements.txt


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python2_sitelib}/gbpservice/neutron/tests
rm -rf %{buildroot}%{python2_sitelib}/gbpservice/tests


%files
%doc LICENSE
%doc README.rst
%doc etc/grouppolicy.ini
%{_bindir}/gbp-db-manage
%{python2_sitelib}/gbpservice
%{python2_sitelib}/group_based_policy-%%{version}*.egg-info


%changelog
* Mon Jan  5 2015 Robert Kukura <rk@theep.net> - 2014.2-0.5.rc2
- Update to rc2
- Updates for renamed top-level python module

* Tue Dec 30 2014 Robert Kukura <rk@theep.net> - 2014.2-0.4.rc1
- Update to rc1
- Remove Group tag
- Use python2_sitelib instead of python_sitelib
- Package sample config file fragment

* Mon Dec 15 2014 Robert Kukura <rk@theep.net> - 2014.2-0.3.acb85f0git
- Don't require specific neutron stable version
- Update to latest upstream commit

* Thu Dec  4 2014 Robert Kukura <rk@theep.net> - 2014.2-0.2.acb85f0git
- Update to commmit with renamed resources

* Mon Nov 17 2014 Robert Kukura <rk@theep.net> - 2014.2-0.1.b3be657git
- Initial package for Fedora
