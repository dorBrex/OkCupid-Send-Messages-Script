# The Cupid Swindler (jk)
A script that connects to your OkCupid user and send opening lines to the people you liked already on the app.



# How to use the script

[![N|Solid](https://lh3.googleusercontent.com/a-/AOh14GgMyfq8jQjkbS5klwFUwR3LfhFTxDe3mQWKNdncuQ=s96-c-rg-br100)](https://www.linkedin.com/in/dor-barak/)

The Cupid Swindler is a python writted script using Selenium to save you time and effort in finding your Rapunzel.

- Easy to use
- Saving time
- ✨Magical✨

## Features

- Import a HTML file and watch it magically convert to Markdown
- Drag and drop images (requires your Dropbox account be linked)
- Import and save files from GitHub, Dropbox, Google Drive and One Drive
- Drag and drop markdown and HTML files into Dillinger
- Export documents as Markdown, HTML and PDF

Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.
As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Tech

Dillinger uses a number of open source projects to work properly:

- [Python] - Python 3.4+ to run the script on your computer
- [Pycharm] - Free IDE - text editor and developers environment in order to edit the script.
- [Git Bash] - A program to clone the repo from github to your local machine.


And of course CupidSwindler itself is open source with a [public repository][dill]
 on GitHub.

## Installation

Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Plugins

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox |  |
| GitHub |  |
| Google Drive |  |
| OneDrive |  |
| Medium |  |
| Google Analytics |  |

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```

## Docker
To be added

## License

IOU

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax, and also to https://dillinger.io/)

   [Python]: <https://www.python.org/downloads/>
   [Pycharm]: <https://www.jetbrains.com/pycharm/>
   [Git Bash]: <https://git-scm.com/downloads>
   [CupidSwindler]: <https://github.com/dorBrex/OkCupid-Send-Messages-Script>
