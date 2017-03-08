
## Added
 - Command enable / disable
 - Command aliases with `!alias` ([documentation](http://cactusbot.readthedocs.io/en/stable/user/alias.html))
 - Command modifiers ([documentation](http://cactusbot.readthedocs.io/en/stable/user/variables.html#modifiers))
 - Better `!cactus` command: now with helpfulness!
 - Absolutely no easter eggs anywhere...
 - `!multi` command ([documentation](http://cactusbot.readthedocs.io/en/stable/user/multi.html))
 - Custom `!social` storage ([documentation](http://cactusbot.readthedocs.io/en/stable/user/social.html))
 - Better [documenation](http://cactusbot.readthedocs.io/en/stable/)!

## Fixed
 - Repeat system

## Changed
 - *Every single line of code*
 - `!config` command ([documentation](http://cactusbot.readthedocs.io/en/stable/user/config.html))
 - Made all variables `%UPPERCASE%`
     - "targets" renamed to "variables"
 - `!friend` command renamed to `!trust`

## Removed
 - v0.3 nonsense™
 - `!test` command

## [0.3.6](https://github.com/CactusDev/CactusBot/releases/tag/v0.3.6)

#### Released: October 1st, 2016

### Fixed
 - Friend command regex (again)

### Added
 - Constellation support

### Removed
 - Liveloading

## [0.3.5](https://github.com/CactusDev/CactusBot/releases/tag/v0.3.5)

#### Released: September 2nd, 2016

### Fixed
 - `!friend` command regex
 - Websocket reconnections
 - Deleting own links

### Removed
 - Unused statistics

## [0.3.4](https://github.com/CactusDev/CactusBot/releases/tag/v0.3.4)

#### Released: July 31st, 2016 

### Fixed
 - Beam CSRF token usage.
 - Message removal
 - `!repeat` command

## [0.3.3](https://github.com/CactusDev/CactusBot/releases/tag/v0.3.3)

#### Released: July 21st, 2016

### Added
 - Documentation is in the bot now

### Fixed
 - Repeat command
 - Cube command crashing when no arguments are present
 - Social command

## [0.3.2](https://github.com/CactusDev/CactusBot/releases/tag/v0.3.2)

#### Released: July 16th, 2016 

### Added
 - User loading into the database on bot start
 - Hosting alerts

### Fixed
 - Exponential-backoff for chat connections
 - Liveloading connection now only happens once
 - Follow alerts spam
 - `spamprot` command crashing when no arguments are present
 - Friend command not allowing for `@`

### Changed
 - `silent` is now `quiet`

## [0.3.1](https://github.com/CactusDev/CactusBot/releases/tag/v0.3.1)

#### Released: April 10th, 2016 

### Added
 - Uptime command
 - Multi-message responses using `\n`
 - `beam` as a social argument

### Fixed
 - Ghost columns in the database
 - Autorestart conditions
 - `repeat` crash on command removal
 - Whispered responses
 - Message removal

### Changed
 - Command prefix limit to 1

## [0.3.0](https://github.com/CactusDev/CactusBot/releases/tag/v0.3)

#### Released: April 9th, 2016

### Added
 - Repeating commands
 - Following and subscriptions notifications
 - User permissions for custom commands
 - Command line arguments for `silent` and `debug`

### Fixed
 - Reconnection spam
 - Random disconnections
 - `!cube`ing emotes

### Changed
 - Move from `asyncio` to `tornado`

## [0.2.1](https://github.com/CactusDev/CactusBot/releases/tag/v0.2.1)

#### Released: March 27th, 2016

### Fixed
 - Spam protection command

### Disable
 - Statistics tracking

### Added
 - `autorestart` to config

## [0.2.0](https://github.com/CactusDev/CactusBot/releases/tag/v0.2)

#### Released: March 27th, 2016

### Added
 - Command permissions
 - Spam protection

### Changed
 - Config organizations

## [0.1.0](https://github.com/CactusDev/CactusBot/releases/tag/v0.1)

#### Released: March 5th, 2016 

### Added
 - Custom commands
 - Quotes
 - Social command
 - Response targets
