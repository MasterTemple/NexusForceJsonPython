# Nexus Force To Json with Python
These json files are used by a discord bot, but you can use them for something else if you would like to.
This is not the actual bot, rather it creates the files for the bot.

# How It Works
This project uses the `cdclient.sqlite` and `locale.xml` to generate json files. You can use `cdclient.fdb` instead of `cdclient.sqlite`, doing so will just result in the program converting the .fdb to .sqlite then running like normal. (I am using lcdr's tool do this convert the file). This feature exists so this bot can stay up to date with servers that add new content. The `LootTableIndexNames.json` is a file of shorthand names for LootTableIndexes created by Krysto and MasterTemple to make browsing much easier.

# Setup
1. Install Python 3.6 (other versions might work but this program runs off 3.6)
2. You need in NexusForceJsonPython/work the following files:
   ```
   cdclient.fdb or cdclient.sqlite
   config.json
   locale.xml
   LootTableIndexNames.json
   ```
3. Specify in NexusForceJsonPython/work/config.json how you would like the files to be generated. There are multiple ways.\
   Set `startFromFdb = true` if you want to generate the cdclient.sqlite from the cdclient.fdb\
   Set `startFromSqlite = true` if you want to completely regenerate the entire program. This method takes a long time, but will make sure everything is updated. You do not need to set this value = true if startFromFdb is true\
   Set `justUpdateGivenInfo = true` if you just want to add new items and not regenerate all the files. If you do this, make sure to add the IDs to their respective list.
   Set output to where you would like the files to be generated. The default path is `NexusForceJsonPython/output`. You can do `C:\\Users\\MasterTemple\\Bot\\json` or just `jsonFiles` will create `NexusForceJsonPython/jsonFiles`
4. Run `main.py` by typing `python main.py` in the command prompt of corresponding directory.

#Contact
If you have any questions regarding use or any suggestions for features, feel free to contact me on Discord at `MasterTemple#0233` (my ID is `789705048035688458` just in case my name is changed)
