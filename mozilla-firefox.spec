# NOTE: PLD distributes iceweasel instead
#
# TODO:
# - (12:22:58)  patrys:  can you also move _libdir/mozilla-firefox to just _libdir/firefox?
#   (12:23:25)  patrys:  it's not like we ship official firefox
# - fix wrapper script to allow playing with profiles (must not use -remote)
#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnome		# synonym for gnomeui (gconf, libnotify and gio are still enabled)
%bcond_without	kerberos	# disable krb5 support
%bcond_without	xulrunner	# system xulrunner

%if %{without gnome}
%undefine	with_gnomeui
%endif

%if %{without xulrunner}
# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)
%endif

Summary:	Firefox Community Edition web browser
Summary(pl.UTF-8):	Firefox Community Edition - przeglądarka WWW
Name:		mozilla-firefox
Version:	11.0
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}.source.tar.bz2
# Source0-md5:	4b07acf47857aff72776d805409cdd1b
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-install.patch
Patch1:		%{name}-gcc3.patch
Patch2:		%{name}-agent.patch
Patch3:		%{name}-agent-ac.patch
Patch4:		%{name}-ti-agent.patch
Patch5:		%{name}-branding.patch
Patch6:		%{name}-prefs.patch
Patch7:		%{name}-nss_cflags.patch
Patch8:		%{name}-no-subshell.patch
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.2-5
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	glib2-devel >= 1:2.18
BuildRequires:	gtk+2-devel >= 2:2.14
%{?with_kerberos:BuildRequires:	heimdal-devel >= 0.7.1}
BuildRequires:	hunspell-devel
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libdnet-devel
BuildRequires:	libevent-devel >= 1.4.7
# standalone libffi 3.0.9 or gcc's from 4.5(?)+
BuildRequires:	libffi-devel >= 6:3.0.9
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libiw-devel
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libnotify-devel >= 0.4
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 1.4.1
BuildRequires:	libstdc++-devel
BuildRequires:	libvpx-devel >= 1.0.0
BuildRequires:	nspr-devel >= 1:4.9
BuildRequires:	nss-devel >= 1:3.13.3
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.9
BuildRequires:	python-modules
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sqlite3-devel >= 3.7.7.1
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
%if %{with xulrunner}
BuildRequires:	xulrunner-devel >= 2:%{version}
%endif
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
%if %{with xulrunner}
%requires_eq_to	xulrunner xulrunner-devel
%else
Requires:	browser-plugins >= 2.0
Requires:	cairo >= 1.10.2-5
Requires:	dbus-glib >= 0.60
Requires:	glib2 >= 1:2.18
Requires:	gtk+2 >= 2:2.14
Requires:	libpng >= 1.4.1
Requires:	libpng(APNG) >= 0.10
Requires:	myspell-common
Requires:	nspr >= 1:4.8.9
Requires:	nss >= 1:3.13.1
Requires:	pango >= 1:1.14.0
Requires:	sqlite3 >= %{sqlite_build_version}
Requires:	startup-notification >= 0.8
%endif
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Obsoletes:	mozilla-firefox-lang-en < 2.0.0.8-3
Obsoletes:	mozilla-firefox-libs
Conflicts:	mozilla-firefox-lang-resources < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't satisfy other packages (don't use %{name} here)
%define		_noautoprovfiles	%{_libdir}/mozilla-firefox
# and as we don't provide them, don't require either
%define		_noautoreq	libmozjs.so libxpcom.so libxul.so %{!?with_xulrunner:libmozalloc.so}

%if "%{cc_version}" >= "3.4"
%define		specflags	-fno-strict-aliasing -fno-tree-vrp -fno-stack-protector
%else
%define		specflags	-fno-strict-aliasing
%endif

%description
Firefox Community Edition is an open-source web browser, designed for
standards compliance, performance and portability.

%description -l pl.UTF-8
Firefox Community Edition jest przeglądarką WWW rozpowszechnianą
zgodnie z ideami ruchu otwartego oprogramowania oraz tworzoną z myślą
o zgodności ze standardami, wydajnością i przenośnością.

%prep
%setup -qc
mv -f mozilla-release mozilla
cd mozilla

# libvpx fix
grep -q VPX_CODEC_USE_INPUT_PARTITION configure.in && sed -i 's#VPX_CODEC_USE_INPUT_PARTITION#VPX_CODEC_USE_INPUT_FRAGMENTS#' configure || exit 1

%patch0 -p1

%if "%{cc_version}" < "3.4"
%patch1 -p2
%endif

%if "%{pld_release}" == "th"
%patch2 -p1
%endif

%if "%{pld_release}" == "ac"
%patch3 -p1
%endif

%if "%{pld_release}" == "ti"
%patch4 -p1
%endif

%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p2

# config/rules.mk is patched by us and js/src/config/rules.mk
# is supposed to be exact copy
cp -a config/rules.mk js/src/config/rules.mk

%build
cd mozilla
cp -f %{_datadir}/automake/config.* build/autoconf

cat << EOF > .mozconfig
. \$topsrcdir/browser/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

# Options for 'configure' (same as command-line options).
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
ac_add_options --disable-elf-hack
%if %{?debug:1}0
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags} -Os"
%endif
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnomeui}
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomeui
%endif
ac_add_options --disable-gnomevfs
ac_add_options --disable-crashreporter
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-gio
ac_add_options --enable-libxul
ac_add_options --enable-pango
ac_add_options --enable-shared-js
ac_add_options --enable-startup-notification
ac_add_options --enable-system-cairo
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --with-distribution-id=org.pld-linux
%if %{with xulrunner}
ac_add_options --with-libxul-sdk=$(pkg-config --variable=sdkdir libxul)
%endif
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-ffi
ac_add_options --with-system-jpeg
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
EOF

%{__make} -f client.mk build \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

%{__make} -C obj-%{_target_cpu}/browser/installer stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_DIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

install -d \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins

%if %{with xulrunner}
# >= 5.0 seems to require this
ln -s ../xulrunner $RPM_BUILD_ROOT%{_libdir}/%{name}/xulrunner
%endif

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/modules $RPM_BUILD_ROOT%{_datadir}/%{name}/modules
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins $RPM_BUILD_ROOT%{_datadir}/%{name}/searchplugins
%if %{without xulrunner}
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs.js $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs.js
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
%endif

ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions
ln -s ../../share/%{name}/modules $RPM_BUILD_ROOT%{_libdir}/%{name}/modules
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/searchplugins $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins
%if %{without xulrunner}
ln -s ../../share/%{name}/greprefs.js $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs.js
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res
%endif

%if %{without xulrunner}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
%endif

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
chmod 755 $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
ln -s mozilla-firefox $RPM_BUILD_ROOT%{_bindir}/firefox

cp -a browser/branding/unofficial/content/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# files created by firefox -register
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

%if %{with xulrunner}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/run-mozilla.sh
%endif

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{name}/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

%{_libdir}/%{name}/firefox -register

rm -rf $HOME
EOF
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults extensions greprefs.js icons res searchplugins; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

%post
%{_sbindir}/%{name}-chrome+xpcom-generate
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_sbindir}/%{name}-chrome+xpcom-generate

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}
%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom.so
%attr(755,root,root) %{_libdir}/%{name}/libxul.so
%endif
%{_libdir}/%{name}/blocklist.xml

%if %{with crashreporter}
%{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter-override.ini
%{_libdir}/%{name}/crashreporter.ini
%{_libdir}/%{name}/Throbber-small.gif
%endif

# config?
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/chrome.manifest

%dir %{_libdir}/%{name}/components

%{_libdir}/%{name}/components/ChromeProfileMigrator.js
%{_libdir}/%{name}/components/FeedConverter.js
%{_libdir}/%{name}/components/FeedWriter.js
%{_libdir}/%{name}/components/PlacesProtocolHandler.js
%{_libdir}/%{name}/components/Weave.js
%{_libdir}/%{name}/components/WebContentConverter.js
%{_libdir}/%{name}/components/browser.xpt
%{_libdir}/%{name}/components/fuelApplication.js
%{_libdir}/%{name}/components/nsBrowserContentHandler.js
%{_libdir}/%{name}/components/nsBrowserGlue.js
%{_libdir}/%{name}/components/nsPrivateBrowsingService.js
%{_libdir}/%{name}/components/nsSafebrowsingApplication.js
%{_libdir}/%{name}/components/nsSessionStartup.js
%{_libdir}/%{name}/components/nsSessionStore.js
%{_libdir}/%{name}/components/nsSetDefaultBrowser.js
%{_libdir}/%{name}/components/nsSidebar.js

%{_libdir}/%{name}/components/components.manifest
%{_libdir}/%{name}/components/interfaces.manifest

%if %{without xulrunner}
%{_libdir}/%{name}/platform.ini
%{_libdir}/%{name}/components/ConsoleAPI.js
%{_libdir}/%{name}/components/FeedProcessor.js
%{_libdir}/%{name}/components/GPSDGeolocationProvider.js
%{_libdir}/%{name}/components/NetworkGeolocationProvider.js
%{_libdir}/%{name}/components/PlacesCategoriesStarter.js
%{_libdir}/%{name}/components/TelemetryPing.js
%{_libdir}/%{name}/components/addonManager.js
%{_libdir}/%{name}/components/amContentHandler.js
%{_libdir}/%{name}/components/amWebInstallListener.js
%{_libdir}/%{name}/components/contentAreaDropListener.js
%{_libdir}/%{name}/components/contentSecurityPolicy.js
%{_libdir}/%{name}/components/crypto-SDR.js
%{_libdir}/%{name}/components/jsconsole-clhandler.js
%{_libdir}/%{name}/components/nsBadCertHandler.js
%{_libdir}/%{name}/components/nsBlocklistService.js
%{_libdir}/%{name}/components/nsContentDispatchChooser.js
%{_libdir}/%{name}/components/nsContentPrefService.js
%{_libdir}/%{name}/components/nsDefaultCLH.js
%{_libdir}/%{name}/components/nsDownloadManagerUI.js
%{_libdir}/%{name}/components/nsFilePicker.js
%{_libdir}/%{name}/components/nsFormAutoComplete.js
%{_libdir}/%{name}/components/nsFormHistory.js
%{_libdir}/%{name}/components/nsHandlerService.js
%{_libdir}/%{name}/components/nsHelperAppDlg.js
%{_libdir}/%{name}/components/nsINIProcessor.js
%{_libdir}/%{name}/components/nsInputListAutoComplete.js
%{_libdir}/%{name}/components/nsLivemarkService.js
%{_libdir}/%{name}/components/nsLoginInfo.js
%{_libdir}/%{name}/components/nsLoginManager.js
%{_libdir}/%{name}/components/nsLoginManagerPrompter.js
%{_libdir}/%{name}/components/nsPlacesAutoComplete.js
%{_libdir}/%{name}/components/nsPlacesExpiration.js
%{_libdir}/%{name}/components/nsPrompter.js
%{_libdir}/%{name}/components/nsProxyAutoConfig.js
%{_libdir}/%{name}/components/nsSearchService.js
%{_libdir}/%{name}/components/nsSearchSuggestions.js
%{_libdir}/%{name}/components/nsTaggingService.js
%{_libdir}/%{name}/components/nsTryToClose.js
%{_libdir}/%{name}/components/nsURLFormatter.js
%{_libdir}/%{name}/components/nsUpdateTimerManager.js
%{_libdir}/%{name}/components/nsUrlClassifierHashCompleter.js
%{_libdir}/%{name}/components/nsUrlClassifierLib.js
%{_libdir}/%{name}/components/nsUrlClassifierListManager.js
%{_libdir}/%{name}/components/nsWebHandlerApp.js
%{_libdir}/%{name}/components/storage-Legacy.js
%{_libdir}/%{name}/components/storage-mozStorage.js
%{_libdir}/%{name}/components/txEXSLTRegExFunctions.js
%endif

%attr(755,root,root) %{_libdir}/%{name}/components/libbrowsercomps.so
%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so
%endif

%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
%endif

%attr(755,root,root) %{_libdir}/%{name}/firefox
%dir %{_libdir}/%{name}/plugins
%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/run-mozilla.sh
%attr(755,root,root) %{_libdir}/%{name}/firefox-bin
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%endif

%{_pixmapsdir}/mozilla-firefox.png
%{_desktopdir}/mozilla-firefox.desktop

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/extensions
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/modules
%{_libdir}/%{name}/searchplugins
%if %{with xulrunner}
%{_libdir}/%{name}/xulrunner
%else
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/greprefs.js
%{_libdir}/%{name}/res
%endif

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/searchplugins
%if %{without xulrunner}
%{_datadir}/%{name}/greprefs.js
%{_datadir}/%{name}/res
%endif

%dir %{_datadir}/%{name}/extensions
# the signature of the default theme
%{_datadir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

# files created by firefox -register
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat
