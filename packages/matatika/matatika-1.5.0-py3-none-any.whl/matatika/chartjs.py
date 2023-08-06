"""chartjs module"""

import json
from matatika.dataset import Dataset

COLOURS = {
    'backgroundColor': [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
    ],
    'borderColor': [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
    ]
}


def _chart_label(metadata, field):
    """Resolve a chart label"""

    m_name = metadata['name']
    m_aggregates = metadata['related_table']['aggregates']

    aggregate = next(
        a for a in m_aggregates if f"{m_name}.{a['name']}" == field)

    duplicates = list(
        filter(lambda item: item['label'] == aggregate['label'], m_aggregates))

    if len(duplicates) > 1:
        return f"{aggregate['label']} [Source: {aggregate.get('source')}]"

    return aggregate['label']


def to_chart(dataset: Dataset, data: list):
    """Converts dataset data and metadata to the Chart.js specification"""

    if not dataset.metadata or not data:
        return None

    chart_type = json.loads(dataset.visualisation)[
        'chartjs-chart']['chartType']

    chart_data = {
        'labels': [],
        'datasets': []
    }

    metadata = json.loads(dataset.metadata)

    fields = data[0].keys()
    aggregates = []
    try:
        aggregates = metadata['related_table']['aggregates']
    except KeyError:
        pass

    aggregates = list(
        map(lambda item: f"{metadata['name']}.{item['name']}", aggregates))

    columns = set(fields) - set(aggregates)

    datasets = {}
    for data_point in data:
        label = []
        for i, field in enumerate(fields):
            if field not in columns:
                colour = {t: c[i % len(c)] for t, c in COLOURS.items()}
                if not datasets.get(field):

                    datasets[field] = {
                        'label': _chart_label(metadata, field),
                        'data': [],
                        'backgroundColor': colour['backgroundColor'],
                        'borderColor': colour['borderColor'],
                        'borderWidth': 1
                    }

                    if chart_type == 'line':
                        datasets[field]['fill'] = False
                    elif chart_type == 'area':
                        datasets[field]['fill'] = True
                    elif chart_type == 'scatter':
                        datasets[field]['showLine'] = False

                datasets[field]['data'].append(data_point[field])

            else:
                label.append(data_point[field])

        label = "-".join([str(e) for e in label])
        label = label[:50] if len(label) > 50 else label
        chart_data['labels'].append(label)

    for dataset_values in datasets.values():
        chart_data['datasets'].append(dataset_values)

    return {
        'data': chart_data,
        'chart_type': chart_type,
        'options': None
    }
