"""
Import json data from JSON file to Datababse
"""
from django.core.management.base import BaseCommand, CommandError
import os
import json
from ...models import *
from datetime import datetime, time


class Command(BaseCommand):

    def get_log(self):

        printers = ['Druk-XL', 'Druk-XXXL', 'druk-xxl-new', 'druk-eco'
                                                            '']
        # printers = ['Druk-XXXL']

        for printer in printers:
            data_folder = os.path.join('/data', 'workflow', '{}'.format(printer))  #'/data/workflow/...'

            # Check if directory exists
            try:
                os.makedirs(data_folder)
            except FileExistsError:
                # directory already exists
                pass

            # Start getting RIP logs
            rip = os.system(r"smbclient '//{}/Onyx12records' -c 'lcd '{}'; get JobLog.txt' -U Root%zaq1!QAZ".format(printer, data_folder))
            if rip == 0:
                try:
                    ripinput = open(os.path.join(data_folder, 'JobLog.txt'), 'r', encoding='cp1251')
                except IOError:
                    print("Not found input file")

                try:
                    ripoutput = open(os.path.join(data_folder, 'JobLog.json'), 'w', encoding='utf-8')
                except IOError:
                    print("Not found output json file")

                output = []
                for input_text in ripinput:
                    S = ((input_text.replace("{{ ", "")).replace(" }}", "")).split('" "')
                    status = int(S[0].replace('"', ''))
                    name = S[1].replace('"', '')
                    timestamp = int(S[3])
                    width_px = int(S[5].replace('"', ''))
                    height_px = int(S[6].replace('"', ''))
                    width_cm = round(width_px / float(S[11].replace(',', '.')) * 0.0254, 3)
                    height_cm = round(height_px / float(S[10].replace(',', '.')) * 0.0254, 3)
                    date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d, %H:%M:%S')
                    count = int(S[9].replace('"', ''))

                    days_count = (datetime.now() - datetime.strptime(date_time, '%Y-%m-%d, %H:%M:%S')).days

                    if days_count <= 33:
                        data = {
                            'status': status,
                            'name': name,
                            'width_px': width_px,
                            'height_px': height_px,
                            'width': width_cm,
                            'height': height_cm,
                            'date_time': date_time,
                            'count': count,
                            'timestamp': timestamp
                        }

                        output.append(data)
                    else:
                        pass
                j = json.dumps(output)
                ripoutput.write(j)
                ripoutput.close()

                # Printers creating
                printer_rip_update = {
                    "name": printer
                }
                try:
                    printer_rip = Printers.objects.get(name=printer)
                    for key, value in printer_rip_update.items():
                        setattr(printer_rip, key, value)
                    printer_rip.save()
                    display_format = "\nPrinter, {}, has been edited."
                    print(display_format.format(printer_rip))
                except Printers.DoesNotExist:
                    printer_rip_create = {
                        "name": printer
                    }
                    printer_rip_update.update(printer_rip_update)
                    printer_rip = Printers(**printer_rip_create)
                    printer_rip.save()
                    display_format = "\nPrinter, {}, has been created."
                    print(display_format.format(printer_rip.name))

                # Opening RIP-JSON file
                with open(os.path.join(data_folder, "JobLog.json"), encoding='utf-8') as data_file:
                    data = json.loads(data_file.read())
                    for data_object in data:
                        status    = data_object['status']
                        name      = data_object['name']
                        width     = data_object['width']
                        height    = data_object['height']
                        # date_time = datetime.strptime(data_object['date_time'], '%Y-%m-%d, %H:%M:%S')
                        date_time = datetime.strptime(data_object['date_time'], '%Y-%m-%d, %H:%M:%S')
                        count     = data_object['count']
                        timestamp = data_object['timestamp']

                        # PrinterLog creating
                        # printer_rip_log_update = {
                        #     "printer": printer_rip,
                        #     "status": status,
                        #     "work_name": name,
                        #     "width": width,
                        #     "height": height,
                        #     "count": count,
                        #     "datetime": date_time,
                        #     "timestamp": timestamp
                        # }
                        try:
                            printer_rip_log = RipLog.objects.get(printer_id=int(printer_rip.id), timestamp=timestamp)
                            # for key, value in printer_rip_log_update.items():
                            #     setattr(printer_rip_log, key, value)
                            # printer_rip_log.save()
                            # display_format = "\nRIP Log, {}, has been edited."
                            # print(display_format.format(printer_rip_log.work_name))
                        except RipLog.DoesNotExist:
                            printer_rip_log_create = {
                                "printer": printer_rip,
                                "status": status,
                                "work_name": name,
                                "width": width,
                                "height": height,
                                "count": count,
                                "datetime": date_time,
                                "timestamp": timestamp
                            }
                            # printer_rip_log_update.update(printer_rip_log_update)
                            printer_rip_log = RipLog(**printer_rip_log_create)
                            printer_rip_log.save()
                            display_format = "\nRIP Log, {}, has been created."
                            print(display_format.format(printer_rip_log.work_name))
            else:
                print('Error:', rip)

##################################################################################################################################################
            # Start getting PRINTER logs
            prt = os.system(r"smbclient '//{}/PrintedLog' -c 'lcd '{}'; get PrintedArea.Log' -U Root%zaq1!QAZ".format(printer, data_folder))
            if prt == 0:
                try:
                    prtinput = open(os.path.join(data_folder, 'PrintedArea.Log'), 'r', encoding='utf-8')
                except IOError:
                    print("Not found input file")

                try:
                    prtoutput = open(os.path.join(data_folder, 'PrintedArea.json'), 'w', encoding='utf-8')
                except IOError:
                    print("Not found output json file")

                output = []
                # for input_text in finput:
                for line in prtinput.readlines():
                    line = line.replace(' PM :', ' PM;').replace(' AM :', ' AM;').replace('\ufeff', '').replace('\n', '')
                    dim_in = line.split('; ')
                    date_time_begin = (datetime.strptime(dim_in[2], '%m/%d/%Y-%I:%M %p'))

                    how_days = ((datetime.now() - datetime.strptime(dim_in[2], '%m/%d/%Y-%I:%M %p')).days)  ## Сколько дней назад

                    f_name = (dim_in[1]).split('\\')
                    name = str(f_name[-1]).replace('.prt', '')  # Имя файла

                    time_print_1 = (dim_in[3]).split(':')
                    time_print = time(int(time_print_1[0]), int(time_print_1[1]), int(time_print_1[2]))

                    percent = int(str(dim_in[4]).replace('%', ''))  # %
                    square = float(str(dim_in[5]).replace(' m2', ''))  # Площадь

                    if how_days <= 33:
                        data = {
                            'date_time_begin': str(date_time_begin),
                            'time_print': str(time_print),
                            'name': name,
                            'square': square,
                            'percent': percent
                        }

                        output.append(data)
                    else:
                        pass

                prtinput.close()
                jp = json.dumps(output)
                prtoutput.write(jp)
                prtoutput.close()

                # Opening PRT-JSON file
                with open(os.path.join(data_folder, "PrintedArea.json"), encoding='utf-8') as data_file:
                    data = json.loads(data_file.read())
                    for data_object in data:

                        # print(data_object['date_time_begin'])
                        printer_rip = Printers.objects.get(name=printer)
                        # start = datetime.strptime(data_object['date_time_begin'])
                        start = data_object['date_time_begin']
                        name = data_object['name']
                        duration = data_object['time_print']
                        percentage = data_object['percent']
                        m_kv = data_object['square']

                        # PrinterLog creating
                        # printer_log_update = {
                        #     "printer": printer_rip,
                        #     "start": start,
                        #     "work_name": name,
                        #     "duration": duration,
                        #     "percentage": percentage,
                        #     "m_kv": m_kv
                        # }
                        try:
                            printer_log = PrintLog.objects.get(printer_id=int(printer_rip.id), start=start, work_name=name)
                            # for key, value in printer_log_update.items():
                            #     setattr(printer_rip_log, key, value)
                            # printer_log.save()
                            # display_format = "\nPrint Log, {}, has been edited."
                            # print(display_format.format(printer_log.work_name))
                        except PrintLog.DoesNotExist:
                            printer_log_create = {
                                "printer": printer_rip,
                                "start": start,
                                "work_name": name,
                                "duration": duration,
                                "percentage": percentage,
                                "m_kv": m_kv
                            }
                            # printer_log_update.update(printer_log_update)
                            printer_log = PrintLog(**printer_log_create)
                            printer_log.save()
                            display_format = "\nPrint Log, {}, has been created."
                            print(display_format.format(printer_log.work_name))
            else:
                print('Error:', prt)

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.get_log()

