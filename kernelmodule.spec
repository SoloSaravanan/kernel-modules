%global module_name linuwu_sense
%global kernel_version %(uname -r)
%global debug_package %{nil}

Name:             kernel-modules-solosaravanan
Version:          1.0
Release:          1%{?dist}
Summary:          Kernel module: %{module_name} from Solosaravanan's kernel modules collection
License:          GPLv2
URL:              https://github.com/SoloSaravanan

# Correct tarball reference
Source0:          kernel-modules-solosaravanan-1.0.tar.gz

BuildRequires:     make gcc kernel-devel
Requires(post):    kmod
Requires(postun):  kmod
Provides:          kmod(%{module_name})

%description
My kernel module collection.

%prep
%setup -q -n kernel-modules

%build
make KVER=%{kernel_version} -C %{_builddir}/kernel-modules/Linuwu-Sense

%install
mkdir -p %{buildroot}/lib/modules/%{kernel_version}/kernel/drivers/platform/x86
install -m 644 Linuwu-Sense/linuwu_sense.ko %{buildroot}/lib/modules/%{kernel_version}/kernel/drivers/platform/x86/

%post
/sbin/depmod -a %{kernel_version} || true

%postun
/sbin/depmod -a %{kernel_version} || true

%files
/lib/modules/%{kernel_version}/kernel/drivers/platform/x86/%{module_name}.ko
