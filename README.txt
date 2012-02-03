NineHoles - Your Local VimGolf Challenge Leaderboard

Abstract
======================
NineHoles is designed for groups to have their own VimGolf 'league' leaderboard. It can also import offical VimGolf challenges.

Installation and Setup
======================

Install ``nineholes`` using the setup.py script::

    $ cd nineholes
    $ python setup.py install

Create the project database for any model classes defined::

    $ paster setup-app development.ini

Start the paste http server::

    $ paster serve development.ini

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ paster serve --reload development.ini

Then you are ready to go.
