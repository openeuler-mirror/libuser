Name:    libuser
Version: 0.62
Release: 22
Summary: A user and group account administration library
License: LGPLv2+
URL:     https://pagure.io/libuser
Source:  http://releases.pagure.org/libuser/libuser-%{version}.tar.xz

# Patch0 : this patch is from fedora.
Patch0:    0001-Fix-errors-with-Werror-format-security.patch
Patch1:    0009-Check-negative-return-of-PyList_Size.patch
Patch2:    0010-files.c-Init-char-name-to-NULL.patch
Patch3:    0011-merge_ent_array_duplicates-Only-use-values-if-valid.patch
Patch4:    0012-editing_open-close-fd-after-we-ve-established-its-va.patch
Patch5:    libuser-do-not-use-deprecated-flask.h-and-av_permissions.patch

BuildRequires: cyrus-sasl-devel, nscd, linuxdoc-tools, pam-devel, popt-devel, gcc
BuildRequires: libselinux-devel, openldap-devel, python3-devel, glib2-devel, gdb
BuildRequires: fakeroot, openldap-clients, openldap-servers, openssl

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
%setup -qn libuser-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure --with-ldap --with-selinux --with-html-dir=%{_prefix}/share/gtk-doc/html \
	PYTHON=%{_bindir}/python3
make

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' || :

%find_lang %{name}

%check

#make -C python2 check || { cat python2/test-suite.log; false; }
#LC_ALL=C.UTF-8 make -C python3 check \
#	|| { cat python3/test-suite.log; false; }
#LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_prefix}/%{_lib}:${LD_LIBRARY_PATH}
#export LD_LIBRARY_PATH
#cd $RPM_BUILD_ROOT/%{python2_sitearch}
#python2 -c "import libuser"
#cd $RPM_BUILD_ROOT/%{python3_sitearch}
#LC_ALL=C.UTF-8 python3 -c "import libuser"

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
%{_prefix}/share/gtk-doc/html/*

%files help
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Thu Oct 29 2020 wangchen <wangchen137@huawei.com> - 0.62-22
- remove python2

* Thu Jul 30 2020 zhangxingliang <zhangxingliang3@huawei.com> - 0.62-21
- do not use deprecated flask.h and av_permissions.h

* Sat Mar 21 2020 chengquan<chengquan3@huawei.com> - 0.62-20
- add necessary BuildRequires

* Tue Sep 10 2019 caomeng<caomeng5@huawei.com> - 0.62-19
- Package init
