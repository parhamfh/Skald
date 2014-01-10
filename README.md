Skald
=====

*Ja visst är det fint när orden talar?*

Application built on top of **Orpheus**, a project developed at Sagayama Lab, Graduate School of Information Science and Technology at the University of Tokyo. Orpheus is a project that is the engine behind the Orpheus website which allows users to write Japanese lyrics and specify musical parameters and then generates a song based on that information.

Most importantly, the melody for the song is based on the actual pronounciation of the Japanese words, aiming to resemble how they sound when spoken. The user is given the resulting song in the form of sheet music and a .mp3 file of the generated song played by MIDI with the voice synthesized.

Skald is an attempt to adapt and use Orpheus for Swedish. The main addition to Orpheus that Skald brings is to generate a rhythm for the melody of the text based on the pronounciation of the Swedish words, besides modelling the height of the melody after pronounciation as in the Japanese case.

This differs from Orpheus since standard Japanese does have an even rhythm where every mora has the same duration, so Orpheus allows users to select the rhythm from a set of pregenerated static rhythm patterns.

### Prerequisites
* TeX
* lilypond

### Installation
* clone repo
* init submodule (make sure that you meet its prerequisites)
* install TeX (MacTeX 2013 in OS X case)
* install lilypond (For Mac, use brew, requires MacTeX)

That should be it! Run it!
<<
#### OS X 10.9 (at least) + brew lilypond issue

The formula for lilypond provided by brew does not manage to build lilypond together with libc++ under OS X 10.9, so you need to use this formula instead https://github.com/adamv/homebrew/commit/acf61d7 and run with the developer flag:

`brew install --devel lilypond`

Download the lilypond formula from adamv and replace the `lilypond.rb` formula (back it up) in your Homebrew formula folder (Homebrew uses a `/Library` replica[1][2] which by default is placed under `/usr/local/`): `$HOMEBREW_PREFIX/Library/Formula`.

Also, when you currently install MacTeX-2013 it installs a version of mpost (metapost) not compatible with brew, so when you try to run `brew install --devel lilypond` it will further down in the process give the error:

```
ERROR: Please install required programs:  mpost (due to a bug in metapost, versions 1.600 <= x < 1.803 are not supported; installed: 1.802) 
```

So you need to upgrade mpost which can be quite hard finding information about how to do on OS X but you just need to open **TeX Live Utility**, make sure the *Updates* tab is selected and then search for `metapost` (not mpost) and upgrade it to 1.803. Now you can `brew install lilypond`

[Source](https://github.com/Homebrew/homebrew/issues/23336#issuecomment-29144066)

[1] - http://superuser.com/questions/391497/os-x-lion-easy-install-requires-sudo/405405#405405 / https://github.com/Homebrew/homebrew/wiki/Gems%2C-Eggs-and-Perl-Modules
[2] - After upgrading to an OS X post 10.7 (from, say, 10.6, ehm) you might experience that you lack permissions in /usr/local/, which `brew` likes to use. This [SO question](http://superuser.com/questions/254843/cant-install-brew-formulae-correctly-permission-denied-in-usr-local-lib) suggested this [gist](https://gist.github.com/rpavlik/768518) which resolves the permission issues.
