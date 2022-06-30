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

### Status: Development on hold...again...

Currently, the libraries used to mitigate recaptcha from stopping your bot dead in its tracks are either deprecated or require the user to sign up and configure a third party service to resolve the recaptcha challenges for you. As I am exhausted of the development community always pushing the employment of another paid API access, I refuse to employ them in my coding. Paid API services create barriers to use and access. They also stifle development and the progress of computer innovation.

So, until either new methods are created, or old libraries updated. This project will be on hold.

### Original Intentions

Originally intended to be based off of a sniper for EBay, this project has veered far from that course. The reason for this 
is the obstacles present in the modern webframework prevent unwanted automation from occurring. Implementations of cloudflare
and ReCaptcha have made the job of automation difficult to accomplish. As such, the original sniper was unsuited for the task.

### Setup

Below offers an abridged inconclusive overview of what is required to  configure your system and run the sniper.

#### Requirements

In order to set up this application there are several requirements that will be needed. 

* the latest geckodriver installed on your that matches the version of firefox on your system
* firefox
* Python (obviously)
* required dependencies installed
* poetry

### Bidding on GunBroker

Just a few words of wisdom earned during my experience with the site. 

* GunBroker places the seller first, and you, the potential buyer, last.
* Unlike eBay, which informs you of the amount of the highest bid, GunBroker leaves this to your imagination. You can and will be outbid, without ever knowing it.
* The seller's word does not have to be honored.
* If for some reason, the seller refuses to sell the gun to you after placing the winning bid, gunbroker will not do anything about it.


### Diagram

![Project Puml](https://www.plantuml.com/plantuml/svg/NOox3KCX303xJ94CaES-5QiOi0011lcZh1_IlkfEEkc26ehv78zNupGyqxEQRVq0b6RLuvNM1EILFNKepb5M9tahjqq2Wb-Og7RqtgxzlmRYVFW3)

