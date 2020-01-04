from random import randint
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import sys
import json


def main(args):
    data = pd.read_csv(args[0])
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

    model = LogisticRegression()

    model.fit(X_train, y_train)

    predicted_classes = model.predict(X_test)

    accuracy = accuracy_score(y_test.flatten(), predicted_classes)

    model2 = RandomForestClassifier(
        n_estimators=100, criterion='entropy', random_state=100)

    model2.fit(X_train, y_train)

    predicted_classes = model2.predict(X_test)

    accuracy2 = accuracy_score(y_test.flatten(), predicted_classes)

    print(round(100*max(accuracy, accuracy2), 3), '%')

    # Choosing the best model
    model = model2 if accuracy2 >= accuracy else model

    list_colors_liked = []
    list_colors_hated = []

    def toHex(dec):
        x = (dec % 16)
        digits = "0123456789ABCDEF"
        rest = dec // 16
        if (rest == 0):
            return '0' + str(digits[x])
        return '' + digits[rest-1] + digits[x]

    max_per_list = 20
    for i in range(200):
        if len(list_colors_liked) == max_per_list and len(list_colors_hated) == max_per_list:
            break
        color = [randint(0, 256), randint(0, 256), randint(0, 256)]
        clrfrm = '#' + toHex(color[0]) + toHex(color[1]) + toHex(color[2])
        if model.predict([color])[0] == 1:
            if len(list_colors_liked) < max_per_list:
                list_colors_liked.append(clrfrm)
        else:
            if len(list_colors_hated) < max_per_list:
                list_colors_hated.append(clrfrm)

    print(json.dumps(list_colors_liked))
    print(json.dumps(list_colors_hated))


if __name__ == "__main__":
    main(sys.argv[1:])
