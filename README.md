# EatingClubHub

Team members: Ella Colby, Johnny Ramirez, Muhammad Zaeem, Brian Zhou

## Installation guide

Check to see that yarn is installed on your local environment by running:

```
yarn -v
```

If your yarn version isn't printed, then follow the instructions to install yarn on the yarn website.

After having yarn installed on your local environment, activate the Python virutal environment by running:
```
yarn install && yarn activate
```
To install the Python packages, checkout the backend directory and run:
```
pip install -r requirements.txt
```
If there are any issues with installation, make sure that pip is installed on your local environment. If it is, then contact the service administrator.

Also include the `DATABASE_URL` environment variable in a .env file.

To install the packages on the frontend, checkout the frontend directory and run:
```
yarn install
```

Finally, to run the website, checkout the root project directory and run:
```
yarn start
```
Open the website on `localhost:3000` and the website should appear.
