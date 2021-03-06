import csv
import datetime as dt
from basicInfo import privateInfo as pr

class filterfields:
    data = []

    def resetdate(self, date_value, should_be_zero=True):
        return date_value.replace(hour=0, minute=0, second=0) \
            if should_be_zero \
            else date_value.replace(hour=23, minute=59, second=59)

    def createweekinfo(self, start_date, end_date, anchor_date):
        current_start_date = anchor_date
        while current_start_date > start_date:
            current_start_date = current_start_date - dt.timedelta(days=7)
        week_info = {}
        current_end_date = current_start_date + dt.timedelta(days=6)
        current_start_date = self.resetdate(current_start_date, True)
        current_end_date = self.resetdate(current_end_date, False)
        idx = 1
        while current_start_date < end_date:
            week_info[idx] = (current_start_date, current_end_date)
            idx += 1
            current_start_date = self.resetdate(current_end_date + dt.timedelta(days=1), True)
            current_end_date = self.resetdate(current_end_date + dt.timedelta(days=7), False)
        return week_info


    def getstartenddates(self, data_to_work = []):
        data_to_work = self.data if [] == data_to_work else data_to_work
        start_date = dt.datetime.max
        end_date = dt.datetime.min
        for data_row in data_to_work:
            cur_date = self.converttodate(data_row[pr.m_time_sent])
            if cur_date < start_date:
                start_date = cur_date
            if cur_date > end_date:
                end_date = cur_date
        return start_date, end_date

    def converttodate(self, string_date, dt_format = '%Y-%m-%d %H:%M:%S'):
        return dt.datetime.strptime(string_date, dt_format)

    def filterbetweendates(self, start_date, end_date, data_to_work = [], right_equality=False,
                           date_field=pr.m_time_sent):
        filtered_data = []
        data_to_work = self.data if [] == data_to_work else data_to_work
        for data_row in data_to_work:
            cur_date = self.converttodate(data_row[date_field])
            if right_equality:
                if start_date <= cur_date <= end_date:
                    filtered_data.append(data_row)
            else:
                if start_date <= cur_date < end_date:
                    filtered_data.append(data_row)
        return filtered_data

    def setdata(self, data):
        self.data = data

    def __readfile(self, fname=''):
        if '' == fname:
            print 'no fname given, use setdata()'
            return []
        temp_data = []
        f = open(fname, 'r')
        csv_obj = csv.reader(f, delimiter = ',')
        for row in csv_obj:
            temp_data.append(row)
        f.close()
        return temp_data

    def removebyequality(self, field_no, to_equate):
        data_to_replace_with = []
        for idx in range(len(self.data)):
            if to_equate not in self.data[idx][field_no].lower():
                data_to_replace_with.append(self.data[idx])
        self.setdata(data_to_replace_with)

    def replacebyequality(self, field_no, to_equate, to_replace_with):
        replacements = 0
        for idx in range(len(self.data)):
            if to_equate in self.data[idx][field_no].lower():
                self.data[idx][field_no] = to_replace_with
                replacements += 1
        print 'Number of replacements: ', replacements
        return replacements


    def filterbyequality(self, field_no, to_equate, data=None):
        filtered_data = []
        data = self.data if data is None else data
        for data_row in data:
            if to_equate in data_row[field_no].lower():
                filtered_data.append(data_row)
        print 'Original data: ', len(data), ' filtered data:', len(filtered_data)
        return filtered_data

    def getuniqueelements(self, field_no, data=None):
        data = self.data if data is None else data
        unique_elements = set()
        for data_row in data:
            unique_elements.add(data_row[field_no])
        return list(unique_elements)

    def getdata(self):
        return self.data

    def __init__(self, fname=''):
        self.data = self.__readfile(fname)
