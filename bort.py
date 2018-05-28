import click
import json
from clasificador_intencion import ClasificadorIntencion


@click.group()
def bort():
    pass


@bort.command()
@click.argument('input', nargs=-1, type=click.File('r'))
@click.argument('out', nargs=1, type=click.Path())
@click.option('--nlp-model', default='es_core_news_sm', type=click.STRING)
def entrenar(input, out, nlp_model):
    input_sets = [json.load(input_set) for input_set in input]
    examples = [example for input_set in input_sets for example in input_set]

    model = ClasificadorIntencion(nlp_model)
    model.entrenar(examples)

    click.echo('Entrenando con {} ejemplos'.format(len(examples)))
    click.echo('Intenciones entrenadas:')
    for _, v in model.intent_idx.items():
        click.echo(' - ' + v)

    model.persistir(out)


@bort.command()
@click.argument('model', nargs=1, type=click.Path())
@click.argument('text', nargs=1, type=click.STRING)
def predecir(model, text):
    model = ClasificadorIntencion.cargar(model)

    pred, prob = model.predecir(text)
    prob.sort()
    click.echo(pred)
    click.echo(prob)


@bort.command()
@click.argument('out', nargs=1, type=click.File('w'))
def exportar(out):
    from app import Mensaje

    mensajes = [{'mensaje': mensaje.texto, 'intencion': mensaje.intencion_real}
                for mensaje in Mensaje.query.filter_by(humano=True,
                                                       etiquetado=True)]
    click.echo(mensajes)
    json.dump(mensajes, out)


if __name__ == '__main__':
    bort()
