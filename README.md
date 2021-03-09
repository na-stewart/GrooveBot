<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">GrooveBot</h3>

  <p align="center">
    The Official r/Animusic Bot.
    <br />
    <a href="https://github.com/sunset-developer/GrooveBot_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/sunset-developer/GrooveBot_name/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Images](#Images)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

GrooveBot is a bot specially coded for the r/Animusic Discord server. Some of Groovebot's unique 
features include music and abbreviation organization, suspending and striking users, join and leave messages, verification,
and more.

Currently, all data is stored locally on a SQLite database. A pre-populated database file is included with this repository. Use .help for user commands and .adminhelp for admin commands. 

## Images

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot1.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot2.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot3.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot4.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot5.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot6.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot7.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot8.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot9.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot10.png)

![alt text](https://github.com/sunset-developer/GrooveBot/blob/master/images/groovebot11.png)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

First install pip, which contains all of the necessary packages.
* pip
```sh
sudo apt install python3-pip
```

### Installation

* Clone the repo
```sh
git clone https://github.com/sunset-developer/GrooveBot
```

* Install Pip Packages
```sh
pip3 install -r requirements.txt
```

* Create a groove.ini file in the GrooveBot/resources directory, then configure GrooveBot using the example below:
```ini
[GROOVE]
token=NYeeOweIPUyuHHuygODQ0MTYx.X7PcFg.k-BedTOIUgwOHIBbsQSi5aVAE
prefix=.
general_channel_id=general-discussion-1
suspended_role_id=818172621720083812
verified_role_id=827182728768211978

[TORTOISE]
schema=groovebot.sqlite3
models=groovebot.core.models
generate=true
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Please contact sunsetdev or Denyul on discord at:
https://discord.gg/yDfyhfA


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Be the first! Submit a pull request.](https://github.com/sunset-developer/GrooveBot/pulls)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/sunset-developer/GrooveBot.svg?style=flat-square
[contributors-url]: https://github.com/sunset-developer/GrooveBot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sunset-developer/GrooveBot.svg?style=flat-square
[forks-url]: https://github.com/sunset-developer/GrooveBot/network/members
[stars-shield]: https://img.shields.io/github/stars/sunset-developer/GrooveBot.svg?style=flat-square
[stars-url]: https://github.com/sunset-developer/GrooveBot/stargazers
[issues-shield]: https://img.shields.io/github/issues/sunset-developer/GrooveBot.svg?style=flat-square
[issues-url]: https://github.com/sunset-developer/GrooveBot/issues
[license-shield]: https://img.shields.io/github/license/sunset-developer/GrooveBot.svg?style=flat-square
[license-url]: https://github.com/sunset-developer/GrooveBot/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username
[product-screenshot]: images/screenshot.png
