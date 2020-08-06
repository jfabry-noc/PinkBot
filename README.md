# PinkBot
This is a Twitter bot giving you a daily dose of being unusually pink. Posts a shade of pink with the hex color, RGB color values, and link to the color. One post is made, pulling randomly from a local repository. To run at a regular interval, the script should be set as a `cron` job, or equivalent for whatever operating system you're using.

Leverages the [Twython](https://github.com/ryanmcgrath/twython) library.

The script expects a `configuration.json` file to be in the same directory with the application key/secret and access ID/secret.
