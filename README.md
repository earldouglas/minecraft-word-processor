This script extracts [Book and Quill][1] text from a Minecraft world,
which can be handy if you have kids who use Minecraft as a word
processor.

## Usage

First, find the [Minecraft world folder][2].

Then, run the script on the `db` folder within the Minecraft world
folder:

```
$ devenv shell
$ python main.py path/to/db
Found 2 books:
* Call of the Mild, by John Chill -> target/0-call-of-the-mild.md
* The Oddyssey, by Math Jokington -> target/1-the-oddyssey.md
```

## References

* [Amulet NBT API][3]

[1]: https://minecraft.fandom.com/wiki/Book_and_Quill
[2]: https://web.archive.org/web/20191107044447/https://help.mojang.com/customer/portal/articles/1480874-where-are-minecraft-files-stored-
[3]: https://amulet-nbt.readthedocs.io/en/3.0/api_reference/index.html
