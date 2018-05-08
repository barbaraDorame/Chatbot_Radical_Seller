import click
import json
from clasificador_intencion import ClasificadorIntencion


@click.group()
def bort():
    click.echo('Hello twitch chat')


@bort.command()
@click.argument('input', nargs=-1, type=click.File('r'))
@click.argument('out', nargs=1, type=click.Path())
@click.option('--init-model', default=None, type=click.File())
@click.option('--nlp-model', default='es_core_news_sm', type=click.STRING)
def entrenar(input, out, init_model, nlp_model):
    input_sets = [json.load(input_set) for input_set in input]
    examples = [example for input_set in input_sets for example in input_set]

    model = ClasificadorIntencion(nlp_model)
    model.entrenar(examples)

    model.persistir(out)


@bort.command()
@click.argument('model', nargs=1, type=click.Path())
@click.argument('text', nargs=1, type=click.STRING)
def predecir(model, text):
    model = ClasificadorIntencion.cargar(model)

    pred, prob = model.predecir(text)
    prob.sort(reverse=True)
    click.echo(pred)
    click.echo(prob)


if __name__ == '__main__':
    bort()
