# Playmaker

* mongogateway
  * get mails without status
  * finds previous step of mailer
  * set status an email to the story piece id sent to the player
* storygateway
  * get a story piece
* mailgateway
  * send mail
* game
  * resolve what's the next id
* mailer
  * collects mails that needs processing with *mongogateway*
  * finds previous story id with *mongogateway*
  * gets that piece with *storygateway*
  * finds out what next piece should be with *game*
  * gets that story piece with *storygateway*
  * sends mail with *mailgateway*
  * sets status on the incoming mail with *mongogateway*
  * sleeps for an some minutes
