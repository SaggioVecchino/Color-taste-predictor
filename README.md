# Color taste predictor

> Application of ML classification in a desktop app, for predicting the color taste (may like, may hate) of the user according to his preferences provided !

For the classification two models were trained : Logistic Regression and Random Forrest, and the one giving a better accuracy is used to the classification (Prediction in this case), to suggest colors that the user may like and colors that he may hate !

#### Build Setup

```bash
# install dependencies
npm install

# serve with hot reload at localhost:9080
npm run dev

# build electron application for production (Won't work perfectly due to the python script. I have to add my own builder that handle the python script -This isn't for the moment my goal-, or you can just add it manually to the installation folder once you built the project.)
npm run build


```
