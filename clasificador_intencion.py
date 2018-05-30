import numpy as np
import pickle
import spacy
from sklearn.svm import SVC
from util import leer_configuracion


def build_category_vector(examples, var):
    labels = [example[var] for example in examples]
    label_idx = {key: value for value, key in enumerate(set(labels))}
    reverse_idx = {value: key for key, value in label_idx.items()}
    label_arr = np.array([label_idx[intent] for intent in labels])

    return label_arr, reverse_idx


def build_feature_matrix(nlp, examples):
    example_docs = [nlp(example['mensaje']).vector for example in examples]

    return np.asarray(example_docs)


class ModeloMensaje:
    """ Modelo para inferir todas las variables de un mensaje con todas las
    variables definidas en un archivo de configuración """
    def __init__(self, nlp_model, config):
        self.config = leer_configuracion(config)['variables_mensaje']
        self.modelos = {nombre: crear_modelo(nombre, info_var)
                        for nombre, info_var in self.config}

        self.nlp_model = nlp_model
        self.nlp = spacy.load(nlp_model)

    def entrenar(self, ejemplos):
        feats = build_feature_matrix(self.nlp, ejemplos)
        for name, info_var in self.config.items():
            etiquetas = [ej.get(name, default=info_var['default'])
                         for ej in ejemplos]
            self.modelos[name].entrenar(feats, etiquetas)

        if variable['tipo'] == 'clasificador':
            pass


class ModeloClasificador:
    def __init__(self, nlp_model, classifier=None, intent_idx=None):
        self.nlp_model = nlp_model
        self.nlp = spacy.load(nlp_model)
        if classifier is None:
            classifier = SVC(C=1.0, cache_size=200, class_weight=None,
                             coef0=0.0, decision_function_shape='ovr',
                             degree=3, gamma='auto', kernel='rbf',
                             max_iter=-1, probability=True,
                             random_state=None, shrinking=True, tol=0.001,
                             verbose=False)

        self.intent_idx = intent_idx
        self.classifier = classifier

    def entrenar(self, examples):
        intents, self.intent_idx = build_category_vector(examples)
        feat_mat = build_feature_matrix(self.nlp, examples)

        return self.classifier.fit(feat_mat, intents)

    def predecir(self, text):
        feats = np.array(self.nlp(text).vector).reshape(1, -1)

        pred = self.intent_idx[self.classifier.predict(feats)[0]]
        proba = [(p, self.intent_idx[i]) for i, p
                 in enumerate(self.classifier.predict_proba(feats)[0])]
        return pred, proba

    def persistir(self, filepath):
        model_info = {'nlp_model': self.nlp_model,
                      'classifier': self.classifier,
                      'intent_idx': self.intent_idx}
        with open(filepath, 'wb') as fp:
            pickle.dump(model_info, fp)

    @classmethod
    def cargar(cls, filepath):
        with open(filepath, 'rb') as fp:
            model_info = pickle.load(fp)
        nlp = model_info['nlp_model']
        classifier = model_info['classifier']
        intent_idx = model_info['intent_idx']

        return cls(nlp, classifier, intent_idx)
