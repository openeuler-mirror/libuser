Name    : libuser
Version : 0.62
Release : 19
Summary : A user and group account administration library
License : LGPLv2+
URL     : https://pagure.io/libuser
Source  : http://releases.pagure.org/libuser/libuser-%{version}.tar.xz

# Patch1 : this patch is from fedora.
Patch1   :    0001-Fix-errors-with-Werror-format-security.patch

Patch9000:    0009-Check-negative-return-of-PyList_Size.patch
Patch9001:    0010-files.c-Init-char-name-to-NULL.patch
Patch9002:    0011-merge_ent_array_duplicates-Only-use-values-if-valid.patch
Patch9003:    0012-editing_open-close-fd-after-we-ve-established-its-va.patch

BuildRequires: cyrus-sasl-devel, nscd, linuxdoc-tools, pam-devel, popt-devel, gcc
BuildRequires: libselinux-devel, openldap-devel, python3-devel, glib2-devel
BuildRequires: python2-devel, fakeroot, openldap-clients, openldap-servers, openssl

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

%package -n python2-libuser
Summary: the libuser library used for binding Python 2
%{?python_provide:%python_provide python2-libuser}
Requires: libuser%{?_isa} = %{version}-%{release}
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}

%description -n python2-libuser
The libuser library which provides a Python 2 API implements a
standardized interface for manipulating and administering user
and group accounts.

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
%setup -qc

pushd libuser-%{version}
%patch1 -p1
%patch9000 -p1
%patch9001 -p1
%patch9002 -p1
%patch9003 -p1
popd

cp -dpR libuser-%{version} python2 || :
cp -dpR python2 python3 || :
rm -rf libuser-%{version} || :

pushd python2
cp -pr COPYING AUTHORS NEWS README TODO docs ../ || :
popd

%build
pushd python2
%configure --with-ldap --with-selinux --with-html-dir=%{_prefix}/share/gtk-doc/html \
	PYTHON=%{_bindir}/python2
make
popd

pushd python3
%configure --with-ldap --with-selinux --with-html-dir=%{_prefix}/share/gtk-doc/html \
	PYTHON=%{_bindir}/python3
make
popd

%install
make -C python3 install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' || :
make -C python2 install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' || :

%find_lang %{name}

%check

make -C python2 check || { cat python2/test-suite.log; false; }
LC_ALL=C.UTF-8 make -C python3 check \
	|| { cat python3/test-suite.log; false; }
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_prefix}/%{_lib}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH
cd $RPM_BUILD_ROOT/%{python2_sitearch}
python2 -c "import libuser"
cd $RPM_BUILD_ROOT/%{python3_sitearch}
LC_ALL=C.UTF-8 python3 -c "import libuser"

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

%files -n python2-libuser
%doc python2/python/modules.txt
%{python2_sitearch}/*.so
%exclude %{python2_sitearch}/*.la

%files python3
%doc python3/python/modules.txt
%{python3_sitearch}/*.so
%exclude %{python3_sitearch}/*.la

%files devel
%{_exec_prefix}/%{_lib}/*.so
%{_exec_prefix}/%{_lib}/pkgconfig/*
%{_includedir}/libuser
%{_prefix}/share/gtk-doc/html/*

%files help
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Tue Sep 10 2019 caomeng<caomeng5@huawei.com> - 0.62-19
- Package init
