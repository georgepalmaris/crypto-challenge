<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

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
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/georgepalmaris/crypto-challenge">
    <img src="https://www.webopedia.com/wp-content/uploads/1996/10/what-is-cryptography-scaled.webp" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Crypto Challenge</h3>

  <p align="center">
    This project is for working through the CryptoPals challenges along with any other crypto based challenges that may come along (https://cryptopals.com/)
    It has also extended into interactive terminal exploration and graph generation in terminals.
    <br />
    <a href="https://github.com/georgegeorgepalmaris/crypto-challenge/tree/main/docs"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#built-with">Built With</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


### Built With

[![Python][PythonBadge]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Really, all that is needed for this project is Python, this can be installed in whatever manner you prefer, but I would recommend using pyenv for this.

### Prerequisites

This how to install/create a python environment specifically for this project.
* python
  ```sh
  brew install pyenv
  brew install pyenv-virtualenv
  ```
* pyenv
  ```sh
  pyenv install 3.13
  pyenv virtualenv 3.13 crypto
  pyenv active crypto
  ```
* pip
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/georgepalmaris/crypto-challenge.git
   ```
2. Install Pip Requirements
   ```sh
   pip install -r requirements.txt
   ```
3. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin georgepalmaris/crypto-challenge
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Ideally all usage should be done through the interactive terminal, that can be ran via:

   ```sh
   python main.py
   ```

Running the help command will tell you everything you can do:

   ```sh
   python main.py --help
   ```

_For more examples, please refer to the [Documentation](https://github.com/georgegeorgepalmaris/crypto-challenge/tree/main/docs)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/georgepalmaris/crypto-challenge/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=georgepalmaris/crypto-challenge" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

George Finn - [@linkedin_handle](https://www.linkedin.com/in/georgefinn/) - george.charles.finn@gmail.com

Project Link: [https://github.com/georgepalmaris/crypto-challenge](https://github.com/georgepalmaris/crypto-challenge)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/georgepalmaris/crypto-challenge.svg?style=for-the-badge
[contributors-url]: https://github.com/georgepalmaris/crypto-challenge/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/georgepalmaris/crypto-challenge.svg?style=for-the-badge
[forks-url]: https://github.com/georgepalmaris/crypto-challenge/network/members
[stars-shield]: https://img.shields.io/github/stars/georgepalmaris/crypto-challenge.svg?style=for-the-badge
[stars-url]: https://github.com/georgepalmaris/crypto-challenge/stargazers
[issues-shield]: https://img.shields.io/github/issues/georgepalmaris/crypto-challenge.svg?style=for-the-badge
[issues-url]: https://github.com/georgepalmaris/crypto-challenge/issues
[license-shield]: https://img.shields.io/github/license/georgepalmaris/crypto-challenge.svg?style=for-the-badge
[license-url]: https://github.com/georgepalmaris/crypto-challenge/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/georgefinn/ 
[PythonBadge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/