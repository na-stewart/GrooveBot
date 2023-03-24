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

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">GrooveBot</h3>

  <p align="center">
    The official r/Animusic Discord bot. 
    <br />
    <a href="https://github.com/sunset-developer/GrooveBot/issues">Report Bug</a>
    ·
    <a href="https://github.com/sunset-developer/GrooveBot/pulls">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Contributing](#contributing)
* [License](#license)



<!-- ABOUT THE PROJECT -->
## About The Project

![alt text](https://github.com/na-stewart/GrooveBot/blob/main/img/pipe-dream.jpg)

GrooveBot is a bot specially coded for the r/Animusic Discord server. It was created as an easy way to reference
Wayne Lytle's (and other's) work as well as understand abbreviations that may be used within the server. There are also security features such as verification, user strikes, and join/leave messages.

`v3.1.3`


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

* Create a groove.ini file in the project directory. Below is an example of its contents:

Note: You will need a database, local or remote.

```ini
[SETTINGS]
token=Nzc4MjYzMjAwMDQyODQ0MTYx.X7PcFg.k-BedTOS3LgoEU6teXsQSi5aVAE
message_on_join=Welcome to the official r/Animusic Discord server!
database_url=sqlite://db.sqlite3
general_channel_id=1625118263628154181
verification_channel_id=176371620648173633
verified_role_id=1625184182632815125
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
