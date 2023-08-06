import os
from bienes_inmuebles.dataset.csv_utilities import CSV, PATH4


class ML():
    def __init__(self, df):
        self.df = df

    def split_out(self):
        array = dataset.values
        X = array[:, 0:2]
        Y = array[:, 2]
        validation_size = 0.20
        seed = 7
        X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)
        return X_train, X_validation, Y_train, Y_validation

    def metricas (self):
        self.num_folds = 10
        self.seed = 7
        self.scoring = 'accuracy'

    def test_puntual(self):
        # Usaremos 6 tipos:
        models = []
        models.append(('LR', LogisticRegression()))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))

        # Evaluamos cada modelo por turnos
        results = []
        names = []
        for name, model in models:
            kfold = KFold(n_splits=num_folds, random_state=seed)
            cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)

    def comparacion_plot (self):
        # Escogemos el más preciso, que en este caso será SVM
        fig = pyplot.figure()
        fig.suptitle('Comparación de Algoritmos')
        ax = fig.add_subplot(111)
        pyplot.boxplot(results)
        ax.set_xticklabels(names)
        pyplot.show()

    def test_puntual_estandarizado(self):
        pipelines = []
        pipelines.append(('ScaledLR', Pipeline([('Scaler', StandardScaler()), ('LR', LogisticRegression(solver='lbfgs', max_iter=500))])))
        pipelines.append(('ScaledLDA', Pipeline([('Scaler', StandardScaler()), ('LDA', LinearDiscriminantAnalysis())])))
        pipelines.append(('ScaledKNN', Pipeline([('Scaler', StandardScaler()), ('KNN', KNeighborsClassifier())])))
        pipelines.append(('ScaledCART', Pipeline([('Scaler', StandardScaler()), ('CART', DecisionTreeClassifier())])))
        pipelines.append(('ScaledNB', Pipeline([('Scaler', StandardScaler()), ('NB', GaussianNB())])))
        pipelines.append(('ScaledSVC', Pipeline([('Scaler', StandardScaler()), ('SVC', SVC(gamma='scale'))])))
        results = []
        names = []
        for name, model in pipelines:
            kfold = KFold(n_splits=num_folds, random_state=seed)
            cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)

    def comparacion_plot_estandarizados(self):
        # Escogemos el más preciso, que en este caso será SVM
        fig = pyplot.figure()
        fig.suptitle('Comparación Escalada de Algoritmos')
        ax = fig.add_subplot(111)
        pyplot.boxplot(results)
        ax.set_xticklabels(names)
        pyplot.show()

if __name__ == "__main__":
    csv = CSV(os.path.join(PATH4, "data/csv_barcelona.csv"))