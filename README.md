# gunbroker-sniper
A sniper for gunbroker auctions. Based off of an ebay sniper.

## Currently In Development 02-2022

### Status

Currently there are two seperate projects located in this repository.

1. The original extremely cleanly coded ebay sniper used to inspire the project
2. A Development scraper coded in the usual manner I have come accustomed to working with scrapers.

The original sniper appears to have facilitated both the use of requests and of selenium to setup the snipe. 
This is actually a brilliant strategy, as requests will always complete the transaction before selenium can even load the page.
To simplify the management of the chrome driver, it is planned to incorporate the use of selenoid to make the project as flexible and uniform as one can.

