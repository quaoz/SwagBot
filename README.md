# GaymerBot

# Commands:

- All commands must be preceded by the command prefix, which by default is backslash (\\), or by @ mentioning the bot

## Join:

- Joins the specified voice channel
- Aliases: summon, connect

Syntax:

```
join [channel name]
```

E.g:

```
join General
```

## Play:

- Plays from the specified url or searches for the terms on YouTube
- Requires the person who sends the message to be connected to a voice channel
- Should be able to play from any site that [youtube-dl supports.](https://yt-dl.org/supportedsites.html)

Syntax:

```
play [url or something to search for]
```

E.g:

```
play Collared Greens
```

## Leave:

- Disconnects from the voice channel
- Aliases: shut, disconnect, dc

Syntax:

```
stop
```

---

## Translate:

- Translates the text into the specified language
- Aliases: trans, t

Syntax:

```
trans [target language] [text]
```

- The `[target language]` parameter can also take language codes or language names.

E.g:

```
trans german where is the child
```

- If the `[target language]` parameter is left out or the language isn't recognised it will attempt to translate the text into English.

E.g:

```
trans ich esse gern
```

## Define:

- Defines the specified word(s)
- If the definitions are over 2000 characters it will split them up into smaller parts and send them individually so the formatting may be a little weird (I might fix this at some point)
- Aliases: def, d, meaning

Syntax:

```
define [words]
```

E.g:

```
define arms
```


## Lyrics:

- Returns the lyrics of the song
- Like with `define` if the lyrics are over 2000 characters it will split them up into smaller parts and send them individual so the formatting may be a little weird (again I might fix this eventually)
- Aliases: l, lyric

Syntax:

```
lyrics [song title]
```

E.g:

```
lyrics ADMIT IT
```

## Random:

- Generates a random number
- Aliases: r, rand

Syntax:

```
random [number one] [number two]
```

- If the [number two] parameter is left out it will pick a number between zero and the given number

E.g:

```
random 1000 100
```

---

## Info:

- Gets information about a minecraft server
- Aliases: status, server

Syntax

```
info [server ip]
```

- If the [server ip] parameter is left out it will return info about the default server from the config

E.g:

```
info nucleoid.xyz
```

## Launch

- Starts the [aternos](https://aternos.org/) minecraft server specified in the config
- Aliases: start

Syntax:

```
launch
```

## Stop

- Stops the [aternos](https://aternos.org/) minecraft server specified in the config
- Aliases: terminate

Syntax:

```
stop
```

## Restart

- Restarts the [aternos](https://aternos.org/) minecraft server specified in the config
- Aliases: reboot

Syntax:

```
stop
```
---

## Connect-Four

- Starts a connect-four game and the mentioned person
- Aliases: c4, connect4, connectfour

Syntax

```
connect-four [user]
```

E.g:

```
connect-four @steve
```

---

## Credits:
- [Aternos-On-Discord](https://github.com/Mekolaos/Aternos-On-Discord) by [Mekolaos](https://github.com/Mekolaos) for the initial implementation to control an aternos server
