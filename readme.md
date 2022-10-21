# Off-Flix - Offline Netflix Clone

This is an offline version of Netflix built with Python libraries including Flask, urllib, os, sqlite3, pymediainfo, hashlib, flaskwebgui, mimetypes, random, and shutil.

## Usage

To use the app, run the `gui.py` file. This will launch the user interface where you can add your downloaded shows to the app by providing the path to the show. The app stores the path in a database and generates thumbnails from random frames of the video file.

You can explore your library by switching between different seasons of shows and marking episodes as watched. The app also includes a random button that plays a random episode from the selected show.

You can delete a show from your library by clicking on the delete button.
![Alt text](screenshots\1.png)


![Alt text](screenshots\2.png)


## Libraries Used

- Flask
- urllib
- os
- sqlite3
- pymediainfo
- hashlib
- flaskwebgui
- mimetypes
- random
- shutil

## Installation

1. Clone the repository
2. Navigate to the project directory: `cd off-flix`
3. Install the required libraries
4. Run the app: `python gui.py`

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the [MIT License](https://github.com/yourusername/offline-netflix-clone/blob/main/LICENSE).
