```text
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

### Status: Conceptual Development

Originally intended to be based off of a sniper for EBay, this project has veered far from that course. The reason for this lies in obstacles present in the modern web that prevent unwanted automation from taking place. Implementations of cloudflare and ReCaptcha have made the job of surfing and acquiring information in an automated fashion quite difficult to accomplish. As such, the original sniper is unsuited to accomplish these tasks. 

Current efforts revolve around thwarting recaptcha to enable the sniper to work.

### Setup

In order to setup this application there are several requirements that will be needed. 

* Selenium
* Python (obviously)

### Bidding on GunBroker

Just a few words of wisdom earned during my experience with the site. 

* GunBroker places the seller first, and you, the potential buyer, last.
* Unlike eBay, which informs you of the amount of the highest bid, GunBroker leaves this to your imagination. You can and will be outbid, without ever knowing it.
* The seller's word does not have to be honored.
* If for some reason, the seller refuses to sell the gun to you after placing the winning bid, gunbroker will not do anything about it.


### Diagram (Work in progress!)

![Project Puml](https://www.plantuml.com/plantuml/svg/NOox3KCX303xJ94CaES-5QiOi0011lcZh1_IlkfEEkc26ehv78zNupGyqxEQRVq0b6RLuvNM1EILFNKepb5M9tahjqq2Wb-Og7RqtgxzlmRYVFW3)

