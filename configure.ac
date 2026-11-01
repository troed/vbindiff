#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.72])
AC_INIT([[Visual Binary Diff]], [[3.0_beta5]], [[vbindiff AT cjmweb.net]], [[vbindiff]], [[https://www.cjmweb.net/vbindiff/]])
AM_INIT_AUTOMAKE([1.9 foreign])
AC_CONFIG_SRCDIR([vbindiff.cpp])
AC_CONFIG_HEADERS([config.h])
AC_LANG([C++])
AC_REVISION([m4_esyscmd([./tools/configure.commit])])

# Decide whether to enable debugging:
CFLAGS="${CFLAGS=}"

AC_MSG_CHECKING(whether to enable debugging)
AC_ARG_ENABLE(debug,
  [AS_HELP_STRING([--enable-debug], [turn on debugging (default is no)])],
  , enable_debug=no)

if test "x$enable_debug" = "xyes"; then
  CFLAGS="-g -DDEBUG $CFLAGS"
  AC_MSG_RESULT(yes)
else
  CFLAGS="-O2 $CFLAGS"
  AC_MSG_RESULT(no)
fi

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC

# Checks for libraries.
AC_SEARCH_LIBS([initscr], [ncurses], ,
             [AC_MSG_ERROR([The ncurses library is required])])
AC_SEARCH_LIBS([cbreak], [ncurses tinfo], ,
             [AC_MSG_ERROR([The ncurses/tinfo library is required])])
AC_SEARCH_LIBS([new_panel], [panel], ,
             [AC_MSG_ERROR([The panel library is required])])

# Checks for header files.
m4_warn([obsolete],
[The preprocessor macro 'STDC_HEADERS' is obsolete.
  Except in unusual embedded environments, you can safely include all
  C89 headers unconditionally.])dnl
# Autoupdate added the next two lines to ensure that your configure
# script's behavior did not change.  They are probably safe to remove.
AC_CHECK_INCLUDES_DEFAULT
AC_PROG_EGREP

AC_CHECK_HEADERS([errno.h fcntl.h limits.h panel.h ncurses/panel.h stdlib.h string.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_CONST
AC_C_INLINE
AC_TYPE_OFF_T
AC_TYPE_SIZE_T

# Checks for library functions.
AC_FUNC_MEMCMP
AC_CHECK_FUNCS([atexit memset strchr strerror strrchr strtoul])

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
