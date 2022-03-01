# dsdump
Now you can use [resymbol](https://github.com/paradiseduo/resymbol) replace this tool.

An improved nm + objc/swift class-dump ([writeup](https://derekselander.github.io/dsdump/))

Based on [DerekSelander/dsdump](https://github.com/DerekSelander/dsdump)

Because of the original project does not support outputting the results directly to files, So I use Python to output the scan results to files.

Use it like this (**If you want to better view the class name of swift, you can use -d option.
But -d option will slow down dsdump speed.**):
```bash
> git clone https://github.com/paradiseduo/dsdump.git
> cd dsdump
> python3 dsdump.py

    .         .
    |         |                    {Version: 2.0}
 .-.| .--. .-.| .  . .--.--. .,-.
(   | `--.(   | |  | |  |  | |   )
 `-'`-`--' `-'`-`--`-'  '  `-|`-'
                             |
                             '

python3 dsdump.py
 -i <inputfile>
 -o <outputfile>
 -a [ arm64 | armv7 ]
 -d
> python3 dsdump.py -i ~/Downloads/Payload/xxx.app/xxx -o ~/Desktop/classes
/Users/x/Desktop/classes/NSObject.h
/Users/x/Desktop/classes/XMIAudioPlayerListProtocol.h
/Users/x/Desktop/classes/UIScrollViewDelegate.h
/Users/x/Desktop/classes/UIPageViewControllerDataSource.h
/Users/x/Desktop/classes/UIPageViewControllerDelegate.h
/Users/x/Desktop/classes/NYTPhotoViewControllerDelegate.h
/Users/x/Desktop/classes/KKListAdapterProtocol.h
/Users/x/Desktop/classes/ZHParallaxHeaderDelegate.h
............
/Users/x/Desktop/classes/xxx.XXSAppConfigInviteModel.swift
/Users/x/Desktop/classes/xxx.XXSNewUserGuideView.swift
/Users/x/Desktop/classes/xxx.XXSLikeUserListCell.swift
> 
> cat /Users/x/Desktop/classes/xxxKnowledge.XXSShareWebpageModel.swift
 class xxxKnowledge.XXSShareWebpageModel : XXSShareModel {

	// Properties
	var webpageUrlString : String

	// ObjC -> Swift bridged methods
	0x1003722bc  @objc XXSShareWebpageModel.webpageUrlString <stripped>
	0x100372378  @objc XXSShareWebpageModel.setWebpageUrlString: <stripped>
	0x1003724f8  @objc XXSShareWebpageModel.init <stripped>
	0x1003724e4  @objc XXSShareWebpageModel..cxx_destruct <stripped>

	// Swift methods
	0x100372324  func <stripped> // getter
	0x1003723e0  func <stripped> // setter
	0x10037243c  func <stripped> // modifyCoroutine
 }%
```


## Stargazers over time

[![Stargazers over time](https://starchart.cc/paradiseduo/dsdump.svg)](https://starchart.cc/paradiseduo/dsdump)

