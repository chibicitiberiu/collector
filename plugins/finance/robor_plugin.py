import datetime

import lxml.html
import requests
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin


class Robor(BaseModel):
    date = DateField(index=True, default=datetime.date.today(), null=False)
    field = TextField(null=False)
    value = FloatField(null=False)


class RoborPlugin(Plugin):
    models = [Robor]

    def __init__(self):
        self.__table = None

    def get_interval(self):
        return config.ROBOR_INTERVAL

    def get_column_index(self, table, column_name):
        header_row = table.find('tr')
        for elem in header_row.iter('th'):
            if column_name in elem.text_content():
                return header_row.index(elem)

        return None

    def values_newer_than(self, table, oldest_date: datetime.date, col_date, col_value):
        # Items are ordered descending, so stop when we reach date
        for row in table.iter('tr'):
            dt_str = row[col_date].text_content()
            val_str = row[col_value].text_content()

            try:
                dt = datetime.datetime.strptime(dt_str, '%d/%b/%Y')
                val = float(val_str)
            except ValueError:
                continue
            
            dt = dt.date()
            if (oldest_date is not None) and (dt <= oldest_date):
                break

            yield (dt, val)

    def execute(self):
        # Get last existing date
        latest_date = Robor.select(Robor.date) \
                           .order_by(Robor.date.desc()) \
                           .limit(1) \
                           .scalar()

        # Fetch & parse data
        response = requests.get('https://www.bnro.ro/StatisticsReportHTML.aspx?icid=801&table=642', verify=False)
        response.raise_for_status()

        html = lxml.html.fromstring(response.text)

        # Read data from table
        table = html.find('.//table[@class="stat_table"]')

        for field in config.ROBOR_FIELDS:
            col_date = self.get_column_index(table, 'Date')
            col_value = self.get_column_index(table, field)

            for date, value in self.values_newer_than(table, latest_date, col_date, col_value):
                entry = Robor()
                entry.date = date
                entry.field = field
                entry.value = value
                entry.save()



