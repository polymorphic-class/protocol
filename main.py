import json
import click
import terraform as tf
import bureaucracy as by
from jinja2 import Environment, FileSystemLoader

def pluralize(str, end_ptr = None, rep_ptr = ""):
    if end_ptr and str.endswith(end_ptr):
        return str[:-1*len(end_ptr)]+rep_ptr
    else:
        return str+'s'


@click.command()
@click.option('--statefile', default="terraform.tfstate", help='path to terraform statefile')
@click.option('--inventoryfile', default="production", help='output ansible inventory')

def generate(statefile, inventoryfile):
    with open(statefile) as data_file:
        data = json.load(data_file)

    droplets = tf.TerraformState(data).droplets
    groups = tf.DropletGroups(droplets).groups
    groupings = by.InventoryGrouping(groups, droplets).generate()

    env = Environment(loader=FileSystemLoader('.'))
    env.filters['pluralize'] = pluralize

    template = env.get_template('inventory.j2')

    output_from_parsed_template = template.render(
      groups=groups, droplets=droplets, groupings=groupings
    )

    with open(inventoryfile, "wb") as fh:
        fh.write(output_from_parsed_template)


if __name__ == '__main__':
    generate()
