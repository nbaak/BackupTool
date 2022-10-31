# BackupTool
A simple tool to create backups of files or folders.

## How do I use it
If you want to see a manpage you can use teh command `./BackupTool -h`
To Add files/folders to the Backup System, you use teh commad `./BackupTool add <path>`, it will create a Backup Job and an alias for the job. If you want to specify the alias your self, you can add the parameter -a `./BackupTool add <path> -a <yourAlias>`.
To see all the active Backup Jobs, you use the command `./BackupTool show`, for a little more details add the parameter -d `./BackupTool show -d`. And to see all the created Backup Files for one specifiy alias `./BackupTool show -a <alias>`.
If you don't need a Backup Job anymore, you can remove it with the command `./BackupTool remove <alias>`. To also remove all the created zip files just add the parameter -d or --delete `./BackupTool remove <alias> -d` (there is no way to undo this operation!).
To run all backup Jobs, use the command `./BackupTool backup -r` I recommend to set up a cronjob for this. If you don't want to run the backup for all aliases and just for one you can specify the backup jobn with `./BackupTool backup -a <alias> -r` and just one alias will be backed up if it exists.

To configure the Tools archive path you write `./BackupTool config -b <path>` and to specify how many files will be stored in the Backup System `./BackupTool config -n <number:int>`.



## How to does it work
The Backup Tool copies the target folder or file and creates a zip file of it. The it mvoes the zip to the backup archive and removes the temporary copied folder/file. It also stores the owner of the target to be able to restore it. A zip file does not contain information about the owner of files/folders.
After storing a new zip file in the archive, the tool checks how many files are stored and if there are more than set in the config file (number, default 5), it will remove the oldest file(s).


## Future
Things that maybe implemented in the future.
1. Upload of archived items to a remote ftp/sftp
2. Option to create tar/zip files if wanted.