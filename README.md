# GaymerBot

# Commands:

- All commands must be preceded by the command prefix, which by default is `/`, or by @ mentioning the bot

## Join:

- Joins the specified channel.

Syntax:

```
join [channel name]
```

E.g:

```
join General
```

## Play:

- Plays from the specified url or searches for the terms on youtube
- Requires the person who sends the message to be connected to a voice channel.
- Should be able to play from any site that [youtube-dl supports.](https://yt-dl.org/supportedsites.html)

Syntax:

```
play [url or something to search for]
```

E.g:

```
play Hayloft
```

## Stop:

- Disconencts from the voice channel.

Syntax:

```
stop
```

## Translate:

- Translates the text into the specified language

Syntax:

```
trans [target language] [text]
```

- The `[target language]` parameter can also take language codes or language names.

E.g:

```
trans german where is the child
```

- If the `[target language]` parameter is left out or the language isn't recognised it will attepmt to translate the text into English.

E.g:

```
trans ich esse gern
```

## Define:

- Defines the specified word(s)
- If the defenitions are over 2000 characters it will split them up into smaller parts and send them individualy so the formating may be a little weird

Syntax:

```
d [words]
```

E.g:

```
d anarchist
```

## Lyrics:

- Returns the lyrics of the song
- Like with `define` if the lyrics are over 2000 characters it will split them up into smaller parts and send them individualy so the formating may be a little weird

Syntax:

```
lyrics [song title]
```

E.g:

```
lyrics Verbatim
```
