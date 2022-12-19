# DeleteShortSegments.glyphsFilter

This is a plugin for the [Glyphs font editor](http://glyphsapp.com/) by Georg Seifert. After installation, it will add the menu item *Filter > Delete Short Segments* (de: *Kurze Segmente löschen*). You can set a keyboard shortcut in System Preferences.

![DeleteShortSegments](DeleteShortSegments.png "Delete Short Segments Screenshot")

*Filter > Delete Short Segments* deletes line and curve segments from your selected paths (or all if none are selected) that are shorter than the specified *Max Length.* This can be very useful for cleaning up roughened paths when you have a grid step finer than 1 unit. Values smaller than 0.1 are treated as 0.1.

The process is repeated as often as indicated by the *Passes* value you specify. 1 or 2 passes are recommended. Values lower than 1 pass are treated as 1 pass.

### Installation

1. One-click install *DeleteShortSegments* from *Window > Plugin Manager*
2. Restart Glyphs.

### Usage Instructions

1. Open a glyph in Edit View.
2. Choose *Filter > Delete Short Segments.*

### Custom Parameter

You can trigger the filter at export time with a custom parameter in *File > Font Info > Instances:*

    Property: Filter
    Value: DeleteShortSegments;

Or with any of the `maxLength` and `passes` options:

    Property: Filter
    Value: DeleteShortSegments; maxLength: 3; passes: 1

`maxLength` is the default threshold size (in units) below which the segment will be deleted. Default: 1 unit. 

`passes` is the amount of times the filter goes through all your paths. By default, the filter goes *twice* through your paths. A single pass is significantly faster, but sometimes misses a few cases, especially if a couple of very short segments follow each other.

### Requirements

The plugin needs Glyphs 2.4.1 or higher, running on OS X 10.9 or later. It does NOT work with Glyphs 1.x.

### License

Copyright 2017 Rainer Erich Scheichelbauer (@mekkablue).
Based on sample code by Georg Seifert (@schriftgestalt) and Jan Gerner (@yanone).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
