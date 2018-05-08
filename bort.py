import click
import json
from intent_classifier import IntentClassifier


@click.group()
def bort():
    click.echo('Hello twitch chat')


@bort.command()
@click.argument('input', nargs=-1, type=click.File('r'))
@click.argument('out', nargs=1, type=click.Path())
@click.option('--init-model', default=None, type=click.File())
@click.option('--nlp-model', default='es_core_news_sm', type=click.STRING)
def train(input, out, init_model, nlp_model):
    input_sets = [json.load(input_set) for input_set in input]
    examples = [example for input_set in input_sets for example in input_set]

    model = IntentClassifier(nlp_model)
    model.fit(examples)

    model.persist(out)


@bort.command()
@click.argument('model', nargs=1, type=click.Path())
@click.argument('text', nargs=1, type=click.STRING)
def predict(model, text):
    model = IntentClassifier.load(model)

    pred, prob = model.predict(text)
    prob.sort(reverse=True)
    click.echo(pred)
    click.echo(prob)


if __name__ == '__main__':
    bort()
