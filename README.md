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

Originally intended to be based off of a sniper for EBay, this project has veered far from that course. The reason for
this lies in obstacles present in the modern web that prevent unwanted automation from taking place. Implementations of
cloudflare and ReCaptcha have made the job of surfing and acquiring information in an automated fashion quite difficult to
accomplish. As such, the original sniper is unsuited to accomplish these tasks. 

The original sniper appears to have facilitated both the use of requests and of selenium to setup the snipe. 
This is actually a brilliant strategy, as requests will always complete the transaction before selenium can even load the page.
To simplify the management of the chrome driver, it is planned to incorporate the use of selenoid to make the project as flexible and uniform as one can.

### Setup

In order to setup this application there are several requirements that will be needed. 

* Docker (for selenoid)
* Selenoid
* Python (obviously)

### Credits

Without the work of Noah Cardoza this project would not be possible, and it would behove anyone using this program to help
support him and his work. 

https://github.com/NoahCardoza

### Diagram (Work in progress!)

```plantuml
@startuml
'https://plantuml.com/activity-diagram-beta
title GunBroker Sniper
header A sniper for gunbroker auctions
footer shooting for the smarter

actor dude [
	Title: The Dude
	===
	Lang: Grunts
]
rectangle localhost{
	stack Docker{
		node selenoid [
			Title: Selenoid
			===
			Lang: Docker Image
			---
			Facility: Dockerized Headless WebDriver
		]
		package sel_view [
			Title: Selenium-ui
			===
			Notes: Simply provides VNC of Selenoid
		]
		node cloud_proxy [
			Title: CloudProxy
			---
			Lang: TypeScript
			===
			Notes: Commands must be in JSON
		]
		node captcha_harvester [
			Title: CaptchaHarvester
			===
			Lang: Python
			---
			Notes: requires sitekey and domain to run in docker
			....
			But will receive separate instructions from cloud proxy
		]
	}
	card main_py
	component selenium [
		TITLE: Selenium
		===
		Lang: Python
		---
		Notes: Python interface to the webdriver api.
	]
}
cloud gunbroker{
	frame recaptchav2 [
	Title: Recaptcha V2
	===
	Lang: JavaScript
	---
	Notes: Interfaces with Google's Recaptcha API
	]
	artifact item [
	TITLE: Desired Item
	===
	Lang: Pew-Pew
	]
}
dude --> sel_view
sel_view ~~> selenoid : ""'Magic'""
main_py --> selenium
selenium ..> selenoid : ""Docker Socket""
selenoid ~~> item : ""HTTP Request""
selenoid <~~> cloud_proxy : ""???""
cloud_proxy ~~> gunbroker : ""HTTP Request""
cloud_proxy ~~> captcha_harvester : ""json""
captcha_harvester <-- recaptchav2 : ""HTTP Response""

@enduml

```
