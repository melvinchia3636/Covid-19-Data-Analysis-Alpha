# Author: RedFantom
# License: GNU GPLv3
# Copyright (c) 2017-2020 RedFantom

package require Tk 8.6
set png_theme_dir [file join [pwd] [file dirname [info script]]]

array set png_themes {
  breeze 0.6
}

foreach {theme version} [array get png_themes] {
  package ifneeded ttk::theme::$theme $version \
    [list source [file join $png_theme_dir $theme $theme.tcl]]
}

