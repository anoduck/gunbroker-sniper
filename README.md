```text
==================================================================================================
 ▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄ ▄         ▄ ▄                     ▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄ ▄         ▄ ▄ 
▐░░░░░░░░░░░▐░░░░░░░░░░░▐░▌       ▐░▐░▌                   ▐░░░░░░░░░░░▐░░░░░░░░░░░▐░▌       ▐░▐░▌
▐░█▀▀▀▀▀▀▀█░▐░█▀▀▀▀▀▀▀▀▀▐░▌       ▐░▐░▌                   ▐░█▀▀▀▀▀▀▀█░▐░█▀▀▀▀▀▀▀▀▀▐░▌       ▐░▐░▌
▐░▌       ▐░▐░▌         ▐░▌       ▐░▐░▌                   ▐░▌       ▐░▐░▌         ▐░▌       ▐░▐░▌
▐░█▄▄▄▄▄▄▄█░▐░█▄▄▄▄▄▄▄▄▄▐░▌   ▄   ▐░▐░▌    ▄▄▄▄▄▄▄▄▄▄▄    ▐░█▄▄▄▄▄▄▄█░▐░█▄▄▄▄▄▄▄▄▄▐░▌   ▄   ▐░▐░▌
▐░░░░░░░░░░░▐░░░░░░░░░░░▐░▌  ▐░▌  ▐░▐░▌   ▐░░░░░░░░░░░▌   ▐░░░░░░░░░░░▐░░░░░░░░░░░▐░▌  ▐░▌  ▐░▐░▌
▐░█▀▀▀▀▀▀▀▀▀▐░█▀▀▀▀▀▀▀▀▀▐░▌ ▐░▌░▌ ▐░▐░▌    ▀▀▀▀▀▀▀▀▀▀▀    ▐░█▀▀▀▀▀▀▀▀▀▐░█▀▀▀▀▀▀▀▀▀▐░▌ ▐░▌░▌ ▐░▐░▌
▐░▌         ▐░▌         ▐░▌▐░▌ ▐░▌▐░▌▀                    ▐░▌         ▐░▌         ▐░▌▐░▌ ▐░▌▐░▌▀ 
▐░▌         ▐░█▄▄▄▄▄▄▄▄▄▐░▌░▌   ▐░▐░▌▄                    ▐░▌         ▐░█▄▄▄▄▄▄▄▄▄▐░▌░▌   ▐░▐░▌▄ 
▐░▌         ▐░░░░░░░░░░░▐░░▌     ▐░░▐░▌                   ▐░▌         ▐░░░░░░░░░░░▐░░▌     ▐░░▐░▌
 ▀           ▀▀▀▀▀▀▀▀▀▀▀ ▀▀       ▀▀ ▀                     ▀           ▀▀▀▀▀▀▀▀▀▀▀ ▀▀       ▀▀ ▀ 
==================================================================================================

 ██████╗ ██╗   ██╗███╗   ██╗██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗██████╗ 
██╔════╝ ██║   ██║████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗
██║  ███╗██║   ██║██╔██╗ ██║██████╔╝██████╔╝██║   ██║█████╔╝ █████╗  ██████╔╝
██║   ██║██║   ██║██║╚██╗██║██╔══██╗██╔══██╗██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝██║  ██║╚██████╔╝██║  ██╗███████╗██║  ██║
 ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
  /$$$$$$            /$$                              
 /$$__  $$          |__/                              
| $$  \__/ /$$$$$$$  /$$  /$$$$$$   /$$$$$$   /$$$$$$ 
|  $$$$$$ | $$__  $$| $$ /$$__  $$ /$$__  $$ /$$__  $$
 \____  $$| $$  \ $$| $$| $$  \ $$| $$$$$$$$| $$  \__/
 /$$  \ $$| $$  | $$| $$| $$  | $$| $$_____/| $$      
|  $$$$$$/| $$  | $$| $$| $$$$$$$/|  $$$$$$$| $$      
 \______/ |__/  |__/|__/| $$____/  \_______/|__/      
                        | $$                          
                        | $$                          
                        |__/
```


## gunbroker-sniper
A sniper for gunbroker auctions

### Original Intentions

Originally intended to be based off of a sniper for EBay, this project has veered far from that course. The reason for this 
is the obstacles present in the modern webframework prevent unwanted automation from occurring. Implementations of cloudflare
and ReCaptcha have made the job of automation difficult to accomplish. As such, the original sniper was unsuited for the task.

### Captcha Handling

__The current release of captcha buster is currently successfully handling recaptchas for the project.__

### Setup

Below offers an abridged inconclusive overview of what is required to configure your system and run the sniper.

#### Requirements

In order to set up this application there are several requirements that will be needed. 

* the latest geckodriver installed on your that matches the version of firefox on your system
* firefox
* Python (obviously)
* required dependencies installed
* poetry


### Diagram of proposed captcha bypass method

![Project Puml](https://www.plantuml.com/plantuml/svg/NOox3KCX303xJ94CaES-5QiOi0011lcZh1_IlkfEEkc26ehv78zNupGyqxEQRVq0b6RLuvNM1EILFNKepb5M9tahjqq2Wb-Og7RqtgxzlmRYVFW3)


### Bidding on GunBroker

Just a few words of wisdom earned during my experience with the site. 

* GunBroker places the seller first, and you, the potential buyer, last.
* Unlike eBay, which informs you of the amount of the highest bid, GunBroker leaves this to your imagination. You can and will be outbid, without ever knowing it.
* The seller's word does not have to be honored.
* If for some reason, the seller refuses to sell the gun to you after placing the winning bid, gunbroker will not do anything about it.

### GunBroker's 15min rule

Although this rule is purposefully designed to counteract sniping, it does not counteract automation of the bidding process all together.
[15 min rule](https://support.gunbroker.com/hc/en-us/articles/221437107-15-Minute-Rule)

### TODO:

- [ ] Sync Time Remaining
- [ ] Save Cookie
- [ ] Saving item information upon execution
- [ ] Retrieving saved item information
- [ ] Go truly headless
- [ ] Sleeper Cell before snipe
- [ ] Item Stalking before snipe 
- [ ] Price Settings 
- [ ] reporting result of snipe
- [ ] Bid and win on an item
- [ ] Cleanup repository
- [ ] Mitigate the 15min rule