Name:    libuser
Version: 0.63
Release: 2
Summary: A user and group account administration library
License: LGPLv2+
URL:     https://pagure.io/libuser
Source:  http://releases.pagure.org/libuser/libuser-%{version}.tar.xz

Patch0: libuser-0.63-PR49_add_yescrypt.patch
Patch1: libuser-0.63-downstream_test_xcrypt.patch
Patch2: change-bdb-to-mdb-for-slapd-test.patch

BuildRequires: cyrus-sasl-devel, nscd, linuxdoc-tools, pam-devel, popt-devel, gcc
BuildRequires: libselinux-devel, openldap-devel, python3-devel, glib2-devel
BuildRequires: openldap-clients, openldap-servers, openssl
BuildRequires: bison, make, libtool, gettext-devel, gtk-doc, audit-libs-devel

%description
The libuser library implements a standardized interface for manipulating
and administering user and group accounts. The library uses pluggable
back-ends to interface to its data sources. Sample applications modeled
after those included with the shadow password suite are included.

%package devel
Summary: Development libraries and files for %{name}
Requires: glib2-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The package contains lib and header files for developing application
that use %{name}

%package python3
Summary: the libuser library used for binding Python 3
Requires: libuser%{?_isa} = %{version}-%{release}

%description python3
The libuser library which provides a Python 3 API implements a
standardized interface for manipulating and administering user
and group accounts.

%package help
Summary:        Documents files for %{name}
Requires:       man, info

%description help
Man pages and other related documents for %{name}

%prep
%autosetup -n libuser-%{version} -p1

%build
./autogen.sh
%configure --with-ldap --with-selinux --with-html-dir=%{_prefix}/share/gtk-doc/html \
	PYTHON=%{_bindir}/python3
make

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' || :

%find_lang %{name}

%check
%make_build check || { cat test-suite.log; false; }

LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_prefix}/%{_lib}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH
cd $RPM_BUILD_ROOT/%{python3_sitearch}
python3 -c "import libuser"

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README TODO docs/*.txt
%config(noreplace) %{_sysconfdir}/libuser.conf
%attr(0755,root,root) %{_exec_prefix}/bin/*
%{_prefix}/%{_lib}/%{name}/*.so
%{_prefix}/%{_lib}/*.so.*
%dir %{_prefix}/%{_lib}/%{name}
%attr(0755,root,root) %{_exec_prefix}/sbin/*
%exclude %{_prefix}/%{_lib}/%{name}/*.la
%exclude %{_prefix}/%{_lib}/*.la

%files python3
%doc python/modules.txt
%{python3_sitearch}/*.so
%exclude %{python3_sitearch}/*.la

%files devel
%{_exec_prefix}/%{_lib}/*.so
%{_exec_prefix}/%{_lib}/pkgconfig/*
%{_includedir}/libuser

%files help
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Sat Jan 8 2022 panxiaohe <panxiaohe@huawei.com> - 0.63-2
- change bdb to mdb for ldap_test and defult_pw_test

* Sat Nov 27 2021 fuanan <fuanan3@huawei.com> - 0.63-1
- update version to 0.63

* Tue Jul 20 2021 fuanan <fuanan3@huawei.com> - 0.62-23
- Remove redundant gdb from BuildRequires

* Thu Oct 29 2020 wangchen <wangchen137@huawei.com> - 0.62-22
- remove python2

* Thu Jul 30 2020 zhangxingliang <zhangxingliang3@huawei.com> - 0.62-21
- do not use deprecated flask.h and av_permissions.h

* Sat Mar 21 2020 chengquan<chengquan3@huawei.com> - 0.62-20
- add necessary BuildRequires

* Tue Sep 10 2019 caomeng<caomeng5@huawei.com> - 0.62-19
- Package init
