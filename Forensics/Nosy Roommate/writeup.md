# Nosy Roommate

We are given an AD1 file. This is a custom content disk image file which was created with [FTK Imager](https://accessdata.com/products-services/forensic-toolkit-ftk/ftkimager) and can be opened by the same. From the application, we can extract the files required to answer our questions:

## First question

To find the last time of startup, we can open the `system.evtx` event log file which is at `C:\Windows\System32\winevt\Logs\` and looking at the timestamps of `Kernel-Boot` events.

## Second question

Since, this is supposed to be an easy password, we can crack it by cracking the password hash which is stored in the `SAM` registry hive and is encrypted by the system boot key which is in the `SYSTEM` registry hive, both of which are at `C:\Windows\System32\config`. [Mimikatz](https://github.com/gentilkiwi/mimikatz/wiki) will do this for us when we run the `lsadump::sam` module in the mimikatz console with the path to SAM and SYSTEM files extracted from the image as parameters.

## Third question

We can find out that the application which was installed is **Tor Browser**. One way to find this out would be the setup file in the Downloads folder which wasn't deleted. For the timestamp, we cannot use event logs or registry keys as Tor's installer doesn't log installation by default. One way to do this would be to look at the **ShellBags**, which are registry subkeys located in **UsrClass.dat** and **NTUSER.dat** (both at **C:\Users\\(username)**) used primarily to store the folder view settings for Explorer. This also stores folder creation timestamps even for the deleted folders such as the program files for Tor Browser. We can use an application such as the one [here](https://ericzimmerman.github.io/#!index.md) called **'ShellBags Explorer'** to parse this and obtain the timestamp:

![installation-time](https://imgur.com/wobyQDw.png)

From the various folder creation timestamps of different folders under **'Desktop\Tor Browser'**, we can place the installation time to be at **08:50**.

## Fourth Question

Windows has a feature called System Resource Usage Monitor (SRUM) which collects a lot of statistics about resource consumption for each application that was run. This includes network data usage as well. This data is written out periodically at every hour and at shutdown to `SRUDB.dat` at `C:\Windows\System32\sru\`. We can parse this data using an application such as [srum-dump](https://github.com/MarkBaggett/srum-dump) to obtain this info in a readable format. This particular application will output an Excel file with the statistics of different resource usages as shown below:

![network-usage](https://imgur.com/lLfH3Ck.png)

From here, we can calculate the total network usage from the two entries. These are exhaustive as the application was installed only recently.

## Fifth Question

The USB drive removal time can be found out from the registry key at `\SYSTEM\CurrentControlSet\Enum\USBSTOR\(drive-info)\(serial-number)\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\0067`. Note that `CurrentControlSet` in this case would be `ControlSet001` (which can be verified from the Select subkey at **SYSTEM**) since the registry data is being read offline.
We can use an application such as the one [here](https://ericzimmerman.github.io/#!index.md) called **'Registry Explorer'** to read registry hives and keys.

You can convert the UTC times reported by the tools you use to the PC's time zone which can be found out at `\SYSTEM\CurrentControlSet\Control\TimeZoneInformation`.  (CurrentControlSet == ControlSet001 in this case)
