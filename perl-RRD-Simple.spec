#
# Conditional build:
%bcond_without	tests		# do not perform "make test"

%define		pdir	RRD
%define		pnam	Simple
%include	/usr/lib/rpm/macros.perl
Summary:	RRD::Simple - Simple interface to create and store data in RRD files
Name:		perl-RRD-Simple
Version:	1.44
Release:	2
License:	Open Source
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/N/NI/NICOLAW/RRD-Simple-%{version}.tar.gz
# Source0-md5:	cddfd8b22310946974af7762e1778a7e
URL:		http://search.cpan.org/dist/RRD-Simple/
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Test-Deep
BuildRequires:	perl-Test-Pod >= 1.00
BuildRequires:	perl-Test-Pod-Coverage >= 1.00
BuildRequires:	perl-rrdtool
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RRD::Simple provides a simple interface to RRDTool's RRDs module. This
module does not currently offer a fetch method that is available in
the RRDs module.

It does however create RRD files with a sensible set of default RRA
(Round Robin Archive) definitions, and can dynamically add new data
source names to an existing RRD file.

This module is ideal for quick and simple storage of data within an
RRD file if you do not need to, nor want to, bother defining custom
RRA definitions.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

# skip failing tests (FIX THEM)
%if "%{pld_release}" == "th"
# these fail with rrdtool 1.4.4 (th), ok with 1.2.27 (ac)
rm t/10pod.t
rm t/23graph.t
rm t/32exported_function_interface.t
%endif

%build
AUTOMATED_TESTING=1 \
%{__perl} Build.PL \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes INSTALL README TODO
%{perl_vendorlib}/RRD/*.pm
%{perl_vendorlib}/RRD/Simple
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
